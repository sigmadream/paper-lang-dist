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

## 현재 구현 범위와 논문 실험 완료 기준

이 저장소의 현재 구현은 RTT 논문 실험을 위한 **first-pass metric 수집/리포팅 인프라**입니다. 즉,
RTT 실행 경로에서 컴파일 체크, 기능 체크, change-count, residual similarity,
semantic preservation, complexity delta 상태를 안정적인 artifact schema로 남기는 데 초점을 둡니다.

논문 실험이 완료되었다고 보려면 구현 통과와 별도로 아래 실행 산출물이 필요합니다.

1. 논문 대상 문제 전체를 설정합니다: `IPOP_1436`, `IPOP_2110`, `IPOP_2217`, `IPOP_2579`, `IPOP_5567`.
2. 각 문제에 대해 `cpp -> c -> cpp'`, `cpp -> java -> cpp'`, `cpp -> python -> cpp'` 경로를 실행합니다.
3. 새 run-id로 전체 실행 후 `summary.json`/`summary.md`를 재생성합니다.
4. 최소 `5 problems × 3 target languages = 15`개 result가 생성되었는지 확인합니다.
5. 각 result에 `distance_metrics.schema_version == 1`과 하위 지표가 존재하는지 확인합니다.

기존 `artifacts-lmstudio/lmstudio-rtt-demo`는 과거 데모 실행 산출물일 수 있으므로,
논문 표나 분석에 사용하려면 현재 코드로 새 run을 생성한 뒤 검증해야 합니다.

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
| `translation_steps[].compile_check` | 각 변환 단계의 컴파일/문법 체크 결과(`passed`, `failed`, `skipped`, `not_evaluated`) |
| `translation_steps[].functionality_check` | 각 변환 단계의 기능/fixture 체크 결과(`passed`, `failed`, `not_run`, `not_evaluated`) |
| `evaluation_checks` | 마지막 iteration의 단계별 컴파일/기능 체크 집계 |
| `distance_metrics` | 논문 지표용 묶음(`schema_version == 1`): change-count, residual similarity, semantic preservation, complexity delta |
| `distance_metrics.change_count` | `rtt_distance`에서 투영한 change-count 거리. 경로 미완료 시 `available=false`, `reason=no_completed_route` |
| `distance_metrics.residual_similarity` | 원본 C++와 최종 왕복 C++의 정규화 토큰 멀티셋 Sørensen-Dice 유사도 |
| `distance_metrics.semantic_preservation` | `evaluation_checks`에서 투영한 논문용 의미 보존 상태(`pass`, `degraded`, `fail`, `not_evaluated`) |
| `distance_metrics.complexity_delta` | 선택적 복잡도 지표 표면. 기본 실행에서는 lizard 등 필수 의존성을 추가하지 않고 하위 지표별 `unavailable`을 기록 |
| `convergence_outcome` | `fixed_point`, `oscillation`, `continue`, `terminated_on_failure` 등 |
| `semantic_summary.overall` | 기존/raw 실행 검증 요약. 논문용 의미 보존 판단은 `distance_metrics.semantic_preservation.status`를 우선 사용 |
| `artifacts.final_conversion_log_path` | 변환 과정 로그 파일 |

각 변환 단계는 번역 결과 생성 직후 컴파일/문법 체크와 기능/fixture 체크를 기록합니다.
중간 단계에서 컴파일은 통과했지만 기능 체크가 실패한 경우에는 실패 상태를
`completed_with_functionality_failure`로 남기고 다음 변환을 계속 진행합니다. 따라서
후속 단계와 최종 `seed'`가 성공하면 고정점 판정(`fixed_point`)은 완료된 전체 경로를
기준으로 반영됩니다. 컴파일 실패나 최종 `seed'` 단계의 기능 실패는 기존처럼 해당
iteration을 실패로 종료합니다.

첫 번째 논문 지표 구현에서는 AST 편집 거리와 MOSS 유사도는 범위에서 제외합니다.
해당 섹션은 산출물에 생성하지 않으며, 향후 별도 어댑터를 도입할 때 명시적으로
스키마를 확장합니다. 복잡도 델타도 선택적 어댑터 표면만 제공하므로 기본 환경에서는
`loc`, `token_count`, `cyclomatic`, `function_count`, `max_nesting` 각각이
`optional_tool_not_configured_or_not_installed` 사유로 unavailable일 수 있습니다.

## 테스트

### 전체 테스트

```bash
uv run pytest
```

### 소스 컴파일 확인

```bash
uv run python -m compileall -q src
```
