# RTT Experiment Methodology Upgrade

## TL;DR
> **Summary**: Upgrade the existing RTT experiment tool so each run chooses one seed language, executes ordered directional pairs without collapsing `A->B` and `B->A`, tracks convergence in both language states, and persists offline-reproducible final embedding similarity plus richer aggregate statistics.
> **Deliverables**:
> - Seed-language-aware config, corpus validation, artifact layout, and prompt/client contracts
> - Dual-state convergence and resume-safe metadata persistence
> - OpenAI-backed embedding similarity behind a provider abstraction, persisted as a final artifact
> - `report_summary.v2` with per-result entries plus ordered-pair aggregates for mean/stddev/divergence rate
> - Pytest unit/integration/e2e regression coverage for non-`cpp` seeds, ordered-pair runs, offline report regeneration, and schema compatibility
> **Effort**: Large
> **Parallel**: YES - 2 waves
> **Critical Path**: Task 1 -> Task 3 -> Task 6 -> Task 7 -> Task 8 -> Task 9

## Context
### Original Request
- Improve the experiment process by adding: configurable seed language, bidirectional `A->B` / `B->A` aggregation, embedding-based final similarity, fixed-point detection expanded to both language states, mean/stddev/divergence-rate reporting, and persisted experiment metadata (`seed`, `prompt version`, `model revision`).

### Interview Summary
- One run uses exactly one `seed_language`; mixed-seed execution inside the same `run_id` is out of scope.
- Embedding similarity uses a provider abstraction with OpenAI embeddings as the MVP backend.
- Test strategy is `tests-after`, using the existing pytest unit/integration/e2e structure.
- Preserve existing CLI verbs (`validate-corpus`, `run`, `resume`, `report`) and keep reverse directions distinct instead of merging them.

### Metis Review (gaps addressed)
- Ordered-pair identity is explicit and path-safe: the plan standardizes on `(seed_language, target_language)` plus an `ordered_pair_key` and forbids `seed_language == target_language`.
- Non-`cpp` seeds use an explicit corpus contract: `corpus/solutions/<problem_id>/reference.<ext>` selected by `seed_language`; validation fails fast when the required file is absent.
- Dual-state convergence has a concrete truth table: overall `fixed_point` only when both seed-state and target-state histories are fixed, overall `oscillation` when either state oscillates before both are fixed, otherwise `continue` until max-iteration termination.
- Legacy token `residual_similarity` keeps its current meaning and remains measurable only for `seed_language == "cpp"`; all other seeds report it as `unavailable` with an explicit reason while the new embedding-based `final_similarity` becomes the cross-seed metric.
- Final embedding similarity is persisted during `run`/`resume`; `report` consumes saved artifacts only and must never trigger new network calls.
- Schema versioning is mandatory for both run manifests and summaries; new writes are `run_manifest.v2` and `report_summary.v2`, while report generation keeps an explicit legacy-read path for existing v1 artifacts.

## Work Objectives
### Core Objective
- Make the RTT experiment runner direction-aware and seed-language-aware without sacrificing resumability, offline report regeneration, or current CLI ergonomics.

### Deliverables
- Updated config/corpus contract for `seed_language` across `cpp`, `c`, `java`, and `python`.
- Ordered-pair-aware artifact tree and manifest contract.
- Generic translation prompt/client interface for `seed_language -> target_language -> seed_language`.
- Dual-state convergence metrics and persisted histories for both seed-side and target-side states.
- Embedding provider abstraction with OpenAI MVP and persisted `final-similarity.json` evidence.
- Summary/report v2 outputs containing per-result entries and ordered-pair aggregates with mean/stddev/divergence-rate fields.
- Regression coverage for config validation, resume compatibility, report offline behavior, and directional smoke flows.

### Definition of Done (verifiable conditions with commands)
- `python -m pytest tests/unit -q` exits `0`.
- `python -m pytest tests/integration -q` exits `0`.
- `RTTDIST_OPENAI_MOCK_RESPONSES=tests/fixtures/e2e/smoke_openai_responses.json python -m pytest tests/e2e/test_smoke_experiment.py -q` exits `0`.
- `python -m rttdist.cli validate-corpus --config tests/fixtures/config/minimal.yaml` exits `0`.
- `python -m rttdist.cli run --config tests/fixtures/config/minimal.yaml --run-id smoke-upgrade` exits `0` and writes schema-v2 artifacts under the ordered-pair directory layout.
- `python -m rttdist.cli report --config tests/fixtures/config/minimal.yaml --run-id smoke-upgrade` exits `0` without network access and emits `summary.json` and `summary.md` containing ordered-pair aggregates and final similarity provenance.

### Must Have
- `seed_language` is an explicit config field and must be one of `cpp`, `c`, `java`, `python`.
- `seed_language == target_language` is invalid configuration and fails in validation before execution.
- Corpus seed selection uses `reference.cpp`, `reference.c`, `reference.java`, or `reference.py` according to `seed_language`; missing files fail with exact path diagnostics.
- Artifact identity includes `seed_language`, `target_language`, and an `ordered_pair_key`; `A->B` and `B->A` never share directories or aggregate buckets.
- Dual-state convergence stores separate histories for seed-language roundtrips and target-language translations.
- Overall convergence is `fixed_point` only when both histories stabilize, `oscillation` when either history oscillates before both stabilize, otherwise `continue` or `max_iter_no_convergence`.
- Final embedding similarity is cosine similarity between the original seed source and final seed-language roundtrip source, computed once per completed run and persisted with provider/model/dimension/request-id evidence.
- OpenAI embedding evidence stores the configured model alias, observed response `model`, embedding `dimensions`, token usage, request id, and source hashes; the plan treats this as revision evidence because OpenAI does not expose a true internal revision id.
- `residual_similarity` remains the existing normalized C++ token metric and is reported as unavailable for non-`cpp` seeds with reason `seed_language_not_cpp`.
- Aggregates compute population mean/stddev across measured numeric values only; `stddev` is `0.0` when exactly one measured value exists.
- `divergence_rate` is the fraction of successful measured directional runs whose overall convergence outcome is not `fixed_point`; infrastructure failures are excluded from the denominator and reported separately as unavailable/infrastructure counts.
- `report` never performs embedding or translation network calls; it only reads persisted artifacts.

### Must NOT Have (guardrails, AI slop patterns, scope boundaries)
- Must NOT support mixed-seed execution inside one `run_id`.
- Must NOT collapse `A->B` and `B->A` into one aggregate row.
- Must NOT change the semantic meaning of existing `residual_similarity` in place.
- Must NOT let `report` recompute embeddings or call remote services.
- Must NOT add non-OpenAI embedding backends in this change beyond the abstraction seam.
- Must NOT require new benchmark problems or broad corpus expansion outside test fixtures.
- Must NOT silently reinterpret old manifests/summaries without an explicit legacy-read path.

## Verification Strategy
> ZERO HUMAN INTERVENTION - all verification is agent-executed.
- Test decision: `tests-after` with existing `pytest` unit/integration/e2e suites.
- QA policy: Every task includes executable happy-path and failure-path scenarios.
- Evidence: `.sisyphus/evidence/task-{N}-{slug}.{ext}`.

## Execution Strategy
### Parallel Execution Waves
> Target: 5 tasks per wave. Foundation contracts land first; pipeline/reporting consume them second.

Wave 1: Tasks 1-5 - config/corpus identity, ordered-pair artifact contract, generic prompt/client API, convergence rules, embedding abstraction contract.

Wave 2: Tasks 6-10 - pipeline/resume persistence, final similarity artifacting, reporting v2 aggregates, smoke/integration regression expansion, docs/fixture refresh.

### Dependency Matrix (full, all tasks)
| Task | Depends On | Notes |
| --- | --- | --- |
| 1 | - | Defines new run identity and non-`cpp` seed contract |
| 2 | 1 | Validation and CLI error paths rely on contract |
| 3 | 1 | Artifact layout and manifest versioning depend on ordered-pair identity |
| 4 | 1, 2 | Prompt/client generalization depends on explicit languages |
| 5 | 1, 3, 4 | Dual-state semantics consume artifact and direction contracts |
| 6 | 2, 3, 4, 5 | Pipeline/resume work needs all core contracts |
| 7 | 4, 6 | Final similarity artifact depends on generic clients and pipeline terminal state |
| 8 | 3, 5, 6, 7 | Reporting v2 needs schema v2 data and persisted similarity artifacts |
| 9 | 2, 6, 7, 8 | Integration/e2e regression locks behavior end-to-end |
| 10 | 8, 9 | Docs/config examples must reflect final schema and smoke behavior |

### Agent Dispatch Summary (wave -> task count -> categories)
| Wave | Task Count | Categories |
| --- | --- | --- |
| 1 | 5 | `deep`, `unspecified-high`, `quick` |
| 2 | 5 | `deep`, `unspecified-high`, `writing` |

## TODOs
> Implementation + Test = ONE task. Never separate.
> EVERY task MUST have: Agent Profile + Parallelization + QA Scenarios.

<!-- TASKS -->

- [ ] 1. Lock the v2 experiment identity and non-`cpp` seed contract

  **What to do**: Define the new canonical run identity as `(run_id, problem_id, seed_language, target_language)` plus `ordered_pair_key = "{seed_language}->{target_language}"`. Extend the config/corpus contract so each run declares one `seed_language`, the corpus validator resolves `corpus/solutions/<problem_id>/reference.<ext>` from that seed, and same-language pairs are rejected before execution. Explicitly choose schema names `run_manifest.v2` and `report_summary.v2`, and document that legacy v1 artifacts remain readable but all new writes use v2 semantics.
  **Must NOT do**: Do not introduce mixed-seed runs, silent auto-migration, or fallback-to-`reference.cpp` behavior when a non-`cpp` seed file is missing.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: this task locks the identity, schema, and validation rules every later task depends on.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: NO | Wave 1 | Blocks: 2, 3, 4, 5, 6, 8, 9, 10 | Blocked By: -

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `src/rttdist/config.py` - Current config lacks `seed_language` and only models `target_languages`; extend this contract without changing CLI verbs.
  - Pattern: `src/rttdist/corpus.py` - Current validator hard-codes `reference.cpp`; replace with seed-language-based resolution.
  - Pattern: `src/rttdist/reporting.py` - Current summaries group by `target_language` only and write `report_summary.v1`; use this as the place to bump summary schema/version semantics.
  - Pattern: `src/rttdist/run_state.py` - Existing checksum/resume validation is the right place to thread manifest schema versioning.
  - Test: `tests/unit/test_reporting.py` - Existing summary schema assertions must be updated rather than bypassed.
  - Test: `tests/integration/test_corpus_validation_service.py` - Existing validation flow is the right regression anchor for new seed rules.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/integration/test_corpus_validation_service.py -q -k seed_language` exits `0`.
  - [ ] `python -m pytest tests/unit/test_reporting.py -q -k schema_version` exits `0`.
  - [ ] `python -m rttdist.cli validate-corpus --config tests/fixtures/config/minimal.yaml` exits `0` for a valid seed-aware config.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Non-cpp seed resolves the correct curated seed file
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_corpus_validation_service.py -q -k seed_language`
    Expected: Validation passes when `seed_language` points at an existing `reference.<ext>` and surfaces the resolved file in the returned corpus entry/manifest metadata
    Evidence: .sisyphus/evidence/task-1-seed-contract.txt

  Scenario: Same-language or missing-seed config fails fast
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_corpus_validation_service.py -q -k invalid_seed_language`
    Expected: Validation rejects `seed_language == target_language` and missing `reference.<ext>` with deterministic path-rich errors
    Evidence: .sisyphus/evidence/task-1-seed-contract-error.txt
  ```

  **Commit**: YES | Message: `feat(config): add seed language contract` | Files: `src/rttdist/config.py`, `src/rttdist/corpus.py`, `src/rttdist/run_state.py`, `tests/integration/test_corpus_validation_service.py`, `tests/fixtures/config/minimal.yaml`

- [ ] 2. Extend CLI/config validation for ordered-pair runs without changing verbs

  **What to do**: Thread `seed_language` through CLI load/validate/run/report flows while keeping the existing commands and argument names. Ensure `validate-corpus`, `run`, `resume`, and `report` surface precise errors for unsupported seed languages, same-language pairs, and incompatible v2/v1 manifest expectations. Update config fixtures so smoke and integration flows cover both the default `cpp` seed and one non-default seed path.
  **Must NOT do**: Do not add new top-level CLI commands or make `report` depend on live network credentials.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: CLI and validation changes are user-facing and need careful compatibility handling.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: LIMITED | Wave 1 | Blocks: 6, 9, 10 | Blocked By: 1

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `src/rttdist/cli.py` - Preserve existing subcommands and error-exit behavior while threading the new config field.
  - Pattern: `src/rttdist/config.py` - Reuse current validation style for provider/model/runtime fields when adding seed validation.
  - Pattern: `README.md` - Existing documented commands must remain valid after the change.
  - Test: `tests/integration/test_cli.py` - Existing CLI integration tests should absorb new config/validation cases.
  - Test: `tests/e2e/test_smoke_experiment.py` - Current smoke path is the end-to-end contract to preserve.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/integration/test_cli.py -q -k seed_language` exits `0`.
  - [ ] `python -m pytest tests/e2e/test_smoke_experiment.py -q -k config_validation` exits `0`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Existing CLI verbs still execute with seed-aware config
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_cli.py -q -k seed_language`
    Expected: `validate-corpus`, `run`, `resume`, and `report` accept seed-aware configs without introducing new commands or argument names
    Evidence: .sisyphus/evidence/task-2-cli.txt

  Scenario: Invalid seed configuration exits with validation status
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_cli.py -q -k invalid_seed_language`
    Expected: CLI exits through the validation-error path and prints a specific message for same-language or unsupported seed cases
    Evidence: .sisyphus/evidence/task-2-cli-error.txt
  ```

  **Commit**: YES | Message: `feat(cli): validate seed-aware runs` | Files: `src/rttdist/cli.py`, `src/rttdist/config.py`, `tests/integration/test_cli.py`, `tests/e2e/test_smoke_experiment.py`, `tests/fixtures/config/minimal.yaml`

- [ ] 3. Version the artifact tree around ordered-pair identity

  **What to do**: Replace the current `run_id/problem_id/target_language` layout with an ordered-pair-safe directory contract such as `run_id/problem_id/{seed_language}-to-{target_language}`. Add explicit manifest schema versioning, keep direction metadata immutable, and update report manifest discovery/resume recovery so v2 paths are discovered by ordered pair while v1 paths are still readable through a dedicated legacy branch. Rename seed artifact semantics away from hard-coded C++ assumptions so persisted seed files accurately reflect the chosen seed language.
  **Must NOT do**: Do not preserve v1 path assumptions inside v2 code paths, and do not let report discovery infer direction from directory depth alone.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: artifact layout and schema versioning affect run, resume, and report correctness simultaneously.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: LIMITED | Wave 1 | Blocks: 5, 6, 8, 9, 10 | Blocked By: 1

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `src/rttdist/artifacts.py` - Current run directory, file extension map, and `seed_language` constant live here.
  - Pattern: `src/rttdist/run_state.py` - Manifest loading/recovery/checksum code must become schema-aware.
  - Pattern: `src/rttdist/reporting.py` - Manifest discovery currently assumes target-only directory shape.
  - Pattern: `src/rttdist/pipeline.py` - Seed artifact naming currently assumes `reference.cpp`; update the source-of-truth artifact naming here.
  - Test: `tests/unit/test_artifact_contract.py` - Existing artifact contract tests should define the new ordered-pair tree.
  - Test: `tests/integration/test_resume.py` - Resume parity should verify v2 manifests and legacy-read handling.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/unit/test_artifact_contract.py -q -k ordered_pair` exits `0`.
  - [ ] `python -m pytest tests/integration/test_resume.py -q -k manifest_v2` exits `0`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Ordered-pair artifact tree is written and rediscovered correctly
    Tool: Bash
    Steps: Run `python -m pytest tests/unit/test_artifact_contract.py -q -k ordered_pair` and `python -m pytest tests/integration/test_resume.py -q -k manifest_v2`
    Expected: New manifests use `{seed_language}-to-{target_language}` paths, include schema version `run_manifest.v2`, and resume reconstructs the same run identity
    Evidence: .sisyphus/evidence/task-3-artifacts.txt

  Scenario: Legacy v1 artifacts do not get misread as reverse-direction v2 runs
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_resume.py -q -k legacy_read_path`
    Expected: v1 artifacts are handled only by the explicit legacy branch and never reinterpreted as v2 ordered-pair manifests
    Evidence: .sisyphus/evidence/task-3-artifacts-error.txt
  ```

  **Commit**: YES | Message: `feat(artifacts): version ordered-pair manifests` | Files: `src/rttdist/artifacts.py`, `src/rttdist/run_state.py`, `src/rttdist/reporting.py`, `src/rttdist/pipeline.py`, `tests/unit/test_artifact_contract.py`, `tests/integration/test_resume.py`

- [ ] 4. Generalize prompts and translation clients from `cpp`-specific legs to ordered language pairs

  **What to do**: Replace `translate_cpp_to_target()` / `translate_target_to_cpp()` assumptions with a generic translation contract that accepts `source_language` and `target_language` explicitly while still driving a roundtrip of `seed_language -> target_language -> seed_language`. Update prompt bundles, request metadata, and client implementations so direction labels, source labels, and persisted metadata all reflect the actual pair being executed. Keep current providers (`openai`, `ollama`) but make both clients conform to the same generic interface.
  **Must NOT do**: Do not add extra translation providers, and do not keep hidden `cpp` defaults inside metadata or prompt rendering.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: prompt/client changes span multiple providers and affect artifact/debug payloads.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: 5, 6, 7, 9 | Blocked By: 1, 2

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `src/rttdist/prompts.py` - Current prompt bundle design already has direction labels and is the correct seam for generic language parameters.
  - Pattern: `src/rttdist/openai_client.py` - Request metadata still injects `seed_language: "cpp"`; replace with actual runtime values.
  - Pattern: `src/rttdist/ollama_client.py` - Mirror the same metadata/prompt changes for Ollama so both clients stay contract-compatible.
  - Pattern: `src/rttdist/pipeline.py` - Consume one generic translation interface instead of provider-specific direction methods.
  - Test: `tests/integration/test_prompt_templates.py` - Existing prompt tests are the right place to lock new generic rendering behavior.
  - Test: `tests/integration/test_openai_client.py` - Existing client tests should absorb request metadata and generic direction assertions.
  - Test: `tests/integration/test_ollama_client.py` - Provider parity must be preserved here.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/integration/test_prompt_templates.py -q` exits `0`.
  - [ ] `python -m pytest tests/integration/test_openai_client.py -q -k generic_translation` exits `0`.
  - [ ] `python -m pytest tests/integration/test_ollama_client.py -q -k generic_translation` exits `0`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Prompt metadata reflects the actual ordered pair
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_prompt_templates.py -q`
    Expected: Prompt bundles and request metadata show the configured `source_language`, `target_language`, and direction label for both legs of the roundtrip
    Evidence: .sisyphus/evidence/task-4-prompts.txt

  Scenario: No provider leaves hidden cpp assumptions in payloads
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_openai_client.py -q -k generic_translation` and `python -m pytest tests/integration/test_ollama_client.py -q -k generic_translation`
    Expected: Captured request payloads for both providers no longer hard-code `seed_language: cpp` unless the configured seed is actually `cpp`
    Evidence: .sisyphus/evidence/task-4-prompts-error.txt
  ```

  **Commit**: YES | Message: `refactor(prompts): generalize translation directions` | Files: `src/rttdist/prompts.py`, `src/rttdist/openai_client.py`, `src/rttdist/ollama_client.py`, `src/rttdist/pipeline.py`, `tests/integration/test_prompt_templates.py`, `tests/integration/test_openai_client.py`, `tests/integration/test_ollama_client.py`

- [ ] 5. Implement dual-state convergence primitives and metric-availability policy

  **What to do**: Extend the fixed-point module so it can classify both seed-language and target-language histories independently, then derive one overall convergence outcome using the agreed truth table: `fixed_point` only when both histories are fixed, `oscillation` when either history oscillates before both are fixed, otherwise `continue`. Keep `compute_residual_similarity()` as the legacy C++ token metric, and add explicit measurement-availability helpers so non-`cpp` seeds emit `unavailable(reason="seed_language_not_cpp")` instead of a misleading number.
  **Must NOT do**: Do not replace the legacy residual similarity algorithm, and do not declare overall fixed-point when only one language state has stabilized.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: convergence semantics are core experiment methodology and must be precisely testable.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: 6, 8, 9 | Blocked By: 1, 3, 4

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `src/rttdist/fixed_point.py` - Current adjacent-hash and two-cycle logic is the basis for both state-specific classifiers.
  - Pattern: `src/rttdist/normalize.py` - Legacy residual similarity implementation must remain untouched except for availability gating.
  - Pattern: `src/rttdist/pipeline.py` - Current pipeline only appends roundtrip-C++ history; this task defines the semantics it will later consume.
  - Test: `tests/unit/test_fixed_point.py` - Add dual-state truth-table coverage here instead of inventing a new test surface.
  - Test: `tests/unit/test_reporting.py` - Measurement availability reasons should be validated through reporting-facing tests as well.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/unit/test_fixed_point.py -q -k dual_state` exits `0`.
  - [ ] `python -m pytest tests/unit/test_reporting.py -q -k seed_language_not_cpp` exits `0`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Dual-state truth table classifies fixed, oscillation, and continue correctly
    Tool: Bash
    Steps: Run `python -m pytest tests/unit/test_fixed_point.py -q -k dual_state`
    Expected: Tests cover both states fixed, one fixed/one continue, one oscillating, and both oscillating without ambiguous outcomes
    Evidence: .sisyphus/evidence/task-5-convergence.txt

  Scenario: Non-cpp seeds do not emit bogus residual similarity
    Tool: Bash
    Steps: Run `python -m pytest tests/unit/test_reporting.py -q -k seed_language_not_cpp`
    Expected: Summary/output helpers return `unavailable` with reason `seed_language_not_cpp` rather than a measured token score
    Evidence: .sisyphus/evidence/task-5-convergence-error.txt
  ```

  **Commit**: YES | Message: `feat(convergence): add dual-state semantics` | Files: `src/rttdist/fixed_point.py`, `src/rttdist/reporting.py`, `tests/unit/test_fixed_point.py`, `tests/unit/test_reporting.py`

- [ ] 6. Persist dual histories and schema-v2 metadata through pipeline and resume

  **What to do**: Refactor the pipeline/run-state loop so each iteration persists both the target-language source history and the seed-language roundtrip history, carries ordered-pair identity through the manifest, and records the new overall convergence outcome. Ensure resume reconstruction restores both histories, preserves immutable metadata boundaries, and validates schema, ordered pair, seed language, prompt version, and embedding settings before continuing. Rename seed artifact persistence so the stored seed snapshot matches the actual seed language and source extension.
  **Must NOT do**: Do not reconstruct target-history or metadata heuristically from report outputs, and do not allow resume to continue when ordered-pair identity or schema version mismatches are detected.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: the loop, manifest, and resume flows are tightly coupled and easy to corrupt without end-to-end care.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: NO | Wave 2 | Blocks: 7, 8, 9, 10 | Blocked By: 2, 3, 4, 5

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `src/rttdist/pipeline.py` - Current iteration payload writing, history updates, and final-record logic all live here.
  - Pattern: `src/rttdist/run_state.py` - Resume validation/checksum logic must be extended to dual histories and schema-v2 metadata.
  - Pattern: `src/rttdist/artifacts.py` - Use the ordered-pair path and source-extension helpers defined earlier.
  - Pattern: `src/rttdist/failure_taxonomy.py` - Preserve existing failure typing while adding dual-state convergence details in `details`.
  - Test: `tests/integration/test_rtt_pipeline.py` - Existing pipeline integration tests are the right anchor for persisted iteration payloads.
  - Test: `tests/integration/test_resume.py` - Resume mismatch and recovery paths must be extended here.
  - Test: `tests/integration/test_run_idempotency.py` - Idempotency regression should protect re-runs under the new manifest rules.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/integration/test_rtt_pipeline.py -q -k dual_state_history` exits `0`.
  - [ ] `python -m pytest tests/integration/test_resume.py -q -k ordered_pair_or_embedding_metadata` exits `0`.
  - [ ] `python -m pytest tests/integration/test_run_idempotency.py -q` exits `0`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Pipeline writes schema-v2 manifests with both histories and convergence states
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_rtt_pipeline.py -q -k dual_state_history`
    Expected: Iteration artifacts include both seed-state and target-state histories/metrics, and final manifests carry immutable ordered-pair metadata
    Evidence: .sisyphus/evidence/task-6-pipeline.txt

  Scenario: Resume rejects incompatible ordered-pair or embedding metadata
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_resume.py -q -k ordered_pair_or_embedding_metadata`
    Expected: Resume fails fast when schema version, ordered pair, seed language, prompt version, or embedding settings differ from the persisted manifest
    Evidence: .sisyphus/evidence/task-6-pipeline-error.txt
  ```

  **Commit**: YES | Message: `feat(pipeline): persist dual-state manifests` | Files: `src/rttdist/pipeline.py`, `src/rttdist/run_state.py`, `src/rttdist/artifacts.py`, `tests/integration/test_rtt_pipeline.py`, `tests/integration/test_resume.py`, `tests/integration/test_run_idempotency.py`

- [ ] 7. Add embedding provider abstraction and persist final similarity artifacts

  **What to do**: Introduce a small embedding-provider seam that takes plain source text and returns vectors plus provenance, then implement the MVP with the existing OpenAI Python SDK. Compute final similarity exactly once after a run reaches a terminal state with a final seed-language source available, store the result in a dedicated artifact such as `final-similarity.json`, and record provider/model/dimensions/token-usage/request-id/source-hash evidence. Use cosine similarity inside one provider/model/dimension space only, and make `report` read the saved artifact instead of recomputing. If OpenAI exposes no true internal revision id, persist `configured_model`, observed response `model`, and SDK request id under a `revision_evidence` structure.
  **Must NOT do**: Do not recompute embeddings in `report`, compare vectors from different models/dimensions, or store only the score without provenance.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: this adds a new external-service seam plus persistence rules and offline behavior constraints.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: LIMITED | Wave 2 | Blocks: 8, 9, 10 | Blocked By: 4, 6

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `src/rttdist/openai_client.py` - Reuse the existing SDK client lifecycle and request/response testing style for embeddings.
  - Pattern: `src/rttdist/pipeline.py` - Final similarity must be written during terminal pipeline execution, not deferred to reporting.
  - Pattern: `src/rttdist/reporting.py` - Reporting must consume a persisted artifact and expose availability/provenance, never call the API.
  - Pattern: `pyproject.toml` - Use the already pinned OpenAI SDK dependency; do not add a second embedding SDK.
  - Test: `tests/integration/test_openai_client.py` - Extend this file to cover embedding request/response normalization and request-id capture.
  - Test: `tests/integration/test_report_generation.py` - Add offline regeneration assertions using persisted final-similarity artifacts.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/integration/test_openai_client.py -q -k embedding` exits `0`.
  - [ ] `python -m pytest tests/integration/test_report_generation.py -q -k offline_embedding_artifact` exits `0`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Final similarity artifact captures score plus provenance
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_openai_client.py -q -k embedding`
    Expected: Embedding responses are normalized into a provider-agnostic artifact containing model, dimensions, usage, request id, source hashes, and cosine score
    Evidence: .sisyphus/evidence/task-7-embedding.txt

  Scenario: Reporting stays offline when similarity artifact already exists
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_report_generation.py -q -k offline_embedding_artifact`
    Expected: Report generation succeeds with network clients disabled because it reads only the persisted `final-similarity.json` artifact
    Evidence: .sisyphus/evidence/task-7-embedding-error.txt
  ```

  **Commit**: YES | Message: `feat(similarity): persist embedding final score` | Files: `src/rttdist/pipeline.py`, `src/rttdist/openai_client.py`, `src/rttdist/reporting.py`, `tests/integration/test_openai_client.py`, `tests/integration/test_report_generation.py`

- [ ] 8. Upgrade reporting to `report_summary.v2` with ordered-pair aggregates and statistics

  **What to do**: Redesign summary generation so v2 output contains both per-result entries and ordered-pair aggregate sections keyed by `ordered_pair_key`. Add aggregate metrics for mean/stddev/divergence rate, measured-counts, and unavailable/infrastructure counts. Keep per-result fields explicit for `seed_language`, `target_language`, dual-state convergence, legacy residual-similarity availability, and embedding final similarity provenance. Add an explicit v1 legacy-read adapter so preexisting manifests and summary expectations keep working when the reporter is pointed at older runs.
  **Must NOT do**: Do not merge reverse directions, infer aggregate denominators from raw result count, or overwrite v1 semantics while still calling the output `report_summary.v1`.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: reporting now spans schema evolution, math definitions, and backward compatibility.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: NO | Wave 2 | Blocks: 9, 10 | Blocked By: 3, 5, 6, 7

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `src/rttdist/reporting.py` - Current summary construction and markdown rendering must be evolved instead of replaced ad hoc.
  - Pattern: `src/rttdist/metrics.py` - Metric naming and delta shapes must stay consistent inside per-result entries.
  - Pattern: `src/rttdist/moss.py` - Optional MOSS behavior already demonstrates additive reporting fields and availability handling.
  - Test: `tests/unit/test_reporting.py` - Use this file to define v2 JSON/Markdown shapes, aggregate math, and unavailable-reason rendering.
  - Test: `tests/integration/test_report_generation.py` - Use this file to validate reporter behavior against persisted manifests/artifacts.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/unit/test_reporting.py -q -k ordered_pair` exits `0`.
  - [ ] `python -m pytest tests/integration/test_report_generation.py -q` exits `0`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Ordered-pair aggregates compute correct mean/stddev/divergence semantics
    Tool: Bash
    Steps: Run `python -m pytest tests/unit/test_reporting.py -q -k ordered_pair`
    Expected: `cpp->python` and `python->cpp` remain separate, `stddev` is population-based, and divergence excludes infrastructure failures from its denominator
    Evidence: .sisyphus/evidence/task-8-reporting.txt

  Scenario: Legacy v1 runs remain reportable via explicit adapter logic
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_report_generation.py -q -k legacy_v1`
    Expected: Reporter can still read old manifests/summaries through a dedicated compatibility path without confusing them with v2 ordered-pair data
    Evidence: .sisyphus/evidence/task-8-reporting-error.txt
  ```

  **Commit**: YES | Message: `feat(reporting): add ordered-pair summary v2` | Files: `src/rttdist/reporting.py`, `src/rttdist/metrics.py`, `tests/unit/test_reporting.py`, `tests/integration/test_report_generation.py`

- [ ] 9. Expand integration and smoke coverage for non-default seed runs

  **What to do**: Update integration fixtures and the e2e smoke flow so at least one non-`cpp` seed directional run is exercised with mocked translation responses and persisted embedding artifacts. Cover ordered-pair identity, same-language rejection, resume compatibility, and offline report generation. Keep the smoke corpus small and deterministic by using fixtures/mocks instead of adding broad new benchmark content.
  **Must NOT do**: Do not add live OpenAI embedding calls to smoke tests, and do not require real non-test corpus expansion to verify the new behavior.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: this task stitches together the new contracts across realistic test flows.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: LIMITED | Wave 2 | Blocks: 10 | Blocked By: 2, 6, 7, 8

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `tests/e2e/test_smoke_experiment.py` - Existing smoke flow already covers validate/run/resume/report and should remain the end-to-end anchor.
  - Pattern: `tests/fixtures/e2e/smoke_openai_responses.json` - Extend this deterministic fixture set rather than inventing live network behavior.
  - Pattern: `tests/fixtures/config/minimal.yaml` - Keep the canonical small config but make it seed-aware.
  - Pattern: `tests/integration/test_resume.py` - Resume correctness is part of the upgraded smoke story, not a separate concern.
  - Pattern: `tests/integration/test_report_generation.py` - Report/offline behavior should be locked here and echoed in smoke.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `RTTDIST_OPENAI_MOCK_RESPONSES=tests/fixtures/e2e/smoke_openai_responses.json python -m pytest tests/e2e/test_smoke_experiment.py -q` exits `0`.
  - [ ] `python -m pytest tests/integration/test_resume.py -q -k seed_language` exits `0`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Smoke run covers a non-default seed with ordered-pair reporting
    Tool: Bash
    Steps: Export `RTTDIST_OPENAI_MOCK_RESPONSES=tests/fixtures/e2e/smoke_openai_responses.json` and run `python -m pytest tests/e2e/test_smoke_experiment.py -q`
    Expected: The smoke flow validates, runs, resumes, and reports a seed-aware directional experiment with schema-v2 outputs and offline final similarity data
    Evidence: .sisyphus/evidence/task-9-smoke.txt

  Scenario: Resume and report catch mismatched seed-aware fixtures
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_resume.py -q -k seed_language`
    Expected: Integration tests reject stale or mismatched fixtures/manifests instead of silently replaying incompatible artifacts
    Evidence: .sisyphus/evidence/task-9-smoke-error.txt
  ```

  **Commit**: YES | Message: `test(e2e): cover seed-aware directional smoke` | Files: `tests/e2e/test_smoke_experiment.py`, `tests/fixtures/e2e/smoke_openai_responses.json`, `tests/fixtures/config/minimal.yaml`, `tests/integration/test_resume.py`, `tests/integration/test_report_generation.py`

- [ ] 10. Refresh README, example configs, and artifact expectations for the new methodology

  **What to do**: Update user-facing documentation and example config/comments so the repository explains `seed_language`, ordered-pair directory layout, dual-state convergence, residual-vs-embedding similarity semantics, aggregate statistics, offline report behavior, and legacy compatibility limits. Ensure examples use the final schema-v2 artifact names and mention that OpenAI revision evidence is limited to model string plus request-id provenance.
  **Must NOT do**: Do not document behaviors that differ from the implemented schema-v2 contracts, and do not promise additional providers or mixed-seed runs.

  **Recommended Agent Profile**:
  - Category: `writing` - Reason: this is user-facing technical documentation bound to the final implementation contract.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: - | Blocked By: 2, 3, 5, 7, 8, 9

  **References** (executor has NO interview context - be exhaustive):
  - Pattern: `README.md` - Current usage, similarity, convergence, and artifact descriptions must be updated in place.
  - Pattern: `tests/fixtures/config/minimal.yaml` - Keep docs aligned with the canonical smoke config shape.
  - Pattern: `src/rttdist/reporting.py` - Documentation must mirror final `report_summary.v2` semantics exactly.
  - Pattern: `src/rttdist/fixed_point.py` - Use the implemented dual-state truth table terminology, not a looser prose version.
  - Test: `tests/e2e/test_smoke_experiment.py` - Reference the smoke-verified workflow instead of speculative commands.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/e2e/test_smoke_experiment.py -q` exits `0` after the documented commands/configs are updated.
  - [ ] `python -m pytest tests/integration/test_cli.py -q` exits `0` after README/config examples are brought in line with actual CLI behavior.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Documented smoke workflow matches the verified seed-aware CLI flow
    Tool: Bash
    Steps: Run `python -m pytest tests/e2e/test_smoke_experiment.py -q`
    Expected: Smoke tests still pass using the README-aligned config and command examples
    Evidence: .sisyphus/evidence/task-10-docs.txt

  Scenario: Docs do not drift from actual CLI/config semantics
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_cli.py -q`
    Expected: CLI integration still passes after example config fields and usage text are updated, proving documentation changes did not require hidden CLI behavior
    Evidence: .sisyphus/evidence/task-10-docs-error.txt
  ```

  **Commit**: YES | Message: `docs(readme): describe seed-aware reporting v2` | Files: `README.md`, `tests/fixtures/config/minimal.yaml`, `tests/e2e/test_smoke_experiment.py`

## Final Verification Wave (4 parallel agents, ALL must APPROVE)
- [ ] F1. Plan Compliance Audit - oracle
- [ ] F2. Code Quality Review - unspecified-high
- [ ] F3. Real Manual QA - unspecified-high
- [ ] F4. Scope Fidelity Check - deep

## Commit Strategy
- Land Wave 1 as 2-3 commits: contract/config, artifact/prompt API, convergence/embedding seams.
- Land Wave 2 as 3-4 commits: pipeline persistence, reporting v2, regression fixtures/tests, docs/examples.
- Keep schema/version changes isolated from reporting math where possible so regressions are easier to bisect.

## Success Criteria
- Configured non-`cpp` seeds validate correctly and fail fast when the required `reference.<ext>` is absent.
- Ordered-pair runs write distinct schema-v2 manifests/artifacts and resume safely.
- Both seed-state and target-state convergence histories are persisted and influence overall convergence exactly as specified.
- Final embedding similarity is available offline from persisted artifacts and includes provenance evidence.
- `summary.json` / `summary.md` expose per-result and ordered-pair aggregate metrics with correct availability semantics.
- Existing v1 artifacts remain reportable through an explicit legacy-read path.
