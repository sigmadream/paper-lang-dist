# RTT Language Distance Experiment Tool

## TL;DR
> **Summary**: Build a fresh Python experiment runner that uses curated C++ reference solutions for `problem/`, performs `C++ -> {C, Java, Python} -> C++` round-trip translation with OpenAI, detects fixed-point convergence, and reports RTT distance, residual token similarity, AST distance, and complexity deltas with reproducible artifacts.
> **Deliverables**:
> - Python CLI/batch tool with reproducible run artifacts
> - Curated corpus/config contract for `problem/` fixtures plus reference C++ solutions
> - OpenAI-backed RTT pipeline with convergence, oscillation, and failure classification
> - AST-normalized distance metrics, complexity metrics, and report generation
> - Pytest-based unit/integration/e2e verification with mocked model responses
> **Effort**: Large
> **Parallel**: YES - 3 waves
> **Critical Path**: Task 1 -> Task 2 -> Task 4 -> Task 7 -> Task 10 -> Task 12

## Context
### Original Request
- Build the code needed to experiment on the idea in `ref/idea.md`, using the paper in `ref/왕복 번역과 고정점을 이용한 언어 거리 계산.pdf` as the starting point.
- Use the problems under `problem/` as the experiment set.

### Interview Summary
- First-phase scope is not RTT-only; it includes RTT, AST, and complexity metrics.
- Target languages are `C`, `Java`, and `Python`, with `C++` as the seed language.
- Translation backend for v1 is OpenAI-only; do not add multi-provider abstraction.
- Repository currently contains dataset material only: `problem/`, `ref/`, and planning files under `.sisyphus/`.
- Problem directories already provide runnable sample fixtures as paired `.inp` / `.out` files.
- Test infrastructure must be created as part of the work, not replaced with ad-hoc QA only.

### Metis Review (gaps addressed)
- Fixed-point detection is defined explicitly in this plan as normalized C++ token-stream hash equality across adjacent RTT iterations.
- Oscillation is treated as a distinct outcome when a normalized C++ hash repeats with period 2 before fixed-point convergence.
- Failing translations are not mixed into similarity scores; compile/runtime/wrong-answer failures are tracked as separate outcome classes.
- Cross-language AST comparison is constrained to a language-agnostic normalized AST IR to avoid raw heterogeneous parser-tree comparison.
- v1 excludes provider abstraction, hidden-judge generation, dashboards, extra languages, and composite scoring.

## Work Objectives
### Core Objective
- Create a reproducible local experiment tool that measures how much a curated C++ solution changes when repeatedly translated through `C`, `Java`, or `Python` and back to `C++`, while also recording structural and complexity differences across the translation chain.

### Deliverables
- Python project scaffold with CLI entrypoints, config parsing, and pytest suite.
- Corpus contract that maps existing `problem/IPOP_*` fixtures to manually curated reference solutions.
- OpenAI translation client with deterministic prompt templates and mockable I/O boundaries.
- Execution adapters for `C`, `C++`, `Java`, and `Python` that compile/run candidate programs against `.inp` / `.out` fixtures.
- RTT loop engine with artifact capture, convergence detection, oscillation detection, and iteration cap handling.
- AST metric pipeline built on normalized per-language parse trees.
- Complexity metric pipeline built on cross-language metrics that are actually comparable in v1.
- Machine-readable and human-readable experiment reports.

### Definition of Done (verifiable conditions with commands)
- `python -m pytest tests/unit -q` exits `0`.
- `python -m pytest tests/integration -q` exits `0` using mocked OpenAI responses.
- `python -m pytest tests/e2e -q` exits `0` on a tiny curated corpus.
- `python -m rttdist.cli validate-corpus --config tests/fixtures/config/minimal.yaml` exits `0`.
- `python -m rttdist.cli run --config tests/fixtures/config/minimal.yaml --run-id smoke` exits `0` and creates the expected artifact tree.
- `python -m rttdist.cli report --run-id smoke` exits `0` and emits both `summary.json` and `summary.md`.

### Must Have
- Python is the implementation language for v1, with `pyproject.toml` and `pytest` as the canonical local workflow.
- Config files are YAML and must pin model name, temperature, max iterations, timeout budget, and selected problem IDs.
- Seed programs are manually curated C++ solutions stored in-repo under a dedicated corpus directory; v1 does not generate them.
- Fixed-point criterion is normalized-token equality on successive round-tripped C++ outputs.
- Iteration cap is `20`, matching the paper's experimental ceiling.
- Failure taxonomy includes `api_error`, `parse_error`, `compile_error`, `runtime_error`, `timeout`, `wrong_answer`, `oscillation`, and `max_iter_no_convergence`.
- Artifact capture is mandatory for every iteration: prompt payload, raw model response, extracted code, compile log, execution log, and metrics JSON.
- Similarity outputs remain separate: RTT convergence distance, residual token similarity, AST distance, and complexity deltas are reported independently.

### Must NOT Have (guardrails, AI slop patterns, scope boundaries)
- Must NOT add Gemini or any other provider abstraction in v1.
- Must NOT auto-generate reference C++ seeds from problem statements.
- Must NOT infer hidden correctness beyond the provided sample fixtures.
- Must NOT collapse RTT, AST, and complexity into a single weighted score.
- Must NOT build a dashboard, web UI, or notebook-first workflow before the CLI and artifact model are stable.
- Must NOT compare raw heterogeneous parser trees directly; use the normalized AST IR only.

## Verification Strategy
> ZERO HUMAN INTERVENTION - all verification is agent-executed.
- Test decision: `TDD` with `pytest`; unit and integration tests use mocks/golden fixtures, while e2e smoke tests run on a tiny curated corpus.
- QA policy: Every task below includes executable happy-path and failure-path scenarios.
- Evidence: `.sisyphus/evidence/task-{N}-{slug}.{ext}`.

## Execution Strategy
### Parallel Execution Waves
> Target: 5-8 tasks per wave. Shared contracts land first to maximize safe parallelism.

Wave 1: Tasks 1-5 - project bootstrap, corpus/config contract, test harness, OpenAI boundary, normalization contract.

Wave 2: Tasks 6-10 - execution adapters, RTT engine, AST metric pipeline, complexity pipeline, reporting.

Wave 3: Tasks 11-13 - resumability/orchestration, CLI surface, e2e smoke experiment and usage docs.

### Dependency Matrix (full, all tasks)
| Task | Depends On | Notes |
| --- | --- | --- |
| 1 | - | Establish Python project and test tooling |
| 2 | 1 | Defines in-repo corpus and config schema |
| 3 | 1, 2 | Locks golden tests around schema and artifacts |
| 4 | 1, 2, 3 | OpenAI client and prompt renderer must satisfy tests |
| 5 | 1, 3, 4 | Normalization and extraction rely on prompt/response shape |
| 6 | 1, 2, 3 | Compile/run adapters depend on corpus and test harness |
| 7 | 4, 5, 6 | RTT loop needs translation, normalization, and execution |
| 8 | 2, 5, 7 | AST IR depends on corpus contract and emitted sources |
| 9 | 2, 6, 7 | Complexity metrics depend on emitted sources and execution outputs |
| 10 | 7, 8, 9 | Reports aggregate all metric and status outputs |
| 11 | 7, 10 | Resume/idempotency layer wraps completed pipeline |
| 12 | 10, 11 | CLI binds validation, run, resume, and report commands |
| 13 | 6, 10, 12 | Smoke corpus uses final CLI and execution/reporting |

### Agent Dispatch Summary (wave -> task count -> categories)
| Wave | Task Count | Categories |
| --- | --- | --- |
| 1 | 5 | `unspecified-high`, `deep`, `quick` |
| 2 | 5 | `unspecified-high`, `deep` |
| 3 | 3 | `deep`, `quick`, `unspecified-high` |

## TODOs
> Implementation + Test = ONE task. Never separate.
> Every task below includes agent profile, parallelization, references, acceptance criteria, QA scenarios, and commit guidance.

- [x] 1. Bootstrap the Python experiment project

  **What to do**: Create a fresh Python package layout centered on `src/rttdist/` with `pyproject.toml`, `pytest` configuration, dependency groups, and a minimal importable CLI module built with stdlib `argparse`. Pin libraries needed for v1: `openai`, `pytest`, `PyYAML`, `tree-sitter`, `tree-sitter-c`, `tree-sitter-cpp`, `tree-sitter-java`, `tree-sitter-python`, `apted`, and `lizard`. Add a tiny smoke test that proves the package imports and test discovery works.
  **Must NOT do**: Do not add provider plugins, notebook scaffolding, dashboards, or non-Python entrypoints.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: repo bootstrap touches multiple foundational files and test configuration.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: NO | Wave 1 | Blocks: 2, 3, 4, 5, 6 | Blocked By: -

  **References**:
  - `ref/idea.md:31` - RTT is iteration-driven; the package structure should support repeatable batch runs.
  - `problem/` - Existing dataset root the new tool must consume rather than replace.
  - `https://docs.pytest.org/` - Canonical test runner behavior for the new suite.
  - `https://platform.openai.com/docs/overview` - Official API baseline for the chosen provider.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/unit/test_bootstrap.py -q` exits `0`.
  - [ ] `python -c "import rttdist"` exits `0` in the project virtual environment.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Project imports and pytest starts
    Tool: Bash
    Steps: Create virtualenv, install project deps, run `python -m pytest tests/unit/test_bootstrap.py -q`
    Expected: Pytest reports passing bootstrap tests and exit code `0`
    Evidence: .sisyphus/evidence/task-1-bootstrap.txt

  Scenario: Missing dependency is surfaced clearly
    Tool: Bash
    Steps: Run `python -m pytest tests/unit/test_bootstrap.py -k missing_dependency_guard -q`
    Expected: Guard test passes by asserting an actionable installation error path exists
    Evidence: .sisyphus/evidence/task-1-bootstrap-error.txt
  ```

  **Commit**: YES | Message: `chore(python): bootstrap experiment project` | Files: `pyproject.toml`, `src/rttdist/**`, `tests/unit/test_bootstrap.py`

- [x] 2. Define the corpus and config contract

  **What to do**: Formalize how existing `problem/IPOP_*` statements and sample fixtures map to manually curated seed programs. Add YAML config and corpus schema handling for problem IDs, target languages, OpenAI model settings, iteration cap, timeouts, and output locations. Choose a canonical in-repo seed layout such as `corpus/solutions/<problem-id>/reference.cpp` and make validation fail fast when a listed problem lacks a seed or fixture pair.
  **Must NOT do**: Do not auto-generate C++ seeds from the statements, and do not invent hidden tests.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: this task locks the experiment contract that all later work depends on.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: NO | Wave 1 | Blocks: 3, 4, 6, 8, 9 | Blocked By: 1

  **References**:
  - `problem/IPOP_1436.md:8` - Problem statements already define the public experiment prompt context.
  - `problem/IPOP_1436/` - Sample fixtures already exist as `.inp` / `.out` pairs.
  - `problem/IPOP_2579.md:27` - Input/output contract format must remain discoverable across problems.
  - `ref/idea.md:2` - C++ is the explicit reference language for the experiment.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/unit/test_corpus_schema.py -q` exits `0`.
  - [ ] `python -m pytest tests/integration/test_corpus_validation_service.py -q` exits `0`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Valid corpus config is accepted
    Tool: Bash
    Steps: Run `python -m pytest tests/unit/test_corpus_schema.py -q` and `python -m pytest tests/integration/test_corpus_validation_service.py -q`
    Expected: Both commands exit `0`; validation reports the discovered seed, statement, and fixture files through the service layer
    Evidence: .sisyphus/evidence/task-2-corpus.txt

  Scenario: Missing reference seed fails fast
    Tool: Bash
    Steps: Run `python -m pytest tests/unit/test_corpus_schema.py -k missing_seed -q`
    Expected: Validation raises a deterministic error naming the missing `reference.cpp` path
    Evidence: .sisyphus/evidence/task-2-corpus-error.txt
  ```

  **Commit**: YES | Message: `feat(corpus): define seed and config contract` | Files: `src/rttdist/config.py`, `src/rttdist/corpus.py`, `tests/unit/test_corpus_schema.py`, `tests/integration/test_corpus_validation_service.py`, `tests/fixtures/config/minimal.yaml`

- [x] 3. Lock artifact and mock contracts with TDD fixtures

  **What to do**: Add golden tests that define the run directory layout, expected artifact filenames, mock OpenAI payload shapes, and failure-taxonomy serialization. Include fixtures for one tiny curated problem so later tasks can satisfy stable tests without guessing paths. Ensure tests cover success, compile failure, wrong answer, timeout, oscillation, and max-iteration outcomes at the JSON contract level.
  **Must NOT do**: Do not implement live API calls or compile/run logic yet; this task defines contracts only.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: contract-first tests influence every later implementation task.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: LIMITED | Wave 1 | Blocks: 4, 5, 6, 7, 10, 11 | Blocked By: 1, 2

  **References**:
  - `ref/왕복 번역과 고정점을 이용한 언어 거리 계산.pdf` - The paper motivates iteration-cap and convergence artifact capture.
  - `problem/IPOP_1436/1.inp` - Existing sample files should drive fixture-backed tests.
  - `problem/IPOP_1436/1.out` - Result matching must be treated as a first-class contract.
  - `.sisyphus/drafts/rtt-experiment-tool.md` - Planning assumptions already require separate failure classes.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/unit/test_artifact_contract.py -q` exits `0`.
  - [ ] `python -m pytest tests/unit/test_failure_taxonomy.py -q` exits `0`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Golden artifact contract is stable
    Tool: Bash
    Steps: Run `python -m pytest tests/unit/test_artifact_contract.py -q`
    Expected: Tests assert the exact run tree and JSON keys for a mocked successful iteration
    Evidence: .sisyphus/evidence/task-3-artifacts.txt

  Scenario: Unknown status is rejected
    Tool: Bash
    Steps: Run `python -m pytest tests/unit/test_failure_taxonomy.py -k invalid_status -q`
    Expected: The suite confirms invalid statuses cannot be serialized into result JSON
    Evidence: .sisyphus/evidence/task-3-artifacts-error.txt
  ```

  **Commit**: YES | Message: `test(contracts): lock artifact and failure schemas` | Files: `tests/unit/test_artifact_contract.py`, `tests/unit/test_failure_taxonomy.py`, `tests/fixtures/**`

- [x] 4. Implement the OpenAI translation boundary and prompt renderer

  **What to do**: Build the OpenAI client wrapper, deterministic prompt templates, and response parser used for `C++ -> target` and `target -> C++` translation. The boundary must store raw request/response payloads, support injection of mocked responses for tests, and enforce single-file code extraction even when the model returns markdown fences or prose. Pin the model in config and default temperature to `0`.
  **Must NOT do**: Do not add other providers, chat UI wrappers, or silent prompt changes outside versioned templates.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: prompt determinism and API isolation are central methodological decisions.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: LIMITED | Wave 1 | Blocks: 5, 7 | Blocked By: 1, 2, 3

  **References**:
  - `ref/idea.md:31` - RTT requires explicit directional transformations and repeated iterations.
  - `ref/왕복 번역과 고정점을 이용한 언어 거리 계산.pdf` - The paper uses low-temperature, deterministic settings and an iteration cap of `20`.
  - `https://platform.openai.com/docs/overview` - Official API behavior for request/response handling.
  - `problem/IPOP_1436.md` - Real problem text should drive one of the prompt fixtures.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/integration/test_openai_client.py -q` exits `0`.
  - [ ] `python -m pytest tests/integration/test_prompt_templates.py -q` exits `0`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Mocked round-trip translation payload succeeds
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_openai_client.py -q`
    Expected: The client persists raw payloads and extracts exactly one compilable source blob per translation step
    Evidence: .sisyphus/evidence/task-4-openai.txt

  Scenario: Markdown-fenced response is sanitized
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_prompt_templates.py -k fenced_response -q`
    Expected: The parser strips prose/fences and returns a deterministic single-file source string
    Evidence: .sisyphus/evidence/task-4-openai-error.txt
  ```

  **Commit**: YES | Message: `feat(openai): add deterministic translation boundary` | Files: `src/rttdist/openai_client.py`, `src/rttdist/prompts.py`, `tests/integration/test_openai_client.py`, `tests/integration/test_prompt_templates.py`

- [x] 5. Implement source extraction, normalization, and fixed-point detection primitives

  **What to do**: Add the code-extraction helpers, per-language normalization rules, normalized C++ token hashing, normalized C++ token-similarity scoring, and oscillation detection primitives used by the RTT loop. Normalization for v1 must remove comments and collapse insignificant whitespace without renaming identifiers or rewriting semantics. Expose functions that classify `fixed_point`, `oscillation`, or `continue` based on iteration history, and compute residual similarity against the seed C++ token stream with a Sørensen-Dice coefficient over normalized tokens.
  **Must NOT do**: Do not call external formatters, and do not perform semantic rewrites such as identifier anonymization or import sorting.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: correctness here directly affects the validity of convergence measurements.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: YES | Wave 1 | Blocks: 7, 8 | Blocked By: 1, 3, 4

  **References**:
  - `ref/idea.md:35` - Convergence is defined by small change between iterations; v1 resolves that into a concrete hash-based rule.
  - `ref/왕복 번역과 고정점을 이용한 언어 거리 계산.pdf` - Fixed-point generation and divergence handling motivate explicit iteration-state tracking and residual similarity reporting.
  - `.sisyphus/drafts/rtt-experiment-tool.md` - The planning draft already fixes convergence and failure-taxonomy expectations.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/unit/test_normalization.py -q` exits `0`.
  - [ ] `python -m pytest tests/unit/test_fixed_point.py -q` exits `0`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Adjacent normalized hashes trigger fixed point
    Tool: Bash
    Steps: Run `python -m pytest tests/unit/test_fixed_point.py -k adjacent_hash_match -q`
    Expected: The classifier marks the run as `fixed_point` when two successive normalized C++ outputs match
    Evidence: .sisyphus/evidence/task-5-normalization.txt

  Scenario: Two-state loop triggers oscillation
    Tool: Bash
    Steps: Run `python -m pytest tests/unit/test_fixed_point.py -k two_cycle -q`
    Expected: The classifier marks the history as `oscillation` instead of falsely converging
    Evidence: .sisyphus/evidence/task-5-normalization-error.txt
  ```

  **Commit**: YES | Message: `feat(core): add normalization and convergence primitives` | Files: `src/rttdist/extract.py`, `src/rttdist/normalize.py`, `src/rttdist/fixed_point.py`, `tests/unit/test_normalization.py`, `tests/unit/test_fixed_point.py`

- [x] 6. Implement compile/run adapters for C, C++, Java, and Python

  **What to do**: Build per-language execution adapters that compile when needed, run programs against every discovered `.inp` / `.out` pair for a problem, capture stdout/stderr/exit code, enforce timeouts, and classify wrong answers separately from runtime failures. Standardize temporary work directories and emitted logs so the RTT engine can call one uniform interface regardless of language.
  **Must NOT do**: Do not depend on hidden tests, Docker, or sandbox products in v1; stay with local subprocess execution and explicit timeout guards.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: multi-language execution is the riskiest operational part of the tool.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: 7, 9, 13 | Blocked By: 1, 2, 3

  **References**:
  - `problem/IPOP_1436/` - Existing sample fixtures define the runner contract.
  - `problem/IPOP_2110/` - Multiple fixture pairs must be executed as a batch, not as a single sample only.
  - `problem/IPOP_2579.md:32` - Output matching is line-oriented and should be treated deterministically.
  - `.sisyphus/drafts/rtt-experiment-tool.md` - Failure classes were fixed during planning and must remain separate.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/integration/test_execution_adapters.py -q` exits `0`.
  - [ ] `python -m pytest tests/integration/test_fixture_runner.py -q` exits `0`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: All sample fixtures pass for a known-good seed
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_fixture_runner.py -k known_good_seed -q`
    Expected: The adapter compiles/runs the seed program and marks every sample as passed
    Evidence: .sisyphus/evidence/task-6-execution.txt

  Scenario: Infinite loop is cut off as timeout
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_execution_adapters.py -k timeout_case -q`
    Expected: The runner returns `timeout` with captured stderr/stdout metadata and no hanging process remains
    Evidence: .sisyphus/evidence/task-6-execution-error.txt
  ```

  **Commit**: YES | Message: `feat(exec): add compile and fixture-run adapters` | Files: `src/rttdist/exec/**`, `tests/integration/test_execution_adapters.py`, `tests/integration/test_fixture_runner.py`

- [x] 7. Implement the RTT loop engine and artifact writer

  **What to do**: Orchestrate `C++ -> target -> C++` iterations for each target language, persist every iteration artifact, invoke semantic evaluation after each generated program, and stop on fixed point, oscillation, failure, or iteration cap. Store a run manifest that records timestamps, config hash, problem ID, target language, iteration index, and status transitions. Ensure failed target-language steps do not prevent the run from writing a complete diagnostic artifact set.
  **Must NOT do**: Do not hide intermediate artifacts, and do not treat a failed compile/run as a valid similarity datapoint.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: this is the core experimental pipeline that joins translation, execution, and convergence logic.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: NO | Wave 2 | Blocks: 8, 9, 10, 11, 12, 13 | Blocked By: 4, 5, 6

  **References**:
  - `ref/idea.md:31` - The translation loop is the primary experiment mechanism.
  - `ref/idea.md:35` - Threshold-based convergence motivation is resolved here into explicit statuses and iteration caps.
  - `ref/왕복 번역과 고정점을 이용한 언어 거리 계산.pdf` - The paper's `N_max = 20` and fixed-point framing inform the stopping rules.
  - `.sisyphus/drafts/rtt-experiment-tool.md` - Artifact requirements and failure separation were fixed during planning.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/integration/test_rtt_pipeline.py -q` exits `0`.
  - [ ] `python -m pytest tests/integration/test_pipeline_service.py -q` exits `0`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Minimal run converges and writes full artifacts
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_rtt_pipeline.py -k converges -q`
    Expected: The pipeline writes per-iteration request, response, source, execution, and manifest files until `fixed_point`
    Evidence: .sisyphus/evidence/task-7-rtt.txt

  Scenario: Iteration cap is enforced cleanly
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_rtt_pipeline.py -k max_iter -q`
    Expected: The pipeline stops at iteration `20`, records `max_iter_no_convergence`, and preserves all prior artifacts
    Evidence: .sisyphus/evidence/task-7-rtt-error.txt
  ```

  **Commit**: YES | Message: `feat(rtt): add round-trip orchestration engine` | Files: `src/rttdist/pipeline.py`, `src/rttdist/artifacts.py`, `tests/integration/test_rtt_pipeline.py`, `tests/integration/test_pipeline_service.py`

- [x] 8. Implement the normalized AST IR and tree-distance metrics

  **What to do**: Parse `C`, `C++`, `Java`, and `Python` outputs into per-language parse trees, map them into one shared normalized AST IR at statement/expression granularity, and compute `apted` tree-edit distance against the seed C++ tree plus the round-tripped C++ tree. Record parser failures as explicit metric-status entries rather than crashing the run. Add golden tests for representative constructs such as loops, branches, function calls, arrays, and returns.
  **Must NOT do**: Do not compare raw parser node labels across languages, and do not promise semantic equivalence from AST similarity alone.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: cross-language structural comparison needs careful normalization to remain scientifically defensible.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: 10, 13 | Blocked By: 2, 5, 7

  **References**:
  - `ref/idea.md:12` - AST-based syntactic distance is explicitly in scope.
  - `ref/idea.md:15` - Tree edit distance is the recommended structural metric family.
  - `https://tree-sitter.github.io/tree-sitter/` - Parser infrastructure for all four languages.
  - `problem/IPOP_2579.md` - Use a branch-heavy problem as one representative structure fixture.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/unit/test_ast_ir.py -q` exits `0`.
  - [ ] `python -m pytest tests/integration/test_ast_distance.py -q` exits `0`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Equivalent loop skeletons normalize consistently
    Tool: Bash
    Steps: Run `python -m pytest tests/unit/test_ast_ir.py -k loop_normalization -q`
    Expected: C/C++/Java/Python loop examples normalize into the same abstract node family layout
    Evidence: .sisyphus/evidence/task-8-ast.txt

  Scenario: Parser failure is recorded, not fatal
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_ast_distance.py -k parser_failure -q`
    Expected: The metric result marks parser failure explicitly and the run continues to emit remaining metrics
    Evidence: .sisyphus/evidence/task-8-ast-error.txt
  ```

  **Commit**: YES | Message: `feat(ast): add normalized tree distance metrics` | Files: `src/rttdist/ast_ir.py`, `src/rttdist/ast_metrics.py`, `tests/unit/test_ast_ir.py`, `tests/integration/test_ast_distance.py`

- [x] 9. Implement complexity and lexical metric extraction

  **What to do**: Add a v1 metric set that is genuinely comparable across the four supported languages: `loc`, `token_count`, `cyclomatic_complexity`, `function_count`, and `max_nesting_depth`. Use one shared extractor interface and record deltas versus the seed C++ program and versus the immediately previous RTT iteration. Include fixtures that show how Java boilerplate and Python brevity affect the metrics without collapsing them into a single score.
  **Must NOT do**: Do not claim Halstead parity unless the chosen extractor computes it consistently across all four languages; if not, leave Halstead out of v1.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: this task is metric-heavy but should remain narrow and test-driven.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: 10, 13 | Blocked By: 2, 6, 7

  **References**:
  - `ref/idea.md:18` - Complexity and lexical distance are required workstreams.
  - `ref/idea.md:20` - Cyclomatic-complexity-style evidence is explicitly desired.
  - `problem/IPOP_2217.md` - Include at least one greedy-style problem in fixtures to expose control-flow differences.
  - `https://pypi.org/project/lizard/` - Chosen cross-language complexity extractor for C/C++/Java/Python.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/unit/test_complexity_metrics.py -q` exits `0`.
  - [ ] `python -m pytest tests/integration/test_metric_deltas.py -q` exits `0`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Metrics are emitted for all supported languages
    Tool: Bash
    Steps: Run `python -m pytest tests/unit/test_complexity_metrics.py -k supported_languages -q`
    Expected: Each language yields the full v1 metric set with stable field names and numeric values
    Evidence: .sisyphus/evidence/task-9-complexity.txt

  Scenario: Unsupported metric request is rejected clearly
    Tool: Bash
    Steps: Run `python -m pytest tests/unit/test_complexity_metrics.py -k unsupported_metric -q`
    Expected: The code raises a deterministic error instead of silently emitting partial data
    Evidence: .sisyphus/evidence/task-9-complexity-error.txt
  ```

  **Commit**: YES | Message: `feat(metrics): add complexity and lexical metrics` | Files: `src/rttdist/metrics.py`, `tests/unit/test_complexity_metrics.py`, `tests/integration/test_metric_deltas.py`

- [x] 10. Implement report aggregation and run summaries

  **What to do**: Aggregate per-iteration artifacts into stable `summary.json` and `summary.md` outputs per run. Report, per problem and target language, the final status, iteration count, fixed-point or oscillation outcome, residual token similarity to the seed C++ program, semantic pass/fail summary, AST distance, and metric deltas. Add helpers that clearly separate missing metrics caused by failures from legitimate measured values.
  **Must NOT do**: Do not build charts, dashboards, or notebook outputs in v1; the deliverable is artifact-first text and JSON reporting.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: multiple upstream outputs must be reconciled into one stable report format.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: YES | Wave 2 | Blocks: 11, 12, 13 | Blocked By: 7, 8, 9

  **References**:
  - `ref/idea.md:36` - The paper-inspired distance definition must appear explicitly in the report.
  - `ref/idea.md:37` - Iterations-to-convergence are a first-class output.
  - `ref/idea.md:38` - Residual similarity to the original program must remain visible in the final summary.
  - `.sisyphus/drafts/rtt-experiment-tool.md` - Reporting must keep RTT, AST, and complexity outputs separate.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/unit/test_reporting.py -q` exits `0`.
  - [ ] `python -m pytest tests/integration/test_report_generation.py -q` exits `0`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Run summary includes all required fields
    Tool: Bash
    Steps: Run `python -m pytest tests/unit/test_reporting.py -k summary_fields -q`
    Expected: `summary.json` and `summary.md` contain status, iteration count, semantic outcome, AST distance, and complexity deltas
    Evidence: .sisyphus/evidence/task-10-reporting.txt

  Scenario: Failed metric inputs are rendered explicitly
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_report_generation.py -k failed_metric_inputs -q`
    Expected: Reports show why a metric is unavailable instead of omitting the field silently
    Evidence: .sisyphus/evidence/task-10-reporting-error.txt
  ```

  **Commit**: YES | Message: `feat(report): add run summary generation` | Files: `src/rttdist/reporting.py`, `tests/unit/test_reporting.py`, `tests/integration/test_report_generation.py`

- [x] 11. Add resumability, idempotent reruns, and run-manifest recovery

  **What to do**: Implement the orchestration layer that resumes interrupted runs from the last completed iteration, skips already-materialized artifacts when the config hash matches, and refuses unsafe resume attempts when the config or seed source changed. Add manifest checksums for config, prompt template version, and seed source hash so resumed runs remain reproducible and auditable.
  **Must NOT do**: Do not silently overwrite prior run artifacts, and do not resume when the config hash changed.

  **Recommended Agent Profile**:
  - Category: `deep` - Reason: resumability affects correctness, reproducibility, and artifact integrity.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: YES | Wave 3 | Blocks: 12, 13 | Blocked By: 7, 10

  **References**:
  - `ref/왕복 번역과 고정점을 이용한 언어 거리 계산.pdf` - Repeated iteration is core to the method, so interrupted runs must be recoverable.
  - `ref/idea.md:34` - Intermediate outputs must be stored by iteration for later recovery.
  - `.sisyphus/drafts/rtt-experiment-tool.md` - Reproducible artifact ownership and manual seed assumptions were fixed during planning.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/integration/test_resume.py -q` exits `0`.
  - [ ] `python -m pytest tests/integration/test_run_idempotency.py -q` exits `0`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Interrupted run resumes from the next missing iteration
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_resume.py -k happy_resume -q`
    Expected: Resume skips completed iterations, executes only missing work, and preserves prior artifacts unchanged
    Evidence: .sisyphus/evidence/task-11-resume.txt

  Scenario: Changed config blocks resume
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_resume.py -k config_hash_mismatch -q`
    Expected: Resume aborts with a clear mismatch error and does not overwrite the run directory
    Evidence: .sisyphus/evidence/task-11-resume-error.txt
  ```

  **Commit**: YES | Message: `feat(run): add resumable execution manifests` | Files: `src/rttdist/run_state.py`, `tests/integration/test_resume.py`, `tests/integration/test_run_idempotency.py`

- [x] 12. Expose the validated workflow through CLI commands

  **What to do**: Implement `validate-corpus`, `run`, `resume`, and `report` CLI commands on top of the finished pipeline using stdlib `argparse`. Standardize exit codes, logging verbosity, and file-path output so automation agents can call the tool without inspecting source. Add command-level help text and tests that verify command-line flags and error messages.
  **Must NOT do**: Do not add interactive prompts, TUI workflows, or shell scripts as the primary interface.

  **Recommended Agent Profile**:
  - Category: `quick` - Reason: once the underlying modules exist, this is a thin but important interface layer.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: YES | Wave 3 | Blocks: 13 | Blocked By: 10, 11

  **References**:
  - `ref/idea.md:6` - The work is explicitly a planned experiment tool, so the CLI must cover the full experiment lifecycle.
  - `problem/` - Command examples must operate on the existing repository dataset rather than a new dataset shape.
  - `https://docs.python.org/3/library/argparse.html` - Standard CLI behavior reference for the chosen parser.
  - `.sisyphus/drafts/rtt-experiment-tool.md` - The fixed workflow is `validate-corpus`, `run`, `resume`, `report`.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/integration/test_cli.py -q` exits `0`.
  - [ ] `python -m rttdist.cli --help` exits `0` and lists all four commands.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: CLI help and subcommands are discoverable
    Tool: Bash
    Steps: Run `python -m rttdist.cli --help` and `python -m pytest tests/integration/test_cli.py -k help_output -q`
    Expected: Help output lists `validate-corpus`, `run`, `resume`, and `report` with stable flag names
    Evidence: .sisyphus/evidence/task-12-cli.txt

  Scenario: Invalid command arguments fail clearly
    Tool: Bash
    Steps: Run `python -m pytest tests/integration/test_cli.py -k invalid_args -q`
    Expected: The CLI exits non-zero and prints a deterministic validation error without stack-trace noise
    Evidence: .sisyphus/evidence/task-12-cli-error.txt
  ```

  **Commit**: YES | Message: `feat(cli): expose experiment commands` | Files: `src/rttdist/cli.py`, `tests/integration/test_cli.py`

- [x] 13. Add a tiny curated smoke corpus and end-to-end verification flow

  **What to do**: Check in the minimum viable curated seed corpus for exactly two representative problems, `IPOP_1436` and `IPOP_2579`, wire the config fixture to that corpus, and add e2e tests plus a short usage section in `README.md` that demonstrates the full local workflow. Ensure the smoke run produces a human-readable summary and stable evidence paths.
  **Must NOT do**: Do not expand to the full `problem/` set in this task, and do not treat the smoke corpus as a scientifically meaningful final dataset.

  **Recommended Agent Profile**:
  - Category: `unspecified-high` - Reason: the task closes the loop across corpus, pipeline, CLI, and reporting.
  - Skills: `[]` - No extra skill is required.
  - Omitted: `[]` - No specialized skill should be loaded.

  **Parallelization**: Can Parallel: NO | Wave 3 | Blocks: - | Blocked By: 6, 8, 9, 10, 11, 12

  **References**:
  - `problem/IPOP_1436.md` - Use as the straightforward smoke problem.
  - `problem/IPOP_2579.md` - Use as the branch/state-heavy smoke problem.
  - `problem/IPOP_1436/` - Existing sample fixtures already cover one smoke dataset.
  - `problem/IPOP_2579/` - Existing sample fixtures already cover the second smoke dataset.

  **Acceptance Criteria** (agent-executable only):
  - [ ] `python -m pytest tests/e2e -q` exits `0`.
  - [ ] `python -m rttdist.cli run --config tests/fixtures/config/minimal.yaml --run-id smoke` exits `0` and creates `summary.json` plus `summary.md`.

  **QA Scenarios** (MANDATORY - task incomplete without these):
  ```text
  Scenario: Smoke experiment completes end to end
    Tool: Bash
    Steps: Run `python -m pytest tests/e2e/test_smoke_experiment.py -q` and `python -m rttdist.cli report --run-id smoke`
    Expected: The e2e test passes and the report command emits both machine-readable and human-readable summaries
    Evidence: .sisyphus/evidence/task-13-smoke.txt

  Scenario: Missing toolchain dependency is reported cleanly
    Tool: Bash
    Steps: Run `python -m pytest tests/e2e/test_smoke_experiment.py -k missing_toolchain -q`
    Expected: The smoke flow fails with a clear dependency message naming the missing compiler/runtime rather than a generic crash
    Evidence: .sisyphus/evidence/task-13-smoke-error.txt
  ```

  **Commit**: YES | Message: `test(e2e): add curated smoke corpus workflow` | Files: `corpus/solutions/**`, `tests/e2e/**`, `README.md`

## Final Verification Wave (MANDATORY - after ALL implementation tasks)
> 4 review agents run in PARALLEL. ALL must approve. Present consolidated results to user and get explicit "okay" before completing.
> Do NOT auto-proceed after verification. Wait for user's explicit approval before marking work complete.
> Never mark F1-F4 as checked before getting user's okay. Rejection or user feedback -> fix -> re-run -> present again -> wait for okay.
- [x] F1. Plan Compliance Audit - oracle

  **Tool**: Task (`oracle`)
  **Steps**: Ask Oracle to compare the implemented diff, test evidence, and run artifacts against `.sisyphus/plans/rtt-experiment-tool.md`; require a pass/fail list keyed by task number.
  **Expected**: Oracle reports no skipped tasks, no unmet guardrails, and no missing acceptance criteria.
  **Evidence**: `.sisyphus/evidence/f1-plan-compliance.md`

- [x] F2. Code Quality Review - unspecified-high

  **Tool**: Task (`unspecified-high`)
  **Steps**: Review changed source and tests for dead code, brittle abstractions, poor error handling, and duplicated logic; require exact file-level findings or an explicit approval.
  **Expected**: Reviewer returns either `APPROVED` or a concrete fix list; final completion requires `APPROVED`.
  **Evidence**: `.sisyphus/evidence/f2-code-quality.md`

- [x] F3. Real Manual QA - unspecified-high (+ playwright if UI)

  **Tool**: Task (`unspecified-high`) plus Bash
  **Steps**: Run the full verification command set from `Definition of Done`, inspect the generated smoke-run artifact tree, and compare report outputs against expected fields.
  **Expected**: All commands exit `0`, the smoke run produces `summary.json` and `summary.md`, and the reviewer confirms the artifacts are complete and readable.
  **Evidence**: `.sisyphus/evidence/f3-manual-qa.md`

- [x] F4. Scope Fidelity Check - deep

  **Tool**: Task (`deep`)
  **Steps**: Compare the shipped implementation to the original request, interview decisions, and guardrails; explicitly verify that v1 did not add extra providers, dashboards, hidden tests, or extra languages.
  **Expected**: Reviewer confirms scope fidelity and lists zero out-of-scope additions.
  **Evidence**: `.sisyphus/evidence/f4-scope-fidelity.md`

## Commit Strategy
- `chore: bootstrap python experiment project`
- `test: add schema and artifact contract coverage`
- `feat: add OpenAI translation and execution pipeline`
- `feat: add RTT metrics and report generation`
- `test: add smoke experiment coverage for curated corpus`

## Success Criteria
- A new contributor can clone the repo, install Python dependencies, add one curated C++ solution, and run a smoke experiment without guessing file layout or commands.
- Each run produces deterministic artifact paths and separates translation failures from metric outputs.
- At least one tiny curated corpus passes end-to-end tests with mocked translations and local compile/run evaluation.
- Report outputs make it obvious, per target language, whether the run converged, oscillated, failed semantically, or hit the iteration cap.
