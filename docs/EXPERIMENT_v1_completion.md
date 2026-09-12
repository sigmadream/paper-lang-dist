# 1차 실험 완료 점검

2026-09-11. 요청 범위는 docs/PLAN_v1_metrics.md에 따른 예비/본 실험과 루트 RESULT_v1.1.md의 결과·해석이다. 아래 근거는 실제 완료 산출물과 실행 결과를 확인한 기록이다.

| 요구사항 | 확인한 근거 | 판정 |
|---|---|---|
| 원본 20문제 사전 실행 검증 및 내용 해시 | artifacts-lmstudio/corpus_validation.json, validation/. 19문제 통과, IPOP_1260 제외. 본 실험 감사가 검증 스냅샷과 현재 입력 해시를 대조 | 충족 |
| 5문제 x 3경로 예비 실행 및 자원 실측 | pilot-v1-qwen25-7b-a/summary.json, diagnostics.json, completion_audit.json: 15/15 완료. 실행·호출·토큰 및 생성 C++ AST 71쌍 실측은 EXPERIMENT_v1_log.md | 충족 |
| 본 실험 조건 사전 고정, 의존성/실행 코드 보존 | lmstudio_v1.yaml, 세 run의 run_metadata.json과 code_snapshot. 동일 조건 해시 및 lock/코드/실제 프롬프트/추출기 해시를 감사 | 충족 |
| 19문제 x 3경로 x 3회, 채택 attempt 하나씩 | 각 run 57개, 통합 171개. attempts.json 채택 참조와 관측 키 유일성을 report 및 completion_audit.json이 확인 | 충족 |
| SF 정의, 후보 K=10/확인 c=0..5, 실패 prefix와 재개 | tests/test_experiment_v1.py의 경계·중간 실패·확인 실패·순환·재개·attempt/재시도 검사. 실제 171건의 해시/단계 결과에서 성공식을 독립 재계산 | 충족 |
| schema 2의 p_SF/d_SF, tau, Delta_0, Delta_step, 실패 범주 | v1-combined/summary.json 및 각 iteration.json. 실패 범주 합·c별 단조성·성공 왕복 수 tau+5·토큰 변화량 재계산 통과 | 충족 |
| AST 표현·결측·자원 제한과 변형 반응 | preflight-v1/similarity_variants.json, AST 단위 검사, 원본/예비 AST 실측. 본 실험 c=5 성공 101건 모두 AST 측정, 결측 합계 검사 통과 | 충족 |
| 문제 단위 대응 bootstrap, c=1/5 조건부 통계, 반복/민감도 | 통합 summary.json에 2000회/seed=20260911, 대응 경로 차이, 조건부 중앙값 CI, run별 Wilson, 반복 평균/범위, parse 제외 분모 보존. RESULT_v1.1.md에 표로 출력 | 충족 |
| 응답 전수 감사, 인프라/미완료 제외 공개 | 세 diagnostics.json: 논리 요청/API 시도 1602/1602, 오류·절단·형식 오류 0. 통합 exclusions=[], complete=true. 원본 응답과 실행 소스 대조 통과 | 충족 |
| 구버전 별도 재평가와 기존 동작 유지 | lmstudio-rtt-demo/legacy_sf_reassessment.json: 3경로 c=0 후보/단계 증거, c>=1 unavailable, 본 실험 미포함. 구버전 report 재생성 및 전체 기존 테스트 통과 | 충족 |
| 표·그림 재생성 | summary.md에 성공률·조건부 통계·실패 표. presentation/v1/results-v1.1에 PNG/PDF 각 5개. 5종 그림을 시각 확인하고 사분위수 계산을 표와 일치시킴 | 충족 |
| 결과 절, 실제 사례 해석, 한계, 슬라이드 정의 | RESULT_v1.1.md에 주 표/그림/부록 및 해석. fixture 중복, 단일 모델/프롬프트, 성공 조건부 선택, CI 한계 명시. presentation/v1/논문준비_v0.0.2.md에 SF/tau/c/분모 노트 반영 | 충족 |
| 전체 테스트와 저장 자료 재생성 | `uv run pytest -q -o cache_dir=.pytest_cache_v1`: 110 passed. git diff --check 통과. regeneration_audit.json에서 보고서/통합 JSON/PNG 5개의 바이트 일치 확인. 문서 링크 12개에 누락 없음 | 충족 |

실험 프로세스는 모든 반복 완료 메시지와 종료 코드 0으로 종료했다. 본 실험의 inference 소스는 실행 중 변경하지 않았다. 종료 후 reporting_v1.py에 Markdown 표 출력을 보완했으며 통합 summary.json의 SHA256이 변경 전후 동일함을 확인했다. 통계·원본 응답·선정 결과를 바꾸는 재실행은 하지 않았다.

주 결과는 c=5에서 C 26/57, Java 35/57, Python 40/57이며, 경로 간 차이의 문제 단위 95% 구간은 모두 0을 포함한다. 이 완료 판정은 정해진 실험과 산출물의 완료를 뜻하며 언어 고유 거리나 일반적인 기능 동치를 검증했다는 뜻은 아니다.
