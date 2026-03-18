# Current Measurement Notes

## Why this note exists

This repository already measures several useful quantities, but they are not exactly the same as the three questions below.

1. Repeated `C++ -> Python -> C++ -> Python ...` transformation process
2. Distance as the number of `C++ -> Python` changes
3. Similarity between the original C++ and the transformed C++

This note maps the current implementation to those three questions.

## Update for current repo state

This note originally described the early `cpp`-seed-only implementation. The current repository now supports configurable `seed_language`, ordered-pair artifact paths (`seed-to-target`), dual-state convergence (`seed_state`, `target_state`, `overall`), and a persisted embedding-based `final_similarity` artifact for the final comparison step.

Two important consequences:

- `residual_similarity` remains a `cpp`-token metric and is only measured when `seed_language == "cpp"`.
- For non-`cpp` seeds, the final comparison signal is the persisted embedding-based `final_similarity`, which `report` reads offline from artifacts.

## Quick answer

- Question 1: implemented
- Question 2: implemented in a simple form
- Question 3: implemented, but with a specific token-based definition

## 1. Repeated `C++ -> Python -> C++ -> Python ...` process

This is implemented.

The main loop is `run_rtt_loop()` in `src/rttdist/pipeline.py`.

At each iteration, the pipeline does this:

1. Take the current C++ source as input
2. Translate `C++ -> target language`
3. Execute the target-language code on all sample fixtures
4. Translate `target language -> C++`
5. Execute the round-trip C++ code on all sample fixtures
6. Compute residual similarity and convergence status
7. If convergence is not reached, use the new C++ as the next iteration input

So when `target_language="python"`, the actual behavior is:

`C++ -> Python -> C++ -> Python -> C++ -> ...`

Relevant code:

- `src/rttdist/pipeline.py:106` - `run_rtt_loop()`
- `src/rttdist/pipeline.py:226` - `translate_cpp_to_target()` call
- `src/rttdist/pipeline.py:285` - `translate_target_to_cpp()` call
- `src/rttdist/pipeline.py:381` - next-iteration C++ update

## 2. Distance as the number of `C++ -> Python` changes

This is now implemented in a **simple cycle-count form**.

The current repository defines change-count distance as:

> `C++ -> target -> C++` 왕복 1회를 거리 1로 계산한다.

So if `target_language="python"`, then:

- first completed `C++ -> Python -> C++` cycle = distance 1
- second completed cycle = distance 2
- third completed cycle = distance 3
- if the run fails before the round-trip back to C++ is produced, that iteration does not count as a completed cycle

This means the current implementation does **not** count low-level edits inside the conversion.
It counts the number of completed round-trip transformation cycles.

Relevant code:

- `src/rttdist/pipeline.py:192` - one iteration loop
- `src/rttdist/reporting.py` - summary field `change_count_distance`

### What is still NOT implemented?

The following is still missing:

- literal edit-operation count between C++ and Python
- AST-edit count specifically for the `C++ -> Python` leg alone
- token-edit count for a single translation leg

So the current metric is intentionally simple:

- `change_count_distance = completed RTT cycle count`
- an iteration that stops before round-trip C++ is produced contributes `0` additional distance

## 3. Similarity between original C++ and transformed C++

This is implemented.

The current implementation compares:

- original seed C++
- the current round-trip C++ produced at each iteration

The similarity is called `residual_similarity`.

Relevant code:

- `src/rttdist/fixed_point.py:27` - `compute_residual_similarity()`
- `src/rttdist/normalize.py:64` - `cpp_token_sorensen_dice_similarity()`

## What "residual similarity" actually means

It is **not** raw string equality.

Instead, the current code does this:

1. Normalize both C++ programs into token sequences
2. Remove comments and insignificant whitespace effects
3. Treat the normalized C++ token sequences as multisets
4. Compute Sorensen-Dice similarity over those token multisets

This means the similarity is:

> "How much overlap exists between the normalized C++ token multisets?"

So a score of `1.0` means the normalized C++ token multiset is identical, not necessarily that the original raw source text is byte-for-byte the same.

## What "fixed point" means in this code

The code does **not** use a BLEU-like threshold.

Instead, fixed point is defined as:

- hash the normalized C++ tokens
- if the last two hashes are equal, status is `fixed_point`

Oscillation is defined as a 2-cycle:

- `A, B, A, B` with `A != B`

Relevant code:

- `src/rttdist/fixed_point.py:13` - `classify_hash_history()`
- `src/rttdist/fixed_point.py:33` - adjacent fixed point rule
- `src/rttdist/fixed_point.py:39` - 2-cycle oscillation rule

## Mapping current implementation to research terms

### Already present

- RTT process
- convergence iteration count
- fixed point / oscillation detection
- residual similarity between seed C++ and round-trip C++
- cross-language AST distance
- complexity delta
- semantic preservation via sample I/O execution

### Missing if you want a richer version later

- a per-leg edit-count metric for `C++ -> Python`
- a cumulative AST-edit metric across iterations
- an explicit distinction between:
  - cycle-count distance
  - cross-language AST edit distance
  - residual similarity

## Recommended interpretation

For now, read the metrics like this:

- `change_count_distance` -> how many full RTT cycles were needed
- `residual_similarity` -> how close the final round-trip C++ is to the original C++
- `ast_distance` -> how structurally different the target representation is
