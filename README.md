# RTT Language Distance Experiment Tool

> C++ 기준 해법을 여러 언어 경로로 번역한 뒤 다시 C++로 닫는 RTT(Round-Trip Translation) 실험 도구입니다.

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

## 실제 실험: LM Studio 사용

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
problem_root: ./problem
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

중단된 동일 run-id를 이어서 보려면:

```bash
uv run -m rttdist.cli resume --config lmstudio_1.yaml --run-id lmstudio-rtt-demo
```

기존 artifact에서 요약만 다시 만들려면:

```bash
uv run -m rttdist.cli report --config lmstudio_1.yaml --run-id lmstudio-rtt-demo
```

## 결과 확인

```bash
cat artifacts-lmstudio/lmstudio-rtt-demo/summary.md
```

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

## 테스트

### 전체 테스트

```bash
uv run pytest
```

### 소스 컴파일 확인

```bash
uv run python -m compileall -q src
```
