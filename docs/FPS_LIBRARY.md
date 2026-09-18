# FPS 라이브러리와 재현

새 실험은 `fps-text-v1` 프로토콜이며 기존 C++ 해시 고정점 실험의 의미를 변경하지 않는다. `src/rttdist/fps_experiment.py`가 설정, 번역 provider, 세 언어 평가기, 상태 계수, 유사도, 체크포인트를 연결한다. 예비·본 단계는 서로 다른 출력 폴더와 계약 파일을 가진다.

분석·Word 생성 의존성은 `uv sync --extra analysis`로 설치한다. 컴파일러와 JPlag의 Java/JAR 경로는 `fps_v1.yaml`에서 지정한다. 이번 Windows 환경에서는 GHC 내부 컴파일러를 실행할 수 있는 권한이 필요하다.

```powershell
.venv/Scripts/rttdist.exe fps --config fps_v1.yaml --phase pilot
.venv/Scripts/rttdist.exe fps --config fps_v1.yaml --phase main
.venv/Scripts/rttdist.exe fps --config fps_v1.yaml --phase main --action resume
.venv/Scripts/rttdist.exe fps --config fps_v1.yaml --phase main --action report
```

`run`과 `resume` 모두 완료된 관측과 응답을 보존한다. 같은 결과를 다시 생성하는 동작은 없다. `report`는 모델 호출 없이 저장된 응답·코드·평가·JPlag 점수로 표, CSV, JSON, 그림, 완료 감사를 다시 만든다. `freeze`는 데이터, 설정, 프롬프트, 실행기 소스 해시가 다른 재개를 차단한다. `implementation/`에는 실행 당시 소스 사본도 보존한다. 상태를 처음부터 재구성하므로 중복 코드와 재개가 FPS 크기를 늘리지 않는다.

## 모델과 provider 교체

새 설정은 `llm` 블록을 사용하며 `lmstudio` 블록을 요구하지 않는다. 기존 `lmstudio` 설정도 호환 입력으로 유지한다. 일반 pipeline은 `translation_factory`를 통해, 과거 v1 실행기의 요청 함수와 새 FPS 실행기는 `providers.create_provider(config)`를 통해 같은 provider 계약을 사용한다. `complete(payload, folder)` 응답은 원본 body, 실제 model, usage, latency_seconds, received_at, 요청 옵션, 실제 적용 옵션의 가용성을 담는다. 공개되지 않은 usage나 적용 옵션은 null이다. 추출·평가는 공통 실행기가 담당하여 공급자에 종속되지 않는다. 과거 v1의 평가·해시 종료 정책과 결과 파일명은 유지하며 새 provider 로그를 별도 하위 폴더에 보존한다.

별도 호환 API 사용 예시는 다음과 같다. 실제 주소와 모델은 사용자가 나중에 제공할 때 확정한다. 현재 실험은 이 예시 endpoint를 호출하지 않았다.

```yaml
llm:
  provider: openai_compatible
  endpoint: https://YOUR-ENDPOINT/v1
  model: YOUR-MODEL
  api_key_env: RTT_API_KEY
  generation:
    temperature: 0
    top_p: 1
    max_tokens: 4096
    seed: 20260918
  request_timeout: 300
  retries: 2
```

model·endpoint·generation 변경은 반드시 새 output_root로 분리한다. 모델이 지원하지 않는 옵션은 명시적으로 제거하고 조건 차이를 새 설계에 기록한다. 현재 호환 adapter가 허용하는 옵션은 temperature, top_p, max_tokens, seed이며 LM Studio에 한해 top_k와 repeat_penalty도 허용한다. 알 수 없는 옵션은 오류다. 허용된 옵션의 실제 모델 지원은 예비 요청으로 확인해야 한다. 서버가 유효 설정을 돌려주지 않으면 요청값을 적용값이라고 주장하지 않는다.

API 키는 환경변수로만 읽고 값과 인증 헤더를 요청·오류 로그에 기록하지 않는다. 401/설정 오류는 즉시 실패하고, 지정된 일시 HTTP/연결 오류에만 재시도한다. 원본 응답 수신 뒤에는 파싱 오류나 프로그램 실패를 이유로 재생성하지 않는다. 비호환 API는 동일한 `complete` 응답 계약을 구현하고 factory에 분기를 추가한다. 실제 외부 endpoint와 두 번째 LLM은 사용자 결정으로 유예했으며, 모의 검사 통과를 실제 연결 완료로 표현하지 않는다.

## 소스와 평가

`fps_execution.evaluate`는 runtime.tools의 언어별 실행 경로를 사용한다. 컴파일·로딩·실행 명령과 stdout/stderr, 제한 시간, 각 입력의 결과를 저장한다. `fps_state`는 LF 변환 이외의 정규화를 하지 않는다. JPlag는 text 입력 사본을 사용하고 실행 소스 자체는 변경하지 않는다. 과거 C++ 전용 native 점수는 이번 text 점수와 합산하지 않는다.

실행기 핵심 검사, provider 모의 검사, 실제 기준 코드 검증은 서로 다른 증거다. 본 캠페인의 실제 기준 코드 검사와 model 호출 결과는 `artifacts-lmstudio/fps-v1/`에 있다. 기존 Scala 전용 회귀 검사는 컴파일러 JAR 부재로 별도 제외되며 이번 세 언어 실험에는 사용하지 않는다. 관련 회귀 검사 192개는 GHC 실행 권한과 프로젝트 내부 임시 폴더를 설정한 환경에서 통과했다(`tests-final.xml`). 추가 경계 검사는 별도로 실행 기록을 남긴다.
