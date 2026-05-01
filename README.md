# RTT Language Distance Experiment Tool

> C++ 기준 해법을 다른 언어로 왕복 번역(`C++ -> target -> C++`)하면서, 언어 간 거리와 의미 보존 정도를 실험하는 도구입니다.

이 저장소는 발표 자료(`presentation/slides.md`)의 아이디어를 직접 실험해 볼 수 있게 만든 CLI 프로젝트입니다.
초급자라면 먼저 **mock 실습**으로 전체 흐름을 익히고, 그다음 **LM Studio** 실험으로 넘어가면 됩니다.

## 이 프로젝트에서 보는 것

한 번의 실험은 아래 순서로 진행됩니다.

1. 기준 해법(`seed_language`)을 고릅니다.
2. 다른 언어로 번역합니다.
3. 다시 기준 언어로 왕복 번역합니다.
4. 샘플 입출력으로 실행해 의미가 유지되는지 확인합니다.
5. 코드가 더 이상 크게 바뀌지 않으면 `fixed_point`, 번갈아 바뀌면 `oscillation`으로 기록합니다.

README에서 꼭 알아둘 지표는 3개만 보면 됩니다.

- `Iterations`: 고정점/종료 상태에 도달할 때까지 걸린 왕복 횟수
- `Semantic`: 샘플 입출력을 통과했는지 여부
- `Residual similarity`: 최종 round-trip C++가 원본 C++와 얼마나 비슷한지

즉, **빨리 수렴하는지**, **의미가 유지되는지**, **최종 코드가 얼마나 닮았는지**를 함께 보는 실험입니다.

---

## 가장 빠른 실습: mock으로 전체 흐름 익히기

외부 API나 로컬 모델 없이 바로 실행해 볼 수 있는 가장 쉬운 방법입니다.

### 1) 준비

필수 도구:

- Python 3.10+
- `uv`
- `gcc`, `g++`, `java`, `javac`

설치:

```bash
uv sync
```

### 2) mock 응답 활성화

```bash
export RTTDIST_LLM_MOCK_RESPONSES=tests/fixtures/e2e/smoke_llm_responses.json
```

### 3) 코퍼스 검증 → 실험 실행

```bash
uv run -m rttdist.cli validate-corpus --config tests/fixtures/config/minimal.yaml
uv run -m rttdist.cli run --config tests/fixtures/config/minimal.yaml --run-id tutorial-mock
```

### 4) 결과 확인

`run` 명령만 실행해도 `summary.json`, `summary.md`가 함께 생성됩니다. 기존 산출물로 다시 요약만 만들고 싶을 때만 `report`를 쓰면 됩니다.

아래 파일을 보면 됩니다.

- `artifacts/tutorial-mock/summary.json`
- `artifacts/tutorial-mock/summary.md`

`summary.md`를 열면 문제별로 다음을 바로 확인할 수 있습니다.

- 어떤 언어 쌍이 성공했는지
- 몇 번 만에 수렴했는지
- 의미 보존이 되었는지

> mock 실습은 README 흐름을 익히는 용도입니다. 실제 모델 성능 비교는 아래 LM Studio 실험을 사용하세요.

---

## 실제 실험: LM Studio로 실행

로컬 LLM 서버인 [LM Studio](https://lmstudio.ai/)를 사용하여 비용 없이 실험할 수 있습니다.

### 1) LM Studio 준비

1. LM Studio를 실행하고 원하는 모델(예: `qwen2.5-coder:7b`)을 다운로드합니다.
2. **Local Server** 탭에서 서버를 시작합니다. (기본 포트: 1234)
3. 서버 설정에서 `CORS`를 허용하거나 기본 설정을 유지합니다.

### 2) 실행

mock을 꺼야 합니다.

```bash
unset RTTDIST_LLM_MOCK_RESPONSES
uv run -m rttdist.cli validate-corpus --config lmstudio_5.yaml
uv run -m rttdist.cli run --config lmstudio_5.yaml --run-id lmstudio-demo
```

### 3) 결과 위치

- `artifacts-lmstudio/lmstudio-demo/summary.json`
- `artifacts-lmstudio/lmstudio-demo/summary.md`

---

## 어떤 설정 파일을 쓰면 되나요?

| 파일 | 추천 상황 |
| --- | --- |
| `tests/fixtures/config/minimal.yaml` | 가장 쉬운 첫 실습(mock) |
| `lmstudio_5.yaml` | 5개 문제를 LM Studio로 실험 |

처음에는 **`minimal.yaml` → `lmstudio_5.yaml`** 순서로 가는 것을 추천합니다.

---

## 결과를 어떻게 읽으면 되나요?

`summary.md`의 핵심 컬럼만 보면 충분합니다.

- `Final status`: 성공인지, compile/runtime error인지
- `Iterations`: 왕복 몇 번 후 종료되었는지
- `Convergence`: `fixed_point`, `oscillation`, `terminated_on_failure` 중 무엇인지
- `Residual similarity`: 최종 C++가 원본 C++와 얼마나 비슷한지
- `Semantic`: 샘플 테스트 통과 여부

초급자 기준 해석법은 아래처럼 보면 됩니다.

- `success + fixed_point` → 안정적으로 수렴한 실험
- `Iterations`가 작음 → 두 언어가 상대적으로 가깝다고 해석 가능
- `Semantic = fail` → 코드가 비슷해 보여도 의미 보존은 실패

---

## 초급자용 활용법 2가지

### 1) 언어별 차이 보기
같은 문제를 `c`, `java`, `python`으로 돌려서 어떤 언어가 더 빨리 수렴하는지 비교합니다.

### 2) 중간 산출물 직접 보기
각 실험 폴더 안의 iteration 파일을 열면 왕복 번역 과정에서 코드가 어떻게 변하는지 볼 수 있습니다.

예:

- `artifacts-lmstudio/<run-id>/<problem>/<pair>/iterations/iter-001/translated.<ext>`
- `artifacts-lmstudio/<run-id>/<problem>/<pair>/iterations/iter-001/roundtrip.cpp`

---

## 저장소 구조

```text
presentation/   발표 자료
problem/        문제 설명 + 샘플 입출력
corpus/solutions/  기준 해법(reference.cpp 등)
src/rttdist/    실험 CLI 및 파이프라인 구현
tests/          테스트와 mock 실습용 설정
results/        저장해 둔 예시 결과 요약
```

---

## 자주 헷갈리는 점

### `run-id`는 왜 중요하나요?
같은 `run-id`를 다시 쓰면 기존 산출물을 이어서 보게 됩니다. 새 실험은 새 `run-id`를 쓰는 것이 안전합니다.


### 왜 mock 실습부터 하라고 하나요?
로컬 모델을 돌리기 전에 전체 흐름이 정상인지 가장 빠르게 확인할 수 있는 방법이기 때문입니다.

---

## 테스트

테스트까지 실행하려면 먼저 dev 의존성을 설치하세요.

```bash
uv sync --extra dev
```

전체 테스트:

```bash
uv run -m pytest -q
```

mock 기반 e2e만 빠르게 확인:

```bash
export RTTDIST_LLM_MOCK_RESPONSES=tests/fixtures/e2e/smoke_llm_responses.json
uv run -m pytest tests/e2e -q
```
