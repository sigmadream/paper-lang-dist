# RTT Language Distance Experiment Tool

> C++ 기준 해법을 여러 언어 경로로 번역한 뒤 다시 C++로 닫는 RTT(Round-Trip Translation) 실험 도구입니다.

```yaml
seed_language: cpp
target_languages: [c, java, python]
```

`target_languages`는 혼합 경로가 아니라 독립 실험 대상 목록입니다. 따라서 위 설정은 아래 3개 RTT 실험을 각각 실행합니다.

```text
cpp -> c -> cpp'
cpp -> java -> cpp'
cpp -> python -> cpp'
```

각 독립 실험에서 한 사이클은 `seed -> target -> seed'`로 닫히며, 이 경우 각 실험의 `translation_count_per_cycle`은 2입니다.

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

- LM Studio 외 다른 로컬 LLM 실행기
- 기존 언어쌍별 실험/보고서
- 별도 구조/유사도/복잡도 지표
- 외부 API 실행 경로
- 대체 응답 fixture를 통한 실험 실행

향후 지표나 실행 경로는 현재 RTT-only 구조 위에 새 모듈로 추가하면 됩니다.

---

## 실제 실험: LM Studio 사용

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

### 2) LM Studio 준비

1. LM Studio를 실행합니다.
2. 사용할 코드 모델을 다운로드합니다. 예: `qwen2.5-coder:7b` 또는 로컬 환경에 맞는 코드 모델
3. Local Server를 시작합니다.
4. 기본 주소가 아래와 같은지 확인합니다.

```text
http://localhost:1234/v1
```

### 3) 설정 파일 확인

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

`target_languages`는 독립 RTT 실험 대상 목록입니다. 위 설정은 한 문제마다 `cpp -> c -> cpp'`, `cpp -> java -> cpp'`, `cpp -> python -> cpp'` 세 실험을 실행합니다.

### 4) 실행

```bash
uv run -m rttdist.cli validate-corpus --config lmstudio_1.yaml
uv run -m rttdist.cli run --config lmstudio_1.yaml --run-id lmstudio-rtt-demo
```

실행 중에는 다음과 같은 진행 로그가 콘솔에 출력됩니다.

```text
[RTT] IPOP_1436: RTT route cpp->c->cpp (2 translations per cycle)
[RTT] IPOP_1436: iteration 1 step 1/2 cpp->c translating
[RTT] IPOP_1436: iteration 1 step 1/2 cpp->c complete
...
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

## 결과 확인

```bash
cat artifacts-lmstudio/lmstudio-rtt-demo/summary.md
```

주요 산출물:

```text
artifacts-lmstudio/<run-id>/summary.json
artifacts-lmstudio/<run-id>/summary.md
artifacts-lmstudio/<run-id>/<problem>/<route>/run.json
artifacts-lmstudio/<run-id>/<problem>/<route>/iterations/iter-001/metrics.json
artifacts-lmstudio/<run-id>/<problem>/<route>/iterations/iter-001/conversion.log
```

---

## 핵심 지표 읽기

`summary.md`와 `summary.json`에서 아래 값을 확인합니다.

| 필드 | 의미 |
| --- | --- |
| `rtt_route_key` | 실행한 독립 RTT 경로. 예: `cpp->python->cpp` |
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
RTT route: cpp->python->cpp
RTT cycle count: 1
Translations per RTT cycle: 2
Completed translations in final iteration: 2
Semantic summary: pass
```

이는 `cpp -> python -> cpp'` 변환이 2번 모두 완료되어 Python 대상 RTT 1사이클이 끝났다는 뜻입니다.

---

## iteration별 로그

각 iteration에는 사람이 읽을 수 있는 `conversion.log`가 생성됩니다.

예:

```text
problem_id=IPOP_1436
iteration=1
language_route=cpp->python->cpp
translation_count_per_cycle=2
step 1/2 START cpp->python
step 1/2 TRANSLATED cpp->python chars=1234
step 1/2 COMPLETE cpp->python
...
summary attempted=2 completed=2 failed=0
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
tests/                 실제 코드 경로 검증 테스트
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
