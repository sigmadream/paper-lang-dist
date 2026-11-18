# HTTP 생성 상태 불명 처리 수정 보고

실제 524 이후 재전송이 허용된 원인을 공용 공급자 코드에서 확인하고 모의 실패 회귀부터 실행하였습니다. 실제 API·사전 점검·새 캠페인은 실행하지 않았으며, 보존된 실제 실험 원자료·과거 원장·기존 실행 계약은 수정하거나 승격하지 않았습니다.

## 정책과 공식 근거

생성 요청은 비멱등 POST이며, HTTP 오류 응답만으로 생성이나 과금이 없었다고 단정하지 않습니다. 비멱등 요청은 최초 요청이 적용되지 않았다는 근거 또는 멱등성 근거 없이 자동 재전송하지 않는 원칙에 맞췄습니다. [RFC 9110 9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)

| 오류·상황 | 확인한 의미와 적용 정책 | 근거 |
| --- | --- | --- |
| 524 | 원서버 연결 후 응답 대기 또는 쓰기가 제한을 넘길 수 있으므로 최초 전송 뒤 unknown 처리하고 재전송하지 않습니다. | [Cloudflare 524](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-5xx-errors/error-524/) |
| 504·502 | 상위 서버의 응답 지연·비정상 응답이므로 생성 미실행의 근거로 사용하지 않습니다. | [RFC 9110 15.6](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.6) |
| 500·503와 기타 5xx | 코드·Retry-After만으로 비멱등 요청의 미실행을 입증하지 못하므로, 500~599 전체를 보수적으로 unknown 처리합니다. | [RFC 9110 15.6](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.6) |
| Cloudflare 520 | 원서버가 빈 응답·알 수 없는 응답·예상 밖 응답을 반환한 경우이며, 생성 전 실패라는 기존 가정을 제거하였습니다. | [Cloudflare 520](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-5xx-errors/error-520/) |
| Cloudflare 522 | 원서버 접촉 중 발생한 시간 초과로 연결 전·후 경우가 나뉩니다. HTTP 코드만으로 생성 미실행을 확정하지 않습니다. | [Cloudflare 522](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-5xx-errors/error-522/) |
| Cloudflare 521·523 | 문서는 해당 원서버 연결 거부·연락 불가를 설명합니다. 다단계 제공자 경로 전체의 생성 미실행을 이 클라이언트가 입증한 것은 아니므로, 자동 재시도 예외를 두지 않는 보수적 판단입니다. | [Cloudflare 521](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-5xx-errors/error-521/), [Cloudflare 523](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-5xx-errors/error-523/) |
| 408 | 요청 수신 시간 초과입니다. 생성 POST와 중간 게이트웨이의 처리 여부를 확정하지 못하므로 unknown으로 보존합니다. | [RFC 9110 15.5.9](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.9) |
| 429 | 요청 제한 거부는 사용자·설계에서 허용한 제한 재시도 범위를 유지합니다. v1.6은 Retry-After와 최대 두 번 재시도를 적용합니다. | [RFC 6585 4](https://www.rfc-editor.org/rfc/rfc6585.html#section-4) |
| DNS 실패·연결 거부 | socket.gaierror·ConnectionRefusedError로 확인되는 전송 전 실패만 제한 재시도합니다. 일반 시간 초과·연결 재설정 등은 unknown입니다. | [Python socket](https://docs.python.org/3/library/socket.html#socket.gaierror), [Python 연결 거부 예외](https://docs.python.org/3/library/exceptions.html#ConnectionRefusedError) |

위 표의 보수적 unknown 분류는 모델 생성·과금 여부가 확인되지 않았다는 구현 정책이며, 모든 해당 HTTP 응답에서 실제 생성이 있었다는 주장이 아닙니다. 그 밖의 기존 요청 거부 오류는 자동 재시도하지 않는 처리를 유지하였습니다.

## 수정 파일과 동작

- `src/rttdist/providers.py`: HTTP 자동 재시도 목록을 429로 제한하고, 408·모든 5xx의 전송 상태와 요청 원장 상태를 unknown으로 보존
- `src/rttdist/hops_experiment.py`: UnknownRequestState를 타입으로 구분하여 request_outcome_unknown 중단 사유로 기록
- `tests/integration/test_http_unknown_recovery.py`: HTTP별 불명 상태·예약·재개·프로세스 복구·응답 비용 재생·원문 비노출·실행기 연결 회귀
- `tests/integration/test_provider_recovery.py`: 제한 재시도 예산 검사를 명시적 거부인 429로 변경
- `tests/unit/test_fps_providers.py`: 503·520 재시도를 기대하던 과거 검사를 새 안전 정책에 맞추고 기존 정상 응답·비용 호환성 검사 유지
- `tests/test_experiment_v1.py`: 공용 제공자를 이용하는 과거 v1 요청 연결 검사의 재시도 입력을 503에서 429로 변경하고 요청 내용·시도 기록·완료 응답 재생 검증 유지

v1.6에서는 retries=2여도 최초 불명 HTTP 응답 뒤 전송 시도는 한 번입니다. 원장에는 unknown과 HTTP 상태만 남으며, 기존 예약 금액과 cost_usd=null을 유지합니다. 같은 논리 요청을 새 객체·다른 폴더·별도 프로세스에서 재개해도 전송하지 않습니다. 이미 완료된 다른 요청의 원문·정규화 응답·비용·완료 원장 바이트는 그대로 재생합니다.

이전 프로토콜의 공용 CompatibleProvider도 불명 HTTP·통신 오류를 unknown_request.json에 저장하고 이후 재전송을 차단하도록 맞췄습니다. 정상 완료 응답과 원문 캐시는 계속 우선 재생합니다.

HTTP 오류 본문·이유 문자열·응답 헤더의 비밀값은 저장하지 않습니다. 고정 가짜 키와 비밀값을 포함한 모의 오류로 예외 메시지·JSON·장부·오류 파일에 값이 남지 않는지 검사하였습니다.

## 실패에서 통과로 전환한 근거

신규 회귀 32개 중 최초 실행은 29개 실패·세 개 통과였습니다. 실패에는 실제 524 형태의 HTTPError를 한 번 받은 뒤 UnknownRequestState로 중단하지 않는 문제, 408·5xx의 잘못된 재시도·상태 분류, 새 프로세스 복구, 정상 완료 비용 재생 연결, 이전 프로토콜의 재생성, 실행기의 일반 provider_error 분류가 포함되었습니다. 기존 429·DNS 실패·연결 거부 재시도 세 사례는 처음부터 통과하였습니다.

수정 후 신규 32개 모두 통과하였습니다. 524·504는 별도의 Python 프로세스를 두 번 실행하여 자동 전송이 차단되고 원장 예약이 유지되는 것을 확인하였습니다. 19개 불명 HTTP 상태에 대해 최초 전송 한 번, 추가 대기·재전송 없음, unknown 원장, 예약 0.1 유지와 후속 예산 초과 차단을 검사하였습니다.

관련 기존 검사 최초 실행에서는 과거에 503·520 재시도를 기대하던 세 검사가 새 정책과 충돌하였습니다. 재시도 횟수와 응답 재생을 확인하는 두 검사는 429로 바꿨으며, 520 검사는 unknown·재전송 차단을 요구하도록 변경하였습니다. 이후 관련 회귀 104개가 통과하였습니다.

최초 전체 검사에서는 493개 통과·한 개 실패였으며, 과거 v1 연결 검사도 503 재시도를 기대하던 경우였습니다. 해당 입력을 429로 변경한 뒤 신규 HTTP 검사와 v1 관련 50개가 통과하였고 전체 검사를 다시 실행하였습니다. 최초 전체 결과는 별도 로그로 보존하였습니다.

## 명령과 검사 로그

```powershell
uv run --no-sync pytest tests/integration/test_http_unknown_recovery.py -q --tb=short
uv run --no-sync pytest tests/integration/test_http_unknown_recovery.py tests/unit/test_provider_ledger.py tests/integration/test_provider_recovery.py tests/unit/test_fps_providers.py tests/integration/test_provider_factory.py tests/unit/test_provider_protocols.py tests/integration/test_hops_resume.py tests/integration/test_hops_deadlines.py tests/integration/test_hops_clock_abort.py -q --tb=short
uv run --no-sync pytest tests/test_experiment_v1.py tests/integration/test_http_unknown_recovery.py -q --tb=short
uv run --no-sync black --check src/rttdist/providers.py src/rttdist/hops_experiment.py tests/integration/test_http_unknown_recovery.py tests/integration/test_provider_recovery.py tests/unit/test_fps_providers.py tests/test_experiment_v1.py
uv run --no-sync pytest -q --tb=short
```

- 신규 최초 실패: `http-unknown-red.log`
- 신규 수정 후 통과: `http-unknown-green.log`
- 기존 정책 기대값 충돌: `http-unknown-policy-regression-initial.log`
- 관련 104개 통과: `http-unknown-related.log`
- v1 연결·신규 HTTP 50개 통과: `http-unknown-v1-regression.log`
- 최초 전체 검사 한 개 실패: `http-unknown-full-pytest-initial.log`
- 전체 검사: `http-unknown-full-pytest.log`

최종 전체 검사는 `494 passed, 1166 warnings in 187.92s (0:03:07)`이며 종료 코드 0입니다. 경고는 기존 보고 그림 저장의 Matplotlib 사용 중단 예정 경고이며 경고 필터를 추가하지 않았습니다. black 검사는 변경 Python 파일 여섯 개에서 통과하였습니다.

## 다음 실행과 남은 관문

공급자·core 구현 변경으로 실행 계약의 구현 해시가 바뀝니다. 기존 GLM 자료와 중단한 DeepSeek 자료는 원계약과 함께 보존하며, 새 코드 계약으로 자동 승격하거나 과거 원장을 보정하지 않았습니다. 이미 발생한 불명 요청의 생성·과금 여부는 이 수정으로 확정할 수 없습니다.

내일 DeepSeek 실행을 이어가기 전 최종 독립 검토를 통과하고, 수정된 코드·공급자 프로파일·예산·기준 구현 검증·파일럿 완전성이 일치하는 안전한 새 campaign과 동결 계약을 사용해 주셔야 합니다. 기존 불명 논리 요청을 자동 재생성하여 재개하지 않습니다. 새 캠페인·실제 사전 점검·실제 API 호출은 이 작업에서 실행하지 않았습니다.
