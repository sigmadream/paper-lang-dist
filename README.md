# RTT Language Distance Experiment Tool

> 이 저장소는 C++ 기준 해법을 `C`, `Java`, `Python`으로 왕복 번역한 뒤 다시 C++로 되돌리면서, 언어 간 거리를 정량화하기 위한 실험 도구입니다.

핵심 아이디어는 다음 세 가지를 함께 보는 것입니다.

- 왕복 번역이 몇 번 만에 고정점(`fixed_point`)에 도달하는가
- 최종 round-trip C++가 원본 C++와 얼마나 비슷한가
- 구조(AST)와 복잡도 메트릭이 언어별로 어떻게 달라지는가

## 현재 저장소에 들어 있는 것

- 기준 문제 코퍼스: `problem/`
- 기준 C++ 해법: `corpus/solutions/`
- 실험 코드: `src/rttdist/`
- 테스트: `tests/`
- 스모크 실행 결과: `artifacts/smoke/`
- 검증 증거: `.sisyphus/evidence/`

현재 스모크 코퍼스는 정확히 두 문제만 사용합니다.

- `IPOP_1436`: 영화감독 숌 (`problem/IPOP_1436.md`)
- `IPOP_2579`: 계단 오르기 (`problem/IPOP_2579.md`)

두 문제 모두 샘플 픽스처 10쌍(`1.inp`~`10.inp`, `1.out`~`10.out`)을 가지고 있습니다.

## 요구 사항

- Python 3.10+
- 로컬 툴체인
  - `gcc` (`C`)
  - `g++` (`C++`)
  - `javac` + `java` (`Java`)
  - `python` (`Python`)

오프라인 스모크 테스트는 OpenAI 네트워크 호출 대신 mock 응답 파일을 사용합니다. 실제 OpenAI API로 실행하려면 `RTTDIST_OPENAI_MOCK_RESPONSES`를 설정하지 않고 OpenAI SDK가 요구하는 인증 환경 변수를 준비해야 합니다.

## 설치

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

## 기본 사용법

CLI 엔트리포인트는 `python -m rttdist.cli` 입니다.

모든 실행 방식에서 공통으로 쓰는 기본 명령은 같습니다.

```bash
python -m rttdist.cli validate-corpus --config <config.yaml>
python -m rttdist.cli run --config <config.yaml> --run-id <run-id>
python -m rttdist.cli resume --config <config.yaml> --run-id <run-id>
python -m rttdist.cli report --run-id <run-id>
```

`validate-corpus` 는 다음을 검사합니다.

- `problem_ids`
- 대상 언어 목록
- 문제 설명 파일 존재 여부
- 샘플 입출력 픽스처 존재 여부
- `corpus/solutions/<problem-id>/reference.cpp` 존재 여부

## 실행 방식

이 저장소는 현재 세 가지 방식으로 사용할 수 있습니다.

### 1) Mock 사용

가장 안정적이고 재현 가능한 회귀 테스트 경로입니다.

- 설정 파일: `tests/fixtures/config/minimal.yaml`
- mock 응답 파일: `tests/fixtures/e2e/smoke_openai_responses.json`
- 출력 루트: `artifacts/`

설정 내용:

- 문제: `IPOP_1436`, `IPOP_2579`
- 대상 언어: `c`, `java`, `python`
- 모델 설정: `gpt-4o-mini`, `temperature=0`
- 반복 한도: `20`
- 타임아웃: `30초`

mock 응답 파일에는 총 8개의 응답이 들어 있습니다.

- `IPOP_1436`: `cpp -> c/java/python` 3개 + `target -> cpp` 1개
- `IPOP_2579`: `cpp -> c/java/python` 3개 + `target -> cpp` 1개

실행 예시는 다음과 같습니다.

```bash
export RTTDIST_OPENAI_MOCK_RESPONSES=tests/fixtures/e2e/smoke_openai_responses.json

python -m rttdist.cli validate-corpus --config tests/fixtures/config/minimal.yaml
python -m rttdist.cli run --config tests/fixtures/config/minimal.yaml --run-id smoke
python -m rttdist.cli resume --config tests/fixtures/config/minimal.yaml --run-id smoke
python -m rttdist.cli report --run-id smoke
```

추천 용도:

- 빠른 회귀 테스트
- CI성 검증
- 고정된 결과를 기준으로 artifact/report 형식 검증

### 2) Ollama 사용

로컬 모델로 실제 번역을 시험하고 싶을 때 쓰는 경로입니다.

지원 방식은 두 가지입니다.

- 전체 스모크 코퍼스용 설정: `tests/fixtures/config/minimal-ollama.yaml`
- 가장 작은 1문제 x 1언어 smoke용 설정: `real-ollama-smoke.yaml`

`tests/fixtures/config/minimal-ollama.yaml`:

- provider: `ollama`
- 문제: `IPOP_1436`, `IPOP_2579`
- 대상 언어: `c`, `java`, `python`
- 모델: `qwen2.5-coder:7b`
- 호스트: `http://localhost:11434`
- 출력 루트: `artifacts-ollama/`

`real-ollama-smoke.yaml`:

- provider: `ollama`
- 문제: `IPOP_1436`
- 대상 언어: `python`
- 모델: `qwen2.5-coder:7b`
- 출력 루트: `artifacts-real-ollama/`

실행 전 확인:

```bash
ollama list
ollama serve
```

현재 개발 환경에서는 다음 모델들이 확인되었습니다.

- `qwen2.5:3b`
- `qwen3:latest`
- `codellama:7b`
- `qwen2.5-coder:7b`

가장 작은 Ollama smoke 실행 예시:

```bash
python -m rttdist.cli validate-corpus --config real-ollama-smoke.yaml
python -m rttdist.cli run --config real-ollama-smoke.yaml --run-id ollama-smoke-001
python -m rttdist.cli resume --config real-ollama-smoke.yaml --run-id ollama-smoke-001
python -m rttdist.cli report --config real-ollama-smoke.yaml --run-id ollama-smoke-001
```

전체 2문제 x 3언어 Ollama smoke 예시:

```bash
python -m rttdist.cli validate-corpus --config tests/fixtures/config/minimal-ollama.yaml
python -m rttdist.cli run --config tests/fixtures/config/minimal-ollama.yaml --run-id ollama-minimal
python -m rttdist.cli resume --config tests/fixtures/config/minimal-ollama.yaml --run-id ollama-minimal
python -m rttdist.cli report --config tests/fixtures/config/minimal-ollama.yaml --run-id ollama-minimal
```

주의 사항:

- Ollama는 로컬 모델 품질과 머신 자원에 따라 결과 편차가 큽니다
- 재현성을 위해 현재 구현은 `ollama.temperature = 0` 만 허용합니다
- mock smoke와 달리 실행 시간이 더 길고 결과가 덜 고정적일 수 있습니다

### 3) OpenAI 사용

OpenAI SDK를 통해 실제 API 호출로 실험하는 경로입니다.

- 최소 실제 smoke 설정: `real-smoke.yaml`
- 문제: `IPOP_1436`
- 대상 언어: `python`
- 모델: `gpt-4o-mini`
- 출력 루트: `artifacts-real-openai/`

현재 `tests/e2e/test_smoke_experiment.py` 는 mock 기반 smoke만 검증합니다. 즉, 테스트를 그대로 돌린다고 해서 실제 OpenAI API를 호출하지는 않습니다.

실제 OpenAI SDK 경로는 `src/rttdist/openai_client.py` 에 있습니다.

- `RTTDIST_OPENAI_MOCK_RESPONSES` 가 설정되어 있으면 mock transport를 사용합니다
- 이 변수가 없으면 `OpenAI()` 클라이언트를 만들고 `client.chat.completions.create(...)` 를 호출합니다
- 현재 모델은 `gpt-4o-mini` 로 고정이고, 온도는 `0`만 허용합니다

실행 전 준비:

```bash
unset RTTDIST_OPENAI_MOCK_RESPONSES
export OPENAI_API_KEY=...your key...
```

실행 예시:

```bash
python -m rttdist.cli validate-corpus --config real-smoke.yaml
python -m rttdist.cli run --config real-smoke.yaml --run-id real-smoke-001
python -m rttdist.cli resume --config real-smoke.yaml --run-id real-smoke-001
python -m rttdist.cli report --config real-smoke.yaml --run-id real-smoke-001
```

주의 사항:

- OpenAI 사용은 호출 비용이 발생합니다
- `temperature=0` 이어도 mock처럼 완전한 고정 응답을 보장하지는 않습니다
- iteration 수가 늘면 호출 수와 비용도 함께 증가합니다

## 어떤 방식을 언제 쓰면 좋은가

- `mock`: 가장 빠르고 재현 가능. 기본 회귀 테스트용
- `ollama`: API 비용 없이 로컬 모델 품질을 보고 싶을 때
- `openai`: 실제 서비스형 모델 기준 결과를 보고 싶을 때

## 코드 유사도 비교 방식

이 프로젝트는 단순 문자열 diff가 아니라, 다음 축을 함께 기록합니다.

### 1. Round-trip 반복

한 실험 단위는 다음 순서로 진행됩니다.

1. 기준 C++ 해법 선택
2. `C++ -> 대상 언어` 번역
3. `대상 언어 -> C++` round-trip 번역
4. 대상 언어 코드와 round-trip C++ 코드를 모두 샘플 픽스처로 실행
5. 고정점/진동 여부와 유사도 계산
6. 필요하면 다음 iteration 반복

구현 위치:

- `src/rttdist/pipeline.py`
- `src/rttdist/exec/adapters.py`

### 2. 잔차 코드 유사도(residual similarity)

원본 C++와 현재 round-trip C++의 유사도는 `src/rttdist/normalize.py` 와 `src/rttdist/fixed_point.py` 에 구현되어 있습니다.

세부 규칙은 다음과 같습니다.

- `Python`은 표준 라이브러리 `tokenize`로 토큰화합니다
- `C/C++/Java`는 주석 제거 후 정규식 기반 토큰화로 문자열, 식별자, 숫자, 연산자를 추출합니다
- 주석과 의미 없는 공백 차이는 무시합니다
- 정규화된 C++ 토큰을 `\x00`로 이어 붙인 뒤 SHA-256 해시를 만들어 iteration 간 동일성 비교에 사용합니다
- 원본 C++와 round-trip C++의 유사도는 정규화된 C++ 토큰 멀티셋에 대한 Sorensen-Dice 계수로 계산합니다

즉, 이 프로젝트의 residual similarity는 “정규화된 C++ 토큰 멀티셋이 얼마나 겹치는가”를 보는 방식입니다.

핵심 함수:

- `normalize_tokens()`
- `hash_normalized_cpp_tokens()`
- `cpp_token_sorensen_dice_similarity()`
- `compute_residual_similarity()`

### 3. 고정점 판정(fixed point / oscillation)

고정점 판정은 `src/rttdist/fixed_point.py` 에 있습니다.

- `fixed_point`: 마지막 두 round-trip C++의 정규화 해시가 같으면 성립
- `oscillation`: 마지막 네 해시가 `A, B, A, B` 이고 `A != B` 이면 2-cycle 진동으로 판정
- 그 외에는 `continue`

즉, 현재 구현은 “임계값 기반 유사도 수렴”이 아니라 “정규화된 round-trip C++ 토큰 해시의 반복 패턴”을 고정점 기준으로 사용합니다.

### 4. 변경횟수 기반 거리(change-count distance)

간단한 버전의 변경횟수 기반 거리는 이제 구현되어 있습니다.

현재 정의는 다음과 같습니다.

> `C++ -> target -> C++` 왕복 1회를 거리 1로 계산한다.

즉:

- `C++ -> target -> C++` 왕복이 실제로 완료되면 거리 1 증가
- 2회 왕복이 완료된 뒤 fixed point면 거리 2
- 첫 번째 iteration에서 `C++ -> target` 단계에서 바로 실패하면 거리 0

이 값은 리포트에서 `change_count_distance` 로 노출됩니다.

중요한 점은, 이것은 **AST edit count** 나 **문장 단위 편집 횟수**가 아니라, 현재 단계에서는 **왕복 변환 cycle 수**를 거리로 쓰는 단순 지표라는 것입니다.

### 5. AST 구조 거리

구조적 차이는 `src/rttdist/ast_ir.py` 와 `src/rttdist/ast_metrics.py` 에 구현되어 있습니다.

- 파서: `tree-sitter` (`c`, `cpp`, `java`, `python`)
- 공통 IR: `function_def`, `for_loop`, `while_loop`, `if_stmt`, `return_stmt`, `call_expr`, `subscript_expr`, `block` 같은 공통 노드군으로 정규화
- 거리 계산: `apted` Tree Edit Distance

현재 리포트는 다음 두 거리를 기록합니다.

- 대상 언어 AST vs 기준 C++ AST
- 대상 언어 AST vs round-trip C++ AST

중요한 점은 raw parser node label을 그대로 비교하지 않고, 언어 독립적인 IR로 바꾼 뒤 비교한다는 것입니다.

### 6. 복잡도/어휘 메트릭

복잡도 메트릭은 `src/rttdist/metrics.py` 에 구현되어 있습니다.

추출기:

- `lizard`

현재 v1 메트릭 세트:

- `loc`
- `token_count`
- `cyclomatic_complexity`
- `function_count`
- `max_nesting_depth`

리포트에는 현재 코드의 절대값과 함께 다음 delta가 들어갑니다.

- `delta_vs_seed_cpp`
- `delta_vs_previous`

즉, “원본 C++ 대비 얼마나 길어졌는가/단순해졌는가”, “직전 iteration 대비 얼마나 변했는가”를 같이 봅니다.

### 7. 의미 보존 여부

유사도만 보는 것이 아니라, 매 iteration에서 생성된 코드가 실제 샘플 입출력을 통과하는지도 확인합니다.

- 대상 언어 코드 실행
- round-trip C++ 코드 실행
- 각 문제의 모든 `.inp` / `.out` 샘플 쌍 검사

이 결과는 `semantic_summary` 로 리포트에 들어갑니다.

## 현재 스모크 테스트 자료

현재 스모크 테스트는 아래 자료를 사용합니다.

- 기준 문제 설명: `problem/IPOP_1436.md`, `problem/IPOP_2579.md`
- 기준 C++ 해법: `corpus/solutions/IPOP_1436/reference.cpp`, `corpus/solutions/IPOP_2579/reference.cpp`
- 샘플 픽스처: 각 문제당 10쌍
- mock 번역 응답: `tests/fixtures/e2e/smoke_openai_responses.json`
- e2e 테스트: `tests/e2e/test_smoke_experiment.py`

검증된 흐름:

- `validate-corpus`
- `run`
- `resume`
- `report`
- `pytest tests/e2e -q`

증거 파일:

- `.sisyphus/evidence/task-13-smoke.txt`
- `.sisyphus/evidence/task-13-smoke-error.txt`

## 현재 스모크 결과 요약

현재 저장된 결과는 `artifacts/smoke/summary.json`, `artifacts/smoke/summary.md` 에 있습니다.

### 전체 요약

- 실행 조합: 2문제 x 3언어 = 6개
- 모든 조합 `success`
- 모든 조합 `fixed_point`
- 모든 조합 iteration 수 `2`
- 모든 조합 residual similarity `1.0`
- 모든 조합 target / roundtrip C++ 샘플 10/10 통과

### 조합별 결과

| Problem | Language | Status | Iterations | Residual | AST dist to seed | Target semantic |
| --- | --- | --- | ---: | ---: | ---: | --- |
| IPOP_1436 | c | success | 2 | 1.000000 | 19 | pass (10/10) |
| IPOP_1436 | java | success | 2 | 1.000000 | 19 | pass (10/10) |
| IPOP_1436 | python | success | 2 | 1.000000 | 29 | pass (10/10) |
| IPOP_2579 | c | success | 2 | 1.000000 | 33 | pass (10/10) |
| IPOP_2579 | java | success | 2 | 1.000000 | 24 | pass (10/10) |
| IPOP_2579 | python | success | 2 | 1.000000 | 48 | pass (10/10) |

### 해석 포인트

- 스모크에서는 mock 응답이 안정적으로 설계되어 있어 모든 조합이 2회 만에 고정점에 도달했습니다
- residual similarity가 모두 `1.0` 이므로, 최종 round-trip C++는 정규화 토큰 기준으로 원본 C++와 동일했습니다
- 하지만 AST distance와 complexity delta는 언어별 차이를 여전히 보여줍니다
  - `Java`는 대체로 token 수가 늘어나는 경향이 있습니다
  - `Python`은 `loc`와 `token_count`는 줄지만, 문제에 따라 `max_nesting_depth`가 오를 수 있습니다
  - `C`는 원본 C++와 가까운 편이지만, `cyclomatic_complexity`가 증가하는 경우가 있습니다

예를 들어:

- `IPOP_1436 / java`: `token_count +35`, `loc -1`, AST distance `19`
- `IPOP_1436 / python`: `loc -4`, `token_count -14`, `max_nesting_depth +1`, AST distance `29`
- `IPOP_2579 / python`: `loc -9`, `token_count -24`, `max_nesting_depth +4`, AST distance `48`

즉, 현재 스모크 결과는 “최종 round-trip C++는 매우 안정적이지만, 중간 표현(target language)의 구조와 복잡도는 언어별로 다르게 변형된다”는 점을 보여줍니다.

## 주요 산출물 위치

- 전체 스모크 요약 JSON: `artifacts/smoke/summary.json`
- 전체 스모크 요약 Markdown: `artifacts/smoke/summary.md`
- 개별 실행 manifest: `artifacts/smoke/<problem>/<language>/run.json`
- iteration 아티팩트: `artifacts/smoke/<problem>/<language>/iterations/iter-XXX/`

예를 들어 `IPOP_1436 / python`의 최종 manifest는 다음 위치에 있습니다.

- `artifacts/smoke/IPOP_1436/python/run.json`

## 테스트 실행

전체 테스트:

```bash
python -m pytest -q
```

스모크 e2e만 실행:

```bash
export RTTDIST_OPENAI_MOCK_RESPONSES=tests/fixtures/e2e/smoke_openai_responses.json
python -m pytest tests/e2e -q
```
