"""Write the human-readable companion report from audited final measurements."""
from pathlib import Path
from collections import Counter
from rttdist.experiment_io import read_json

ROOT=Path(__file__).resolve().parents[1]

def num(v):return 'NA' if v is None else f'{v:.3f}'
def interval(v):return 'NA' if v is None else '['+', '.join(num(x) for x in v)+']'

def main():
    root=ROOT/'artifacts-lmstudio/fps-v1/main'
    s=read_json(root/'summary.json');audit=read_json(root/'completion_audit.json')
    assert s['complete'] and audit['passed']
    records=[read_json(p) for p in sorted(root.glob('*/*/observation.json'))]
    nsuccess=sum(r['success'] for r in records)
    lines=['# 세 언어 RTT/FPS 실험 결과','',
           f'본 실험 90관측을 모두 평가했다. 성공 {nsuccess}건, 평가 실패 {90-nsuccess}건, 미평가·미완료 0건이다. '
           '사용자 지시에 따라 LM Studio의 Qwen2.5-Coder 7B Instruct(Q4_K_M) 한 모델로 실행했으며, 예비 18관측은 본 결과와 분리했다.','',
           '[Word 초록](abs/33rd_abstract_sample.docx), [PDF 초록](abs/33rd_abstract_sample.pdf), '
           '[실행 설계와 로그](FPS_EXPERIMENT_LOG.md), [공통 문제와 구현 차이](FPS_CORPUS.md), [라이브러리 재현](FPS_LIBRARY.md).','',
           '## 방향별 측정','', '| 경로 | 성공/평가 | P_sf | Wilson 95% | bootstrap 95% | P_functional |',
           '| --- | --- | ---: | --- | --- | ---: |']
    for route,r in s['routes'].items():
        lines.append(f'| {route} | {r["success"]}/{r["evaluable"]} | {num(r["p_sf"])} | {interval(r["wilson95"])} | {interval(r["bootstrap95"])} | {num(r["p_functional"])} |')
    lines+=['','P_sf는 기능 검사와 근사 수렴의 공동 성공률이며 통계적 p값이 아니다. 성공 0건의 bootstrap은 [0,0]으로 퇴화한다. '
            '이를 모집단 성공률이 정확히 0이라는 증거로 해석하지 않으며 Wilson 구간을 함께 제시한다. '
            '모든 경로를 같은 문제 단위로 2,000회 재표집했으므로 방향 간 대응을 보존한다. R=1로 모델 실행 간 변동성을 추정하지 않는다.','',
            '| 경로 | 성공 표본 n | d_n 중앙값 [Q1,Q3] | Sym_final 중앙값 [Q1,Q3] | Sym_adj 중앙값 [Q1,Q3] |',
            '| --- | ---: | --- | --- | --- |']
    for route,r in s['routes'].items():
        vals=[num(r[k]['median'])+' '+interval([r[k]['q1'],r[k]['q3']]) if r[k]['n'] else 'NA' for k in ['d_n','sym_final','sym_adj']]
        lines.append(f'| {route} | {r["success"]} | '+' | '.join(vals)+' |')
    lines+=['','## 거리의 의미','',
            'd_n은 왕복 횟수가 아니라 출발 상태를 포함한 서로 다른 (언어, 소스 해시) 상태 수다. '
            '예를 들어 원본 복원이 정확히 일치한 A₀→B₀→A₀은 2이고, 비슷하지만 다른 A₁로 복원된 A₀→B₀→A₁은 3이다. '
            '이후 B₀→A₁이 반복돼도 FPS 크기는 3이다. 해시는 줄바꿈만 LF로 맞추고 주석·공백을 보존하며, 유사도로 상태를 합치지 않는다.','',
            '거리와 Sym_final은 성공 조건부다. 실패의 실제 종료 FPS가 작더라도 가까운 언어라고 해석할 수 없다. '
            '성공률이 낮은 경로에서 드물게 성공한 짧은 거리만 비교하면 선택 편향이 생긴다. '
            'Sym_adj는 연속 복원 코드의 안정화, Sym_final은 원본과의 표현 유사도이므로 두 값이 크게 다를 수 있다. '
            '이 거리는 대칭성·삼각부등식이 증명된 수학적 거리함수가 아니다.','',
            '## 대응 비교','', '| 차이 방향 | 지표 | 공통 표본 | 평균 차이 | Bonferroni 95% (3비교) |',
            '| --- | --- | ---: | ---: | --- |']
    for c in s['paired_comparisons']:
        lines.append(f'| {c["left"]} - {c["right"]} | {c["metric"]} | {c["common_n"]} | {num(c["mean_difference"])} | {interval(c["bonferroni95_family3"])} |')
    lines+=['','성공률 차이는 공통 평가 문제, 거리·유사도 차이는 공통 성공 문제에만 근거한다. '
            '공통 표본이 없으면 NA이며, 작은 표본이나 동일한 값에 따른 퇴화 구간은 summary.json에 표시했다. '
            '모델 간 비교는 두 번째 LLM이 없어 이번에는 수행하지 않았다.','',
            '## 예비 사용 문제 제외 민감도','', '| 경로 | 성공/평가 | P_sf | d_n 중앙값 | Sym_final 중앙값 |',
            '| --- | --- | ---: | ---: | ---: |']
    for route,r in s['excluding_pilot_problems']['routes'].items():
        lines.append(f'| {route} | {r["success"]}/{r["evaluable"]} | {num(r["p_sf"])} | {num(r["d_n"]["median"])} | {num(r["sym_final"]["median"])} |')
    lines+=['','예비에 사용한 IPOP_2609, IPOP_9012, LC_0547을 제외했다. 임계값 변화 실험은 본 설계에 등록하지 않았다. '
            '0.85에서 조기 종료한 궤적으로 미관측 0.90 도달 시간이나 거리를 추정하지 않았다.','',
            '## 종료 상태와 실제 사례','', '| 상태 | 건수 |','| --- | ---: |']
    for status,n in sorted(Counter(r['status'] for r in records).items()):lines.append(f'| {status} | {n} |')
    lines+=['','[사전 규칙으로 선택한 실제 코드·오류·비용](../artifacts-lmstudio/fps-v1/main/cases.md)을 함께 확인한다. '
            '오류가 난 코드는 수정하지 않았다. 관측되지 않은 상한 도달 사례는 만들어 넣지 않았다.','',
            '## 한계와 해석','',
            'JPlag text 점수는 연산자 변화에도 1.0을 줄 수 있고 공통 래퍼에 민감하다. '
            '보조 분기 변화 진단은 본 실행 시작 후 수행했으며, 동결된 0.85 임계값·프롬프트·결과를 변경하는 데 사용하지 않았다. '
            '유사도는 표면 안정성의 운영적 척도로만 쓰고 기능은 별도로 검사했다. 13개 유한 입력의 통과는 의미 동등성의 증명이 아니다.','',
            '문제 15개는 모집단 무작위 표본이 아니라 공통 구현 가능성을 기준으로 영역을 맞춘 표본이다. '
            'C++·Haskell·Prolog의 초기 알고리즘과 자료 표현, 짧은 코드와 공통 입출력 부분, '
            'Q4_K_M 양자화·8,192 토큰 로딩 문맥·프롬프트·컴파일러·시간 제한·θ가 결과에 영향을 줄 수 있다. '
            '그러므로 결과를 언어 전체의 순위나 패러다임의 인과 효과로 일반화하지 않는다.','',
            '## 원본과 재현','',
            '- [관측 CSV](../artifacts-lmstudio/fps-v1/main/observations.csv)',
            '- [전체 통계·문제 유형별 결과 JSON](../artifacts-lmstudio/fps-v1/main/summary.json)',
            '- [분포와 궤적 그림](../artifacts-lmstudio/fps-v1/main/distributions.png)',
            '- [원본 응답·평가·JPlag CSV 대조 감사](../artifacts-lmstudio/fps-v1/main/completion_audit.json)',
            '- [모델 호출 없는 재생성 검증](../artifacts-lmstudio/fps-v1/main/reproducibility.json)',
            '- [동결 설정](../fps_v1.yaml) 및 [본 실행 설계](../artifacts-lmstudio/fps-v1/main_design.json)',
            '', '모든 계획 관측과 분모를 대조하고, 저장된 소스를 모델 원응답과, 기능 결과를 실제 stdout과, '
            '유사도를 JPlag 원본 CSV와 비교했다. 표와 그림은 동일 관측에서 재생성한다.']
    (ROOT/'docs/RESULT_FPS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

if __name__=='__main__':main()
