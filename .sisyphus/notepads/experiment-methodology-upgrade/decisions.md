2026-03-19
- Promoted summary schema to `report_summary.v2` while preserving legacy read behavior in reporting by defaulting missing `metadata.seed_language` to `cpp` for old manifests.
- Added explicit run manifest schema constants in run-state and ensured new/recovered manifests write `run_manifest.v2`; normalization preserves `run_manifest.v1` when present.
- Extended resume identity validation and status transitions to include `seed_language` alongside `target_language`.
- Expanded `SUPPORTED_TARGET_LANGUAGES` to include `cpp` so directional reverse configs (e.g., `seed_language: python`, `target_languages: [cpp]`) are valid under task-1 contract.
2026-03-19
- Kept CLI verbs/options unchanged and threaded seed-awareness through existing paths by validating/serializing  in tests rather than introducing new CLI flags.
- Added an explicit  line in  success output to make seed selection visible during CLI validation without altering command semantics.
2026-03-19
- Preserved existing CLI verbs/options and pushed seed-awareness through current config-loading and validation paths via tests rather than adding flags.
- Added a validate-corpus success line that prints the selected seed language for clearer CLI-facing validation feedback without changing command semantics.
2026-03-19
- Fixed task-2 QA by minimally patching the existing missing-model CLI fixture to set seed_language: cpp, preserving command verbs/options and keeping scope confined to test fixture validity.
2026-03-19
- Chose explicit path-selection in pipeline resume (`_select_run_paths_for_resume`) with precedence v2 then v1, so new runs default to ordered-pair directories while existing legacy artifacts remain resumable without silent path reinterpretation.
- Kept legacy v1 support isolated to dedicated helpers/branches (`build_legacy_run_directory`, schema-key branching in run_state, legacy manifest discovery in reporting) to prevent accidental v1/v2 contract blending.
2026-03-19
- Adopted `build_translation_prompt(...)` as the explicit prompt contract and routed provider generic methods through it, while retaining cpp-specific wrapper functions/methods as compatibility adapters.
- Standardized request metadata for translation calls to explicit language pairs (`source_language`, `target_language`) and dropped hard-coded cpp metadata fields.
- Updated pipeline leg execution to use explicit ordered pairs (`config.seed_language -> target_language`, then `target_language -> config.seed_language`) via a single translation helper, with legacy cpp-only client fallback kept only for compatibility.
2026-03-19
- Added explicit dual-state convergence primitives in fixed-point (`classify_dual_hash_histories`, `classify_dual_cpp_histories`, `classify_overall_convergence`) while preserving legacy single-state helpers and normalized-hash fixed/2-cycle detection logic.
- Updated report residual similarity policy to gate on `seed_language == "cpp"`; non-cpp seed runs now emit `availability: unavailable` with reason `seed_language_not_cpp` rather than defaulting to `residual_similarity_not_recorded`.
2026-03-19
- Refactored pipeline/run-state resume contract to persist and restore both seed and target histories, with dual-state convergence classified via task-5 helpers and persisted as structured convergence metadata.
- Tightened resume identity safety for schema-v2 artifacts by validating ordered-pair manifest identity fields (`run_directory`, `run_metadata_path`) in addition to run/problem/language checksums.
- Kept convergence payload migration additive by retaining `convergence_status` as an overall alias while introducing `convergence.{seed_state,target_state,overall}` for task7/report consumers.
2026-03-19
- Added a small embedding seam (`EmbeddingProvider`) and implemented OpenAI MVP in `openai_client` with normalized embedding response parsing, request-id capture, and provider/model/dimension constraints.
- Persisted terminal final similarity as a dedicated run artifact (`final-similarity.json`) keyed by source hashes and enriched with provenance (`provider`, configured/observed model evidence, request ids, usage, dimensions).
- Kept report generation offline by consuming persisted final-similarity artifacts only and surfacing measured/unavailable states without any network fallback.
2026-03-19
- Extended `report_summary.v2` to emit both per-result entries and ordered-pair aggregate sections under `ordered_pair_aggregates`, keyed by `ordered_pair_key` so reverse directions (`A->B`, `B->A`) are never merged.
- Standardized aggregate payload envelopes with explicit availability and denominator semantics (`denominator == measured_count`) across change-count, residual similarity, final-similarity score, and divergence statistics.
- Kept legacy readability by preserving `results` shape and making markdown rendering derive ordered-pair identity when older entries do not carry `ordered_pair_key`.
2026-03-19
- For task-9 smoke coverage, added a single non-default success path (`python -> cpp`) in `tests/e2e/test_smoke_experiment.py` using a temporary one-problem seed corpus so the checked-in corpus remains minimal.
- Extended `tests/fixtures/e2e/smoke_openai_responses.json` with explicit non-default directional metadata and constrained existing roundtrip matches by `target_language: cpp` to avoid stale/misrouted fixture hits.
- Added resume integration coverage for manifest identity tampering on `metadata.seed_language` so stale seed-aware manifests fail fast with `seed_language mismatch`.
