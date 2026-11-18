# DeepSeek V4 Pro 다음 실행 인계

2026-11-17 사용자 지시에 따라 유료 실행을 중지한 상태에서 자료를 정리하였습니다. 조정자가 확정한 범위와 예산으로 2026-11-18용 DeepSeek 전용 설정·래퍼의 오프라인 준비와 최종 합동 독립 검토를 완료하였습니다. 전체 회귀 531개가 통과했고 검토 근거 JSON의 오프라인 검증도 통과했습니다. 실제 새 사전 점검·파일럿·본 실험은 시작하지 않았으며 사용자께서 작업을 재개하시기 전에는 유료 실행을 금지합니다. 이번 완료 범위는 자료 정리와 다음 실행의 오프라인 준비입니다.

## 보존한 기존 실행

후속 사용자 지시에 따라 GLM의 JPlag 측정 불가 3건은 별도 측정 실패로 집계하고 해당 코드를 [GLM 결과 문서](glm-results.md)에 수록했습니다. 이 변경은 GLM 결과 정리의 사후 집계 규칙이며, DeepSeek 실행 코드·새 준비 계약·기존 불명 요청 판정을 변경한 것은 아닙니다. 나머지 작업과 실제 실행은 내일로 미룹니다.

- 캠페인: [commandcode-deepseek_v4_pro-v16-20261117](commandcode-deepseek_v4_pro-v16-20261117/)
- [계약·본 실험 동결](commandcode-deepseek_v4_pro-v16-20261117/main_design.json): `c3a8248256425121a33a1e2342fc9258e6f9146eadadcc9e82877fd98ff543e6`
- main_design.json SHA256: `c6afa0c9bf2d49ecbe92bc6179cca951bbeebb36a68cffbd4680155dd515cc9c`
- [전체 실행 manifest](source-manifest.json) SHA256: `9397d7fe843e7fb7003d743ece51f155a9171c8f7d5540b8925b8826f9ce113d`
- 당시 실행 래퍼 SHA256: `aee0838d6de8c586fb90a714ba80b11f37825d006455f2f110ea92491010ef9e`
- [동결 소스 사본](execution-sources/), [실행 세션·명령](execution-session.json), [실행 로그](run.log), [최초 실행 계획](execution-plan.md), [원장·해시 감사](incident-524.json), [524 영향 연결](audit-derived.json)
- 원장: [사전 점검](commandcode-deepseek_v4_pro-v16-20261117/preflight/provider_ledger.jsonl), [파일럿](commandcode-deepseek_v4_pro-v16-20261117/pilot/provider_ledger.jsonl), [본 실험](commandcode-deepseek_v4_pro-v16-20261117/main/provider_ledger.jsonl), [본 실험 상태](commandcode-deepseek_v4_pro-v16-20261117/main/provider_ledger.jsonl.state.json)

정확 모델 ID `deepseek/deepseek-v4-pro`는 정상응답 98건 전부에서 정확 일치하였습니다. 설정은 max_tokens 16384, reasoning_effort low이며 추론 모드 제약으로 temperature·top_p를 보내지 않았고 seed도 보내지 않았습니다. 실효 설정은 null입니다. GLM과 모델별 별도 조건이며 같은 low를 같은 추론량으로 해석하지 않습니다. Flash 대체는 없습니다.

사전 점검은 새 프로파일로 1회 통과하였습니다. 파일럿 12/12슬롯의 구조 감사·세 임계치 완전성이 통과하여 본 실험을 동결하였습니다. 본 실험은 4/300슬롯 저장, 296슬롯 미저장 상태에서 중지하였습니다. 미저장 중 LC_0283/Haskell/반복 3은 step06까지 처리한 뒤 step07 요청이 진행 중이었으며 나머지 295슬롯은 미시작입니다.

| 저장 슬롯 | 원관측 최종 상태 | 감사 후 구분 |
|---|---|---|
| IPOP_9012/cpp-via-prolog/attempt-04 | runtime_error 기능 실패 | step03 524 재전송 이후 결과이므로 세 임계치 invalid |
| IPOP_9012/cpp-via-haskell/attempt-02 | collection_complete | 보존된 정상 관측 |
| IPOP_1992/cpp-via-prolog/attempt-02 | runtime_error 기능 실패 | 보존된 기능 실패 |
| LC_0062/cpp-via-python/attempt-04 | collection_complete | 보존된 정상 관측 |

이는 계획 300슬롯 중 극히 일부의 상태 안내이며 모델 성능 추정이나 새 실험과 합산에 사용하지 않습니다. [원관측/감사 후 임계치 표](deepseek_v4_pro-audit-thresholds.csv)와 [확인 표](deepseek_v4_pro-audit-confirmation.csv)를 구분해 보존하였습니다.

## 종료와 불명 요청

PID16572는 실행기 python.exe와 명령 패턴을 확인한 뒤 종료하였습니다. 직접 자식 0, 실행 세션 59997 exit 1, 후속 PID 조회 없음이 확인되었습니다. 정확 종료 시각은 별도 수집하지 않았고 UTC 09:37:35.465304를 종료 완료 기록의 상계로 남겼습니다. 상세 근거는 [사고 감사](incident-524.md)에 있습니다.

HTTP 524 영향은 IPOP_9012/Prolog/반복 4/step03의 call_id `8000eb404203af008081cb58606aafea1e725666e16a244ab3463121139a9302`입니다. 두 번째 전송으로 원응답은 저장되었지만 첫 전송의 생성·과금은 불명이며 0.25달러 예약을 유지합니다.

종료 당시 진행 요청은 LC_0283/Haskell/반복 3/step07의 call_id `d193f8f645db4a17a41b779642ad89cf3e3c5e188072a6f008dd6f00f4b74d57`입니다. 전송 시작 UTC 09:35:51.557316, 원장 inflight, 원응답·정규화 응답·슬롯 관측 미저장으로 파생 판정 unknown입니다. 예약 0.25달러를 유지하고 서버 생성 여부가 확인되지 않은 요청을 재생성하지 않습니다. 원장을 초기화하거나 해당 요청·슬롯을 바꾸지 않습니다.

## 확정된 새 캠페인과 예산

조정자가 새 대체 캠페인을 DeepSeek만의 전체 12파일럿+300본 실험으로 확정하였습니다. 새 campaign_id는 `commandcode-deepseek_v4_pro-v16-20261118`이며 출력 루트는 [live-deepseek-20261118](../live-deepseek-20261118/)입니다. 기존 GLM을 실행하지 않습니다. 기존 DeepSeek 4관측·진행 요청·불명 요청·파일럿·사전 점검 응답을 새 캠페인과 합산하거나 재사용하지 않습니다. 아래 기존 비용과 호출은 별도 공개합니다.

| 단계 | 기존 논리/전송 | 정상응답 | 입력/출력 토큰 | 알려진 추정 USD | 불명·진행 예약 USD | 확정 신규 상한 USD |
|---|---|---:|---|---:|---:|---:|
| 사전 점검 | 1/1 | 1 | 13/8 | 0.000048840 | 0 | 0.24 |
| 파일럿 | 67/67 | 67 | 42,757/83,140 | 0.371300776 | 0 | 49.62 |
| 본 실험 | 31/32 | 30 | 18,275/39,850 | 0.174579240 | 0.50 | 49.32 |
| 합계 | 99/100 | 98 | 61,045/122,998 | 0.545928856 | 0.50 | 99.18 |

신규 상한은 기존 추정액과 미해결 예약을 단계별 원래 상한에서 뺀 값을 센트 단위로 내림한 값으로 확정하였습니다. 파일럿·본 실험 요청 예약은 0.25달러를 유지하고 새 사전 점검에만 0.12달러를 사용합니다. 최대 입력 32,768·출력 16,384토큰의 DeepSeek 피크 단가 상계는 0.1081344달러여서 0.12달러 예약으로 덮이며 사전 점검 상한 0.24달러 이내입니다. 새 파일럿·본 실험에 각각 50달러를 다시 부여하지 않습니다.

기존 두 모델 추정액+예약 3.192236496달러에 위 신규 99.18달러를 더하면 102.372236496달러입니다. GLM의 원래 미사용 한도를 포함해 GLM 배정 100.25달러를 전부 유지하는 보수적 배정 계산도 100.25+기존 DeepSeek 1.045928856+신규 DeepSeek 99.18=200.475928856달러로 전체 200.50달러 이내입니다. 이 계산은 청구액 확인이 아니며 실제 청구액은 null입니다. 추정 단가는 백만 토큰당 입력 1.32·출력 3.96·캐시 입력 0.044달러를 사용하였습니다.

입력 토큰에 포함된 캐시 입력은 사전 점검 0·파일럿 11,264·본 실험 5,760토큰입니다. 조정자는 수정된 전송 처리의 새 캠페인에서 독립 OK 요청 1회를 수행하도록 확정하였습니다. 이는 기존 불명 요청의 재전송이 아닙니다. 기존 캠페인 사전 점검 1회와 새 캠페인 사전 점검 1회를 함께 공개하며, 현재 새 캠페인에서 실제 실행한 횟수는 0회입니다.

조정자는 논리/전송 한도를 독립된 계획 캠페인별 한도로 확정하였습니다. 새 파일럿은 최대 144논리/432전송, 본 실험은 최대 3600논리/10800전송이며 통신 재시도는 최대 2회입니다. 새 사전 점검은 최대 1논리/1전송·재시도 0회입니다. 기존 중단 캠페인의 호출을 위 새 한도에서 차감하지 않고 별도 공개하되 비용은 기존 실행과 미해결 예약을 포함하여 전체 200.50달러 상한을 유지합니다. 사용자 원요청 밖의 실행 승인 절차를 추가하지 않습니다.

## 다음 실행의 필수 순서

1. [최종 합동 검토 보고서](../../.test-tmp/v16-orchestration/deepseek-restart-final-review.md)를 확인해 주십시오. 전체 회귀 531개·서식 검사·두 legacy 충돌 지점의 독립 재현이 통과했으며 검토 범위의 미해결 실행 차단 결함은 없습니다. 최종 providers.py SHA256은 `7cd2242c0d1f4bac2527fb4a6179b461c107da0af6fc260060cfc2971512c4d4`입니다.
2. 실제 검토자가 작성한 [독립 검토 근거](../live-deepseek-20261118/independent-review.json)의 통과 판정·보고서 해시·소스 해시가 현재 파일과 일치해야 합니다. 이 파일은 오프라인 require_review 검사에서 수락됐습니다. 준비 당시 passed=false인 양식은 역사적 준비 기록으로 유지하며 실행 근거로 사용하지 않습니다.
3. [오프라인 준비 manifest](../live-deepseek-20261118/source-manifest.json)의 현재 파일·사본·기존 근거 해시가 모두 일치하는지 확인해 주십시오. 준비 후 실행 소스나 설정이 바뀌면 기존 manifest 경고를 우회하거나 과거 main_design을 덮어쓰지 않아야 합니다. 기존 캠페인은 provider 변경으로 그대로 재개할 수 없습니다.
4. 사용자께서 2026-11-18 이후 작업을 재개하시고 위 기술 관문이 통과하면 아래 새 전용 명령으로 실행해 주십시오. 래퍼는 독립 새 사전 점검→실제 core의 전체 12파일럿→완전성 감사→새 본 실험 동결→전체 300슬롯→공식 보고·재현을 단일 프로세스로 순차 호출합니다. 문제·평가·프롬프트·임계치·중단 규칙은 유지합니다.
5. 같은 새 캠페인 안에서 저장 응답은 동일 계약·논리키로만 재사용합니다. 불명·진행 요청이 남으면 래퍼가 재개를 차단하며 새 생성으로 덮어쓰지 않습니다. 기존 중단 캠페인의 응답·슬롯을 가져오거나 실패를 대체하지 않습니다. 실행 중에는 75슬롯 단위 로그를 확인하고 조정자에게 진행을 전달해 주십시오.

## 정확한 오프라인 확인 명령

작업 경로는 `C:/Users/sigma/orca/workspaces/paper-lang-dist/stickleback`입니다. 다음 명령에는 키나 인증 파일 주입이 없고 유료 호출을 하지 않습니다. 회귀 검사는 수정 검토 시 사용할 명령이며 이번 자료 정리에서 이를 다시 실행했다고 주장하지 않습니다.

```powershell
uv run --no-sync pytest tests/integration/test_http_unknown_recovery.py tests/unit/test_provider_ledger.py tests/integration/test_provider_recovery.py tests/integration/test_commandcode_campaign_runner.py -q
uv run --no-sync pytest tests/integration/test_deepseek_restart_runner.py tests/integration/test_commandcode_campaign_runner.py tests/integration/test_http_unknown_recovery.py -q
uv run --no-sync black --check scripts/run_deepseek_v16_20261118.py tests/integration/test_deepseek_restart_runner.py
uv run --no-sync python scripts/run_deepseek_v16_20261118.py --prepare
uv run --no-sync black --check artifacts-rtt-v1.6/live-commandcode-20261117/derive_incident_audit.py
uv run --no-sync python artifacts-rtt-v1.6/live-commandcode-20261117/derive_incident_audit.py
Get-Process -Id 16572 -ErrorAction SilentlyContinue
```

기존 실제 유료 실행의 정확한 명령은 [execution-session.json](execution-session.json)에 증거로만 보존하였습니다. 이 명령과 기존 `--run`은 내일 재개용이 아닙니다. 기존 실패 슬롯 대체·원장 초기화·응답 덮어쓰기·기존 계약 변경 명령은 제공하지 않습니다. [GLM 결과](glm-results.md)는 별도 보존 자료이며 두 캠페인 자료를 합쳐 전체 600슬롯 완료로 표시하지 않습니다.

## 내일 사용할 새 전용 실행 명령

다음 명령은 오늘 실행하지 않았습니다. 기본 모드와 `--prepare`는 인증값 없이 오프라인 준비만 수행합니다. `--run`은 한국 시간 2026-11-18 이후 사용자께서 재개하실 때, 준비 소스 해시 일치, 실제 독립 검토 근거, 새 캠페인의 불명 요청 없음, 필요한 인증값을 확인한 뒤 호출합니다. `independent-review.json`은 생성됐으며 오프라인 검토 관문을 통과했습니다. 기존 중단 캠페인의 불명 요청은 별도로 보존합니다.

```powershell
uv run --env-file 'C:/Users/sigma/works/paper-lang-dist/.env' --no-sync python scripts/run_deepseek_v16_20261118.py --run --review-evidence artifacts-rtt-v1.6/live-deepseek-20261118/independent-review.json > artifacts-rtt-v1.6/live-deepseek-20261118/run.log 2>&1
```

기존 `run_commandcode_v16.py`는 GLM까지 포함하므로 위 명령에서 사용하지 않습니다. 새 설정은 [캠페인 YAML](../../configs/v1.6/campaigns/commandcode_deepseek_v4_pro_20261118.yaml), [공급자 YAML](../../configs/v1.6/providers/commandcode_deepseek_v4_pro_20261118.yaml), 새 래퍼는 [run_deepseek_v16_20261118.py](../../scripts/run_deepseek_v16_20261118.py)입니다. [새 실행 계획](../live-deepseek-20261118/execution-plan.md), [과거 자료 불변 검사](../live-deepseek-20261118/prior-artifact-verification.json), [이번 오프라인 준비 검증](../live-deepseek-20261118/offline-verification.json)을 함께 확인해 주십시오. 기존 script/config/source-manifest·계약·원자료는 수정하지 않았습니다. 과거 handoff-verification.json은 이전 정리 시점의 문서 해시를 보존하며 이번 갱신 문서의 근거는 새 오프라인 검증 파일에 남깁니다.
