# v1.6 상태·실행기 연결 계약

이 파일은 담당 작업자 사이의 연결 기준입니다. 값은 일반 딕셔너리로 주고받습니다.

## 설정

- `manuscript_version: v1.6`, `experiment_version: rtt-hops-v1.6`, `schema_version: observation-v1.6`
- `selection`: 설정 파일 기준 절대 경로로 해석한 `papers/v1.6/data/selection.json`
- `corpus_root`: 설정 파일 기준 절대 경로로 해석한 `data/rtt-v1.6`
- `validation`: `../../artifacts-rtt-v1.6/validation/validation.json`을 설정 기준으로 해석합니다. 해시 순환을 막기 위해 코퍼스 외부에 둡니다.
- `output_root`, `campaign_id`, `profile_id`: 저장 위치는 `output_root/campaign_id/{pilot,main}`입니다.
- `problem_ids`: 설계의 15개 ID, `pilot_problem_ids`: IPOP_11729·IPOP_1992·LC_0053
- `routes`: `[[cpp, python], [cpp, java], [cpp, haskell], [cpp, prolog]]`
- `repeats: 5`, `pilot_repeats: 1`, `threshold: 0.85`, `thresholds: [0.8, 0.85, 0.9]`
- `max_hops: 10`, `confirmation_roundtrips: 1`, `schedule_seed: 20261117`
- `observation_wall_seconds: 900`, `confirmation_wall_seconds: 300`
- `runtime`: `tools` 언어별 실행 도구, `fixture_timeout: 5`, `compile_timeout: 180`, `minimum_evaluation_cases: 13`
- 이 실행 환경의 `runtime.tools`는 코퍼스 담당자의 `corpus-validation-config.json`과 동일한 실제 도구 절대 경로를 사용합니다. 공통 생성기와 테스트에는 사용자 머신 경로를 넣지 않습니다. Java와 JPlag jar 해시도 공통 설정에 동결합니다.
- `similarity`: `java`, `jar`, `jar_sha256`, `minimum_tokens: 9`, `normalize: false`, `similarity_field: averageSimilarity`; 기존 `measure(..., config=cfg['similarity'])`를 사용합니다.
- `llm`: 공급자 설정 딕셔너리입니다. `load_hops_config(path, provider_path)`는 별도 파일의 `llm` 또는 최상위 공급자 설정을 이 키에 합성합니다. 별도 파일이 공통 실험 조건을 변경할 수 없습니다. 공식 `github-copilot-sdk==0.1.32` 선택 의존성을 잠갔으며 Python 3.15.1에서 가져오기를 검증했습니다.
- `llm` 키: `provider`, `protocol`, `model`, `allowed_response_models`, `generation`, `generation_profile`, 인증 환경변수 이름, 주소, 예산 등입니다. `create_provider(cfg['llm'], ledger=<campaign 공유 경로>)`로 연결합니다.
- SDK는 명시적인 `generation: {}`와 유효한 SDK 프로파일을 허용하며 공통 생성 기본값을 채우지 않습니다. SDK 설정에서 generation 키 누락·잘못된 자료형은 거부하고 직접 API의 빈 생성 설정도 동결을 거부합니다. SDK는 모델 ID 보고 여부와 무관하게 `sdk_exploratory`, `confirmatory: false`로 분류합니다.
- 명시적으로 전달한 `provider_path`는 명령 실행 위치 기준이며, 설정 안의 `provider_config` 참조는 공통 설정 파일 기준입니다. 공통 설정의 자료·출력·jar 경로는 설정 파일 기준입니다.
- 실제 공급자 팩터리에는 공통 `budget`을 `max_calls`, `max_transport_attempts`, `cost_cap_usd`로 합성합니다. 같은 phase의 모든 샤드는 `output_root/campaign_id/phase/provider_ledger.jsonl`을 공유합니다.
- `budget`: `max_logical_requests`, `max_transport_attempts`, 선택 `cost_cap_usd`; 공급자에 `max_calls`, `cost_cap_usd`를 전달합니다. 통신 재시도는 최대 2회입니다.

## 관측과 단계

- 작업 키 `job`: `problem_id`, `route: cpp-via-python` 등, `seed_language: cpp`, `target_language`, `repeat`(1부터), `phase`, `campaign_id`
- 관측 키: 위 작업 키와 `schema_version`, `protocol`, `profile_id`, `contract_hash`, `attempt`(repeat 호환), `primary_threshold: '0.85'`, `outcomes`, `terminal_status`, `reason`, `confirmation_status`, `translation_steps`, `steps`, `states`, `complete_by_threshold`, `comparison_class`
- `outcomes['0.80'|'0.85'|'0.90']`: `success`, `category`(success/functional_failure/hop_limit/invalid/incomplete), `reached_step`, `reached_roundtrip`, `unique_state_count_at_reach`, `sym_adj`, `sym_origin`, `reason`
- 성공은 `reached_step` 2·4·6·8·10으로 집계합니다. `complete_by_threshold`는 관측별 유효 여부(`category`가 success/functional_failure/hop_limit)를 담으며 캠페인 완전성은 보고기가 계획 슬롯과 대조합니다.
- `terminal_status`: collection_complete/hop_limit/functional_failure/infrastructure_error, `confirmation_status`: passed/failed/unavailable 또는 주 성공 전 null
- `steps`: `step`, `kind`(discovery/confirmation), `language`, `direction`, `source_sha256`, `source_path`, `evaluation_status`, `evaluation`, `sym_adj`, `sym_origin`, `sym_status`, `call_id`, `request_id`, `requested_generation`, `sent_generation`, `effective_generation`, `actual_model`, `model_evidence`, `usage`, `cost_usd`, `response_path`, `thresholds_reached`
- `call_id`는 campaign/phase/problem/route/repeat/step을 모두 포함합니다. 동일 폴더와 요청 ID를 재개·재시도에 재사용합니다.
- 공급자 payload에는 `logical_request: {campaign, phase, problem, route, repeat, step}`을 넣습니다. 공급자 프로토콜이 허용하지 않는 `call_id`는 요청에 넣지 않고 관측 단계에 보관합니다.
- 공급자 정규화 결과의 `text`를 사용합니다. 응답을 실행기 `provider_result.json`에 먼저 보존한 뒤 추출·평가하며, 재개 시 이를 우선 읽습니다. 공급자 자체 원문 캐시와 장부의 복구는 공급자 담당 범위입니다.
- `requested_generation`, `sent_generation`, `effective_generation`은 공급자 반환값 그대로 보존하고, 알 수 없는 값은 null과 결측 사유를 저장합니다.
- 관측별 `audit_observation(record, contract)`는 `passed`, `errors`를 반환합니다.

## 동결 연결

- `python -m rttdist hops`는 `src/rttdist/__main__.py`에서 공통 CLI로 연결합니다. 해당 파일 추가는 조정자의 후속 지시로 담당 범위에 포함되었습니다.

- `build_run_contract(cfg, manifest, environment)`는 정규화 설정·자료 해시·구현 및 집계기 해시·도구 환경·공급자 및 정지 규칙을 묶고 `contract_hash`를 반환합니다.
- 보고기 호환용 최상위 `problem_ids`, `routes`, `repeats`, `thresholds`, `primary_threshold`, `schema`도 저장합니다. 파일럿 보고에서만 보고용 문제 목록과 반복 수를 제한합니다.
- 코퍼스 검증에서 `passed`, `file_hashes`, `runtime`, `reference_count: 75`, `evaluation_count: 975`를 사용합니다. 문제별 검증 세부 목록도 보존하실 수 있습니다.
- 실제 코퍼스의 validation.file_hashes에는 `manifest.json` 자체 해시가 추가되고 manifest.file_hashes에는 자기 해시가 없습니다. 실행기는 이 차이를 명시적으로 조합하여 전체 파일 집합·해시와 비교합니다. 검증 당시 `tool_versions`의 표준 출력·오류와 현재 실제 도구 버전도 대조합니다.
- `freeze_main_design(cfg, pilot_audit, validation, provider_preflight)`는 `pilot_audit.passed`, `pilot_audit.observation_count: 12`, 검증 해시·생성 프로파일·예산과 정적 공급자 점검을 요구합니다. 실제 직접 API 본 실행은 별도 실접속 모델 확인도 필요합니다.
- `provider_preflight`: `passed`, `live`(실제 여부), `model_evidence`(dict 또는 문자열), `actual_model`, `comparison_class`(direct_api/sdk_exploratory), `generation_profile`, 선택 `environment`를 사용합니다. 정적 통과만으로 실접속 검증을 주장하지 않습니다.
- 정적 점검만으로 main_design.json을 승인하지 않습니다. 이번 작업의 동결·실행 검증에서는 실제 모델 호출 없이 명시적 모의 사전 점검을 사용했습니다.
- 보고기는 `summarize_hops(records, manifest, contract)`로 연결합니다. CLI report는 저장 계약과 선택 매니페스트를 읽고 이 함수를 호출하여 `summary.json`을 저장한 뒤 `scripts.report_v16.write_v16_report(summary, phase_root / 'report')`로 관측 CSV·표·그림·근거·재현 묶음을 함께 생성합니다.

## 상태 전이

`HopsState(origin, thresholds, primary_threshold, max_hops, confirmation_roundtrips)`의 origin은 C++ 소스 문자열 또는 `{language, source}`입니다. `record_step(language, source, functional_status, similarity=None, similarity_status=None)`의 similarity는 수치 또는 `{sym_adj, sym_origin}`입니다. `outcomes()`, `next_step_kind()`와 인프라 중단용 `abort(reason)`를 제공합니다.
