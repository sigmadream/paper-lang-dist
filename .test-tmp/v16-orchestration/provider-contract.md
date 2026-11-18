# v1.6 공급자 연결 계약

- 기존 `create_provider(config, ledger=None)`, `complete(payload, folder)`, `CompatibleProvider`와 레거시 `body`를 유지합니다.
- `protocol` 또는 `base_url`을 명시한 설정은 v1.6 경로입니다. `provider`는 `openai/zai/zai_coding/opencode/opencode_go/compatible/openai_compatible/lmstudio/copilot`, `protocol`은 `chat_completions/responses/copilot_sdk`입니다.
- 설정 키는 `base_url`, `request_path`, `auth: {type: bearer, api_key_env: ENV_NAME}`, `model`, `allowed_response_models`, `generation`, `generation_profile`입니다. 모델 ID는 사용자가 지정해야 합니다.
- `generation_profile`은 `name`, `supported_options`, `output_limit_field`, 선택 `option_values`를 담습니다. 공통 `max_tokens`는 프로토콜의 출력 상한 필드로 변환합니다. 미지원 옵션은 거부합니다.
- payload는 `model/messages` 또는 `model/input/instructions`를 받습니다. generation은 설정과 payload를 합성하고 payload의 값이 우선합니다. `logical_request` 메타데이터는 네트워크에 보내지 않습니다.
- core는 payload에 `logical_request: {campaign, phase, problem, route, repeat, step}`을 넣으시면 됩니다. 전체 키를 제공하면 샤드·폴더 간 같은 논리 요청을 하나로 처리하며 변경된 계약을 거부합니다. 생략하면 절대 폴더 경로의 해시를 사용합니다.
- 반환 필수 키는 `text`, `finish_reason`, `requested_model`, `actual_model`, `model_evidence`, `usage`, `usage_raw`, `cost_usd`, `cost_source`, `request_id`, `requested_generation`, `sent_generation`, `effective_generation`, `raw_response_path`, `protocol`, `provider`입니다. `body`, `latency_seconds`, `received_at`, `applied_generation`도 보존합니다.
- `model_evidence.status`는 `exact/alias/missing/mismatch`, `valid`는 확인 성공 여부입니다. 직접 API에서 missing/mismatch는 `ProviderError`를 발생시키되 원문과 정규화 응답은 보관합니다. Copilot missing은 `execution_class=sdk_exploratory`로 허용합니다.
- 버전 차이를 명시합니다. 기존 FPS의 `model_matches(actual, expected)`는 과거 부분문자열 판정을 그대로 유지합니다. `version='v1.6'` 또는 명시적 별칭 인수를 사용하면 엄격 판정이며, v1.6 공급자는 독립적인 `model_evidence` 엄격 판정을 항상 적용하므로 과거 호환 모드로 우회되지 않습니다.
- `usage`는 `prompt_tokens/completion_tokens/total_tokens`로 정규화하고 원본은 `usage_raw`에 보관합니다. 미확인 비용·실효 설정은 null입니다.
- v1.6 `retries`는 0~2, 기본 2입니다. 응답 수신 여부 불명은 `UnknownRequestState(ProviderError)`이며 재호출을 차단합니다.
- 예산 키는 `max_calls`, `max_transport_attempts`, `cost_cap_usd`, `max_request_cost_usd`, `pricing`, 선택 `max_input_tokens`입니다. 달러 상한은 최대 요청비 추정 또는 명시한 최대 요청비가 필요합니다. 공용 ledger를 모든 샤드에 동일하게 전달해야 합니다.
- `max_calls` 또는 추정 가능한 달러 상한이 없는 v1.6 설정은 거부합니다. `max_input_tokens`를 사용하면 전송 텍스트의 UTF-8 바이트 수와 메시지별 여유분으로 보수적으로 검사하므로 실제 토큰 수보다 일찍 거부할 수 있습니다.
- 5xx/408 응답의 과금 여부는 단정하지 않으며 후속 재시도에 추가 예약을 요구합니다. 비용 미상 응답과 불명 과금 예약은 확인 전까지 해제하지 않습니다. SDK의 premium 요청 단위 비용을 달러로 오해하지 않으며 확인하지 못한 내부 모델 호출 수는 null입니다.
- 공급자 메서드 `reserve_request_budget(call_id, estimate)`, `record_transport_attempt(call_id, attempt_id, metadata)`, `finalize_request(call_id, response)`는 공용 장부를 잠가 갱신합니다. 원장 옆 상태 파일에 예약·전송을, 원장 JSONL에 완료 과금을 기록합니다.
- 원문 수신 후 정규화 실패·모델 불일치·출력 형식 실패는 새 생성을 하지 않습니다. 정상 text의 코드 추출과 기능 판정은 core가 담당합니다.
- SDK 선택 의존성은 공식 `github-copilot-sdk==0.1.32`입니다. core 담당자께서 pyproject.toml 선택 의존성과 uv.lock에 반영해 주셔야 합니다.
- 정적 preflight는 인증값·계정을 탐색하거나 네트워크를 호출하지 않습니다. 라이브 smoke는 명시적 `--live`로만 가능하며 별도 smoke 경로·장부를 사용합니다. 이번 구현에서는 라이브 호출을 하지 않습니다.
