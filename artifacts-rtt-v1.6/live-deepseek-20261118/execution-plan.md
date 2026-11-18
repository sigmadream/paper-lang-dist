# DeepSeek V4 Pro 대체 캠페인 오프라인 준비 명세

작성일은 2026-11-17이며 계획 캠페인 날짜는 2026-11-18입니다. 조정자가 확정한 전체 12파일럿+300본 실험을 새 DeepSeek 전용 캠페인으로 준비하였습니다. 키 없는 prepare와 모의·정적 검사, 최종 합동 독립 검토를 완료했으며 전체 회귀 531개가 통과했습니다. 새 API 호출은 0회이고 사용자께서 작업을 재개하시기 전에는 유료 실행하지 않습니다. 이 완료 범위는 오프라인 실행 준비입니다.

## 범위와 파일

- 캠페인: `commandcode-deepseek_v4_pro-v16-20261118`
- 출력 루트: `artifacts-rtt-v1.6/live-deepseek-20261118`
- [새 캠페인 설정](../../configs/v1.6/campaigns/commandcode_deepseek_v4_pro_20261118.yaml), [새 공급자 설정](../../configs/v1.6/providers/commandcode_deepseek_v4_pro_20261118.yaml), [새 전용 래퍼](../../scripts/run_deepseek_v16_20261118.py), [모의 검사](../../tests/integration/test_deepseek_restart_runner.py)
- [준비 manifest](source-manifest.json), [64개 소스·설정·검증 근거 사본](execution-sources/), [기존 21개 핵심 파일 기준 해시](legacy-baseline.json), [기존 30,567개 원자료 불변 검사](prior-artifact-verification.json)
- [기존 캠페인 보존 상태·사고 감사·인계](../live-commandcode-20261117/deepseek-handoff.md), [기존 사고 감사 JSON](../live-commandcode-20261117/incident-524.json)

기존 GLM과 DeepSeek 캠페인 원자료·장부·동결 계약, 기존 두 모델 래퍼·설정·source-manifest를 수정하지 않았습니다. 이전 4관측·진행 요청·불명 요청·파일럿 응답을 새 실험과 합산하거나 재사용하지 않습니다. 새 래퍼에는 GLM 실행 경로가 없습니다. Windows 기본 경로 제한을 확인하여 사전 점검 잠금 파일의 예상 경로가 261자가 되던 긴 루트 이름을 줄였으며 현재 예상 길이는 249자입니다.

## 조건과 비용

요청 모델 ID는 `deepseek/deepseek-v4-pro`, endpoint는 `https://api.commandcode.ai/provider/v1/chat/completions`, 요청은 max_tokens 16384·reasoning_effort low입니다. temperature·top_p는 추론 모드 문서 제약에 따라 전달하지 않으며 seed도 지원 근거가 없어 전달하지 않습니다. 서버 실효 설정 미보고는 null로 유지합니다. 같은 low를 다른 모델과 같은 추론량으로 해석하지 않습니다. 공식 근거 조회일과 단가는 [기존 실행 계획](../live-commandcode-20261117/execution-plan.md)을 참조하며 이번 오프라인 준비에서 웹 조회·모델 호출을 새로 했다고 표시하지 않습니다.

문제 15개·파일럿 문제 3개·4경로·반복·스케줄 시드 20261117·프롬프트·13사례 평가·JPlag 최소 토큰 9·시간 제한·홉 제한·임계치 0.80/0.85/0.90·확인 규칙은 기존 설계 그대로입니다. 날짜가 바뀌어도 스케줄 시드를 바꾸지 않았습니다. 새 설정과 기존 설정의 공통 조건 일치를 모의 검사에서 확인하였습니다.

| 단계 | 논리/전송 상한 | 비용 상한 USD | 요청 예약 USD | 통신 재시도 |
|---|---|---:|---:|---:|
| 새 독립 사전 점검 | 1/1 | 0.24 | 0.12 | 0 |
| 새 전체 파일럿 | 144/432 | 49.62 | 0.25 | 최대 2 |
| 새 본 실험 | 3600/10800 | 49.32 | 0.25 | 최대 2 |

한도는 독립된 계획 캠페인별로 적용하며 기존 중단 호출은 별도 공개합니다. 새 OK 요청은 기존 불명 요청의 재전송이 아닙니다. 기존 사전 점검 1회와 새 캠페인 1회를 함께 보고하고 현재 새 실접속은 0회입니다. 최대 입력 32768·출력 16384토큰, 백만 토큰당 피크 입력 1.32·출력 3.96·캐시 입력 0.044달러를 사용하여 요청 상계는 0.1081344달러입니다. 실제 청구액은 미보고이며 추정값·불명 예약과 구분합니다.

신규 상한 합계는 99.18달러입니다. 기존 두 모델 추정액+예약 3.192236496달러를 포함한 최대 추가 합계는 102.372236496달러입니다. GLM의 기존 전체 배정 100.25달러까지 보수적으로 유지해도 100.25+기존 DeepSeek 추정·예약 1.045928856+신규 DeepSeek 99.18=200.475928856달러로 기존 전체 200.50달러 이내입니다. 준비 단계에서 기존 원장 근거를 읽어 이 한도를 검증하였고 manifest에 남겼습니다.

## 실행·인증·재개 경계

기본 모드와 `--prepare`는 네트워크 연결과 DNS 조회를 차단하고 인증값 없이 코퍼스 검증 근거·도구 버전·현재 소스 해시·설정을 점검합니다. APIProvider 생성자와 최대 비용 계산만 수행하며 생성 요청을 보내지 않습니다. 준비 manifest는 64개 실행 소스·설정·검증 근거와 사본, 기존 21개 불변 근거, 현재 실행 환경, 제안 계약 해시를 보관합니다. 이것은 실접속 사전 점검이나 main_design 동결이 아닙니다.

래퍼 SHA256은 `b518c8e96a5dfb0c0284ef393112eed57dbb95e34ba1180fa2121a46a6eb527f`, 준비 시 제안 계약 해시는 `7db3da03dab3f81c6c827813158c9988d734a08f2a41c34297cdfc6df26c7991`입니다. 실제 본 실험 동결은 새 실접속·전체 파일럿 관문 통과 후 core가 생성합니다.

새 래퍼는 실제 `run_hops_campaign`·완전성 감사·`freeze_main_design`·`report_hops_campaign`·`verify_v16_reproducibility`를 그대로 사용합니다. 공급자 팩토리는 명시적 protocol을 가진 v1.6 APIProvider임을 검사하며 legacy CompatibleProvider를 실행하지 않습니다. 실제 compile·기능 평가·JPlag·프롬프트·판정은 core 그대로이며 모의 결과로 바꾸지 않습니다.

실행 프로세스가 받은 CMD_API_KEY는 기술 관문 통과 후 메모리에 보관하고 provider.complete 동안만 인증 환경에 넣었다가 finally에서 제거합니다. 평가·컴파일·JPlag에는 환경 허용 목록만 상속합니다. 소스·설정·사본 해시를 매 관측 및 공급자 호출 전 점검하고 기존 루트·경로 탈출 쓰기를 거부합니다. 단일 비차단 실행 잠금으로 중복 실행을 막으며 별도 샤드·모델 병렬 실행은 없습니다.

같은 새 캠페인 안에서 정상 저장 응답은 동일 계약·논리키로 재개할 수 있습니다. 불명·진행 요청이나 불명 예약이 남으면 재개를 차단합니다. HTTP 524는 실제 수정된 공급자 경로의 모의 전송에서 1회만 전송되고 반복 complete에서도 재생성되지 않음을 확인하였습니다. 관측 도중 불명이 남아도 현재 슬롯은 보존하고 이후 실행을 중지합니다. 예외를 유료 실행기 밖으로 그대로 출력하지 않고 유형·저장 상태만 기록하며, 종료 시 비밀정보 저장 감사를 수행합니다.

## 최종 독립 검토 관문

최종 providers.py 해시는 `7cd2242c0d1f4bac2527fb4a6179b461c107da0af6fc260060cfc2971512c4d4`입니다. 이 해시로 prepare를 완료하였습니다. v1.6 HTTP 불명 보호와 GLM 감사에 이어 legacy 충돌 보완·새 래퍼의 [최종 합동 독립 검토](../../.test-tmp/v16-orchestration/deepseek-restart-final-review.md)도 통과했습니다. 전체 회귀 531개, 변경 네 파일 black, 두 충돌 지점의 별도 프로세스 재개 차단과 67개 파일 전후 해시 불변이 확인됐습니다. 검토 범위에서 미해결 실행 차단 결함은 발견되지 않았습니다.

[검토 근거 양식](independent-review.template.json)은 준비 당시 passed=false인 기록으로 유지합니다. 실제 검토자는 별도 [independent-review.json](independent-review.json)에 통과 판정·검토자·보고서 SHA256·검토한 소스 여덟 개의 SHA256·검사 결과를 기록했습니다. require_review 검증 함수도 이 파일을 오프라인으로 수락했습니다. 래퍼는 명시된 소스와 보고서 해시를 검사하므로 이후 변경되면 인증값 접근 전에 실행을 거부합니다. 이 근거는 실제 모델 호출이나 파일럿·본 실험 동결 완료를 의미하지 않습니다.

## 검증 명령과 결과

1. 구현 전 새 래퍼 부재로 2실패·11오류를 관측하였고, 구현 후 13개를 통과하였습니다. 기본 오프라인 준비에서 DNS 이전 차단 검사를 추가하여 1실패를 재현한 뒤 DNS 차단을 보완하고 15개를 통과하였습니다.
2. 새 실제 설정의 공통 조건·12/300슬롯·APIProvider 선택 검사를 추가한 뒤 아래 묶음에서 새 16개·기존 래퍼 5개·HTTP 불명 복구 32개, 합계 53개가 통과하였습니다. 이 숫자를 과거 494개·관련 143개와 중복 합산하지 않습니다.
3. black 포맷팅과 키 없는 prepare가 exit 0으로 종료하였으며 64개 파일 manifest를 저장하였습니다. 기존 원자료 30,567개와 기존 핵심 파일 21개의 SHA256 재확인에서도 변경이 없었습니다.

[이번 검증 JSON](offline-verification.json)에 명령·종료코드·소스 및 문서 해시·실행 미개시 여부를 정리하였습니다. 과거 인계 문서 해시는 과거 검증 파일에 그대로 보존합니다.

```powershell
uv run --no-sync pytest tests/integration/test_deepseek_restart_runner.py tests/integration/test_commandcode_campaign_runner.py tests/integration/test_http_unknown_recovery.py -q
uv run --no-sync black --check scripts/run_deepseek_v16_20261118.py tests/integration/test_deepseek_restart_runner.py
uv run --no-sync python scripts/run_deepseek_v16_20261118.py --prepare
```

## 내일 사용할 명령

오늘 실행하지 않았으며 사용자께서 작업을 재개하신 뒤 독립 검토와 소스 해시가 일치할 때 사용합니다. 한국 시간 2026-11-17에는 래퍼 자체도 유료 실행을 거부합니다. `independent-review.json`은 실제 검토 결과로 생성돼 오프라인 수락을 확인했습니다. 기존 두 모델 래퍼를 실행하는 명령으로 바꾸지 않습니다.

```powershell
uv run --env-file 'C:/Users/sigma/works/paper-lang-dist/.env' --no-sync python scripts/run_deepseek_v16_20261118.py --run --review-evidence artifacts-rtt-v1.6/live-deepseek-20261118/independent-review.json > artifacts-rtt-v1.6/live-deepseek-20261118/run.log 2>&1
```

진행 로그는 새 루트의 progress.jsonl·status.json에 보존하며 본 실험 75슬롯 단위 event를 남깁니다. 실행을 맡은 작업자는 사전 점검·파일럿·동결·75슬롯·보고 완료 시 조정자에게 전달해 주십시오. 기존 실패 슬롯 대체·원장 초기화·기존 응답 덮어쓰기·소스 해시 경고 우회 명령은 제공하지 않습니다. 준비 중 드러난 실행 소스 수정이 필요하면 이 manifest를 덮어써 관문을 통과시키지 말고 변경 근거와 새 준비 계약을 다시 정리해야 합니다.
