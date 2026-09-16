"""Build fixed, auditable evaluation inputs without modifying the v1 fixtures."""
import hashlib
import json
import re
from pathlib import Path

from oracles import METHODS, solve

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[1]
COMMIT = 'b9d7d2c234c39b3b3c67eded0c125e2841685b29'
REPO = 'https://github.com/DhanushNehru/Leetcode'
MAPPINGS = {
    '10988': ('valid_palindrome', '소문자 영문 입력에 한정하고 boolean을 0/1로 변환'),
    '9012': ('valid_parentheses', '소괄호 입력에 한정하고 각 문자열의 boolean을 YES/NO로 변환'),
    '1992': ('construct_quad_tree', 'Node 객체를 제공하고 TL/TR/BL/BR 순서의 BOJ 문자열로 직렬화'),
}
TITLES = {
 '10988':'팰린드롬인지 확인하기', '1158':'요세푸스 문제', '11729':'하노이 탑 이동 순서',
 '1436':'영화감독 숌', '14719':'빗물', '1620':'나는야 포켓몬 마스터 이다솜',
 '18870':'좌표 압축', '1929':'소수 구하기', '1992':'쿼드트리', '2003':'수들의 합 2',
 '2110':'공유기 설치', '2217':'로프', '2579':'계단 오르기', '2609':'최대공약수와 최소공배수',
 '5567':'결혼식', '9012':'괄호', '9251':'LCS', '9663':'N-Queen', '9935':'문자열 폭발',
}
SUMMARIES = {
 '10988': '소문자 문자열 하나를 읽고 팰린드롬이면 1, 아니면 0을 출력한다.',
 '1158': 'N명 중 K번째 사람을 반복 제거한 순서를 꺾쇠와 쉼표 형식으로 출력한다.',
 '11729': 'N개 원판을 1번에서 3번 막대로 옮기는 최소 이동 횟수와 이동 목록을 출력한다.',
 '1436': '십진 표현에 666을 포함하는 수 중 N번째 수를 출력한다.',
 '14719': '높이 H, 너비 W와 각 열의 높이를 읽고 갇히는 빗물의 총량을 출력한다.',
 '1620': '서로 다른 이름 N개와 질의 M개를 읽고 이름과 1-based 번호를 상호 조회한다.',
 '18870': '정수 배열의 각 값을 자신보다 작은 서로 다른 값의 개수로 바꿔 출력한다.',
 '1929': '폐구간 M..N에 있는 모든 소수를 오름차순으로 한 줄에 하나씩 출력한다.',
 '1992': '이진 정사각 영상을 동일 값이면 압축하고 아니면 네 사분면을 재귀 인코딩한다.',
 '2003': '양의 정수 배열에서 합이 M인 비어 있지 않은 연속 구간의 개수를 출력한다.',
 '2110': '서로 다른 집 좌표 중 C곳을 골라 가장 가까운 공유기 간 거리를 최대화한다.',
 '2217': '선택한 로프의 최소 허용 하중과 로프 개수의 곱을 최대화한다.',
 '2579': '1칸 또는 2칸씩 이동하고 세 계단 연속 방문을 금지하며 마지막 계단까지 점수를 최대화한다.',
 '2609': '두 양의 정수의 최대공약수와 최소공배수를 순서대로 출력한다.',
 '5567': '무방향 친구 관계에서 1번 사람과 거리가 1 또는 2인 사람의 수를 출력한다.',
 '9012': 'T개 소괄호 문자열마다 올바른 괄호열이면 YES, 아니면 NO를 출력한다.',
 '9251': '두 대문자 문자열의 최장 공통 부분수열 길이를 출력한다.',
 '9663': 'N×N 체스판에서 N개의 퀸이 서로 공격하지 않는 배치 수를 출력한다.',
 '9935': '폭발 문자열을 반복 제거한 최종 문자열을 출력하고 비었으면 FRULA를 출력한다.',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(text):
    return ' '.join(text.split())


def exclusion(pid):
    statement = ROOT / 'problem' / f'IPOP_{pid}.md'
    paths = [statement] + sorted((ROOT / 'problem' / f'IPOP_{pid}').glob('*.inp'))
    examples = re.findall(r'예제 입력\s*\d+\s*\n(.*?)예제 출력', statement.read_text(encoding='utf-8-sig'), re.S)
    assert examples, f'No statement examples parsed: {pid}'
    inputs = examples + [p.read_text(encoding='utf-8-sig') for p in paths[1:]]
    return {canonical(x) for x in inputs}, paths, len(examples)


def candidates():
    d = {}
    def add(pid, label, value):
        d.setdefault(pid, []).append((label, value.rstrip()+'\n'))
    def nums(pid, label, values):
        add(pid, label, str(len(values))+'\n'+' '.join(map(str, values)))
    for label,s in [('최소 길이','a'),('길이 2 대칭','zz'),('길이 2 비대칭','az'),
                    ('홀수 대칭','radar'),('짝수 대칭','abccba'),('중앙 근처 불일치','abdcba'),
                    ('같은 문자 반복','q'*17),('최대 길이 대칭','a'*50+'a'*50),
                    ('최대 길이 끝 불일치','a'*99+'b'),('긴 짝수 대칭','abcdefghijklmnopqrstuvwxyzzyxwvutsrqponmlkjihgfedcba')]:add('10988',label,s)
    for n,k,label in [(1,1,'최소 N'),(2,1,'K=1'),(2,2,'K=N'),(5,1,'순서 그대로'),(5,5,'모든 인원 수만큼 순환'),
                      (6,4,'공약수 있는 N,K'),(8,3,'서로소 N,K'),(9,2,'홀수 인원'),(10,7,'큰 K'),(31,17,'여러 차례 순환')]:add('1158',label,f'{n} {k}')
    for n in [1,2,4,5,6,7,8,9,10,11]:add('11729',f'N={n}, '+('최소 크기' if n==1 else '홀수/짝수 재귀 이동'),str(n))
    for n in [5,8,9,12,13,19,21,66,666,10000]:add('1436',f'N={n}, '+('최대 순위' if n==10000 else '666 위치 및 연속 출현'),str(n))
    for h,a,label in [(1,[0],'최소 너비'),(1,[1,0,1],'최소 높이 물 고임'),(5,[0,0,0,0],'벽 없음'),
                      (5,[1,2,3,4,5],'단조 증가'),(5,[5,4,3,2,1],'단조 감소'),(5,[5,0,0,5],'깊은 단일 분지'),
                      (4,[4,1,4,1,4],'여러 분지'),(4,[2,2,2,2],'평탄한 벽'),(7,[0,7,2,5,1,6,0],'양끝 낮음'),
                      (500,[500,0,500],'높이 상한')]:add('14719',label,f'{h} {len(a)}\n'+' '.join(map(str,a)))
    name_cases = [(['Aa'],['1']),(['Zz'],['Zz']),(['Ab','Ac'],['2','Ab','1','Ac']),
      (['Ax','Bx','Cx'],['Cx','1','Ax','3']),(['abC','De'],['abC','1','De','2']),
      (['Aa','Ab','Ac','Ad'],['4','Ad','2','Ab','2']),(['Pik','Chu'],['Pik','Chu','1','2']),
      (['A'+'b'*19,'Z'+'y'*19],['1','Z'+'y'*19,'2','A'+'b'*19]),
      (['Alpha','Beta','Gamma','Delta','Omega'],['5','Gamma','1','Delta','2']),
      (['One','Two','Three','Four','Five','Six'],['Six','6','One','1','Three','3','Six'])]
    labels=['최소 사전 숫자 질의','최소 사전 이름 질의','양방향 조회','처음과 마지막 항목','마지막 글자 대문자',
            '동일 질의 반복','유사 이름','이름 길이 상한','비정렬 조회','다양한 질의 순서']
    for (names,queries),label in zip(name_cases,labels):add('1620',label,f'{len(names)} {len(queries)}\n'+'\n'.join(names+queries))
    for a,label in [([0],'최소 크기'),([7,7,7],'모두 같은 값'),([-3,-1,-2],'음수만 포함'),
                    ([1,2,3,4],'오름차순'),([4,3,2,1],'내림차순'),([-10**9,10**9,0],'값 하한과 상한'),
                    ([5,-5,5,0,-5],'반복과 부호 혼합'),([0,0,-1,1,0],'0 반복'),
                    ([11,12,10,11,9,12],'인접 값'),([999999999,-999999999,1,-1,1],'큰 절댓값 혼합')]:nums('18870',label,a)
    for lo,hi,label in [(1,2,'하한 1'),(2,2,'한 개 소수'),(17,17,'동일 소수 경계'),(1,10,'1 제외'),
                       (14,23,'합성수 시작'),(47,53,'양끝 소수'),(90,110,'제곱수 주변'),(120,140,'홀수 합성수 포함'),
                       (997,1020,'천 단위 경계'),(999900,1000000,'최대 상한')]:add('1929',label,f'{lo} {hi}')
    quad=[(['0'],'최소 흰색 픽셀'),(['1'],'최소 검정 픽셀'),(['00','00'],'동일 영역 0'),(['11','11'],'동일 영역 1'),
          (['01','10'],'체커보드'),(['11','00'],'상하 분할'),(['0101','1010','0101','1010'],'모두 분할'),
          (['1000','0000','0000','0000'],'한 픽셀만 다름'),(['0000','0000','1111','1101'],'불균일 깊이'),
          (['0'*32+'1'*32]*32+['1'*32+'0'*32]*32,'최대 변 길이')]
    for rows,label in quad:add('1992',label,str(len(rows))+'\n'+'\n'.join(rows))
    for a,m,label in [([1],1,'최소 배열 정답 1'),([2],1,'최소 배열 정답 0'),([1,1,1,1,1],3,'구간 겹침'),
                      ([1,2,3],6,'배열 전체'),([5,5,5],5,'길이 1 구간'),([3,1,2,1,3],4,'서로 다른 구간 길이'),
                      ([1,2,1,2,1,2],3,'반복 패턴'),([9,1,1,9,1],2,'큰 원소 건너뛰기'),
                      ([30000,30000,1],60000,'원소 상한'),([2,3,4],300000000,'목표 합 상한')]:add('2003',label,f'{len(a)} {m}\n'+' '.join(map(str,a)))
    for a,k,label in [([0,1],2,'최소 좌표 간격'),([0,10**9],2,'좌표 범위 양끝'),([0,2,4,6],4,'모든 집 선택'),
                      ([9,0,4,2],2,'정렬되지 않은 입력'),([0,1,2,100],3,'큰 공백'),([1,4,7,10,13],3,'동일 간격'),
                      ([0,1,3,7,15,31],4,'비균등 간격'),([100,101,102,104,108],3,'좌표 평행 이동'),
                      ([20,5,17,1,9,30],4,'순서 혼합'),([0,2,3,5,8,13,21,34],5,'조합 선택')]:add('2110',label,f'{len(a)} {k}\n'+'\n'.join(map(str,a)))
    for a,label in [([1],'최소 크기와 하중'),([10000],'하중 상한'),([2,2,2],'동일 로프'),([1,10000],'약한 로프 제외'),
                    ([1,2,4,8],'기하급수 하중'),([8,6,4,2],'역순 하중'),([6,6,6,1,1],'부분집합 최적'),
                    ([3,4,5],'전체 선택 최적'),([10,10,1,10],'반복과 이상치'),([9999,10000,9999,10000],'상한 근처')]:nums('2217',label,a)
    for a,label in [([1],'최소 계단과 점수'),([10000],'점수 상한'),([1,2],'두 계단'),([1,10000,1],'세 계단 연속 금지'),
                    ([100,1,1,100],'양끝 고득점'),([7]*5,'동일 점수'),([1,2,3,4,5,6],'증가 점수'),
                    ([6,5,4,3,2,1],'감소 점수'),([1,100,1,100,1,100,1],'번갈아 고득점'),
                    ([8,1,9,2,10,3,11,4,12],'홀수 길이')]:nums('2579',label,a)
    for a,b,label in [(1,1,'두 수의 하한'),(1,10000,'하한과 상한'),(10000,10000,'동일 상한'),(7,13,'서로 다른 소수'),
                      (12,36,'약수 관계'),(36,12,'입력 순서 역전'),(48,180,'공통 인수'),(64,81,'서로소 거듭제곱'),
                      (9999,10000,'상한 근처 연속 수'),(462,1078,'비자명 공약수')]:add('2609',label,f'{a} {b}')
    graphs=[(3,[(2,3)],'본인 고립'),(3,[(1,2)],'직접 친구 한 명'),(3,[(1,2),(2,3)],'거리 2 포함'),
      (5,[(1,2),(2,3),(3,4),(4,5)],'거리 3 이상 제외'),(4,[(1,2),(1,3),(2,3)],'삼각형 중복 경로'),
      (6,[(1,2),(1,3),(1,4),(1,5),(1,6)],'별 모양'),
      (5,[(a,b) for a in range(1,6) for b in range(a+1,6)],'완전 그래프'),
      (7,[(1,2),(1,3),(2,4),(3,4),(4,5),(6,7)],'중복 도달 및 분리 성분'),
      (6,[(1,2),(2,3),(3,4),(4,5),(1,5)],'사이클과 고립점'),
      (500,[(1,499),(499,500),(2,3)],'정점 번호 상한')]
    for n,edges,label in graphs:add('5567',label,f'{n}\n{len(edges)}\n'+'\n'.join(f'{a} {b}' for a,b in edges))
    parens=[(['()'],'최소 올바른 괄호'),([')('],'최소 잘못된 접두사'),(['(())'],'중첩'),(['()()'],'연속 쌍'),
      (['(()'],'닫는 괄호 부족'),(['())'],'여는 괄호 부족'),(['('*25+')'*25],'길이 상한 중첩'),
      ([')'*25+'('*25],'균형만 맞고 접두사 오류'),(['()'*25],'길이 상한 반복'),
      (['((()))','()(())',')()(', '(()))('],'여러 질의 혼합')]
    for strings,label in parens:add('9012',label,str(len(strings))+'\n'+'\n'.join(strings))
    for a,b,label in [('A','A','최소 일치'),('A','B','공통 문자 없음'),('ABCDE','ABCDE','전체 동일'),
                      ('ABCDE','EDCBA','역순'),('AAAAAA','AAA','반복 문자'),('ABCDEF','ACE','부분수열과 부분문자열 구분'),
                      ('ABCBDAB','BDCABA','여러 최적해'),('ABABAB','BABABA','교대 반복'),('XYZ','ABCDEFGHIJK','분리 알파벳'),
                      ('A','B'*999+'A','한쪽 길이 상한')]:add('9251',label,a+'\n'+b)
    for n in [1,2,3,4,5,6,7,9,10,11]:add('9663',f'N={n}, '+('해 없음' if n in (2,3) else '보드 크기별 해 개수'),str(n))
    for s,b,label in [('a','a','최소 입력 완전 소거'),('a','b','최소 입력 변화 없음'),('abc','abc','전체 일치'),
                      ('ab','abc','폭발 문자열이 더 김'),('abababab','ab','연속 소거'),('aabb','ab','연쇄 소거'),
                      ('xabcabyabc','abc','양끝과 내부 잔여'),('AaAa','Aa','대소문자 구분'),('12x1212','12','숫자 패턴'),
                      ('abcxyz','0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ','폭발 문자열 길이 상한')]:add('9935',label,s+'\n'+b)
    return d


def main():
    manifest = {'schema_version':1, 'dataset_id':'ipop19-evaluation-v2-a', 'date':'2026-09-16',
      'input_origin':'locally_generated_from_existing_BOJ_specifications',
      'upstream_repository':REPO, 'upstream_commit':COMMIT, 'evaluation_only':True,
      'input_deduplication':'whitespace-token sequence within each problem',
      'exclusion_scope':'all current problem/IPOP_*.inp plus every statement input example',
      'oracle_comparison':'whitespace-token exact equality; Hanoi additionally checks legality and minimality',
      'problems':[]}
    for pid, cases in candidates().items():
        old, paths, example_count = exclusion(pid)
        folder = BASE/f'IPOP_{pid}'; folder.mkdir(parents=True,exist_ok=True)
        entry = {'problem_id':f'IPOP_{pid}', 'title':TITLES[pid], 'summary':SUMMARIES[pid],
                 'specification':f'../IPOP_{pid}.md', 'boj_url':f'https://www.acmicpc.net/problem/{pid}',
                 'oracle_methods':METHODS[pid], 'excluded_unique_inputs':len(old), 'statement_example_count':example_count,
                 'exclusion_sources':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in paths],
                 'upstream_mapping':None, 'cases':[]}
        if pid in MAPPINGS:
            slug,adaptation=MAPPINGS[pid]; path=f'problems/{slug}/solution.js'
            entry['upstream_mapping']={'relationship':'adapted_algorithm_not_identical_problem', 'path':path,
              'url':f'{REPO}/blob/{COMMIT}/{path}', 'sha256':sha(ROOT/'.tools/leetcode-source'/path),
              'adaptation':adaptation, 'role':'additional_checker_only; evaluation inputs generated locally'}
        seen=set()
        for i,(label,inp) in enumerate(cases,1):
            key=canonical(inp)
            assert key not in old, (pid,label,'existing prompt/fixture input')
            assert key not in seen, (pid,label,'duplicate generated input')
            if pid=='9012':
                old_strings={s for item in old for s in item.split()[1:]}
                assert not (set(inp.split()[1:]) & old_strings), 'Reused individual parentheses example'
            seen.add(key)
            a,b=solve(pid,inp)
            assert canonical(a)==canonical(b), (pid,label,a,b)
            ip=folder/f'case{i:02}.inp'; op=folder/f'case{i:02}.out'
            ip.write_text(inp,encoding='utf-8',newline='\n')
            op.write_text(a.rstrip()+'\n',encoding='utf-8',newline='\n')
            entry['cases'].append({'case_id':f'case{i:02}', 'purpose':label, 'origin':'generated',
              'input':ip.relative_to(BASE).as_posix(),'output':op.relative_to(BASE).as_posix(),
              'input_sha256':sha(ip),'output_sha256':sha(op),
              'canonical_input_sha256':hashlib.sha256(key.encode()).hexdigest(),
              'oracle_cross_check':'pass'})
        assert len(seen)>=10
        lines=[f'# IPOP_{pid}: {TITLES[pid]}','',SUMMARIES[pid],'',
          f'[기존 문제 명세](../../IPOP_{pid}.md) · [원문](https://www.acmicpc.net/problem/{pid})','',
          '입력은 이 평가 묶음에서 자체 생성했다. GitHub 저장소의 공식 테스트를 수집한 것이 아니다.',
          '기존 입력 파일 전체와 문제 본문의 입력 예제를 공백 정규화 후 제외했다. 모든 정답은 아래 두 방식으로 교차 검증했다.','',
          f'- 기준 계산: {METHODS[pid][0]}',f'- 독립 검증: {METHODS[pid][1]}','']
        if entry['upstream_mapping']:
            m=entry['upstream_mapping'];lines += [f"추가 대응 풀이: [{m['path']}]({m['url']}). {m['adaptation']}.",'']
        else:lines += ['이 묶음에서 채택한 LeetCode 대응 풀이는 없다. 로컬 명세와 독립 검증기를 사용한다.','']
        lines += ['| 사례 | 목적 | 입력 | 정답 |','|---|---|---|---|']
        lines += [f"| {c['case_id']} | {c['purpose']} | [입력]({Path(c['input']).name}) | [정답]({Path(c['output']).name}) |" for c in entry['cases']]
        lines += ['','정답 파일은 평가 전용이며 번역 프롬프트에 넣지 않는다. 검증 결과와 파일 해시는 상위 manifest 및 validation_report에 기록한다.','']
        (folder/'README.md').write_text('\n'.join(lines),encoding='utf-8',newline='\n')
        manifest['problems'].append(entry)
        print(f'IPOP_{pid}: {len(seen)} independently checked inputs',flush=True)
    manifest['problem_count']=len(manifest['problems'])
    manifest['case_count']=sum(len(p['cases']) for p in manifest['problems'])
    manifest['generator_sha256']=sha(Path(__file__))
    manifest['oracle_sha256']=sha(BASE/'tools/oracles.py')
    (BASE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


if __name__=='__main__':main()
