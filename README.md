# RTT Language Distance Experiment Tool

2026-09-18의 새 FPS 실험은 [계획](docs/01_PLAN.md)과 [체크리스트](docs/02_TODO.md)에 따라 C++·Haskell·Prolog의 공통 15문제·6방향·LM Studio 단일 모델로 예비 18관측과 본 90관측을 완료했다. [결과 및 거리 해설](docs/RESULT_FPS.md), [Word 초록](docs/abs/33rd_abstract_sample.docx), [PDF 초록](docs/abs/33rd_abstract_sample.pdf), [재현 명령](docs/FPS_LIBRARY.md)을 참고한다. 이 실험의 d_n은 출발 코드를 포함한 서로 다른 언어·소스 상태 수이며, 아래 과거 해시 실험의 왕복 횟수 n과 구분한다. 과거 자료 중 현재 작업 트리에 없는 경로는 이번 결과의 근거로 사용하지 않았다.

현재 ABS 지표의 단위와 선행연구의 차이는 [FPS 거리와 완료 왕복 횟수 n](docs/abs/metric_definition.md)을 따른다. n을 FPS 크기나 편도 번역 수와 혼용하지 않는다.

[ABS 실험 자료](docs/abs/README.md)는 C++ → X → C++의 6개 대상 언어 실험을 다룬다. 후속 [Haskell·Prolog 출발 실험](docs/abs/seed_extensions/README.md)은 같은 40문제와 K=10/c=5로 예비 60관측과 본 480관측을 완료했다. 본 실험의 SF(5) 성공은 Haskell 17/240, Prolog 0/240이다. [세 출발 언어 비교](docs/abs/seed_extensions/results/comparison.md)와 [결과 해석](docs/abs/seed_extensions/results/discussion.md)에 조건·불확실성·실패 사례를 기록했다. 추가 실험의 JPlag text 보조 유사도는 기존 C++의 Sym과 별도로 보고한다.

v2 단일 반복 실험 120건이 완료 감사를 통과했다. [논문과 전체 자료](docs/v2/README.md), [논문 PDF](docs/v2/paper_v2.pdf), [결과 요약](docs/v2/short_v2.md)을 참고한다. 아래 실행 명령과 중간 상태 설명은 실험 이력이며 완료된 실험을 다시 시작할 필요는 없다.

새 평가 입력 40문제·520쌍은 `lmstudio_v2.yaml`로 실행한다. 이 설정의 `dataset_index: ./problem/dataset-index.json`이 평가 데이터 위치를 지정한다. 설정의 상대 경로는 YAML 파일 위치를 기준으로 해석하며, 색인 내부 경로는 색인 파일 위치를 기준으로 해석한다.

2026-09-17 동결 실행과 후속 개정은 [v2 실행 기록](docs/EXPERIMENT_v2_log.md)을 따른다. 사용자 요청으로 본 실험을 3회에서 1회, 총 120건으로 축소했다. 기존 r1의 완료 결과를 보존하고 `scripts/run_v2_single.py`가 나머지 경로와 완료 감사를 실행한다. 현재 실행 상태는 `./.venv/Scripts/python.exe scripts/v2_status.py`, 빠른 잠정 집계는 `./.venv/Scripts/python.exe -X utf8 scripts/v2_quick_report.py`로 확인한다. 실행이 중단된 경우에만 `./.venv/Scripts/python.exe -X utf8 scripts/run_v2_single.py`로 재개한다. 기존 `run_v2.py --stage all`은 개정 전 3회 실행용이다.

40문제는 모두 `problem/<문제 ID>/` 아래에 `statement.md`, `prompt_examples/`, `evaluation/`, `reference.cpp`를 두는 구조다. 색인 schema 2가 이 배치를 지정한다. 명세와 예제 중 파일명 순서상 첫 쌍을 프롬프트에 사용하고 `evaluation`만 채점에 사용한다. 평가 입력·정답·README의 사례 설명·실패 진단은 프롬프트에 전달하지 않는다. 문제 목록과 검증 도구는 [데이터 안내](problem/README.md)를 참고한다.

```powershell
$env:PATH = "$PWD/.tools/gcc/bin;$PWD/.tools/R/bin/x64;" + $env:PATH
$env:PYTHONUTF8 = '1'
uv run rttdist validate-corpus --config lmstudio_v2.yaml --execute
uv run rttdist run --config lmstudio_v2.yaml --run-id v2-a-quality-1-r1
```

`lmstudio_v2.yaml`은 `v2-a-quality-1` 데이터와 P2 프롬프트를 사용하는 설정이다. 데이터 및 난이도 점검 결과는 [검토 보고서](docs/DATASET_QUALITY_v2.md)에 있다. 실행 전에 실험에 맞게 확정한다. 검증 기록과 결과는 `artifacts-lmstudio/v2-a-quality-1`에 저장한다. 색인에 없는 문제, 누락된 예제·평가 파일, 예제와 동일한 평가 입력은 오류로 처리한다. 예제와 평가 파일 모두 검증 해시에 포함되므로 변경하면 다시 검증하고 새 run-id로 시작해야 한다. `dataset_index`를 생략한 기존 설정은 `problem/archive/v1`의 원본 배치와 동작을 유지한다. 경로 정리 전 실행 기록을 이어 쓰려 하지 말고 새 경로로 다시 검증한 뒤 새 run-id를 사용한다.

현재 SF 실험은 `experiment_version`이 있는 설정(`lmstudio_pilot_v1.yaml`, `lmstudio_v1.yaml`)으로 실행한다. 기존 설정과 아래 schema 1 설명은 구버전 실행/리포트에 해당한다. 1차 정의는 [계획](docs/v1/PLAN_v1_metrics.md), 실제 실행 기록은 [실험 로그](docs/v1/EXPERIMENT_v1_log.md)를 참고한다.

SF의 첫 왕복은 t=1이고, tau_c는 최초 인접 정규화 토큰 해시 일치 시점이다. K=10은 후보 탐색에만 적용하며 확인 왕복은 tau_c+1부터 최대 tau_c+5까지 수행한다. `p_SF(c)`는 후보가 존재하고 후보까지 모든 단계가 통과하며 확인 1..c의 해시와 기능이 유지된 비율이다. parse_error를 분모에 포함하고 인프라 중단은 제외한다. tau와 Delta_0는 성공 조건부 통계다.

```powershell
$env:UV_CACHE_DIR = 'D:/works/paper-lang-dist/.uv-cache'
$env:PATH = 'D:/works/paper-lang-dist/.tools/gcc/bin;D:/works/paper-lang-dist/.tools/R/bin/x64;' + $env:PATH
$env:PYTHONUTF8 = '1'
uv run rttdist validate-corpus --config lmstudio_validate_v1.yaml --execute
uv run rttdist run --config lmstudio_pilot_v1.yaml --run-id pilot-example
uv run rttdist report --config lmstudio_pilot_v1.yaml --run-id pilot-example
```

검증을 다시 실행하면 검증 해시가 바뀐다. 이미 실행한 run의 재개에는 그 run과 일치하는 검증 기록과 코드/모델 조건이 필요하다. 원본 응답은 각 단계의 llm-response.json 및 api-attempt 기록에, 선택된 실험 시도는 경로별 attempts.json에 보존된다. 모델 응답이 완료된 단계는 재개 시 재요청하지 않는다.

> C++을 여러 언어 경로로 번역한 뒤 다시 C++로 닫는 RTT(Round-Trip Translation) 실험 도구입니다.

```yaml
seed_language: cpp
target_languages: [c, java, python]
```

`target_languages`는 독립 실험 대상 목록입니다. 따라서 위 설정은 아래 3개 RTT 실험을 각각 실행합니다.

```text
cpp -> c -> cpp'
cpp -> java -> cpp'
cpp -> python -> cpp'
```

각 독립 실험에서 한 사이클은 `seed -> target -> seed'`로 닫히며, 이 경우 각 실험의 `translation_count_per_cycle`은 2입니다.

## 현재 구현 범위와 논문 실험 완료 기준

이 저장소의 현재 구현은 RTT 논문 실험을 위한 first-pass metric 수집/리포팅 인프라입니다. 즉, RTT 실행 경로에서 컴파일 체크, 기능 체크, change-count, residual similarity, semantic preservation, complexity delta 상태를 안정적인 artifact schema로 남기는 데 초점을 둡니다.

논문 실험이 완료되었다고 보려면 구현 통과와 별도로 아래 실행 산출물이 필요합니다.

1. 논문 대상 문제 전체를 설정합니다: `IPOP_1436`, `IPOP_2110`, `IPOP_2217`, `IPOP_2579`, `IPOP_5567`.
2. 각 문제에 대해 `cpp -> c -> cpp'`, `cpp -> java -> cpp'`, `cpp -> python -> cpp'` 경로를 실행합니다.
3. 새 run-id로 전체 실행 후 `summary.json`/`summary.md`를 재생성합니다.
4. 최소 `5 problems × 3 target languages = 15`개 result가 생성되었는지 확인합니다.
5. 각 result에 `distance_metrics.schema_version == 1`과 하위 지표가 존재하는지 확인합니다.

기존 `artifacts-lmstudio/lmstudio-rtt-demo`는 과거 데모 실행 산출물일 수 있으므로, 논문 표나 분석에 사용하려면 현재 코드로 새 run을 생성한 뒤 검증해야 합니다.

## 실행

### 설치

```bash
uv sync
```

### LM Studio 준비

1. LM Studio를 실행합니다.
2. 사용할 코드 모델을 다운로드합니다(Qwen3 14B Code, quantized 4-bit).
3. Local Server를 시작합니다.
4. 기본 주소가 아래와 같은지 확인합니다.

```text
http://localhost:1234/v1
```

### 설정 파일 확인

기본 예시는 `lmstudio_1.yaml`입니다.

```yaml
provider: lmstudio
problem_ids:
  - IPOP_1436
seed_language: cpp
target_languages:
  - c
  - java
  - python
lmstudio:
  model: qwen2.5-coder:7b
  temperature: 0
  host: http://localhost:1234/v1
runtime:
  max_iterations: 10
  timeout_seconds: 30
output_root: ./artifacts-lmstudio
problem_root: ./problem/archive/v1
corpus_root: ./corpus/solutions
```

`target_languages`는 독립 RTT 실험 대상 목록입니다. 위 설정은 한 문제마다 `cpp -> c -> cpp'`, `cpp -> java -> cpp'`, `cpp -> python -> cpp'` 세 실험을 실행합니다.

### 실행

```bash
uv run -m rttdist.cli validate-corpus --config lmstudio_1.yaml
uv run -m rttdist.cli run --config lmstudio_1.yaml --run-id lmstudio-rtt-demo
```

실행 중에는 다음과 같은 진행 로그가 콘솔에 출력됩니다.

```text
Starting run: lmstudio-rtt-demo
Output root: /Users/sd/Works/paper-lang-dist/artifacts-lmstudio
[RTT] IPOP_1436: RTT route cpp->c->cpp (2 translations per cycle)
[RTT] IPOP_1436: iteration 1 starts; expecting 2 translations
[RTT] IPOP_1436: iteration 1 step 1/2 cpp->c translating
[RTT] IPOP_1436: iteration 1 step 1/2 cpp->c complete
[RTT] IPOP_1436: iteration 1 step 2/2 c->cpp translating
[RTT] IPOP_1436: iteration 1 step 2/2 c->cpp complete
[RTT] IPOP_1436: iteration 2 starts; expecting 2 translations
[RTT] IPOP_1436: iteration 2 step 1/2 cpp->c translating
[RTT] IPOP_1436: iteration 2 step 1/2 cpp->c complete
[RTT] IPOP_1436: iteration 2 step 2/2 c->cpp translating
[RTT] IPOP_1436: iteration 2 step 2/2 c->cpp complete
[RTT] IPOP_1436: iteration 3 starts; expecting 2 translations
...
```

중단된 동일 run-id를 이어서 진행하려면 아래와 같이 resume 옵션을 추가해서 진행하면 됩니다.

```bash
uv run -m rttdist.cli resume --config lmstudio_1.yaml --run-id lmstudio-rtt-demo
```

기존 실험자료에서 요약만 다시 만들려면 아래와 같이 report 옵션을 추가해서 진행하면 됩니다.

```bash
uv run -m rttdist.cli report --config lmstudio_1.yaml --run-id lmstudio-rtt-demo
```

## 결과 확인

```bash
cat artifacts-lmstudio/lmstudio-rtt-demo/summary.md
```

## 핵심 지표 읽기

`summary.md`와 `summary.json`에서 아래 값을 확인합니다.

| 필드                                      | 의미                                                                                                                |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `rtt_route_key`                           | 실행한 독립 RTT 경로. 예: `cpp->python->cpp`                                                                        |
| `rtt_distance.value`                      | 완료된 RTT cycle 수                                                                                                 |
| `translation_count_per_cycle`             | RTT 1사이클을 완성하는 데 필요한 번역/변환 횟수                                                                     |
| `attempted_translation_count`             | 마지막 iteration에서 시도한 변환 횟수                                                                               |
| `completed_translation_count`             | 마지막 iteration에서 번역 결과 생성까지 완료한 변환 횟수                                                            |
| `failed_translation_count`                | 마지막 iteration에서 번역 단계 자체가 실패한 횟수                                                                   |
| `translation_steps[].compile_check`       | 각 변환 단계의 컴파일/문법 체크 결과(`passed`, `failed`, `skipped`, `not_evaluated`)                                |
| `translation_steps[].functionality_check` | 각 변환 단계의 기능/fixture 체크 결과(`passed`, `failed`, `not_run`, `not_evaluated`)                               |
| `evaluation_checks`                       | 마지막 iteration의 단계별 컴파일/기능 체크 집계                                                                     |
| `distance_metrics`                        | 논문 지표용 묶음(`schema_version == 1`): change-count, residual similarity, semantic preservation, complexity delta |
| `distance_metrics.change_count`           | `rtt_distance`에서 투영한 change-count 거리. 경로 미완료 시 `available=false`, `reason=no_completed_route`          |
| `distance_metrics.residual_similarity`    | 원본 C++와 최종 왕복 C++의 정규화 토큰 멀티셋 Sørensen-Dice 유사도                                                  |
| `distance_metrics.semantic_preservation`  | `evaluation_checks`에서 투영한 논문용 의미 보존 상태(`pass`, `degraded`, `fail`, `not_evaluated`)                   |
| `distance_metrics.complexity_delta`       | 선택적 복잡도 지표 표면. 기본 실행에서는 lizard 등 필수 의존성을 추가하지 않고 하위 지표별 `unavailable`을 기록     |
| `convergence_outcome`                     | `fixed_point`, `oscillation`, `continue`, `terminated_on_failure` 등                                                |
| `semantic_summary.overall`                | 기존/raw 실행 검증 요약. 논문용 의미 보존 판단은 `distance_metrics.semantic_preservation.status`를 우선 사용        |
| `artifacts.final_conversion_log_path`     | 변환 과정 로그 파일                                                                                                 |

1. 각 변환 단계는 번역 결과 생성 직후 컴파일/문법 체크와 기능/fixture 체크를 기록합니다.
2. 중간 단계에서 컴파일은 통과했지만 기능 체크가 실패한 경우에는 실패 상태를 `completed_with_functionality_failure`로 남기고 다음 변환을 계속 진행합니다. 따라서
   후속 단계와 최종 `seed'`가 성공하면 고정점 판정(`fixed_point`)은 완료된 전체 경로를 기준으로 반영됩니다.
3. 컴파일 실패나 최종 `seed'` 단계의 기능 실패는 기존처럼 해당 iteration을 실패로 종료합니다.

## 확장

향후 별도 어댑터를 도입할 때 명시적으로 스키마를 확장합니다. 복잡도 델타도 선택적 어댑터 표면만 제공하므로 기본 환경에서는 `loc`, `token_count`, `cyclomatic`, `function_count`, `max_nesting` 각각이 `optional_tool_not_configured_or_not_installed` 사유로 unavailable일 수 있습니다.

## 테스트

### 전체 테스트

```bash
uv run pytest
```

### 소스 컴파일 확인

```bash
uv run python -m compileall -q src
```
