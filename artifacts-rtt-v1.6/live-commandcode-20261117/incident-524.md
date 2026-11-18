# HTTP 524 사고와 보존 자료 감사

2026-11-17에 두 모델의 사전 점검·파일럿·본 실험 원장 6개를 오프라인으로 감사하였습니다. 유료 실행은 중지되어 있으며 추가 API·사전 점검·파일럿·새 캠페인은 수행하지 않았습니다. 인증 파일·키·헤더·전체 환경을 읽거나 출력하지 않았습니다. 이 문서는 파생 감사이며 기존 관측·공식 summary·장부·계약을 수정하지 않습니다.

## 원인과 안전 판정

[Cloudflare 공식 524 설명](https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-5xx-errors/error-524/)을 2026-11-17 확인하였습니다. 원 서버 연결 뒤 응답을 기다리다 발생할 수 있는 오류이므로 생성이 없었다고 보장할 수 없습니다. 기존 공급자 구현은 524를 재시도 가능한 HTTP 상태로 처리하였고 불명 비용 예약은 유지했지만 자동 재전송 자체를 차단하지 못했습니다. 해당 API의 멱등 생성 보장은 확인되지 않았습니다.

모든 정상응답의 모델 ID는 요청 ID와 정확히 일치하였습니다. 다만 재전송 후 받은 정상응답은 첫 생성이라는 증거가 없으므로 최초 생성의 기능 실패·확인 판정으로 사용하지 않습니다. 원관측의 값과 감사 후 값은 [audit-derived.json](audit-derived.json), [GLM 임계치 CSV](glm53-audit-thresholds.csv), [GLM 확인 CSV](glm53-audit-confirmation.csv), [DeepSeek 임계치 CSV](deepseek_v4_pro-audit-thresholds.csv)에 별도로 남겼습니다.

## 전체 원장 요약

| 모델·단계 | 논리요청 | 전송 | 정상응답 | HTTP 524 | 추가 전송 | 추정 USD | 불명 예약 | 진행 예약 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| GLM 사전 점검 | 1 | 1 | 1 | 0 | 0 | 0.000077800 | 0 | 0 |
| GLM 파일럿 | 55 | 55 | 55 | 0 | 0 | 0.086116160 | 0 | 0 |
| GLM 본 실험 | 1,386 | 1,387 | 1,386 | 1 | 1 | 1.810113680 | 0.25 | 0 |
| DeepSeek 사전 점검 | 1 | 1 | 1 | 0 | 0 | 0.000048840 | 0 | 0 |
| DeepSeek 파일럿 | 67 | 67 | 67 | 0 | 0 | 0.371300776 | 0 | 0 |
| DeepSeek 본 실험 | 31 | 32 | 30 | 1 | 1 | 0.174579240 | 0.25 | 0.25 |
| 합계 | 1,541 | 1,543 | 1,540 | 2 | 2 | 2.442236496 | 0.50 | 0.25 |

다른 HTTP 상태 오류·추가 재전송은 없었습니다. 상태 원장은 정상응답 1,540건과 진행 중 1건을 구분합니다. 정상응답 원문 파일·정규화 JSON 수 역시 1,540개씩입니다. 알려진 추정액과 예약 합계는 3.192236496달러입니다. 실제 청구액은 미보고로 null이며 예약을 청구액으로 해석하지 않습니다. 모델·단계별 토큰·원장 SHA256·시도 목록은 [incident-524.json](incident-524.json)에 있습니다.

## 영향 논리요청과 슬롯

| 모델 | 영향 슬롯·단계 | 첫 524 전송 시작 UTC | 재전송 응답 ID |
|---|---|---|---|
| GLM | LC_0062/cpp-via-haskell/attempt-02/step-09 | 07:42:57.608710 | 57e4f36a-7250-42be-8587-a5efaea5b485 |
| DeepSeek | IPOP_9012/cpp-via-prolog/attempt-04/step-03 | 09:18:54.841185 | gen_01M7MCYKQ8XBGJ7HYJWC6RN3GB |

원자료 transport attempt의 at는 전송 시작 시각이며 HTTP 524 수신 시각은 별도 기록되지 않았습니다. 이를 정확한 오류 수신 시각으로 바꾸어 쓰지 않습니다. 첫 attempt ID·두 번째 전송·수신 원문·usage·관측 SHA256은 두 JSON의 연결 필드로 확인하실 수 있습니다.

- GLM call_id: `5116f9e6357fa0ebbb7021402b539d26aed620d12b7a29dff2778714798f5234`
- GLM 원관측 SHA256: `98e8c7c03b938b2ce03573bf747f971c99bb0301c618e5af15ede5236bc9b8a9`
- DeepSeek call_id: `8000eb404203af008081cb58606aafea1e725666e16a244ab3463121139a9302`
- DeepSeek 원관측 SHA256: `c8ab094d6a579509503aaa12c875fc1fbe03ac11c9aa4e0e3f4da327390a470c`

GLM은 step08 응답을 UTC 07:42:53.794440에 수신하고 0.80·0.85 최초 도달을 확정하였습니다. 확인 완료 예정은 step10이며 저장 단계는 1~9뿐이므로 524 전 완료 확인이 없습니다. 0.80·0.85 성공은 유지하고 0.90 원관측 functional_failure/format_error는 감사 후 invalid로, 원관측 확인 failed는 unavailable로 분리합니다. 주 0.85 경로별 P/H/D·분모는 실제 재계산 결과 바뀌지 않았습니다. 0.90의 총 유효 분모는 297→296, Haskell 유효는 72→71입니다. 자세한 값은 [GLM 결과](glm-results.md)에 있습니다.

DeepSeek의 해당 원관측은 step05 runtime_error로 끝났지만 step03 이후 생성이 불명 재전송의 후속이므로 세 임계치를 감사 후 invalid로 분리합니다. 기존 기능실패를 정상 첫 생성 결과로 사용하지 않습니다. 나머지 관측을 옛 슬롯 대신 새 캠페인에 합산하지 않습니다.

## 종료 당시 처리 중 요청

DeepSeek의 call_id `d193f8f645db4a17a41b779642ad89cf3e3c5e188072a6f008dd6f00f4b74d57`는 LC_0283/cpp-via-haskell/attempt-03/step-07입니다. 마지막 전송 시작은 UTC 09:35:51.557316이며 원장 상태 inflight, response_body.txt와 response.json 모두 없고 해당 슬롯 observation.json도 없습니다. 중지 후 파생 판정은 unknown이며 0.25달러 예약을 유지합니다. 서버 생성·과금 여부가 확인되지 않았으므로 같은 논리키로 재생성하지 않습니다. 원장 상태를 파생 판정으로 덮어쓰지 않았습니다.

PID16572는 종료 직전 python.exe와 `scripts/run_commandcode_v16.py --run` 명령 패턴을 검사해 대상 실행기임을 확인한 뒤 Stop-Process로 종료하였습니다. 직접 자식은 0개였으며 실행 세션 59997은 exit 1을 반환했고 [후속 조회 기록](pid-stop-check.json)에서도 PID가 없음을 확인하였습니다. 정확한 종료 시각은 별도 캡처하지 않았습니다. 종료가 끝난 뒤 작성된 중지 기록 UTC 09:37:35.465304를 상계로 보존하며 정밀 시각을 만들어내지 않습니다.

## 자료 무결성과 재현 명령

[incident-524.json](incident-524.json)은 30,567개 원자료 파일의 전후 SHA256을 보관하고 모두 일치함을 기록합니다. [audit-derived.json](audit-derived.json)은 원관측 SHA256, 영향 논리키, 배제 단계, 원응답 ID, 524 이전 수신 증거와 감사 후 판정의 연결을 보관합니다. 원자료 집합의 .json/.jsonl/.txt/.csv 및 생성 코드·입출력·zip 등을 대상으로 하였으며 이를 저장소 모든 바이너리의 검사라고 확장하지 않습니다.

아래 명령은 인증이나 네트워크 없이 파생 감사만 재생성합니다. 기존 원장·관측·공식 보고서는 쓰지 않습니다.

```powershell
uv run --no-sync black --check artifacts-rtt-v1.6/live-commandcode-20261117/derive_incident_audit.py
uv run --no-sync python artifacts-rtt-v1.6/live-commandcode-20261117/derive_incident_audit.py
```

black 검사 및 파생 감사의 공식 원관측 지표 일치·0.85 불변·관측 파일 해시 전후 일치 검사는 통과하였습니다. JPlag 주 무효는 최종 3건이며 [GLM 위치·사유 표](glm-results.md)에 정리하였습니다. 공급자 수정은 조정자가 전체 494개 통과를 보고하였으며 독립 검토는 대기 중입니다. 이번 작업자는 공급자 코드를 수정하지 않았고 수정된 코드로 유료 호출을 수행하지 않았습니다. 새 실행의 관문과 예산안은 [DeepSeek 인계](deepseek-handoff.md)에 있습니다.
