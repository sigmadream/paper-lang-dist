# 코퍼스 공유 계약

인터페이스는 scripts.prepare_v16_corpus.prepare_corpus(selection_path, source_root, destination)와 scripts.validate_v16_corpus.validate_corpus(cfg)입니다.

- selection 최상위 키: schema_version(1), corpus_version(rtt-v1.6), languages([cpp, python, java, haskell, prolog]), replacements(이전 ID:새 ID), pilot_problem_ids, problems
- problems 항목 키: problem_id, display_name, group(recursive/comparison), recursive(bool), recursion_kind, mutable_state, backtracking, output_scale, evaluation_cases(13), provenance
- 준비 결과: destination/selection.json, destination/manifest.json, destination/<problem_id>/{statement.md,reference.cpp,reference.py,reference.java,reference.hs,reference.pl,prompt_examples/*,evaluation/*}
- manifest 키: schema_version, corpus_version, selection_sha256, reference_languages, problem_ids, problems, file_hashes
- manifest.problems 항목: problem_id, source, reference_provenance, evaluation_cases, prompt_example_cases
- cfg 필수 키: corpus_root, problem_ids, runtime, validation. runtime.tools는 다섯 언어 도구의 실행 경로이며 fixture_timeout=5, compile_timeout=180을 그대로 사용합니다.
- validation 결과 키: schema_version, corpus_version, created_at, runtime, tool_versions, reference_languages, problem_ids, expected_references(75), expected_cases(975), executed_cases, passed_cases, results, file_hashes, independent_checks, errors, passed
- results 항목 키: problem_id, language, status, case_count, expected_cases(13), passed_cases, evaluation_path, error(실패 시)
- 도구·구현·입출력 누락도 실패 항목으로 남기며 passed=true는 75개 구현과 975개 실행 성공 및 독립 검증 성공을 모두 요구합니다.
- validation 경로는 artifacts-rtt-v1.6/validation/validation.json을 권장하며 평가 근거는 같은 디렉터리의 references/<problem_id>/<language>/evaluation.json에 보존합니다.
- 반환값: prepare_corpus는 manifest 사전, validate_corpus는 validation 사전입니다. CLI는 실패 시 비영 종료합니다.

core-contract.md가 생성되면 이 문서와 연결하고 cfg 키를 점검하겠습니다.

## core 계약 연결

[core 계약](core-contract.md)의 cfg 키와 연결하였습니다. 동결 연결에서 사용하는 reference_count는 성공한 기준 구현 수, evaluation_count는 성공한 개별 평가 수이며 각각 75·975를 요구합니다. 예상 수는 expected_references·expected_cases, 실제 실행 수는 executed_cases로 따로 보존합니다. 검증 결과를 코퍼스에 쓰면 해시가 순환하므로 validation은 artifacts-rtt-v1.6/validation/validation.json에 저장해야 합니다. 파일럿은 core 계약의 IPOP_11729·IPOP_1992·LC_0053 목록을 사용합니다.

문제 항목에는 metadata_basis(cpp_reference)와 implementation_note도 포함합니다. provenance에는 independent_validation(기존 이중 계산기 경로)과 legacy_reference_source(재사용 출처, 해당 없으면 null)를 추가하였습니다. 재귀군 분류와 가변 상태 표시는 C++ 원본 기준이며, Haskell·Prolog의 꼬리 재귀 표현 때문에 문제군을 변경하지 않습니다.

validation에는 validator_source_hashes(prepare·validate 스크립트의 sha256)를 추가하여 검증 구현도 추적합니다. 2026-11-17 실제 검증에서 동결 코퍼스 내부 data/rtt-v1.6/validation.json은 생성되지 않았습니다.

core의 최종 _validated_inputs와 연결하여 validation.file_hashes에는 manifest.file_hashes의 내용 파일과 manifest.json 자체의 해시까지 모두 포함합니다. manifest.json 안의 file_hashes는 자기 자신을 제외하므로 순환하지 않으며, manifest_sha256에도 동일한 매니페스트 해시를 별도로 보존합니다.

