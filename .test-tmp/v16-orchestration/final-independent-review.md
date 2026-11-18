# v1.6 구현 독립 검토 보고서

검토일: 2026-11-17. 기준 HEAD는 `a3acc7b3bc6e6c17771f960da17acc319a4f9a59`이며, 미추적 파일을 포함한 현재 작업본을 검토하였습니다. 소스·설정·기존 테스트는 수정하지 않았습니다.

최신 전체 회귀검사는 392개 통과·실패 0개이지만, 별도 모의 검사에서 우선순위 P1 두 건과 P2 두 건을 재현하였습니다. 따라서 회귀검사 통과와 본 실험 관문 충족을 구분하셔야 합니다. 아래 문제는 수정되지 않은 상태입니다.

## 발견 사항

### P1: 시간 제한을 넘겨 완료된 단계가 새 성공으로 반영됩니다

위치: `src/rttdist/hops_experiment.py:441`, `src/rttdist/hops_experiment.py:505`.

관측 실행기는 새 단계 시작 전에만 900초 탐색·300초 확인 제한을 검사하고, 공급자 응답·기능 검사·유사도 측정 이후에는 시간을 다시 검사하지 않은 채 `state.record_step`을 호출합니다. 이에 따라 탐색 제한 뒤 얻은 최초 도달이 성공으로 남으며, 다음 반복에서 시간 초과로 중단해도 이미 기록한 성공은 유지됩니다. 마지막 단계에서 종료 조건을 충족하면 다음 반복 자체가 없어 초과를 놓칠 수 있습니다. 확인 구간에도 같은 검사 배치가 적용됩니다.

`tests/integration/test_hops_experiment.py`의 `setup.__wrapped__`와 `MockProvider`를 사용하고 실제 시간·네트워크 대신 `hops.time.monotonic`을 모의하였습니다. 시작 시각을 0으로 두고 두 번째 응답 직전에 시각을 901로 바꾸자 `reached_step=2`, `category=success`, `sym_adj=0.95`로 기록되었습니다. 종료 사유는 `observation_wall_clock`이고 확인은 `unavailable`이었지만, 900초 안에 도달하지 않은 주 임계치 성공이 보존되었습니다.

추가로 10홉에서 0.85에 처음 도달하게 한 뒤, 확인 구간의 12번째 응답에서 모의 시각을 301초로 바꾸었습니다. 확인 제한 300초를 초과하였는데도 `confirmation_status=passed`, `terminal_status=collection_complete`가 반환되었습니다.

근거: `final-review-repro.log`의 `search_deadline`, `final-review-chain-repro.log`의 `confirmation_deadline`. 설계의 900초·300초 초과 시 기반시설 중단 규칙에 맞춰, 단계 결과를 최초 도달·확인으로 반영하기 전에 경과 시간을 검사하고 이전에 확정된 결과만 보존하는 보완이 필요합니다. 공급자 호출이나 평가 도중의 즉시 중단까지 검증한 것은 아닙니다.

### P1: 모든 임계치가 불완전한 파일럿도 본 실험 동결을 통과합니다

위치: `src/rttdist/hops_experiment.py:812`, `src/rttdist/hops_experiment.py:938`, `scripts/freeze_v16_design.py:34`.

캠페인의 `completion_audit.passed`는 관측 수와 구조 감사만 확인하므로, 12개 파일럿 관측이 모두 `invalid`여도 참일 수 있습니다. `freeze_main_design`은 해당 참 값·12개 관측·계약 해시만 확인하고 `complete_by_threshold`를 읽지 않습니다. 따라서 파일럿의 연결·성능·평가가 전부 무효여도 본 실험의 유료 호출을 허용하는 동결 파일을 생성할 수 있습니다. 공유 집계 계약 문서도 파일럿 동결 시 관측 수와 필요한 임계치 완전성을 함께 점검하도록 명시합니다.

`tests/integration/test_v16_freeze.py`의 `inputs.__wrapped__`로 정상 모의 검증·사전 점검을 구성하고 파일럿 감사의 세 `complete_by_threshold` 값을 모두 거짓으로 설정하였습니다. `freeze_main_design`은 예외 없이 `approved_for_main=true`, `confirmatory=true`를 반환하였습니다. 실제 API는 호출하지 않았습니다.

별도의 연결 재현에서는 관측 실행기만 0단계·모든 임계치 `invalid`인 결과를 저장하도록 모의하고 실제 `run_hops_campaign`을 실행하였습니다. 12개 관측으로 생성된 실제 `completion_audit.json`은 `passed=true`, `collection_finished=true`, 모든 임계치 완전성 거짓이었고, 이 파일을 그대로 `freeze_main_design`에 전달해 본 실험 승인을 얻었습니다.

근거: `final-review-repro.log`의 `invalid_pilot_freeze`, `final-review-chain-repro.log`의 `all_invalid_campaign_to_freeze`. 동결 관문은 구조 감사와 별도로 필요한 파일럿 임계치의 완전성을 요구해야 합니다. 기능 실패를 유효한 파일럿 결과로 수용하는 것과 기반시설 오류를 통과시키는 것은 구분하셔야 합니다. 파일럿 성공률이나 순위에 따라 실험 조건을 바꾸라는 의미는 아닙니다.

### P2: 검증기·독립 계산기의 소스 해시가 실행 관문에 연결되지 않습니다

위치: `src/rttdist/hops_experiment.py:680`, `src/rttdist/hops_experiment.py:145`, `scripts/validate_v16_corpus.py:121`, `scripts/validate_v16_corpus.py:287`.

코퍼스 검증 결과는 준비·검증 스크립트의 `validator_source_hashes`와 독립 계산기의 `independent_checks.source_hashes`를 저장합니다. 그러나 `_validated_inputs`는 이 해시와 현재 파일을 비교하지 않으며, `build_run_contract`의 구현 해시 목록에도 해당 스크립트와 계산기가 포함되지 않습니다. 검증 코드를 변경한 뒤 오래된 검증 결과를 사용해도 코퍼스 파일만 같으면 실행 관문을 통과할 수 있습니다. 현재 검증 결과가 잘못되었다는 주장은 아니며, 변경 감지 관문의 누락입니다.

현재 실제 설정과 `validation.json`을 읽어 `_validated_inputs`가 통과하는 것을 확인한 뒤, 메모리에 읽은 결과의 검증기 해시 두 값을 `changed`로 바꾸었습니다. 독립 계산 근거도 `passed=false`와 불일치 소스 해시로 바꾸었지만 같은 매니페스트가 반환되었습니다. 디스크의 소스와 검증 JSON은 변경하지 않았습니다.

근거: `final-review-repro.log`의 `stale_validation_source`. 검증 근거의 소스 해시를 현재 파일과 대조하고, 독립 계산 통과·근거 수의 일관성도 확인하는 보완이 필요합니다. 현재 실제 파일의 해시가 저장 값과 일치하는 것은 `final-review-corpus.log`에서 별도로 확인하였습니다.

### P2: 컴파일 시간 초과가 단계 통과율의 실패 분모에서 빠집니다

위치: `src/rttdist/hops_reporting.py:144`, `src/rttdist/fps_execution.py:71`.

평가기는 컴파일 제한 초과를 `compile_timeout`으로 기록하고 홉 상태는 이를 기능 실패로 분류합니다. 반면 `_stage_rates`의 판정 가능 상태 목록에는 이 상태가 없어 `unavailable`로 집계합니다. 컴파일 시간 초과가 있는 경로의 단계 통과율이 높아지거나, 평가 실패 한 건뿐인 단계가 결측 통과율로 표시될 수 있습니다.

`_stage_rates([{'route':'cpp-via-python','steps':[{'step':1,'language':'python','kind':'discovery','evaluation_status':'compile_timeout'}]}])`의 실제 결과는 `attempts=1`, `assessable=0`, `unavailable=1`, `passed=0`, `pass_rate=null`입니다. 해당 결과는 제한 내 컴파일 실패로 판정되었으므로 `assessable=1`, `unavailable=0`, `pass_rate=0`이 되어야 합니다. 모의 입력의 경로는 상태 집계 재현용이며 특정 언어에서 실제 컴파일 시간 초과가 발생했다는 뜻은 아닙니다.

근거: `final-review-additional.log`의 `compile_timeout_stage_rates`. 실제 평가기가 생성하는 기능 실패 상태와 보고기의 판정 가능 상태 목록을 맞추는 보완이 필요합니다.

## 회귀검사와 증거 파일

실행 명령은 `uv run --no-sync pytest -q`이며 최신 종료 코드는 0입니다. 최종 결과는 `392 passed, 1102 warnings in 94.88s (0:01:34)`입니다. 최초 검사는 `389 passed, 1102 warnings in 104.96s (0:01:44)`였으며, 이후 공급자 작업자가 추가한 `scripts/integration_commandcode.py`와 `tests/integration/test_commandcode_smoke.py`를 읽고 API를 대체한 모의 테스트 세 개임을 확인한 뒤 전체 검사를 다시 실행하였습니다. 공급자 연동 스크립트 자체의 실제 실행이나 인증 열람은 하지 않았습니다. 경고는 보고 그림 저장 중 발생한 Matplotlib의 부동소수점 x/y 인자 사용중단 경고이며, 테스트 실패와 구분하였습니다. 경고 무시 설정이나 필터를 추가하지 않았습니다.

- 최신 전체 검사 로그: `.test-tmp/v16-orchestration/final-review-pytest-latest.log`
- 최초 전체 검사 로그: `.test-tmp/v16-orchestration/final-review-pytest.log`
- 세 관문 결함의 모의 재현 결과: `.test-tmp/v16-orchestration/final-review-repro.log`
- 확인 제한·파일럿 감사에서 동결까지의 연결 재현: `.test-tmp/v16-orchestration/final-review-chain-repro.log`
- 단계 통과율 재현 및 해시 비교: `.test-tmp/v16-orchestration/final-review-additional.log`
- 실제 코퍼스·검증 근거 대조: `.test-tmp/v16-orchestration/final-review-corpus.log`
- 검사 전 해시: `.test-tmp/v16-orchestration/final-review-before-hashes.json`
- 검사 후 해시: `.test-tmp/v16-orchestration/final-review-after-hashes.json`
- 최신 검사 요약·보고서 존재·최종 해시 확인: `.test-tmp/v16-orchestration/final-review-verification.log`

검사 전후 및 최신 전체 검사 종료 후 `providers.py`, `hops_experiment.py`, `hops_reporting.py`, `configs/v1.6/experiment.yaml`의 SHA-256은 모두 같았습니다. 전체 검사와 모의 재현에서 동결 해시 충돌은 발생하지 않았습니다. 모든 파일의 변경을 실시간 감시한 것은 아니므로, 이 네 파일 외 공급자 작업의 완료 여부까지 추정하지 않습니다. 최초 보조 재현 시 임시 디렉터리 부모 생성 누락으로 검사 보조 코드가 실패하였으며, 부모를 생성한 뒤 종료 코드 0으로 세 결과를 다시 수집하였습니다. 제품 테스트의 실패는 아니었습니다.

`git diff --check`는 종료 코드 0이며 pyproject.toml·uv.lock의 줄바꿈 안내만 있었습니다. 해당 검사는 미추적 파일을 검사하지 않으므로 신규 파일 전체의 서식 검사 통과로 확대하지 않습니다.

## 범위별 확인 결과와 한계

| 범위 | 확인 결과 | 한계 |
| --- | --- | --- |
| 홉과 거리 | `HopsState`와 `_metrics`에서 최초 성공 `reached_step`의 평균 H, 유효 시도 도달률 P, 반올림 전 D=H/P를 확인하였습니다. 상태 수는 보조 분포입니다. | 시간 초과 단계 반영 결함은 위 P1과 같습니다. |
| 최초 비교·탐색·확인 | 짝수 복원 단계의 인접 비교, 2홉 최초 판정, 10홉 판정 후 미도달 동결, 11·12홉 확인 전용 처리를 확인하였습니다. 후속 기능·측정 실패가 도달 결과를 지우지 않는 회귀검사가 통과하였습니다. | 한 번의 추가 확인은 장기 수렴 증명이 아닙니다. |
| 관측·재개 | 단계별 응답·처리 결과·계약 저장, 같은 논리 요청의 저장 응답 재생, 불명확 전송의 재생성 차단, 원응답 수신 후 정규화·장부 처리 장애 복구 검사가 통과하였습니다. | 실제 네트워크 단절·계정 장애를 발생시키지 않았습니다. |
| 중복 과금·공유 예산 | 논리 키와 요청 지문, 요청별 잠금, 장부 잠금과 예약 금액, 샤드 간 논리·전송 상한을 코드에서 확인하였습니다. 프로세스 간 마지막 예산 슬롯 경쟁과 불명확 비용의 예약 보존 검사도 통과하였습니다. | 공급자 실제 청구와 일치하는지는 검증하지 않았습니다. |
| 모델·실효 설정 | 직접 API의 누락·불일치 모델 거부와 명시 별칭, 요청·전송·실효 값 분리, 미보고 값의 결측 유지, SDK의 탐색 실행 분리를 확인하였습니다. | Command Code GLM-5.3·DeepSeek V4 Pro를 포함한 실제 인증·모델 접근·생성 결과는 검증하지 않았습니다. |
| 동결·실험 분리 | 코드·도구·코퍼스·공급자·생성·중단 규칙 해시, 다른 계약의 재개 거부, pilot/main의 별도 경로·요청 키를 확인하였습니다. | 파일럿 완전성 및 검증기 소스 해시 관문은 위 결함과 같습니다. |
| 고정 코퍼스 | 정확한 15문제와 교체 대응, 재귀군 IPOP_11729·IPOP_1992·IPOP_9663 및 반복형 최대공약수 분류를 확인하였습니다. 매니페스트·692개 파일의 현재 해시를 실행기 관문과 대조하였고 C++ 15개 모두 원본과 바이트가 같았습니다. | 별도 언어 기준 구현을 모두 수작업으로 증명한 것은 아닙니다. |
| 기준 구현 검증 | 저장된 결과는 75개 구현·975개 평가 성공, 독립 계산 195개 성공입니다. 현재 준비·검증·독립 계산기 소스 해시도 기록과 같습니다. | 이번 검토에서 975개 평가와 195개 독립 계산을 새로 전부 실행하지 않았습니다. 저장된 실행 근거·해시와 전체 회귀검사를 대조하였습니다. |
| 통계 | 문제 단위 동일 추출 인덱스로 모든 경로·반복을 함께 재표집하며 10,000회, 6쌍×P/H/D의 18비교 Bonferroni 구간을 확인하였습니다. 불완전 자료·SDK는 확증에서 제외하고 민감도는 미보정으로 표시합니다. | 실제 300슬롯 결과와 연구 가설의 지지는 평가하지 않았습니다. |
| 성공 0·재귀군 | 성공 0의 H/D 결측과 재표집 결측 비율, 정의되지 않은 표본이 있을 때 구간 미산출, 재귀군의 기술통계·대조 경로 차이를 확인하였습니다. | 생성된 실제 Haskell 코드의 특성 주석은 아직 미확인 상태이며 인과 효과로 해석할 수 없습니다. |
| 표·그림·재현 CLI | CLI 전체 보고 연결, 원관측 기반 JSON·CSV·그림 입력·근거 매핑·묶음 생성과 외부 호출을 차단한 두 번 재생성 검사가 전체 검사에 포함되어 통과하였습니다. | 그림 렌더링 바이트·PDF 비수치 메타데이터의 동일성은 재현 계약에서 제외됩니다. 단계별 통신 수 미보고는 결측이며 전체 비용은 함께 보관한 공급자 원장과 별도 대조해야 합니다. |
| 문헌·과거 결과 | v1.5와 v1.6의 코퍼스·중단 규칙 차이, 원자료 없는 과거 수치를 검증 완료로 표시하지 않는 안내를 확인하였습니다. | 참고문헌 원문·판본·인용 대응을 새로 전부 대조하거나 과거 실험을 재검증하지 않았습니다. |

## 후속 검증

1. 시간 제한을 공급자 응답 후·평가 후·최종 단계와 확인 전용 구간에서 넘기는 회귀검사를 추가해 주셔야 합니다.
2. 12개가 모두 무효인 파일럿과 검증기 소스 해시 변경을 동결·재개 관문이 거부하는지 확인해 주셔야 합니다.
3. 컴파일 시간 초과가 단계 통과율의 기능 실패 분모에 포함되는지 확인해 주셔야 합니다.
4. 수정 후 관련 회귀검사와 전체 검사를 다시 실행하셔야 합니다. 계정별 실제 연결·파일럿·본 실험은 별도 실행이며 이번 검토의 통과 항목에 포함하지 않았습니다.

git add·commit, 새 worktree, 하위 작업자 생성, 실제 API 호출, 키 열람은 수행하지 않았습니다. 결과물은 이 보고서와 검토 증거 로그·해시 파일이며, 구현 수정은 수행하지 않았습니다.
