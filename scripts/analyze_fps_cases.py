"""Explain prespecified cases from source and execution logs; no model calls."""
from collections import Counter
from pathlib import Path
from rttdist.experiment_io import read_json,write_json
from rttdist.fps_experiment import load_config

def main():
    cfg=load_config('fps_v1.yaml');root=Path(cfg['output_root'])/'main'
    audit=read_json(root/'completion_audit.json');assert audit['passed']
    records=[read_json(p) for p in sorted(root.glob('*/*/observation.json'))]
    lines=['# 실제 코드 사례와 실행 비용','',
           '사례는 본 실험 전 동결한 대로 종료 유형별 문제 ID·경로의 사전순 첫 관측을 선택했다. 성공률을 높이기 위한 재생성·출력 수정은 없다.','']
    cases={}
    for label,select in [('성공',lambda r:r['success']),('생성 코드 실패',lambda r:r['evaluable'] and not r['functional']),
                         ('거리 상한 도달',lambda r:r['status']=='max_distance_reached')]:
        choices=[r for r in records if select(r)]
        lines+=[f'## {label}','']
        if not choices:lines+=['해당 관측이 없다. 사례를 만들어 넣지 않는다.',''];cases[label]=None;continue
        r=choices[0];cases[label]={'problem_id':r['problem_id'],'route':r['route'],'status':r['status']}
        lines+=[f'{r["problem_id"]}, {r["route"]}: {r["status"]}. 완료 왕복 {r["completed_roundtrips"]}, '
                f'FPS 종료 크기 {r["fps_size_at_stop"]}, 성공 조건부 거리 {r["d_n"]}, '
                f'Sym_adj={r["sym_adj"]}, Sym_final={r["sym_final"]}.','',
                '| 편도 | 언어 | FPS 크기 | 중복 | 기능 평가 | 인접 유사도 | 원본 유사도 |',
                '| ---: | --- | ---: | --- | --- | --- | --- |']
        for s in r['steps']:
            lines.append(f'| {s["step"]} | {s["language"]} | {s["fps_size"]} | {s.get("duplicate")} | {s.get("evaluation_status")} | {s.get("sym_adj")} | {s.get("sym_origin")} |')
        folder=root/r['problem_id']/r['route'];step=folder/f'step-{r["steps"][-1]["step"]:02}'
        e=read_json(step/'evaluation/evaluation.json')
        bad=next((c for c in e['cases'] if c['status']!='success'),None)
        if e['compile']['exit_code']!=0:
            lines+=['','컴파일/로딩 진단:','', '```text',e['compile']['stderr'][:2500],'```','']
        elif bad:
            inp=Path(cfg['corpus_root'])/r['problem_id']/'evaluation'/(bad['case']+'.inp')
            lines+=['',f'첫 실패 입력: {bad["case"]}, {bad["status"]}.','', '```text',
                    'INPUT: '+inp.read_text(encoding='utf-8')[:1000],
                    'EXPECTED: '+inp.with_suffix('.out').read_text(encoding='utf-8')[:1000],
                    'STDOUT: '+bad['stdout'][:1000],'STDERR: '+bad['stderr'][:1500],'```','']
        ext={'cpp':'cpp','haskell':'hs','prolog':'pl'}[r['steps'][-1]['language']]
        source=step/('source.'+ext)
        lines+=['','종료 단계의 실제 소스:','','```'+ext,source.read_text(encoding='utf-8')[:6000],'```','']
    resources={}
    for phase in ['pilot','main']:
        rr=Path(cfg['output_root'])/phase
        replies=[read_json(p) for p in rr.glob('*/*/step-*/response.json')]
        usage=[r['usage'] for r in replies]
        latencies=[r['latency_seconds'] for r in replies]
        resources[phase]={'logical_responses':len(replies),
            'completion_tokens':sum(u['completion_tokens'] for u in usage) if all(u and 'completion_tokens' in u for u in usage) else None,
            'prompt_tokens':sum(u['prompt_tokens'] for u in usage) if all(u and 'prompt_tokens' in u for u in usage) else None,
            'api_seconds':sum(latencies) if all(x is not None for x in latencies) else None,
            'api_error_attempts':sum(len(read_json(p)) for p in rr.glob('*/*/step-*/api_errors.json')),
            'truncated':sum(any(c.get('finish_reason')=='length' for c in r['body'].get('choices',[])) for r in replies)}
    failure_stage=Counter()
    for r in records:
        if not r['success']:
            last=r['steps'][-1]
            failure_stage[(last['language'],'restored' if last['language']==r['seed_language'] else 'intermediate',r['status'])]+=1
    lines+=['## 전체 실패 위치','', '| 생성 언어 | 중간/복원 | 종료 사유 | 건수 |','| --- | --- | --- | ---: |']
    for key,n in sorted(failure_stage.items()):lines.append('| '+' | '.join(key)+f' | {n} |')
    lines+=['','## 비용','', '| 단계 | 응답 수 | 입력 토큰 | 출력 토큰 | API 지연 합계(초) | 오류 시도 | 잘림 |',
            '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for phase,r in resources.items():
        lines.append(f'| {phase} | {r["logical_responses"]} | {r["prompt_tokens"]} | {r["completion_tokens"]} | {r["api_seconds"]} | {r["api_error_attempts"]} | {r["truncated"]} |')
    lines+=['','로컬 API 사용료는 0이며 전력 비용은 측정하지 않았다. API 지연 합계에는 컴파일·프로그램 실행·JPlag 분석 시간이 포함되지 않는다.']
    (root/'cases.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    write_json(root/'resources.json',resources)
    write_json(root/'selected_cases.json',cases)

if __name__=='__main__':main()
