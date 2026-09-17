"""Generate the new 21-task collection, separate from the existing IPOP dataset."""
import hashlib
import json
import os
from pathlib import Path

from catalog import CATALOG, FORMATS, encode, decode, output
from cases import cases
from cpp_sources import source
from oracles import solve

BASE=Path(__file__).resolve().parents[1]
DATA=BASE.parents[1]
ROOT=DATA.parent
UPSTREAM=ROOT/'.tools/leetcode-source'
COMMIT='b9d7d2c234c39b3b3c67eded0c125e2841685b29'
REPO='https://github.com/DhanushNehru/Leetcode'


def relative(p):return Path(os.path.relpath(p,BASE)).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,text):p.write_text(text,encoding='utf-8',newline='\n')
def save_json(p,obj):save(p,json.dumps(obj,ensure_ascii=False,indent=2)+'\n')


def canonical(pid,args):
    # Preserve meaningful spaces in strings; normalize unordered dictionary/edge sets.
    args=json.loads(json.dumps(args))
    if pid in (139,518):args[1]=sorted(args[1])
    if pid==207:args[1]=sorted(args[1])
    return json.dumps(args,ensure_ascii=False,separators=(',',':'))


def main():
    manifest={'schema_version':1,'dataset_id':'leetcode21-extension-v1','date':'2026-09-16',
      'relationship_to_ipop19':'21 additional tasks; previous 19 unchanged; total selected tasks=40',
      'input_origin':'locally_generated; not official hidden tests','selection':'fixed purposive functional coverage; not random benchmark sample',
      'upstream_repository':REPO,'upstream_commit':COMMIT,
      'prompt_policy':'only statement.md and prompt_examples are prompt eligible; evaluation directory and diagnostics excluded',
      'comparison':'whitespace token exact; Two Sum indices canonicalized to ascending order',
      'deduplication':'parsed JSON args; preserve string spaces; sort dictionary, denomination and edge sets',
      'problems':[]}
    case_map=cases();assert set(case_map)==set(CATALOG) and len(CATALOG)==21
    for pid,meta in CATALOG.items():
        name=f'LC_{pid:04d}';folder=DATA/name;folder.mkdir(exist_ok=True)
        for child in ('evaluation','prompt_examples'):(folder/child).mkdir(exist_ok=True)
        upstream_path=f'problems/{meta["slug"]}/solution.js'
        url=f'https://leetcode.com/problems/{meta["slug"].replace("_","-")}/'
        entry={k:v for k,v in meta.items() if k!='public_examples'}
        entry.update({'problem_id':name,'official_url':url,'specification_verified':'2026-09-16',
          'upstream_path':upstream_path,'upstream_url':f'{REPO}/blob/{COMMIT}/{upstream_path}',
          'upstream_sha256':sha(UPSTREAM/upstream_path),'cases':[],'excluded_public_examples':[],
          'reference_origin':'locally_authored C++17 stdin/stdout adaptation'})
        old=set()
        for args in meta['public_examples']:
            a,b=solve(pid,args);assert a==b
            old.add(canonical(pid,args));entry['excluded_public_examples'].append({'args':args,'expected':a})
        save_json(folder/'public_examples.json',{'role':'public inputs checked against official description; outputs independently recomputed',
                                              'source_url':url,'examples':entry['excluded_public_examples']})
        example=entry['excluded_public_examples'][0]
        save(folder/'prompt_examples/example01.inp',encode(pid,example['args']))
        save(folder/'prompt_examples/example01.out',output(example['expected']))
        statement=[f'# {name}: {meta["slug"].replace("_"," ").title()}','',meta['summary'],'',
          '## 제약','',meta['constraints'],'','## 표준입출력 계약','',FORMATS[meta['interface']],
          '출력은 정수 하나 또는 공백으로 구분한 정수 배열이다. 참/거짓은 각각 1/0으로 출력한다. 인덱스는 0부터 시작한다.','']
        if pid==1:statement+=['인덱스 쌍은 작은 인덱스부터 출력한다. 원 문제의 임의 순서 허용을 이 어댑터에서 정규화한 것이다.','']
        if pid==283:statement+=['원래 함수는 배열을 직접 수정한다. 이 프로그램에서는 수정이 끝난 배열을 출력한다.','']
        statement+=['## 공개 예제','', '```text',encode(pid,example['args']).rstrip('\n'),'```','',
                    '출력:','','```text',output(example['expected']).rstrip('\n'),'```','',f'[공식 명세]({url})','']
        save(folder/'statement.md','\n'.join(statement))
        save(folder/'reference.cpp',source(pid))
        seen=set();assert len(case_map[pid])==10
        for i,(purpose,args) in enumerate(case_map[pid],1):
            key=canonical(pid,args);assert key not in old and key not in seen,(pid,purpose,'duplicate')
            seen.add(key);inp=encode(pid,args);assert decode(pid,inp)==args
            a,b=solve(pid,args);assert a==b,(pid,purpose,a,b)
            ip=folder/'evaluation'/f'case{i:02d}.inp';op=ip.with_suffix('.out')
            save(ip,inp);save(op,output(a))
            entry['cases'].append({'case_id':f'case{i:02d}','purpose':purpose,'origin':'generated',
              'input':relative(ip),'output':relative(op),
              'input_sha256':sha(ip),'output_sha256':sha(op),
              'canonical_args_sha256':hashlib.sha256(key.encode()).hexdigest(),'oracle_cross_check':'pass'})
        entry['frozen_files']={relative(p):sha(p) for p in [folder/'reference.cpp',folder/'statement.md',folder/'public_examples.json',folder/'prompt_examples/example01.inp',folder/'prompt_examples/example01.out']}
        lines=[f'# {name}: {meta["slug"].replace("_"," ").title()}','',meta['summary'],'',
          f'- 유형: {meta["category"]}',f'- [문제 명세와 입출력](statement.md)',f'- [C++17 기준 풀이](reference.cpp)',
          f'- [저장소 대응 풀이]({entry["upstream_url"]})',f'- [공식 문제]({url})',
          f'- 정답 교차 검증: {meta["oracle_methods"][0]} / {meta["oracle_methods"][1]}','',
          '공개 입력 예제 전체는 [public_examples.json](public_examples.json)에 기록하고 평가 입력에서 제외했다. 프롬프트에 사용할 수 있는 파일은 statement.md와 prompt_examples뿐이다.',
          '아래 입력은 자체 생성한 평가용 자료이며 공식 비공개 테스트가 아니다.','',
          '| 사례 | 목적 | 입력 | 정답 |','|---|---|---|---|']
        lines += [f'| {c["case_id"]} | {c["purpose"]} | [입력](evaluation/{c["case_id"]}.inp) | [정답](evaluation/{c["case_id"]}.out) |' for c in entry['cases']]
        lines+=['','이 README, evaluation, manifest, 검증 보고서를 번역 프롬프트에 넣지 않는다.','']
        save(folder/'README.md','\n'.join(lines))
        manifest['problems'].append(entry)
        print(f'{name}: 10 distinct non-example cases; independent oracles agree',flush=True)
    manifest['problem_count']=21;manifest['case_count']=210
    manifest['tool_hashes']={relative(p):sha(p) for p in (BASE/'tools').glob('*') if p.is_file()}
    save_json(BASE/'manifest.json',manifest)


if __name__=='__main__':main()
