# v1.6 공급자 구현 보고

T04·T05·T07의 공급자·프로토콜·장부·복구·사전 점검 구현을 완료했습니다. 공통 반환·설정 계약은 같은 폴더의 `provider-contract.md`에 먼저 기록했으며 core 계약의 논리 요청 키와 연결했습니다. git add·commit, 새 worktree, 하위 작업자 생성은 수행하지 않았습니다.

## 변경 파일

- `src/rttdist/providers.py`
- `src/rttdist/provider_protocols.py`
- `src/rttdist/copilot_provider.py`
- `configs/v1.6/providers/openai.yaml`
- `configs/v1.6/providers/zai.yaml`
- `configs/v1.6/providers/zai_coding.yaml`
- `configs/v1.6/providers/opencode.yaml`
- `configs/v1.6/providers/opencode_go.yaml`
- `configs/v1.6/providers/copilot.yaml`
- `configs/v1.6/providers/compatible.yaml`
- `scripts/preflight_v16.py`
- `scripts/make_model_config.py`
- `.env.example`
- `tests/unit/test_provider_protocols.py`
- `tests/unit/test_provider_ledger.py`
- `tests/unit/test_v16_model_config.py`
- `tests/integration/test_provider_recovery.py`
- `tests/integration/test_v16_providers.py`

기존 `tests/unit/test_fps_providers.py`는 최종적으로 원래 내용을 유지했습니다. `pyproject.toml`과 `uv.lock`은 core 담당자가 수정했으며 제 수정 범위에 포함하지 않았습니다.

## 구현 결과

Chat Completions와 Responses의 입력·출력 상한·reasoning·응답 텍스트·사용량을 독립 모듈에서 매핑합니다. 미지원 생성 옵션과 요청 옵션은 거부하며 요청값·전송값·서버 확인 실효값을 분리합니다. 실효값은 미보고 시 null입니다. 새 정규화 결과는 요구된 16개 공통 키와 레거시 `body`를 제공합니다.

v1.6 모델 검증은 정확한 대소문자 포함 ID 또는 명시한 별칭만 허용합니다. 직접 API의 모델 ID 누락·불일치는 원문·응답·과금을 보존한 뒤 오류로 처리합니다. 빈 출력·잘림·복수 코드 블록은 다시 생성하지 않고 core의 형식 판정에 전달합니다.

논리 요청·전송 시도·완료 과금을 분리합니다. 운영체제 파일 잠금과 원자적 기록으로 샤드 사이의 호출·전송·달러 예산을 공유하며 응답 원문을 정규화 전에 저장합니다. 같은 논리 키가 다른 폴더에서 재개되어도 원래 응답을 재생합니다. 429·지정 5xx와 명확한 전송 전 연결 실패는 최대 2회 재시도하며 Retry-After를 적용합니다. 불명 시간 초과와 전송 중 충돌은 자동 재생성을 차단합니다.

비용 미상은 null이며 호출 상한으로 집계합니다. 달러 상한에는 명시한 요청별 최대 비용 또는 단가·최대 입출력 토큰 추정이 필요합니다. 불명 과금·비용 미상 예약은 해제하지 않으며 5xx/408 후 재시도에는 추가 비용 예약을 적용합니다. 서버 보고 비용, 공급자의 추정 비용, 로컬 단가 추정 비용을 구분합니다. 명시한 인증 환경 변수 값과 인증 필드는 요청·원문·응답·장부에서 마스킹하며 HTTP·SDK 예외 본문은 저장하지 않습니다.

공식 Copilot SDK는 새 세션·새 빈 작업 폴더·분리된 설정과 홈·빈 도구 및 MCP 목록·권한 거부·시스템 지침 교체를 적용합니다. 명시한 토큰만 SDK에 전달하며 사용자 로그인 저장소를 탐색하지 않습니다. SDK/CLI 버전과 모델 접근 기능을 실제 요청 시 확인하고, 실제 ID 미보고·내부 컨텍스트·내부 호출 수 미확인은 항상 `sdk_exploratory`로 구분합니다. SDK의 과금 승수를 달러로 변환하거나 SDK 턴 수를 모델 호출 수로 대입하지 않습니다.

## 검증

의미 있는 실패를 먼저 확인한 뒤 구현했습니다. 최초 프로토콜·장부·복구 묶음에서 미구현·잘못된 모델 일치 등 14개 실패를 확인했고 구현 후 통과했습니다. 이후 보수적 비용 예약, 입력 상한, 확장 공급자 등록, 사전 점검 경로 해석의 실패도 각각 확인하고 수정했습니다.

`uv run pytest tests/unit/test_provider_protocols.py tests/unit/test_provider_ledger.py tests/unit/test_v16_model_config.py tests/integration/test_provider_recovery.py tests/integration/test_v16_providers.py tests/unit/test_fps_providers.py tests/integration/test_provider_factory.py tests/integration/test_fps_experiment.py tests/integration/test_v16_freeze.py -q`는 75개 통과했습니다. 이 명령에는 별도 프로세스 예산 예약, 충돌 복구, 최대 재시도, SDK 생성·실패·모델 불일치·재개와 기존 FPS 회귀가 포함됩니다.

core 담당자가 SDK 연결 수정 중인 마지막 재실행에서는 위 묶음 중 `test_mock_campaign_freeze_resume_and_shared_ledger`의 소스 해시 기반 계약 비교가 실패하여 74개 통과·1개 실패였습니다. 제 소유 범위와 기존 FPS 회귀만 다시 실행한 최종 명령 `uv run pytest tests/unit/test_provider_protocols.py tests/unit/test_provider_ledger.py tests/unit/test_v16_model_config.py tests/integration/test_provider_recovery.py tests/integration/test_v16_providers.py tests/unit/test_fps_providers.py tests/integration/test_provider_factory.py tests/integration/test_fps_experiment.py -q`는 63개 전부 통과했습니다. 변경 중 파일 해시를 동결하는 테스트의 최종 확인은 core 변경이 멈춘 뒤 필요합니다.

`uv run black --check src/rttdist/providers.py src/rttdist/provider_protocols.py src/rttdist/copilot_provider.py scripts/preflight_v16.py scripts/make_model_config.py tests/unit/test_provider_protocols.py tests/unit/test_provider_ledger.py tests/unit/test_v16_model_config.py tests/integration/test_provider_recovery.py tests/integration/test_v16_providers.py`는 10개 파일 모두 통과했습니다. 변경 범위의 `git diff --check`도 통과했습니다.

`uv run python scripts/preflight_v16.py --config configs/v1.6/experiment.yaml --provider-config configs/v1.6/providers/openai.yaml`은 네트워크 없이 `passed=false`, `live=false`, 모델 ID 지정 필요를 출력하며 종료 코드 1을 반환했습니다. 예제에 사용자 모델을 지정한 정적 점검과 모의 live smoke의 별도 장부 검증은 테스트에서 통과했습니다.

최종 `uv run pytest -q`는 `provider-full-suite.txt`에 저장했으며 373개 통과·1개 실패·902개 Matplotlib 경고였습니다. 실패한 테스트는 `tests/integration/test_v16_report.py::test_core_observation_reports_and_reproduces_without_api`로, 보고 묶음의 원본 유사도 CSV 포함 여부 검증이었습니다. 해당 파일은 제 소유가 아니며 공유 파일의 후속 구현이 반영된 뒤 같은 테스트만 재실행하여 1개 통과·300개 Matplotlib 경고를 확인했습니다. 앞선 전체 검사에는 기존 자료 인덱스 누락 2건과 공유 소스 변경 중 계약 해시 충돌 1건도 있었으나 마지막 전체 검사에서는 발생하지 않았습니다. 전체 검사의 무실패 완료를 주장하지 않으며 모든 담당자 변경이 정지한 뒤 조정자의 최종 전체 검사가 필요합니다.

`uv run python scripts/make_model_config.py --base configs/v1.6/experiment.yaml --provider-config configs/v1.6/providers/openai.yaml --model offline-test --model-id offline-test --output .test-tmp/v16-orchestration/generated-offline-model.yaml`도 종료 코드 0으로 오프라인 설정을 생성했습니다. 이 파일은 실제 모델 접근을 검증한 설정이 아닙니다.

## 설계 조정과 남은 연결 사항

기존 FPS 테스트와 판정을 보존하기 위해 `model_matches(actual, expected)`의 기본 모드는 과거 FPS 호환입니다. `version='v1.6'` 또는 명시적 별칭을 주면 엄격 판정이며, 새 공급자는 독립적인 엄격 `model_evidence` 판정을 항상 적용합니다. 새 실행에서 과거 부분문자열 일치가 사용되지는 않습니다.

Copilot SDK는 공식 `github-copilot-sdk==0.1.32` API를 기준으로 고정했습니다. core 담당자가 선택 의존성에 해당 버전을 반영한 것을 확인했습니다. SDK의 단일 턴 인터페이스에는 공통 temperature·top_p·seed·출력 상한을 그대로 지정할 수 없으므로 `generation: {}`인 별도 탐색 프로파일을 제공했습니다. core의 본 실험 동결 관문에서 비어 있는 SDK 생성 프로파일을 허용하려면 `copilot_sdk`일 때 별도 분기가 필요합니다. 직접 API에서는 빈 프로파일을 허용할 이유가 없습니다. 이 연결 사항은 조정자에게 보고했고, 조정자가 core 담당자에게 별도 SDK 분기와 호출 연결 테스트를 지시했음을 확인했습니다.

SDK의 내부 모델 호출 수·추가 지침·실효 설정과 모든 공급자의 실제 인증·계정별 모델 접근은 미검증입니다. 실제 API·SDK 생성, 유료 호출, 파일럿·본 실험은 수행하지 않았습니다. 예제의 `model: null`을 사용자 ID로 지정하고 모델별 지원 옵션·가격을 별도 동결한 뒤 명시적인 live 점검이 필요합니다.

참고한 공식 주소는 [OpenCode API](https://opencode.ai/docs/console/api/inference/), [OpenCode 세션과 주소](https://opencode.ai/docs/console/harnesses), [Z.AI API](https://docs.z.ai/api-reference/introduction), [OpenAI Responses](https://developers.openai.com/api/docs/guides/migrate-to-responses), [고정 Copilot SDK 소스](https://github.com/github/copilot-sdk/tree/v0.1.32/python)입니다. 종료된 GitHub Models 주소를 Copilot API로 사용하지 않았습니다.
