2026-03-19
- Added a single config-level source of truth for seed file resolution via `REFERENCE_EXTENSION_BY_LANGUAGE` and `reference_filename_for_language(...)` to avoid scattered `reference.<ext>` literals.
- `seed_language` must be parsed before target validation so same-language rejection can be deterministic (`target_languages[i]` index included in the error).
- Corpus validation can stay language-agnostic once it delegates seed filename selection to config helpers.
- Directional v2 runs require `SUPPORTED_TARGET_LANGUAGES` to include `cpp`; otherwise reverse pairs like `python -> cpp` fail before same-language pair validation can apply.
2026-03-19
- CLI-level seed contract is now exercised through integration and e2e tests: same-language pair rejection is asserted via , and non-default  () validation succeeds when  exists.
- Smoke temp-config writers must explicitly serialize ; relying on inherited defaults is brittle once seed-aware config validation becomes strict.
2026-03-19
- CLI seed contract is now exercised through integration and e2e tests: validate-corpus asserts same-language pair rejection and also validates a non-default seed_language (python) path when reference.py exists.
- Smoke temp-config writers need to serialize seed_language explicitly so workflow configs stay valid under strict seed-aware validation.
2026-03-19
- Broad CLI integration can regress after config contract changes when older inline YAML fixtures omit newly required fields; include seed_language in every temp config builder, not only new seed-specific tests.
2026-03-19
- Artifact v2 directory identity now uses ordered-pair segments (`{seed_language}-to-{target_language}`), while explicit legacy helpers remain for target-only v1 reads.
- Iteration seed snapshots are now language-aware (`input.<seed-ext>` with `input_seed_source_path`), and resume validation branches by manifest schema (`run_manifest.v1` uses legacy key, `run_manifest.v2` requires the new key).
- Report manifest discovery now uses an explicit dual-path scan: v2 glob (`*/*-to-*/run.json`) plus legacy v1 target-only directories, rather than a single ambiguous glob.
2026-03-19
- Generic translation support is easiest to land with an additive seam: introduce explicit `source_language`/`target_language` prompt and client methods, then keep cpp-named wrappers for backward compatibility in untouched tests.
- Provider metadata should rely on explicit `source_language` and `target_language` fields; removing hard-coded `seed_language: cpp` avoids mismatched metadata when non-cpp pairs are configured.
- Pipeline can consume the generic contract without broad redesign by driving both legs through one helper (`seed -> target`, then `target -> seed`) while preserving existing artifact slot names and failure taxonomy.
2026-03-19
- Dual-state convergence can stay additive by composing existing single-history hash classifiers and a small truth-table reducer (`fixed_point` only when both fixed, `oscillation` if either oscillates, else `continue`).
- Residual similarity reporting needs explicit availability gating by `seed_language`; keeping cpp-token measurement unchanged while returning `unavailable(reason="seed_language_not_cpp")` prevents misleading null-style fallthrough.
2026-03-19
- Resume reconstruction must rebuild both histories directly from persisted artifacts (`roundtrip_source_path` for seed state and `translated_source_path` for target state); otherwise resumed runs can falsely classify `fixed_point` too early.
- Dual-state persistence is least disruptive when each iteration writes a backward-compatible `convergence_status` alias plus a structured `convergence` payload (`seed_state`, `target_state`, `overall`) in metrics and final/iteration details.
- Max-iteration terminal payloads should carry the same structured convergence object and history lengths, so downstream reporting/task7 can consume dual-state semantics without another schema break.
2026-03-19
- Final similarity artifacting is safest as a terminal-step persistence hook in pipeline (`run` and terminal `resume`), with source-hash idempotency checks to avoid duplicate embedding requests.
- OpenAI embedding provenance should explicitly separate configured model from observed response model and SDK request ids; there is no stable internal model revision id to persist.
- Report offline behavior is easiest to guarantee by reading only `metadata.final_similarity_artifact_path` (or default `final-similarity.json`) and returning `unavailable` when absent, never embedding on-demand.
2026-03-19
- Ordered-pair report aggregates are safest as an additive top-level map (`ordered_pair_aggregates`) keyed by `ordered_pair_key`, while preserving the full per-result `results` list for downstream consumers.
- Divergence denominator must be explicit (`denominator == measured_count`) and should only include measured outcomes (`success`, `oscillation`, `max_iter_no_convergence`), with infrastructure failures (`api_error`) split into separate unavailable/infrastructure counters.
- Markdown stays direction-aware and v1-readable by rendering ordered pairs from per-result identity when present and deriving fallback keys (`seed_language` default `cpp`) when old entries omit `ordered_pair_key`.
2026-03-19
- A deterministic non-default smoke seed path can run end-to-end without expanding corpus scope by generating a tiny temporary `reference.py` seed corpus for one existing smoke problem and reusing current persisted artifact/report flow.
- Mock transport matching is safer for mixed seed directions when fixture `match` includes explicit language metadata (`source_language`/`target_language`) for the non-default ordered pair, preventing overlap with existing `cpp`-seeded responses.
- Non-`cpp` seed smoke summaries still stay schema-v2 and report `residual_similarity` as unavailable (`seed_language_not_cpp`) while offline `final_similarity` can remain measured from persisted artifacts.
