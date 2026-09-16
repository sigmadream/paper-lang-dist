# 1차 개선 계획: 측정 지표(성공률, 반복 횟수, 코드 변화) 반영

> 근거 슬라이드: `presentation/v1/논문준비_v0.0.2.md`의 "측정 지표: 성공률, 반복 횟수, 코드 변화".
> 근거 코드: `src/rttdist/fixed_point.py`, `pipeline.py`, `metrics.py`, `reporting.py`, `failure_taxonomy.py`, `corpus.py`, `run_state.py`, `lmstudio_client.py`, `exec/adapters.py`.
> 작성일: 2026-09-11 (지표 정합성·재현성·실현 가능성 검토 반영: 2026-09-11)

## 1. 1차 개선의 목표

기존 발표(리뷰_v1.0)의 주 결과는 "고정점까지의 평균 반복 횟수"와 "MOSS 유사도"였다. 그 결과에서 gpt-5.4의 Java·Python 경로는 반복 횟수가 1.0~1.2로 가장 짧았지만 의미 보존율은 0%였다. 즉 빠른 실패가 가까운 거리처럼 보이는 역전이 실제 데이터에 이미 존재한다.

1차 개선의 목표는 이 역전을 제거하는 지표 체계를 정의하고, 코드가 그 정의대로 값을 산출하며, 5문제 예비 실행으로 설정과 실행 시간을 검증한 뒤 최대 20문제의 본 실험에서 새 run으로 표를 재생성하는 것이다.

완료 기준:

1. 슬라이드의 5개 지표(d_SF, p_SF, tau, Delta_0, 실패 이유별 비율)가 summary.json에 경로 단위로 기록된다.
2. 성공 판정이 "후보 안정화 존재 + 확인 왕복까지 코드 유지 + 모든 단계 테스트 통과"로 바뀐다. 기존 데모 산출물(distance_metrics schema 1)은 c = 0만 재평가하고, c >= 1은 `confirmed: unavailable`로 제외한다(4절 단계 3 참조).
3. 예비 실행은 5문제 x 3경로 x 1회, 본 실험은 사전 검증을 통과한 최대 20문제 x 3경로 x 3회로 수행하고 지표 표와 그림을 스크립트로 재생성한다. 자원이 부족하면 본 실험 시작 전에 최소 5문제로 범위를 고정하고 축소 사유를 기록한다. 예비 실행 결과는 본 실험 집계에 합치지 않는다.
4. 논문 본문의 "결과" 절이 반복 횟수 평균 대신 p_SF/d_SF를 주 결과로, tau와 Delta_0를 성공 조건부 보조 결과로 제시한다.

## 2. 지표 정의 확정 (코드 수준)

슬라이드 문장을 그대로 구현하려면 몇 가지가 모호하다. 아래 정의를 1차 개선의 기준으로 제안한다.

기호: x_0는 원본 C++, x_t는 t번째 왕복(C++ -> X -> C++) 후의 C++ 코드. h(x)는 정규화 토큰 해시. K는 후보 탐색 상한(현재 max_iterations=10). c는 확인 왕복 횟수. 실험 단위는 (문제, 경로, run-id) 하나이며 p_SF의 분모는 이 단위로 센다.

반복 번호 규약: 해시 이력은 x_0로 시작하므로(`pipeline.py` 212행) 첫 왕복이 t=1이고 h(x_1) == h(x_0)이면 tau_c = 1이다. 확인 왕복은 tau_c + 1, ..., tau_c + c_max로 번호를 이어 쓰고 iteration.json에 `phase: "confirmation"`과 `confirmation_index: i`를 함께 기록한다. K는 후보 탐색 구간(t <= K)에만 적용되며 확인 왕복은 K 상한에서 제외된다. 따라서 한 실험의 총 왕복 수 상한은 K + c_max이다. tau_c = K인 실험도 확인 왕복을 정상 수행한다.

첨자 SF의 뜻: Stabilized and Functional(안정화되고 기능이 보존됨). 성공은 코드가 더 이상 바뀌지 않는 조건(S)과 모든 단계에서 테스트를 통과하는 조건(F)을 동시에 만족해야 하므로 두 머리글자를 붙였다. 문헌의 표준 약어가 아니므로 논문과 슬라이드에서 처음 쓸 때 정의를 명시한다.

토큰 기반 유사도 2종 (모두 정규화 토큰열 입력, 범위 [0, 1]):

| 이름 | 계산 | 순서 | 무엇에 민감한가 |
| :--- | :--- | :--- | :--- |
| token_multiset_dice | 두 토큰 멀티셋의 겹침 2·overlap / (n_A + n_B) (현재 `metrics.py`의 residual_similarity) | 무시 | 토큰 추가·삭제·이름 변경. 문장 순서 변경에는 둔감 |
| token_sequence_ratio | difflib SequenceMatcher의 ratio 2·M / (n_A + n_B), M은 알고리즘이 찾은 일치 블록들의 토큰 수 합 | 반영 | 위 항목에 더해 문장·블록 순서 변경, 구조 재배치 |

SequenceMatcher는 `isjunk=None, autojunk=False`로 고정한다. 입력 방향은 항상 a = 원본/이전 코드, b = 후보/이후 코드로 두며 이 설정과 Python 버전을 기록한다. ratio는 최장 공통 부분수열의 길이가 아니며 입력 순서에 따라 달라질 수 있으므로 대칭 거리로 해석하지 않는다. 반복 토큰이 많은 코드에서 기본 autojunk 휴리스틱의 영향을 피하기 위한 설정이다. [Python 공식 문서](https://docs.python.org/3.14/library/difflib.html)

Dice가 높고 시퀀스 유사도가 낮으면 재배열 가능성을 살펴보되, 두 값만으로 원인을 확정하지 않는다. 둘 다 식별자 이름 변경을 변화로 세므로 이번 1차의 식별자 추상화 AST 지표와 실제 코드 차이를 함께 확인한다.

| 지표 | 정의 | 비고 |
| :--- | :--- | :--- |
| 후보 안정화 시점 tau_c | h(x_t) == h(x_{t-1})을 만족하는 최소 t (1 <= t <= K) | 현재 `classify_hash_history`의 adjacent fixed point와 동일 |
| 확인 왕복 | tau_c 이후 c회 추가 왕복에서 h(x_{tau_c + i}) == h(x_{tau_c}) 이고 해당 왕복의 모든 단계가 테스트 통과 (i = 1..c) | 슬라이드의 "2회 변환에서도 코드가 유지". 이번 실험은 c_max = 5로 한 번 실행하고 c = 0..5의 결과를 같은 데이터에서 산출 |
| 경로 보존(후보 구간) | 후보 탐색 구간 t = 1..tau_c의 모든 단계(중간 언어와 복원 C++)의 컴파일과 fixture 테스트가 통과 | 현재 중간 단계 기능 실패(컴파일 통과 후 WA/RE/TO)는 `completed_with_functionality_failure`로 계속 진행됨(`pipeline.py` 948-960행). 중간 컴파일 오류는 이미 즉시 종료됨. 새 정의에서는 둘 다 실패 |
| 확인 왕복 i 유지 | h(x_{tau_c + i}) == h(x_{tau_c}) 이고 그 왕복의 모든 단계가 컴파일과 테스트 통과 | 두 조건을 확인 왕복마다 따로 기록(`hash_unchanged`, `all_steps_passed`) |
| 성공(SF, c) | tau_c가 존재하고, 후보 구간 경로 보존이 성립하고, 확인 왕복 1..c가 모두 유지 | c = 0도 후보 안정화와 모든 중간 단계 통과가 필요하므로 현행 판정과 다름. 후보 구간이 통과한 상태에서 확인 왕복이 i번째에 처음 깨지면 c < i는 성공, c >= i는 실패. 확인 왕복별 기록으로 계산(4절 단계 3 참조) |
| p_SF(c) | 성공(c) 실험 수 / 평가 가능한 실험 수 | 평가 가능 = 아래 "평가 가능 실험" 정의 참조. parse_error는 포함. c = 0..5를 한 표로 보고하고 본문 대표값은 c = 1과 c = 5 |
| d_SF | 1 - p_SF | 경로(언어 쌍) 단위, 모델·프롬프트별로 따로 계산 |
| tau | 성공 실험의 tau_c | 중앙값, IQR, n을 보고. 확인 왕복은 tau에 포함하지 않음. tau_c 값 자체는 c와 무관하고 성공 집합만 c에 따라 달라지므로, 본문은 c = 5 성공 집합 기준으로 보고하고 c = 1 기준은 부록에 둔다 |
| Delta_0 | 1 - s(x_0, x_tau) | 성공 실험에서만 계산. x_tau = x_{tau_c}. s는 유사도 함수 3종(토큰 Dice, 토큰 시퀀스, AST TSED)을 각각 보고. tau와 같은 성공 집합 기준 |
| Delta_step | 1 - s(x_{t-1}, x_t) | 현재 `residual_similarity`는 s 자체이므로 `1 - residual_similarity.value`로 변환. 동일 코드의 유사도는 1, 변화량은 0. unavailable은 그대로 전파 |
| 실패 이유 | 아래 분류표 | 경로 단위 비율로 보고 |

평가 가능한 실험의 성공 판정식은 `(tau_candidate is not None) AND (candidate_phase_all_passed is True) AND (confirmations_held >= c)`이다. 후보가 없으면 candidate_phase_all_passed는 null로 두고, 완료된 모든 단계가 통과했더라도 c = 0에서 실패다. 후보 도달 전 실행 경로의 오류는 first_failed_step에 별도로 남긴다. c_max보다 큰 c는 산출하지 않는다. 후보 도달 뒤 기능·형식·해시 오류로 확인 i에서 종료하면 1..i-1의 관찰 결과는 유효하며, i 이후는 종료 규칙상 실패로 계산한다. 인프라 중단은 평가 제외/재개 대상으로 처리하며 실패로 채우지 않는다.

SF는 관찰한 왕복과 fixture에 대한 안정화·기능 통과이며, 영구적인 고정점이나 모든 입력에서의 실행 동치를 보장하지 않는다. 실패 범주 표의 기본 기준은 c = c_max이며, c별 표를 만들 때는 해당 c의 성공/실패 집합으로 다시 집계한다.

실패 분류 (슬라이드 4범주와 현재 FailureStatus의 대응):

| 슬라이드 범주 | 현재 상태값 | 평가 가능 여부 | 비고 |
| :--- | :--- | :--- | :--- |
| 기능 오류 | compile_error(툴체인 있음), runtime_error, wrong_answer, timeout (테스트 실행 중), 컴파일 타임아웃 | 가능 | 중간 단계 기능 실패 후 계속 진행한 경우도 여기로 재분류. 컴파일 타임아웃은 현재 compile_error로 나오므로(`adapters.py` 113-121행) `details.compile_timed_out = true`를 추가해 건수를 따로 셀 수 있게 하되 범주는 기능 오류 |
| 무한 반복 패턴 | oscillation | 가능 | 현재 2주기만 탐지하며 해시 4개가 필요해 t >= 3에서만 발동(`fixed_point.py` 33-40행). 기간 4 확장 시 t >= 7. 기간 5 이상은 최대 허용 횟수 도달로 흡수됨. 후보 안정화 전에만 판정 |
| 최대 허용 횟수 도달 | max_iter_no_convergence | 가능 | K회 안에 후보 안정화 없음 |
| 추가 확인 실패 | (신규) confirmation_failed | 가능 | 후보 안정화 뒤 확인 왕복에서 해시가 바뀜. 확인 왕복 중 테스트 실패는 기능 오류로 분류하고 `details.confirmation_index`로 구분. 후보 안정화 이후에는 순환 판정을 하지 않으므로 oscillation과 겹치지 않음 |
| 출력 형식 오류 | parse_error | 가능 (포함) | 모델 응답에서 코드 추출 불가. 기능 오류와 분리하여 보고. 추출기 결함과 응답 절단은 원본 응답으로 감사하고, 설정 변경과 재실행은 4절 단계 4의 절차를 따름 |
| 인프라 오류 | api_error, 툴체인 미설치로 인한 compile_error | 불가 | 분모에서 제외하고 건수만 보고. 툴체인 부재는 현재 message 문자열에만 남으므로(`adapters.py` 123-135행) FailureRecord.details에 `missing_toolchain: <실행 파일명>`을 구조화 필드로 추가하고, 리포팅은 이 필드로만 인프라 오류를 판정한다 |

평가 가능 실험의 정의: 다음 조건을 모두 만족하는 (문제, 경로, run-id).

1. 문제의 reference.cpp(x_0)가 실행 전 사전 검증에서 모든 fixture를 통과했다. 통과하지 못한 문제는 세 경로 모두 실험 대상에서 제외하며 기능 오류로 세지 않는다.
2. 최종 상태가 api_error가 아니고, details.missing_toolchain이 없다.
3. 본 실험의 고정된 조건과 검증 이력이 일치하며, 지정된 종료 규칙에 따라 완료되었다. 미완료 실험과 예비 실행은 본 실험 분모에서 제외한다.

인프라 오류는 동일 조건에서만 같은 run-id·attempt-id로 `resume`한다(확인 왕복 중 중단 포함). 재개가 불가능하면 기존 산출물을 보존하고 새 attempt-id로 처음부터 재실행한다. 추천 저장 규칙은 `<output_root>/<run_id>/<problem_id>/<route>/attempt-001/`이며, 경로 루트의 `attempts.json`에 채택 attempt를 명시한다(4절 단계 1의 artifacts.py 계약 참조). 원본 응답과 실패 산출물을 삭제하거나 덮어쓰지 않는다. 같은 경로 루트의 `rerun_log.json`에는 이전/신규 attempt, 원인, 시각, 조건 해시, 채택 여부를 남긴다. 자동 재시도는 호출당 최대 3회이며 실험 단위 복구 예산·종료 시각은 예비 실행 후 고정한다. 해결되지 않은 인프라 오류가 있으면 제외 건수와 진행률을 보고하고 본 실험 완료로 표시하지 않는다. 무제한 재개를 일정의 전제로 삼지 않는다.

실험 조건의 기록: summary.json의 `run_metadata`에 다음을 기록한다. 결과 표의 각주에 그대로 옮긴다.

- 모델: 설정의 model 문자열, 실제 로드한 모델 ID/파일 식별자, 양자화, LM Studio 버전을 실행 시작 시 저장. `/v1/models`는 모델 목록 확인용으로 원본 응답을 보존하며, 양자화와 실제 로드 컨텍스트는 설치 버전에 맞는 native API 또는 명시적 서버 설정 기록에서 확보한다. 현재 공식 `/api/v1/models`에는 `quantization`, `loaded_instances[].config.context_length`가 정의되어 있다. 지원되지 않으면 수동 기록과 수집 출처를 남기고 파일명에서 추정하지 않는다. [LM Studio 공식 문서](https://lmstudio.ai/docs/developer/rest/list)
- 디코딩: temperature 0, 명시적 max_tokens, 실제 로드 컨텍스트 길이와 나머지 유효 디코딩 설정을 예비 실행 후 고정. 현재 클라이언트는 max_tokens를 보내지 않으므로(`lmstudio_client.py` 318-323행) 요청 필드를 추가한다. `finish_reason == "length"`는 추출 성공 여부와 관계없이 모든 응답에서 절단으로 기록한다.
- 실행 제한과 툴체인: `timeout_seconds`(현재 30초)는 컴파일과 fixture 각각에 적용된다. g++, gcc, javac, java의 실행 경로·버전과 OS를 기록한다. Python은 uv로 실행한 파이프라인의 `sys.executable` 절대 경로와 `sys.version`, uv 버전을 기록한다. PythonExecutionAdapter도 이 `sys.executable`로 생성 코드를 실행하므로, smoke test와 결과 메타데이터의 Python은 동일한 프로젝트 가상환경의 Python 3.14를 가리켜야 한다. 셸 PATH의 `python`(검토 시 Espressif 배포판)은 실험 인터프리터로 사용하지 않는다.
- 프롬프트와 코드: `PROMPT_TEMPLATE_VERSION`, 실제 템플릿 내용의 체크섬, 추출기 버전, 실행 코드의 커밋과 미커밋 변경 식별 정보. 현재 prompt_template_hash는 버전 문자열의 해시이므로 실제 내용 해시로 보완한다.
- 문제 집합: 사전 검증을 통과한 문제 ID 목록, 제외 사유, 원본·statement·fixture 내용 해시, 검증 결과 식별자.
- 조건 식별: `experiment_version`, `phase`(pilot/main), 반복 번호, 위 모델·프롬프트·코퍼스·실행/디코딩 설정과 지표 설정의 조건 해시. run-id·반복 번호·출력 경로는 조건 해시와 분리한다. 외부 서버 설정 변경도 해시에 반영하고 resume 시 현재 값과 대조한다. 실제 요청·응답과 시도별 호출 시간·토큰 수를 보존한다.

확정된 결정 (2026-09-11):

1. 확인 왕복 횟수 c: 1~5를 모두 본다. 실행은 c_max = 5 한 번으로 하고 확인별 해시·테스트 결과로 c = 0..5를 계산한다. 확인 i에서 기능 오류 또는 parse_error가 나면 해당 상태로, 모든 단계 통과 후 해시만 바뀌면 `confirmation_failed`로 종료하며 `details.confirmation_index = i`를 남긴다. 후보 구간이 통과하고 1..i-1이 유지되었으면 c < i는 성공이다.
2. parse_error: 분모에 포함하고 별도 "출력 형식 오류"로 보고한다. 민감도 표는 최종 상태 parse_error인 실험을 분자·분모 모두에서 제외한 p_SF도 제시하고, c별 성공 건 중 제외된 수를 남긴다. 추출기 수정이나 출력 예산 변경은 새 experiment_version을 만들며, 변경 전후 결과를 같은 조건으로 합산하지 않는다.
3. Delta_0의 s 함수: 토큰 멀티셋 Dice(이미 구현), 토큰 시퀀스 유사도(difflib ratio), AST 편집 거리 기반 TSED 3종을 1차에서 모두 보고한다. PDG/CSSG는 2차로 미룬다.

AST 유사도(TSED)의 구현 방식:

- 파서: tree-sitter와 tree-sitter-cpp. Delta_0는 C++ 대 C++ 비교이므로 C++ 파서 하나면 된다. 후보 버전은 tree-sitter 0.26.0, tree-sitter-cpp 0.23.4, apted 1.0.3이다. 프로젝트 Python 3.14 가상환경에서 설치·로드·파싱을 검증한 뒤 의존성과 lock 파일에 고정한다. 검토 시점에는 해당 가상환경에 세 패키지가 설치되어 있지 않았다.
- 트리 변환: named 노드는 자식 순서를 유지하고 타입을 라벨로 사용하되 주석은 제외한다. 식별자 계열 노드는 타입으로 추상화하고, 리터럴·원시 타입·연산자는 종류와 원문 값을 보존한다. `binary_expression` 등의 연산자는 unnamed 노드여도 원래 위치에 남긴다. 괄호·구분자 등 나머지 unnamed 노드는 제외한다. 포함/제외 노드 타입과 토큰 목록을 `representation_version`으로 고정한다. named 타입만 남기면 `a+b`와 `a-b`의 차이가 사라지므로 그 방식은 사용하지 않는다. [tree-sitter-cpp 문법 정의](https://raw.githubusercontent.com/tree-sitter/tree-sitter-cpp/v0.23.4/src/node-types.json)
- 거리(본 실험 추천 정의): 위 표현의 두 트리에 APTED를 적용하며 삽입·삭제·변경 비용은 각각 1/1/1로 고정한다. `cost_config = {insert: 1, delete: 1, rename: 1}`이며, TSED = max(0, 1 - TED / max(|T_A|, |T_B|))로 정의한다. 세 연산을 동일하게 취급하고 소표본에서 비용 조정을 추가하지 않는 재현 가능한 기준값으로 추천한다. 이는 본 실험이 선택한 기본 비용이며 원 논문의 데이터별 조정값이나 최적 비용을 재현하려는 설정이 아니다. 식별자 추상화도 포함한 본 실험의 정의로 보고하고 파서·표현 버전과 비용 설정을 스키마에 기록한다. 관련 방법의 참고 문헌: [Song 등 논문](https://aclanthology.org/2024.acl-short.3/).
- 파싱 실패 처리: ERROR 노드 수와 missing 노드 수를 각각 기록한다. 하나라도 있으면 AST 값은 unavailable(reason=parse_invalid)이며 AST 유효 집계에서 제외한다. SF 판정과 토큰 지표는 유지한다. 오류 없는 측정값의 n, SF 성공 수 대비 측정률, 제외 사유별 건수를 보고하며 지표 간 산점도는 둘 다 측정된 쌍만 사용한다.
- 성능: 노드 수만으로 실행 가능성을 단정하지 않는다. 20개 원본과 예비 실행의 생성 코드에서 노드 수·계산 시간·최대 메모리를 측정한다. 예비 설정은 노드 상한 5,000개, 코드 쌍당 AST 처리 시간 제한 30초로 두고 본 실험 전에 확정한다. 별도 작업 프로세스로 제한 시간을 강제하고 tree_too_large, ast_timeout, memory_limit 등 실패 사유를 기록한다. AST는 저장된 코드로 후처리하여 번역 run의 완료와 분리한다.

## 3. 현재 코드와의 간극

| 항목 | 현재 동작 | 필요한 변경 |
| :--- | :--- | :--- |
| 고정점 판정 | 인접 해시 일치 즉시 SUCCESS로 종료 (`pipeline.py` 515-526행) | 후보 안정화 후 c회 확인 왕복을 추가 실행하고, 유지될 때만 SUCCESS |
| 성공 판정 | 최종 왕복 C++만 통과하면 iteration SUCCESS. 중간 기능 실패는 `degraded`로 표시만 됨 | 후보 존재, 후보 구간 전체 통과, 확인 1..c 유지로 성공(c)를 판정. 최종 상태와 c별 성공을 분리 |
| 의미 보존 집계 | `distance_metrics.semantic_preservation`은 최종 iteration만 반영 (`reporting.py` 197행) | 후보 구간(t = 1..tau_c)의 통과 여부와 확인 왕복별 통과 여부를 따로 기록하고 최초 실패 단계를 남김. run 전체의 단일 bool은 두지 않음 |
| 반복 횟수 | `rtt_distance.value` = 완료된 왕복 수 (성공·실패 무관) | tau_c, 확인 왕복 수, 최종 상태를 분리 기록 |
| 잔존 유사도 | 직전 주기 입력 vs 복원 코드의 유사도 s | Delta_step = 1-s로 변환하고 x_0 vs x_tau의 Delta_0 추가. README의 설명도 정정 |
| 유사도 함수 | 토큰 멀티셋 Dice 하나 | 토큰 시퀀스 유사도와 AST TSED 추가, 지표별 이름·범위·비용 설정을 스키마에 명시 |
| 실패 분류 | 8개 FailureStatus | confirmation_failed 추가, 슬라이드 범주로의 매핑 테이블 추가 |
| 경로 집계 | divergence_rate(고정점 도달 비율), 반복 수 평균/표준편차 | p_SF, d_SF, tau 중앙값/IQR/n, Delta_0 중앙값/IQR, 실패 범주별 건수와 비율, 95% 신뢰구간 |
| 신뢰구간 | 없음 | 통합 p_SF, tau, Delta_0는 문제 단위 부트스트랩. 단일 run p_SF에만 Wilson 구간을 부가 보고 |
| 실험 키 | run_id, problem_id, route | 모델 ID, 프롬프트 버전, 반복 번호를 summary 키로 승격 (현재는 manifest checksums에만 있음) |
| 문제 수 | README와 설정은 5문제(설정 파일은 1문제) | 저장소에는 20문제의 statement, fixture 10쌍, reference.cpp가 이미 존재. 20문제 사용 가능 여부를 validate-corpus로 확인 |
| 코퍼스 검증 | `validate-corpus`는 statement, fixture 쌍, reference.cpp 파일의 존재만 검사(`corpus.py` 28-63행). 파이프라인도 x_0를 fixture에 대해 실행하지 않음 | `validate-corpus --execute` 옵션 추가: reference.cpp를 컴파일하고 fixture 전체를 실행해 통과 여부와 최대 실행 시간을 기록. `run`은 이 검증을 통과한 문제만 실행 |
| 인프라 오류 식별 | 툴체인 부재는 message 문자열에만 남고 details에는 execution_status만 기록(`pipeline.py` 940-944행) | `details.missing_toolchain`, `details.compile_timed_out` 구조화 필드 추가 |
| LLM 호출 | max_tokens와 재시도 없음, HTTP 타임아웃 300초 고정, api_error는 즉시 종료(`lmstudio_client.py` 318-345행). finish_reason은 저장됨 | max_tokens 설정 추가(본 실험에서는 필수), 일시적 네트워크 오류는 최대 3회 재시도 후 api_error. 유효 서버 설정도 조건 해시에 반영 |
| 재개(resume) | `run_state.py`가 iteration 산출물에서 이력을 복구하고 종결 레코드로 재개 여부를 판정 | 확인 왕복 단계(`phase: "confirmation"`)를 복구 대상에 포함하고, 후보 안정화 시점과 확인 진행 횟수를 manifest에서 복원 |
| 실험 메타데이터 | 모델 문자열, 프롬프트 체크섬만 manifest에 존재 | 2절의 실험 조건 항목을 summary.json `run_metadata`에 기록 |

## 4. 작업 계획

전체 일정은 약 4주의 조건부 추정이다. 단계 4의 추론·감사 시간은 예비 실행의 실측으로 다시 산정한다. 실행 환경 확인 -> 원본 20문제 검증 -> 5문제 예비 실행 -> 조건 고정 -> 본 실험의 순서를 지킨다.

### 단계 0. 정의 확정 (0.5주)

- 2절의 성공 판정식, 유사도/변화량 방향, SequenceMatcher 설정, AST 식별자 추상화와 연산자·리터럴 보존, 반복 집계 단위를 구현 계약으로 확정한다. AST 노드 목록과 자원 제한은 예비 실행에서 검증하고 본 실험 전에 버전으로 고정한다.
- tau의 인덱스 규약(첫 왕복이 t=1, tau_c는 일치가 발생한 t)을 README와 슬라이드 발표자 노트에 통일.
- Python 환경은 uv로 관리한다. Python 3.14를 프로젝트 실행 버전으로 고정하고 `uv sync`로 의존성을 준비한다. 검증·실험·리포팅은 `uv run rttdist ...`, 테스트는 `uv run pytest`, 인터프리터 점검은 `uv run python -c "import sys; print(sys.executable); print(sys.version)"`로 수행한다. 본 실험에서는 확정한 uv.lock과 Python 버전을 유지한다.
- 설정 경로 규칙: `output_root`, `problem_root`, `corpus_root`의 상대 경로는 실행 명령의 작업 디렉터리가 아니라 설정 파일이 있는 디렉터리를 기준으로 해석된다(`src/rttdist/config.py`의 load_experiment_config 참조). `lmstudio_v1.yaml`은 프로젝트 루트에 두는 것을 기본으로 하고, 임시 폴더 등 프로젝트 밖에 설정을 둘 때는 세 경로를 절대 경로로 지정한다. 검증과 run은 같은 설정으로 해석된 경로를 사용한다.
- 검토 시점(2026-09-11) 확인된 기반: 파일 구조 검증은 20문제·200 fixture 쌍을 통과했고 기존 테스트 92개가 통과했다. 현재 셸 PATH에서 g++, gcc, Rscript를 찾지 못했고 프로젝트 가상환경에 AST 패키지가 없었다. 설치 여부 자체와 PATH 노출 여부를 구분해 점검한다. 원본 실행·생성 코드의 실행 성능은 아직 검증되지 않았다. pyproject의 requires-python은 이미 >=3.14이다.

### 단계 1. 파이프라인 변경 (1주)

- `config.py`: `runtime.confirmation_cycles`(기본 5, 범위 0~5)와 `runtime.stop_on_intermediate_failure`(기본 true) 추가. `runtime.max_iterations`는 후보 탐색 상한 K만 의미하도록 문서화. `confirmation_cycles: 0`, `stop_on_intermediate_failure: false` 조합을 `tests/fixtures/config/legacy_control.yaml`로 두어 기존의 확인 없는 실행과 중간 기능 실패 후 진행을 점검한다. 새 SF 판정과 순환 탐지 확장까지 과거와 같다는 뜻은 아니며 과거 결과는 별도 legacy 지표로 유지한다.
- `corpus.py`, `cli.py`: `validate-corpus --execute` 추가. reference.cpp를 g++로 컴파일하고 fixture 전체를 실행해 문제별 통과 여부, fixture별 실행 시간, 툴체인 버전/경로, 컴파일 옵션, OS, 제한 시간을 `<output_root>/corpus_validation.json`에 기록한다. output_root는 설정 파일 기준으로 해석된 절대 경로이며, 검증 명령은 이 위치에 저장하고 `run`도 이 파일만 조회한다. 원본·statement·입출력 fixture의 내용 해시와 검증기 버전을 저장한다. `run`은 현재 파일·검증 조건이 기록과 일치하고 통과한 문제만 실행하며, 검증 파일이 없거나 내용·조건이 바뀌었으면 재검증을 요구한다. 실행에 사용한 검증 결과의 내용과 해시는 run_metadata에 보존해 후속 검증으로 파일이 갱신되어도 이전 run의 근거를 유지한다. g++, gcc, javac, java와 uv로 기동한 프로세스의 `sys.executable`을 별도 smoke test로 점검한다. Python smoke test는 실제 어댑터와 동일하게 `[sys.executable, 시험 코드 경로]`로 수행하고 그 경로·버전을 기록한다.
- `fixed_point.py`: 반환값을 `fixed_point_candidate`, `confirmed`, `oscillation`, `continue`로 세분화. 순환 탐지는 기간 2~4까지 확장(최근 해시 이력에서 반복 패턴 탐색). 순환 판정은 후보 안정화 전 구간에서만 호출한다.
- `pipeline.py`: 후보 안정화 감지 후 확인 왕복 루프(최대 c_max회)를 추가. 확인 왕복의 iteration_index는 tau_c + i로 이어 쓰고 `phase: "confirmation"`, `confirmation_index`, `hash_unchanged`, `all_steps_passed`를 iteration.json에 기록. 확인 중 형식/기능 오류는 해당 상태로, 모든 단계 통과 후 해시가 바뀌면 `confirmation_failed`로 종료하며 confirmation_index를 남긴다. 계산 불가능한 해시/테스트 값은 null로 두고 false와 구분한다. c_max회 모두 유지되고 후보 구간도 통과한 경우 SUCCESS. K 상한 판정은 후보 탐색 구간에만 적용한다. 중간 기능 실패는 stop_on_intermediate_failure가 true면 즉시 종료한다. FailureRecord.details에 missing_toolchain, compile_timed_out을 추가한다.
- `lmstudio_client.py`: `lmstudio.max_tokens`를 요청에 전달하고 본 실험에서는 명시값을 요구한다. 일시적 URLError/HTTP 5xx는 지수 백오프로 최대 3회 재시도(최초 요청 포함 최대 4회) 후 api_error. 각 시도의 요청·응답·시간을 보존한다. 실행 시작/재개 시 모델 목록과 설치 버전에 맞는 native API/서버 기록으로 유효 설정을 수집하고 조건 해시를 확인한다.
- `run_state.py`: 현재 manifest 버전들과 새 확인 상태 지원 버전을 구분하여 올리고, distance_metrics.schema_version과 별개로 관리한다. 확인 왕복의 후보 시점·완료 횟수·유효 prefix를 복구한다. API_ERROR를 무조건 종결 상태로 반환하는 현행 동작을 변경해 동일 조건의 중단 작업을 같은 attempt에서 재개하고 이미 완료한 단계/왕복을 이중 집계하지 않는다. 구버전 manifest는 읽기만 허용하며 재개를 거부한다. 원본/fixture/실제 프롬프트/외부 서버 설정 변경도 검출한다.
- `artifacts.py`의 추천 저장 계약: 경로 루트는 기존 `<output_root>/<run_id>/<problem_id>/<route>/`를 유지하고 첫 실행부터 `attempt-001/`, `attempt-002/`처럼 1부터 증가하는 attempt 디렉터리를 둔다. 각 attempt 안에 `run.json`(manifest), `iterations/`, `exec/` 등 해당 시도의 모든 산출물을 저장한다. 경로 루트의 `attempts.json`은 `{schema_version, condition_hash, active_attempt_id, selected_attempt_id, attempts: [{attempt_id, manifest_path, status}]}`를 저장하며 manifest_path는 경로 루트 기준 상대 경로(예: `attempt-001/run.json`)다. 재실행은 번호를 증가시키고 기존 디렉터리는 보존한다. 개별 API 재시도와 같은 attempt의 resume은 새 attempt 번호를 만들지 않고 시도별 로그를 보존한다.
- attempt 채택과 report 탐색: 지정된 종료 규칙으로 끝나 평가 가능한 첫 attempt를 성공/실패와 관계없이 `selected_attempt_id`에 기록한다. 인프라 중단 또는 미완료 상태에서는 null이다. 완료 manifest를 저장한 뒤 인덱스를 원자적으로 갱신하며 채택된 실패를 더 좋은 결과로 바꾸기 위해 재실행하지 않는다. `report`는 경로 루트의 `attempts.json`에서 이 ID에 해당하는 manifest 하나만 읽고 조건 해시·종료 상태·경로 루트 내부의 상대 경로인지 검증한다. 최신 디렉터리나 성공 attempt를 임의로 선택하지 않는다. null이면 미완료/인프라 제외로 보고하고, 누락·중복 ID·잘못된 참조는 계약 오류로 처리한다. 구버전 경로는 schema를 확인해 기존 legacy 읽기 경로로만 처리한다. 재개/재실행 이력은 경로 루트의 `rerun_log.json`에 남긴다.
- `failure_taxonomy.py`: `CONFIRMATION_FAILED` 추가, `paper_category(record)` 매핑 함수 추가. parse_error는 `format_error` 범주로, details.missing_toolchain이 있으면 `infrastructure`로 매핑.
- 테스트: 확인 유지/변경과 순환 판정 최소 길이, 중간 실패 즉시 종료, tau_c = K에서 확인 수행, 후보 없이 K회 테스트만 통과한 경우 c = 0 실패를 검증한다. 확인 i의 형식/기능 오류에서 c < i 성공, 동일 조건 API 중단 재개 시 완료 prefix 보존·중복 집계 방지, 변경된 조건의 resume 거부도 검증한다. 코퍼스 검증은 원본 또는 fixture 수정 후 과거 통과 기록의 재사용 거부와 실행 실패 문제 제외를 포함한다. attempt 계약은 첫 실행 경로, 동일 attempt 재개, 재실행 시 번호 증가·기존 파일 보존, 성공/실패와 무관한 채택, 미채택/잘못된 참조의 report 처리, API 재시도와 attempt 번호의 분리를 검증한다. Python smoke test와 어댑터가 uv 프로세스의 같은 sys.executable을 사용하는지도 확인한다.

### 단계 2. 지표 확장 (0.5주)

- `metrics.py`: `distance_metrics.schema_version`을 2로 올리고 아래 필드를 추가한다.

| 필드 | 기록 및 계산 규칙 |
| :--- | :--- |
| stabilization | tau_candidate(null 허용), confirmation_cycles_run(완료된 확인 왕복 수), confirmations_held(1부터 연속으로 해시·테스트를 모두 통과한 수), first_broken_confirmation, first_break_reason(hash_changed/test_failed/format_error). 중단된 시도는 완료 수에 포함하지 않고 attempt 기록에 남김 |
| route_preservation | candidate_phase_all_passed(bool 또는 후보 미도달 시 null), first_failed_step, evaluated_step_count, per_confirmation: [{confirmation_index, hash_unchanged, all_steps_passed, status}]. 성공(c)는 2절의 후보 존재를 포함한 판정식을 사용 |
| delta_0 | 지표별 {metric, status, value, reason, reference: "seed_source", candidate: "stabilized_source"}. SF 성공 조건과 지표별 측정 가능 여부를 분리 |
| delta_step | 기존 residual_similarity의 s를 1-s로 변환. measured일 때만 계산하고 unavailable은 전파. 원래 유사도는 legacy 필드로 구분 |

- `normalize.py` 옆에 `similarity.py` 신설: `token_multiset_dice`, `token_sequence_ratio`. 둘 다 정규화 토큰 입력이며 SequenceMatcher의 autojunk=False와 입력 방향을 고정한다.
- `ast_similarity.py` 신설: 2절의 표현 규칙과 APTED로 계산한다. 반환값에는 status, value, reason, ted, 양쪽 노드 수, error/missing 노드 수, cost_config, representation_version, 파서 버전, 처리 시간·메모리를 포함한다. 파서 오류나 자원 제한 초과는 unavailable로 반환하고 SF 값을 바꾸지 않는다.
- `pyproject.toml`, `uv.lock`: tree-sitter, tree-sitter-cpp, apted를 필수 의존성으로 추가하고 버전을 고정한다. `uv sync` 후 `uv run rttdist validate-corpus`가 파서 로드를 함께 검사하도록 한다. 설치·파서 로드·실제 파싱과 관련 테스트를 확인한 뒤, 현재 미커밋 상태인 Python 요구 버전·의존성 변경을 포함해 두 파일을 예비 실행 시작 전에 함께 커밋한다. 해당 커밋 ID와 lock 파일 해시를 예비 실행 메타데이터에 기록하고, 예비 실행 중 의존성을 조정하면 두 파일을 다시 함께 커밋하여 변경 이력을 남긴다. 본 실험은 최종 확정한 커밋과 lock 파일을 사용한다.
- 검증용 변형 집합(`tests/fixtures/similarity/`): (a) 식별자만 일대일 변경하면 추상화 TSED=1. (b) 문장 순서 교환은 Dice=1이며 AST 차이는 추상화 후에도 두 문장이 구별되는 경우와 같은 구조로 합쳐지는 경우를 모두 확인한다. (c) for->while과 (e) 다른 구현은 지표별 실제 반응을 보고하며 감소량 순위를 강제하지 않는다. (d) `a+b`->`a-b`와 별도 리터럴 값 변경은 표현에 보존되어 TSED<1이어야 한다. 이 사례들은 지표 반응 검증이며 모든 변형의 기능 보존을 가정하지 않는다.
- 테스트: 동일 코드에서 similarity=1, Delta_0=Delta_step=0; x_0와 직전 코드가 다른 경우 Delta_0와 Delta_step의 참조 차이; 반복 토큰 200개 이상과 고정 입력 방향; 위 AST 표현 계약을 검증한다. 파서 미설치·ERROR/missing·크기/시간 제한의 unavailable 전파와 SF 유지도 확인한다. 지표 간 감소량 순위를 테스트의 정답으로 두지 않는다.

### 단계 3. 리포팅 변경 (0.5주)

- `reporting.py`의 `_build_rtt_route_aggregates`를 아래 구조로 교체한다.

```text
rtt_route_aggregates[route] = {
  experiment_version, condition_hash, problem_count, run_count,
  evaluable_count, excluded_infrastructure_count, excluded_seed_failure_count,
  incomplete_count, parse_error_count,
  by_confirmation: {                      # c = 0..c_max; 본 실험은 0..5
    c: {success_count, p_sf, d_sf, p_sf_ci95, d_sf_ci95,
        ci_method: "problem_cluster_bootstrap", ci_status,
        p_sf_excluding_parse_error, d_sf_excluding_parse_error,
        sensitivity_evaluable_count, sensitivity_excluded_success_count}
  },
  conditional: {                          # 본문 c=5, 부록 c=1
    c: {success_count,
        tau: {n, median, q1, q3, min, max, median_ci95, ci_status, valid_resamples},
        delta_0: {metric_name: {n, measurement_rate, median, q1, q3,
                               median_ci95, ci_status, valid_resamples,
                               excluded_by_reason}}}
  },
  failures: {confirmation: 5, denominator, categories: {category: {count, rate}}},
  per_run: {run_id: {by_confirmation: {c: {success_count, evaluable_count,
                                           p_sf, p_sf_wilson_ci95}}}},
  repeatability: {by_confirmation: {c: {p_sf_mean, p_sf_min, p_sf_max}}},
  bootstrap: {unit: "problem", resamples: 2000, seed: 20260911,
              paired_routes: true, interval: "percentile"}
}
```

- 성공(c)는 후보 존재를 포함한 2절의 판정식으로 계산한다. 예를 들어 후보 구간과 확인 1..2를 통과한 뒤 확인 3에서 테스트가 실패하면 final_status가 wrong_answer라도 c=0..2는 성공이다. tau_candidate와 후보 코드 경로를 보존해 c=1 성공·c=5 실패인 실험의 조건부 Delta_0도 후처리할 수 있게 한다.
- summary.md에는 경로별 표(c=1/5의 p_SF, d_SF와 각 성공 집합의 tau, Delta_0), c=0..5의 p_SF 추이 표, 기본 c=c_max의 실패 범주 표를 출력한다.
- 기존 distance_metrics schema 1은 해시 이력과 모든 단계 결과가 있을 때만 c=0을 새 정의로 재평가한다. 필요한 기록이 없으면 unavailable로 두며 성공을 추정하지 않는다. c>=1은 확인 정보가 없어 `confirmed: unavailable`이다. 구버전 결과는 별도 legacy 표로 제시하고 본 실험에 합산하지 않는다.
- 반복 표본 집계: `report --runs r1,r2,r3`는 같은 조건 해시·문제 집합의 본 실험만 합산하며 중복 attempt나 예비 실행을 거부한다. 각 경로의 attempts.json에서 selected_attempt_id가 가리키는 manifest만 읽고 집계 관측값에 attempt_id도 남긴다. 주 결과는 통합 p_SF(c)와 문제 단위 부트스트랩 95% 구간이다. run별 p_SF와 평균·최소·최대는 재현성 정보로 보고한다. 문제 수 P와 관측 수 P x 3을 구분하며, 동일 문제의 세 반복을 독립 표본으로 취급한 pooled Wilson 구간은 사용하지 않는다. 단일 run의 Wilson 구간만 부가 보고한다.
- 부트스트랩: P개 문제를 복원추출하고 뽑힌 문제의 모든 경로·반복을 함께 가져온다. 각 재표집에서 c별 p_SF와 해당 성공 집합의 tau/Delta_0 중앙값을 다시 계산한다. 지표별 AST 결측은 별도로 제외한다. 경로 차이도 같은 재표집으로 계산하여 문제 대응을 유지한다. d_SF 구간은 p_SF의 [lo, hi]에서 [1-hi, 1-lo]로 변환한다. n=0인 통계는 null이며 유효 재표집 수가 2,000회 중 95% 미만이면 해당 중앙값 CI는 unavailable로 표기한다. 성공 0건/전건 또는 모든 문제의 값이 같아 구간이 퇴화하면 ci_status=degenerate를 기록하고 불확실성이 없다고 해석하지 않는다.
- 실패 비율은 기본 c=c_max에서 범주 건수 / evaluable_count로 계산하므로 범주 비율의 합은 d_SF(c_max)이다. 인프라·원본 실패·미완료는 제외 건수로 따로 보고한다. 분모가 0이면 비율은 null이다. parse_error 제외 민감도와 legacy 제외에도 각각 분모와 이유를 기록한다.
- `graph/v1/drawFigures.r`: summary.json의 집계와 실험별 관측값을 읽어 (a) 경로별 d_SF와 문제 단위 신뢰구간, (b) 성공 조건부 tau 상자그림, (c) Delta_0 상자그림(지표 3종), (d) Dice 대 TSED 산점도를 생성한다. 관측값에는 문제·경로·run·c별 성공 여부·tau·지표별 값/측정 상태를 포함하고, 그림마다 유효 n과 AST 측정률을 표시한다. v0의 하드코딩 데이터프레임은 사용하지 않는다.
- 리포팅 검증: 동일 문제의 결과를 세 run에 복제해도 독립 문제 수가 늘지 않는지, 재표집에서 경로·반복의 대응이 유지되는지 확인한다. c별 성공/실패 합, 후보 미도달, AST 결측, n=0, CI 퇴화, 서로 다른 조건 해시의 합산 거부를 검증한다. 그림은 저장된 관측값만으로 재생성되는지 확인한다.

### 단계 4. 예비 실행과 본 실험 (잠정 1주, 예비 실행 후 재산정)

1. 실행 환경과 원본 검증: g++, gcc, javac, java와 uv 실행 프로세스의 sys.executable(Python 3.14)의 실행 가능 여부·버전·옵션을 점검하고 Rscript 및 그림 생성 패키지도 준비한다. `uv run rttdist validate-corpus --execute`에 설정 파일 등 필요한 인자를 전달해 20개 reference.cpp를 g++에서 실행한다. 문제별 제외 사유와 검증 해시를 저장한다. C++의 실행 시간만으로 Python 제한이 충분하다고 결론 내리지 않으며, 계산량이 큰 문제는 예비 실행에서도 확인한다.
2. 예비 실행: 검증 통과 문제 중 기존 5문제를 출발점으로 삼되 코드 길이·계산량을 고려해 5개 ID와 선정 근거를 실행 전에 기록한다. `phase: pilot`, 별도 run-id로 5문제 x 3경로 x 1회를 K=10, c_max=5, stop_on_intermediate_failure=true에서 수행한다. 추출 실패, 모든 응답의 절단, 컴파일/실행 시간, LLM 호출 시간·토큰 수, 성공 표본 수, AST 노드 수·처리 시간·메모리를 측정한다. 예비 실행에만 설정 조정을 허용하며 각 시도의 결과를 보존한다.
3. 본 실험 조건 고정: `lmstudio_v1.yaml`에 검증 통과 문제 집합(최대 20), 3경로, K=10, confirmation_cycles=5, stop_on_intermediate_failure=true, 명시적 max_tokens와 제한 시간을 저장한다. 모델·양자화·로드 컨텍스트·프롬프트/추출기·검증·AST 설정을 묶어 experiment_version과 조건 해시를 고정한다. 자원상 축소가 필요하면 이 시점에 문제 집합과 이유를 확정한다. 성공 표본이 적다는 이유로 본 실험 도중 문제를 교체하지 않는다.
4. 본 실험: 같은 조건으로 새 run-id r1~r3(예: `v1-qwen25-7b-p1-r1`)를 실행한다. 같은 문제·경로·t가 세 run 모두에 있는 위치에서 해시 일치율을 계산하고 비교 가능 위치 수와 미도달 수를 함께 보고한다. 후보 탐색/확인 단계 차이도 기록한다. 집계는 단계 3의 규칙을 따른다.
5. 응답 감사와 변경 관리: parse_error 응답을 전수 감사하고, 컴파일 오류를 포함한 모든 응답에서 `finish_reason == "length"`를 검사한다. 절단은 원인 플래그로 남기고 고정 조건에서 발생한 종료 상태와 결과를 유지한다. 본 실험 중 추출기 결함이 확인되면 해당 버전의 결과를 잠정 처리하고 영향을 받은 범위를 기록한다. 추출기·max_tokens·컨텍스트·제한 시간 변경이 필요하면 새 experiment_version/run-id로 고정 문제 집합과 반복 전체를 다시 실행한다. 실패한 실험만 더 큰 예산으로 대체하거나 이전 성공 결과와 합산하지 않는다. 동일 조건의 일시적 인프라 오류만 2절의 resume/attempt 절차로 복구한다.
6. 완료 검증: run별 결과 수는 P x 3경로, 세 run 합계는 P x 3경로 x 3회이며 각 경로 루트의 attempts.json이 유효한 selected_attempt_id 하나를 가리킨다. distance_metrics schema=2, 조건/검증 해시 일치, 인프라 미해결·미완료 0건, c=c_max의 실패 범주 합=실패 수, c=5 성공의 완료 왕복 수=tau_c+5, p_SF(c)의 단조 비증가를 확인한다. AST의 measured+unavailable 건수는 해당 SF 성공 수와 같아야 하며, 유효 측정 n·측정률·제외 사유를 보고한다. AST가 전부 unavailable이어도 SF 결과를 바꾸지 않으며 AST 비교는 자료 부족으로 명시한다. 정해진 복구 예산 안에 인프라 오류를 해결하지 못하면 미완료 상태와 제외 건수를 남긴다.

추론 예산은 논리적 번역 요청 수와 실제 API 시도 수를 구분한다. 20문제 본 실험은 run당 최대 20 x 3 x (10+5) x 2 = 1,800회, 세 run 최대 5,400회다. 예비 실행의 최대 450회는 별도다. 최초 요청 후 최대 3회 재시도가 있으므로 본 실험 API 시도 수의 이론상 상한은 21,600회이며, 실험 단위 재개/재실행으로 추가되는 호출은 별도 집계한다. 실제 완료 예산은 예비 실측과 복구 제한으로 정한다.

| 호출당 평균 시간 가정 | 본 실험 5,400회 순차 호출 시간 |
| :--- | :--- |
| 30초 | 45시간 |
| 60초 | 90시간 |
| 120초 | 180시간 |

위 계산은 조기 종료·재시도·컴파일·fixture 테스트·AST 후처리·감사 시간을 반영하지 않은 시나리오다. 예비 실행의 실제 평균과 긴 호출의 분포, 경로별 조기 종료 비율, 가용 장비 시간을 이용해 단계 4 일정을 확정한다. 1주 안에 완료된다고 가정하지 않는다.

### 단계 5. 논문·슬라이드 반영 (0.5주)

- 결과 절 구성: 표 1 경로별 통합 p_SF/d_SF와 문제 단위 부트스트랩 95% CI(c=1/5), 표 2 c=5 성공 조건부 tau와 Delta_0(지표 3종, 중앙값, IQR, 유효 n, AST 측정률), 표 3 c=5 실패 이유별 비율(출력 형식 오류 별도), 그림 1 c=0..5의 p_SF 추이, 그림 2 토큰 지표와 AST 지표의 관계. 부록에는 c=1 조건부 결과, run별 재현성, parse_error 제외 민감도와 변형 집합의 반응표를 둔다.
- 기존 발표의 표(평균 반복 횟수, MOSS)는 "기존 지표"로 남겨 빠른 실패의 해석 문제를 설명한다. 구버전 데이터로 c>=1의 d_SF를 추정하지 않는다. 모델·프롬프트·문제 집합이 다른 과거 결과와 본 실험의 순위를 직접 비교하지 않으며, 순위 비교가 필요하면 같은 관측 자료에서 산출 가능한 기존 지표와 새 지표를 함께 계산한다.
- 슬라이드 "측정 지표" 페이지에 tau 인덱스 규약, 확인 왕복 c의 범위(1~5)와 사후 계산 방식, 분모 정의(parse_error 포함)를 한 줄씩 추가.
- 한계 절: 단일 모델·단일 프롬프트와 선정한 5~20문제에 대한 탐색적 결과이며 언어 고유 거리로 일반화하지 않는다. 세 반복은 독립 문제 수를 늘리지 않는다. TSED는 구문 구조 유사도이고 fixture 통과도 모든 입력의 실행 동치를 보장하지 않는다. AST 결측과 성공 조건부 선택의 영향을 명시하며 PDG/CSSG는 2차 범위로 둔다.

## 5. 산출물

| 산출물 | 위치 | 완료 판단 |
| :--- | :--- | :--- |
| 지표 정의 문서 | docs/PLAN_v1_metrics.md (본 문서) | 성공 판정·변화량·AST 표현·집계·변경 관리 규칙 확정 |
| 코드 변경 | src/rttdist/{config,corpus,cli,fixed_point,pipeline,failure_taxonomy,lmstudio_client,run_state,artifacts,metrics,similarity,ast_similarity,reporting}.py | `uv run pytest` 전체 통과, 기존 데모 report 재생성 성공(c = 0 판정과 unavailable 표기 확인) |
| 코퍼스 검증 결과 | `<output_root>/corpus_validation.json` | 20문제의 통과 여부, 실행 시간, 파일 내용 해시, 검증 조건·툴체인 기록. run은 같은 경로를 조회하고 사용한 내용·해시를 보존 |
| 예비 실행 산출물 | artifacts-lmstudio/pilot-* | 5문제 x 3경로 x 1회, 실행·추론·AST 성능 측정 및 본 실험 예산 확정 |
| 본 실험 설정 | lmstudio_v1.yaml 및 run_metadata | 문제 집합·모델·출력 예산·실행/AST 제한·복구 예산과 조건 해시 고정 |
| 본 실험 산출물 | artifacts-lmstudio/v1-* | 고정 조건 3회 반복, 단계 4 완료 검증 통과, 원본 응답·attempt·rerun_log 보존 |
| 표·그림 | graph/v1/, presentation/v1/ | summary.json의 집계·관측값에서 재생성, 유효 n·AST 측정률·결측 사유 표시 |
| 논문 결과 절 초안 | 논문 원고 | 표 3개와 논의 1절 |

## 6. 위험과 대응

- 성공 표본이 0인 경로(예: gpt-5.4 Python)는 tau와 Delta_0가 결측이다. 0이나 최대값으로 대체하지 않고 n=0으로 보고한다.
- 확인 왕복 5회는 성공 후보마다 최대 10회의 추가 호출을 요구한다. c = 0..5의 p_SF 추이가 c = 1 이후 평탄하면 후속 실험에서 c를 줄일 근거가 된다.
- temperature 0에서도 LM Studio 응답이 완전히 재현되지 않을 수 있다. 확인 왕복 실패가 언어 특성이 아니라 디코딩 비결정성에서 올 수 있으므로, 확인 실패 건은 두 코드의 차이(Delta_step)를 함께 보고한다.
- parse_error를 포함하면 응답 형식 준수 능력이 약한 모델의 d_SF가 커진다. 민감도 표로 영향 크기를 공개한다. 추출기 결함이나 출력 예산 변경은 새 조건 버전에서 처리하고 실패 사례만 선택적으로 대체하지 않는다. 절단 여부는 최종 오류 종류와 별개로 모든 응답에서 기록한다.
- 토큰 정규화 해시는 공백·주석만 무시하므로 식별자 이름 변경도 "변화"로 센다. 이는 보수적인 판정이므로 그대로 두되, 논문에 정규화 규칙을 명시한다. 안정화 판정(해시)과 Delta_0(유사도)는 목적이 다르므로 판정 규칙을 TSED로 바꾸지 않는다.
- tree-sitter-cpp의 문법 버전에 따라 노드 타입이 달라질 수 있다. 파서와 표현 버전을 고정하고 ERROR/missing 노드를 기록한다. 파싱 실패·크기/시간/메모리 제한은 AST unavailable로 보고하며 SF 결과를 변경하지 않는다. AST 측정률이 낮으면 구조 비교의 근거가 부족함을 명시한다.
- 저장소의 20문제 중 일부는 reference.cpp가 fixture를 통과하지 않을 수 있다. 단계 4의 사전 검증에서 걸러내고 최종 문제 수를 결과와 함께 보고한다.
- fixture당 30초 실행 제한은 Python 경로에서 timeout을 더 자주 만들 수 있어 언어 효과와 실행 환경 효과가 섞인다. 원본 검증과 Python을 포함한 예비 실행을 근거로 제한을 고정하고 timeout을 wrong_answer와 구분해 보고한다. 본 실험에서 실패한 경로만 제한 시간을 늘리지 않는다.
- Python 요구 버전은 이미 >=3.14이다. 프로젝트 가상환경에서 AST 패키지의 설치·로드·실제 파싱을 검증하고 버전과 lock 파일을 고정한다. 설치 가능성 확인과 실제 실행 환경 준비 완료를 구분한다.
- 확인 왕복 중 인프라 중단은 동일 조건의 resume으로 복구하되 정해진 복구 예산을 적용한다. 미해결 건은 진행률·제외 건수와 함께 남기고 완료로 표시하지 않는다. 재개할 때 조건 해시와 검증 이력을 확인하고 이미 완료한 왕복을 중복 집계하지 않는다.
- 20문제에서 10개 성공인 단일 run의 Wilson 95% 구간도 약 30~70%다. 소표본의 미세한 경로 순위를 확정하지 않으며, 부트스트랩 구간이 퇴화하거나 조건부 유효 표본이 부족하면 해당 한계를 표시한다. 성공 0건도 유효한 SF 결과이고 tau/Delta_0는 n=0으로 남긴다.
- 추론 시간은 단계 4의 실측으로 다시 산정한다. 확인 왕복·재시도·감사 비용이 크면 본 실험 시작 전에 문제 수와 일정을 확정하여 조정하고, 진행 중 결과에 따라 조건을 바꾸지 않는다.
- 모델 2개·프롬프트 2종 교차는 2차 범위로 둔다. 1차는 지표 정의와 파이프라인 정합성에 집중한다.
