# DeepSeek 새 캠페인 최종 합동 독립 검토

검토일: 2026-11-17. 최종 legacy 충돌 보완과 2026-11-18용 DeepSeek 전용 래퍼·설정·오프라인 준비 근거를 함께 검토하였습니다. 전체 검사·독립 충돌 재현·실제 core 관문 대조가 통과하였으며, 이번 검토 범위에서 미해결 실행 차단 코드 결함을 발견하지 못하였습니다. 오프라인 실행 준비는 통과로 판정합니다.

실제 인증·API·`--run`·새 사전 점검·파일럿·본 실험은 실행하지 않았습니다. 오늘 유료 중지를 해제하는 판정이 아니며, 실제 모델 접속과 새 캠페인의 분석 완전성은 아직 검증되지 않았습니다.

## 최종 공급자와 legacy 충돌 보완

현재 `src/rttdist/providers.py`의 SHA-256은 지정된 최종 값과 일치합니다.

```text
7cd2242c0d1f4bac2527fb4a6179b461c107da0af6fc260060cfc2971512c4d4
```

기존 P2는 해결된 것으로 확인하였습니다. `CompatibleProvider.complete`는 실제 전송 전에 `transport_state.json`에 inflight를 저장하고, HTTP·통신 오류를 분류한 상태도 오류 이력보다 먼저 보존합니다. 재개 시 진행 기록과 과거 불명 오류 이력을 확인하여 unknown 표식 저장 전 충돌도 차단합니다. 완료 응답·원문 캐시의 우선 재생, 기존 비용 보존과 429·확인된 DNS/연결 거부의 제한 재시도는 유지합니다.

기존 검사 함수를 호출하는 대신 별도 Python 프로세스 세 개씩으로 두 지점을 독립 재현하였습니다. 모의 주소는 example.test이며 실제 네트워크는 사용하지 않았습니다.

| 첫 프로세스의 충돌 지점 | 남은 진행 상태 | 이후 두 프로세스 재개 | 총 전송 | 추가 전송 |
| --- | --- | --- | --- | --- |
| HTTP 524의 api_errors.json 저장 직후 | unknown·HTTP 524 | 모두 UnknownRequestState로 차단 | 1 | 0 |
| 전송 함수 호출 직후, 오류·결과 저장 전 | inflight | 모두 UnknownRequestState로 차단 | 1 | 0 |

오류에 넣은 가짜 비밀 문자열도 저장되지 않았습니다. 독립 재현 종료 코드는 0이며 `restart-review-legacy-reproduction.json`, `.log`, `.exitcode`에 결과를 보존하였습니다. 신규 legacy 회귀 21개와 기존 HTTP·캐시·비용·재개 회귀도 전체 검사에 포함되어 통과하였습니다.

## 새 래퍼와 실행 명세

검토한 주요 파일은 `scripts/run_deepseek_v16_20261118.py`, `tests/integration/test_deepseek_restart_runner.py`, 새 캠페인·공급자 YAML, 준비 execution-plan·source-manifest·offline-verification·검토 양식 및 갱신된 기존 deepseek-handoff입니다.

| 항목 | 확인 결과 |
| --- | --- |
| 기본 오프라인 | 기본 모드와 prepare 분기는 인증값을 꺼내기 전에 오프라인 준비만 수행합니다. DNS·socket 연결 차단 코드와 회귀검사를 확인하였습니다. 본 검토에서는 실제 main이나 prepare를 실행하여 준비 자료를 다시 쓰지 않았습니다. |
| 명시적 공급자 | 새 설정의 protocol=chat_completions와 공급자 compatible을 검사하고 생성되는 객체가 APIProvider임을 확인하였습니다. 설치한 core 팩토리도 APIProvider만 허용합니다. legacy CompatibleProvider는 새 실행 경로에 포함되지 않습니다. |
| 인증 비상속 | 실행 관문을 통과한 뒤 키를 메모리로 가져오고 provider.complete 동안만 환경에 넣었다가 finally에서 제거합니다. 컴파일·평가·JPlag 실행 구간은 허용 목록 환경을 사용합니다. 정상·예외·캐시 경로의 키 제거와 실제 모의 하위 프로세스의 비상속 회귀가 통과하였습니다. 실제 키는 읽지 않았습니다. |
| 경로 보호 | 새 루트·새 campaign_id만 허용하고 기존 루트와 경로 탈출을 거부합니다. 두 거부 조건을 직접 호출로 확인하였습니다. 기존 4관측·파일럿·응답·불명 요청을 새 실험으로 가져오는 경로가 없습니다. |
| 중복 실행 | 최상위 비차단 execution.lock을 사용합니다. 임시 파일 잠금을 보유한 채 별도 프로세스가 같은 잠금을 얻지 못하는 것을 독립 확인하였습니다. 실제 새 루트의 실행 잠금이나 실행 명령은 호출하지 않았습니다. |
| 소스·기존 근거 | 현재 64개 준비 파일과 사본, 기존 21개 보호 파일의 해시가 모두 manifest와 일치하였습니다. 매 관측·공급자 호출 전에도 같은 guard를 호출합니다. |
| 불명 재개 | 새 캠페인의 inflight·unknown·불명 예약을 시작 전과 매 관측 저장 후 확인합니다. 불명 슬롯은 먼저 보존하고 다음 실행을 차단하며 원장이나 실패 슬롯을 초기화하지 않습니다. HTTP 524의 단일 전송과 반복 complete 차단 회귀도 통과하였습니다. |
| 실제 core 연결 | execute는 실제 core의 pilot→완전성 감사→freeze_main_design→main→report 및 재현 검증을 순서대로 호출합니다. 임시 hook은 finally에서 복원됩니다. 순서·인수와 복원 회귀가 통과하였습니다. |
| 실제 core 관문 대조 | 새 설정을 실제 load_hops_config·검증 자료 관문·현재 도구 버전 검사에 연결하였습니다. 75개 기준 구현 결과와 독립 근거 195개를 수용하고 제안 계약 해시가 준비 manifest와 같음을 확인하였습니다. 별도 임시 폴더의 모의 사전 점검·파일럿 근거로 실제 freeze 함수를 호출하여 임계치 하나가 불완전하면 거부하고 완전하면 통과하는 것을 확인하였습니다. 실제 새 루트의 main_design을 생성한 것은 아닙니다. |
| 날짜·검토 관문 | 오늘 날짜의 유료 실행 거부와 passed=false인 template의 거부를 순수 검증 함수로 확인하였습니다. 실제 `--run`은 호출하지 않았습니다. 검토 증거는 보고서·명시한 소스의 현재 SHA-256과 대조됩니다. |

새 독립 캠페인은 정확히 12파일럿+300본 실험이며 기존 4관측을 재사용하지 않습니다. 실제 스케줄 함수의 길이도 각각 12·300입니다. 문제·평가·프롬프트·시드·홉·임계치·확인 조건은 이전 프로토콜과 같으며 새 날짜를 이유로 바꾸지 않습니다.

## 확정된 예산과 사전 점검 횟수

| 단계 | 논리/전송 상한 | 비용 상한 USD | 요청 예약 USD | 최대 재시도 |
| --- | --- | --- | --- | --- |
| 새 독립 사전 점검 | 1/1 | 0.24 | 0.12 | 0 |
| 새 전체 파일럿 | 144/432 | 49.62 | 0.25 | 2 |
| 새 본 실험 | 3600/10800 | 49.32 | 0.25 | 2 |

새 설정과 phase_settings의 실제 반환값·생성자 인수를 대조하였습니다. 새 OK 한 번은 확정된 새 독립 캠페인의 사전 점검이며 기존 불명 요청의 재시도가 아닙니다. 캠페인별 한도를 적용하고 기존 사전 점검 한 번과 새 한 번을 함께 공개한다는 명세를 확인하였습니다. 이 항목을 미확정 관문으로 남기지 않습니다.

최대 입력·출력과 준비 자료의 피크 단가에 따른 요청 상계 0.1081344는 사전 점검 예약 0.12 이하입니다. 신규 단계 상한 합계는 99.18입니다. 준비 manifest의 기존 DeepSeek 추정액·예약과 GLM 전체 배정을 포함한 보수적 합계는 약 200.475928856으로 200.50 이내입니다. 실제 Decimal 비교로 한도를 확인하였습니다. 추정·예약과 미보고 실제 청구액은 구분합니다.

## 검사·무결성 근거

| 검사 | 실제 결과 | 보존 위치 |
| --- | --- | --- |
| `uv run --no-sync pytest -q` | 종료 코드 0, 531 passed, 1166 warnings in 161.11s (0:02:41) | `restart-review-pytest.log`, `restart-review-pytest-command.json` |
| 변경 Python 네 파일 black 검사 | 종료 코드 0, 네 파일 변경 불필요 | `restart-review-black.log`, `restart-review-checks.json` |
| `git diff --check` | 종료 코드 0 | `restart-review-diff.log`, `restart-review-checks.json` |
| legacy 별도 프로세스 독립 재현 | 종료 코드 0, 두 충돌 지점의 재개 추가 전송 모두 0 | `restart-review-legacy-reproduction.json`, `.log`, `.exitcode` |
| 오프라인 준비·실제 core·잠금 대조 | 종료 코드 0 | `restart-review-offline-core-check.json`, `.log`, `.exitcode` |
| 검사 전후 해시 | 67개 파일 변경 0, 기존 보호 21개 변경 0 | `restart-review-before-hashes.json`, `restart-review-after-hashes.json`, `restart-review-final-verification.json` |

경고 종류는 MatplotlibDeprecationWarning 한 종류이며 실패와 구분하였습니다. 경고 억제 옵션·필터는 추가하지 않았습니다. 차이 검사의 줄바꿈 안내는 오류가 아닙니다. 모든 명령의 원출력과 실제 반환 코드를 보존하였습니다.

준비 manifest의 제안 계약은 `7db3da03dab3f81c6c827813158c9988d734a08f2a41c34297cdfc6df26c7991`이며 실제 현재 core 계산과 같습니다. 이것은 아직 새 API·파일럿 근거로 본 실험을 동결했다는 의미가 아닙니다. 새 실제 campaign 디렉터리도 생성되지 않은 상태를 확인하였습니다. 975개 기준 평가 전체를 새로 재실행한 것은 아니며 저장 검증 결과·현재 파일·도구 관문을 대조하였습니다.

## 독립 검토 기록과 남은 실행 범위

실제 검토자는 Codex 독립 검토자이며 세션은 `orca_session_id:6fc8186f-eab4-487c-a3f9-b1823c2f4b84`입니다. 통과 판정의 기계 검증 기록 위치는 새 루트의 `artifacts-rtt-v1.6/live-deepseek-20261118/independent-review.json`입니다. 이 보고서 SHA-256과 실제 내용을 검토한 공급자·core·래퍼·인증 격리 helper·두 신규 테스트·두 설정의 SHA-256, 실제 검사 결과를 별도로 기록합니다. 준비 당시 pending 기록과 passed=false template은 수정하지 않습니다. 해당 근거의 require_review 검증 결과는 `restart-review-evidence-check.json`에 보존하는 방식입니다.

1. 사용자께서 2026-11-18 이후 작업을 재개하실 때도 최종 소스·설정·사본과 독립 검토 근거가 같아야 합니다. 변경되면 경고를 우회하거나 예전 계약을 덮어쓰지 않습니다.
2. 새 독립 OK 한 번·전체 12파일럿·완전성 감사·새 main_design 동결·300슬롯 수집·실제 보고와 재현은 아직 실행하지 않았습니다. 이번 판정은 이 오프라인 실행 준비가 검토 관문을 통과하였다는 의미입니다.
3. 실제 공급자 모델 접근·응답 지연·청구액·새 번역 결과·파일럿 완전성은 이번 오프라인 검사로 보장하지 않습니다. 과거 캠페인과 불명 요청은 별도로 보존하며 결과를 합산하지 않습니다.

소스·기존 원자료·계약은 수정하지 않았고, 검토 보고서·검증 로그·해시·새 독립 검토 JSON만 작성 범위입니다. 하위 작업자 생성과 git add/commit은 수행하지 않았습니다.
