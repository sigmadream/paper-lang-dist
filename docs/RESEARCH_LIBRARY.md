# 연구용 RTT 라이브러리

`rttdist research`는 실행 프로파일, 지표, 모델 목록을 조합하는 공통 실행 경로다.
기존 `run`, `resume`, `report`, `fps` 명령과 과거 기록 형식은 유지한다.
새 연구에는 `research`를 사용한다. 과거 기록의 숫자나 지표 정의를 자동 변경하지 않는다.

## 시작하기

```powershell
uv sync --extra analysis
uv run rttdist research profiles
uv run rttdist research validate --config examples/research/local.yaml
uv run rttdist research run --config examples/research/local.yaml
uv run rttdist research status --experiment artifacts/research/local-demo
uv run rttdist research resume --config examples/research/local.yaml
uv run rttdist research analyze --experiment artifacts/research/local-demo --analysis-id baseline
uv run rttdist research analyze --experiment artifacts/research/local-demo --profile examples/research/analysis.yaml --analysis-id extended
uv run rttdist research replay --experiment artifacts/research/local-demo --replay-id verification
```

`local.yaml`의 모델 ID를 LM Studio에 로드한 실제 모델 ID로 바꾼다.
기본 제공자는 `lmstudio`, 기본 주소는 `http://localhost:1234/v1`이다.
C++ 예제는 PATH의 `g++`를 사용한다. `runtime.tools.cpp`에 실행 파일 경로를 지정할 수도 있다.
예제의 토큰 유사도는 사용 방법을 확인하기 위한 것으로 논문의 JPlag 지표와 다르다.
`validate`는 모델 호출 없이 설정·코퍼스 분리·실행 지표 도구 설정을 검사한다.
`run`은 실행 조건과 입력을 고정하고 기준 프로그램을 검증한 다음 모델을 호출한다.

## 프로파일과 지표

| 프로파일 | 실행 판정 | 주요 집계 |
|---|---|---|
| `paper-abstract-v1` | 인접 복원 코드의 JPlag 유사도 0.85 이상 | 성공률, 성공 시 평균 홉 수, 평균 홉 수 / 성공률 |
| `strict-fixed-point-v1` | C++ 정규화 토큰 해시 일치 후 확인 왕복 | 성공률, 최초 고정점 후보의 홉 수 |
| `fps-v2` | 고유 상태 수 제한과 복수 유사도 임계치 | 문제별 성공률 평균, 성공 시 상태 수, 실패 페널티를 포함한 상태 거리 |

프로파일 이름, YAML 경로 또는 인라인 매핑을 선택한다. `extends`는 등록된 프로파일 하나를 상속한다.
매핑은 재귀 병합하고 목록은 전체 교체한다. 상대 도구 경로는 프로파일이 작성된 YAML 파일을 기준으로 해석한다.

```yaml
profile:
  extends: paper-abstract-v1
  id: my-jplag-study
  version: 1
  execution:
    max_steps: 20
    threshold: 0.85
    metrics:
      - id: adjacent
        metric: jplag
        reference: previous
        options:
          java: java
          jar: ../../jplag-6.3.0-jar-with-dependencies.jar
          language: cpp
          minimum_tokens: 9
  analysis:
    metrics:
      - id: origin_tokens
        metric: token_dice
        reference: origin
    weighting: pooled
    bootstrap_samples: 2000
    seed: 42
```

`execution.metrics`는 실행 중 계산하며 판정 정책에서 사용할 수 있다.
`analysis.metrics`는 보존된 이력으로 나중에 계산한다. 새 분석은 원본 실행 결과를 바꾸지 않는다.
임계치·중단 조건 등 실행 정의가 바뀌면 새 실험이 필요하다. 저장되지 않은 후속 왕복은 오프라인 계산으로 복원할 수 없다.
기본 프로파일은 논문에 누락된 최대 왕복 횟수나 생성 조건을 추정해 재현을 보장하지 않는다.
실제 연구의 조건을 명시해야 한다. `max_steps`는 확인 단계까지 포함한 편도 번역 한도다.

FPS의 `analysis.outcome_threshold`로 실행 중 수집한 다른 임계치의 결과를 집계할 수 있다.
수집하지 않은 임계치는 거부한다. 실행 지표와 분석 지표의 도구 옵션은 각 지표에 명시한다.

각 측정은 이름, 버전, 단위, 언어, 비교 기준, 입력 해시, 옵션, 상태와 사유를 저장한다.
상태는 `measured`, `unavailable`, `not_applicable`, `error`이며 결측을 0으로 대체하지 않는다.
`scope: roundtrip`은 기준 언어로 돌아온 단계에서 계산한다. `reference: previous`는 직전 복원 코드,
`origin`은 최초 코드다. `scope: step`의 `previous`는 해당 편도 번역의 입력 코드다.

기본 지표는 `jplag`, `token_dice`, `token_sequence`, `ast_similarity`, `source_identity`,
`source_bytes_delta`, `llm_latency`, `prompt_tokens`, `completion_tokens`다.
토큰·AST 지표는 C++에 적용한다. AST는 시간·메모리 제한을 사용한다.
JPlag의 `language: text`는 다른 기준 언어에도 사용할 수 있으며 FPS 프로파일의 기본 모드다.
선택하지 않은 지표는 실행하지 않는다.

## 여러 모델과 API

```yaml
models:
  local:
    model: my-local-model
    generation: {temperature: 0.6, top_p: 0.95, max_tokens: 16384}
  remote:
    provider: openai_compatible
    endpoint: https://your-provider.example/v1
    model: your-model-id
    api_key_env: RTT_API_KEY
    generation: {temperature: 0.6, max_tokens: 16384}
    request_timeout: 300
    retries: 2
    min_interval_seconds: 1
    accepted_models: [your-model-id, your-pinned-model-version]
    pricing: {input_per_million: 1.0, output_per_million: 4.0}
    cost_cap_usd: 10
parallel_models: 1
```

주소·모델·가격은 예시다. API 키는 환경변수로 전달하고 YAML에 키 자체를 넣지 않는다.
완전한 설정 예제는 [multi-model.yaml](../examples/research/multi-model.yaml)에 있다.
호환 API의 주소는 `/chat/completions`가 붙기 전의 base URL이다.
다른 API 요청 형식은 제공자 어댑터로 연결한다. 지원되지 않는 생성 파라미터는 기본 어댑터가 거부한다.
요청 설정과 서버가 알려준 적용 정보를 구분하며 적용 여부가 확인되지 않는 값은 미확인으로 남긴다.
`accepted_models`는 응답 모델 ID의 명시적 허용 목록이며 부분 문자열로 모델을 추정하지 않는다.

실험 단위는 `모델 별칭 × 문제 × 언어 경로 × 반복 번호`다. 왕복 전체에 같은 모델을 사용하며 모델별 통계를 분리한다.
`parallel_models`로 동시 모델 수를 정하고 각 모델 내부는 순차 실행한다. 기본값은 1이다.
설정한 `seed`는 반복 번호에 따라 0부터 오프셋을 적용한다. 미지원 모델의 결정성은 보장하지 않는다.
가격·사용량이 없으면 비용은 미확인이다. 비용 한도는 누적 금액이 한도에 도달한 이후의 새 호출을 막는다.
진행 중인 호출로 한도를 초과할 수 있으므로 엄격한 청구 상한은 아니다. 복구 시 논리적 호출별 중복 비용 계산을 방지한다.

## 기록·재개·분석

```text
<output_root>/<experiment_id>/
  contract.json              # 설정, 코퍼스/구현 해시, 도구와 환경
  schedule.json              # 고정 실행 순서
  corpus/                    # 입력 스냅샷
  reference_checks/          # 기준 프로그램 검증
  models/<alias>/            # 진행 상태와 비용 장부
  trials/<model>/<problem>/<route>/<repeat>/
    trial.json
    attempt-001/
      step-0001/
        request.json
        response.json        # 응답과 체크포인트 계약
        provider/            # 원문 응답과 API 오류 이력
        extraction.json
        source.<extension>
        execution.json
        execution/           # 컴파일·테스트별 stdout/stderr
        measurements/
        step.json
        sealed.json          # 완료 파일 해시
        events.jsonl
      progress.json
      result.json            # 평가 가능한 종료 결과
      sealed.json
  analyses/<analysis_id>/    # 지표와 JSON/CSV 집계
  replays/<replay_id>/        # 응답 재추출·재실행
```

요청·응답·실행·측정을 개별 체크포인트로 저장한다. 완료 파일의 해시를 검증하고 재사용한다.
같은 프롬프트라도 다른 반복 시도의 응답을 재사용하지 않는다. 임시 파일을 거쳐 완료 파일을 교체한다.
OS 파일 잠금으로 같은 실험의 동시 쓰기를 차단하며 프로세스가 종료되면 잠금은 해제된다.

기능 실패는 결과로 보존하며 자동 재생성하지 않는다. 인프라 중단은 별도로 기록하고 도달률의 분모에서 제외한다.
`resume`은 같은 attempt를 이어간다. `resume --new-attempt`는 평가 가능한 결과가 없는 시도에만 새 attempt를 만든다.
기존 자료는 보존하고 첫 평가 가능 결과를 최종 선택한다.
응답이 저장되어 있으면 모델을 다시 호출하지 않는다. 서버 처리 후 응답 저장 전 연결이 끊기면 서버 생성 여부는 알 수 없다.
재시도와 인프라 중단을 기록하되 외부 API의 exactly-once 실행은 보장하지 않는다.

`analyze`는 원본을 변경하지 않고 새 지표와 집계를 생성한다.
`replay`는 원본 응답을 다시 추출하고 컴파일·테스트·측정을 수행하여 기존 판정과 비교한다.
둘 다 모델을 호출하지 않는다. replay의 기록이 부족하면 `saved_history_exhausted`로 남긴다.
같은 분석·재생 ID는 같은 입력과 조건에서 재사용하고 다른 조건은 새 ID에 저장한다.

평균 홉 수와 고유 상태 수는 `mean_hops`, `mean_unique_state_count`로 구분한다.
성공이 없으면 평균 홉 수와 보정 거리는 null이다. `pooled`는 시도를 합산하고 `problem`은 문제별 성공률을 동일 가중치로 평균한다.
평균 홉 수는 성공 시도 전체를 대상으로 한다. 문제 단위 군집 부트스트랩의 유효 재표집 수와 퇴화 여부도 기록한다.
기능 테스트 통과는 제공한 테스트에 대한 보존 관측이다.

## 확장 API

```python
from rttdist.research import Metric, register_metric

def line_delta(context, options):
    return {"status": "measured",
            "value": len(context.candidate.splitlines()) - len(context.reference.splitlines())}

register_metric(Metric("line_delta", "1", "lines", line_delta))
```

프로파일에 `metric: line_delta`를 지정한다. 중복 이름 등록과 버전 불일치는 거부한다.
다른 확장점은 `DecisionPolicy`/`register_policy`, `Aggregator`/`register_aggregator`,
`register_profile`, `register_provider`다. 판정 정책은 이력에 대한 순수 함수다.
Python에서 등록 후 실행하거나 명시적으로 선택한 로컬 모듈을 CLI로 로드한다.

```powershell
uv run rttdist research --extension my_research_extensions run --config study.yaml
uv run rttdist research --extension my_research_extensions analyze --experiment artifacts/study
```

제공자 팩토리는 `(config, ledger=None)`를 받고 `complete(payload, folder)`가 있는 객체를 반환한다.
응답 계약은 `body.choices[0].message.content`, `actual_model`, `usage`, `latency_seconds`다.
usage는 `prompt_tokens`, `completion_tokens`로 정규화하며 미제공 값은 null이다.
다른 API의 응답은 어댑터에서 변환하고 코드 추출·기능 검증은 공통 엔진에 맡긴다.
어댑터는 folder별 원문 응답을 보존·재사용하고 인증 정보는 기록하지 않아야 한다.
확장 소스 파일 해시와 지표·정책·집계 버전을 기록한다.

## 검증과 호환성

기존 단일 모델 설정도 계속 동작하며 temperature는 유한한 비음수 값으로 확장했다.
과거 실험을 새 프로파일로 옮길 때는 프롬프트, 번역 한도, 확인 왕복, 유효 시도 정의까지 맞춰야 한다.
과거 데이터는 기존 report 명령으로 읽으며 원본을 자동 변환하지 않는다.

```powershell
uv run --extra analysis python -m pytest -q
```

새 테스트는 모델·반복 격리, 응답 저장 후 복구, 실패 보존, 확장 지표·제공자,
변조 탐지, 오프라인 분석·재생과 지표 정의를 검증한다. 일부 통합 테스트는 설치된 언어 실행 도구를 사용한다.
