# RTT Language Distance Experiment Tool

C++ 기준 해법을 여러 언어 경로로 번역한 뒤 다시 C++로 닫는 **RTT(Round-Trip Translation) 실험 도구**입니다.
현재 코드는 의도적으로 단순화되어 있으며, 실험 실행 경로는 **LM Studio + RTT route**만 지원합니다.

예를 들어 설정이 아래와 같다면:

```yaml
seed_language: cpp
target_languages: [c, java, python]
```

한 사이클은 다음처럼 닫힙니다.

```text
cpp -> c -> java -> python -> cpp'
```

이 경우:

- `RTT cycle count`: 1
- `translation_count_per_cycle`: 4
- `completed_translation_count`: 실제 완료된 변환 단계 수

즉, **A-B-C-D-A'는 4번 번역해서 RTT 1사이클을 완료한 것**으로 기록됩니다.

---

## 현재 지원 범위

지원하는 것:

- LM Studio OpenAI-compatible local server
- RTT route 실험
- 각 변환 단계의 실행 검증
- RTT 사이클 수, 사이클당 변환횟수, 완료/실패 변환횟수
- 실험 중 콘솔 진행 출력
- iteration별 `conversion.log`, `metrics.json`, `execution.json`, `llm-request.json`, `llm-response.json`
- run별 `summary.json`, `summary.md`

지원하지 않는 것:

- Ollama provider
- pairwise 실험/보고서
- 별도 구조/유사도/복잡도 지표
- 외부 API provider

향후 지표나 provider는 현재 RTT-only 구조 위에 새 모듈로 추가하면 됩니다.

---

## 빠른 시작: mock으로 파이프라인 확인

실제 LM Studio 서버 없이 CLI와 artifact 생성을 확인할 수 있습니다.

### 1) 설치

```bash
uv sync
```

필요한 런타임 도구:

- Python 3.10+
- `uv`
- C/C++ 컴파일러
- Java/Javac
- Python 실행 환경

### 2) mock 응답 활성화

```bash
export RTTDIST_LLM_MOCK_RESPONSES=tests/fixtures/e2e/smoke_llm_responses.json
```

### 3) 검증 및 실행

```bash
uv run -m rttdist.cli validate-corpus --config tests/fixtures/config/minimal.yaml
uv run -m rttdist.cli run --config tests/fixtures/config/minimal.yaml --run-id tutorial-mock
```

실행 중에는 다음과 같은 진행 로그가 콘솔에 출력됩니다.

```text
[RTT] IPOP_1436: RTT route cpp->c->java->python->cpp (4 translations per cycle)
[RTT] IPOP_1436: iteration 1 step 1/4 cpp->c translating
[RTT] IPOP_1436: iteration 1 step 1/4 cpp->c complete
...
```

### 4) 결과 확인

```bash
cat artifacts/tutorial-mock/summary.md
```

주요 산출물:

```text
artifacts/<run-id>/summary.json
artifacts/<run-id>/summary.md
artifacts/<run-id>/<problem>/<route>/run.json
artifacts/<run-id>/<problem>/<route>/iterations/iter-001/metrics.json
artifacts/<run-id>/<problem>/<route>/iterations/iter-001/conversion.log
```

---

## 실제 실험: LM Studio 사용

### 1) LM Studio 준비

1. LM Studio를 실행합니다.
2. 사용할 코드 모델을 다운로드합니다. 예: `qwen2.5-coder:7b` 또는 로컬 환경에 맞는 코드 모델
3. **Local Server**를 시작합니다.
4. 기본 주소가 아래와 같은지 확인합니다.

```text
http://localhost:1234/v1
```

### 2) 설정 파일 확인

기본 예시는 `lmstudio_1.yaml`입니다.

```yaml
provider: lmstudio
problem_ids:
  - IPOP_1436
  - IPOP_2110
  - IPOP_2217
  - IPOP_2579
  - IPOP_2609
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
problem_root: ./problem
corpus_root: ./corpus/solutions
```

`target_languages`는 개별 pair 목록이 아니라 **RTT 경로의 중간 언어 순서**입니다.
위 설정은 `cpp -> c -> java -> python -> cpp'` 한 경로를 실행합니다.

### 3) 실행

mock 환경변수를 꺼야 실제 LM Studio를 사용합니다.

```bash
unset RTTDIST_LLM_MOCK_RESPONSES
uv run -m rttdist.cli validate-corpus --config lmstudio_1.yaml
uv run -m rttdist.cli run --config lmstudio_1.yaml --run-id lmstudio-rtt-demo
```

중단된 동일 run-id를 이어서 보려면:

```bash
uv run -m rttdist.cli resume --config lmstudio_1.yaml --run-id lmstudio-rtt-demo
```

기존 artifact에서 요약만 다시 만들려면:

```bash
uv run -m rttdist.cli report --config lmstudio_1.yaml --run-id lmstudio-rtt-demo
```

---

## 핵심 지표 읽기

`summary.md`와 `summary.json`에서 아래 값을 확인합니다.

| 필드 | 의미 |
| --- | --- |
| `rtt_route_key` | 실행한 전체 RTT 경로. 예: `cpp->c->java->python->cpp` |
| `rtt_distance.value` | 완료된 RTT cycle 수 |
| `translation_count_per_cycle` | RTT 1사이클을 완성하는 데 필요한 번역/변환 횟수 |
| `attempted_translation_count` | 마지막 iteration에서 시도한 변환 횟수 |
| `completed_translation_count` | 마지막 iteration에서 번역 결과 생성까지 완료한 변환 횟수 |
| `failed_translation_count` | 마지막 iteration에서 번역 단계 자체가 실패한 횟수 |
| `convergence_outcome` | `fixed_point`, `oscillation`, `continue`, `terminated_on_failure` 등 |
| `semantic_summary.overall` | 각 단계 실행 검증이 통과했는지 여부 |
| `artifacts.final_conversion_log_path` | 변환 과정 로그 파일 |

예시 해석:

```text
RTT route: cpp->c->java->python->cpp
RTT cycle count: 1
Translations per RTT cycle: 4
Completed translations in final iteration: 4
Semantic summary: pass
```

이는 `cpp -> c -> java -> python -> cpp'` 변환이 4번 모두 완료되어 RTT 1사이클이 끝났다는 뜻입니다.

---

## iteration별 로그

각 iteration에는 사람이 읽을 수 있는 `conversion.log`가 생성됩니다.

예:

```text
problem_id=IPOP_1436
iteration=1
language_route=cpp->c->java->python->cpp
translation_count_per_cycle=4
step 1/4 START cpp->c
step 1/4 TRANSLATED cpp->c chars=1234
step 1/4 COMPLETE cpp->c
...
summary attempted=4 completed=4 failed=0
```

함께 볼 파일:

- `metrics.json`: RTT 지표와 변환횟수 지표
- `execution.json`: 각 변환 산출물의 샘플 입출력 실행 결과
- `llm-request.json`: LM Studio 요청 payload
- `llm-response.json`: LM Studio 응답 payload
- `conversion.log`: 변환 진행 요약 로그

---

## 저장소 구조

```text
corpus/solutions/      기준 해법(reference.cpp 등)
problem/               문제 설명과 샘플 입출력
src/rttdist/           RTT 실험 CLI 및 파이프라인
tests/                 테스트와 mock 실험 fixture
lmstudio_1.yaml        LM Studio 실험 예시 설정
artifacts*/            실행 후 생성되는 실험 산출물
```

---

## 테스트

전체 테스트:

```bash
uv run pytest
```

소스 컴파일 확인:

```bash
uv run python -m compileall -q src
```

mock 기반 e2e만 빠르게 확인:

```bash
export RTTDIST_LLM_MOCK_RESPONSES=tests/fixtures/e2e/smoke_llm_responses.json
uv run pytest tests/e2e -q
```
