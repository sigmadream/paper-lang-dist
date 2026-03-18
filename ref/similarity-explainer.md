# Similarity Explainer

## Why this note exists

The current repository uses the word "similarity" in a precise technical sense.

If you read a report and see values such as:

- `residual_similarity = 1.0`
- `fixed_point`
- `AST distance = 29`

that does **not** mean the same thing as "the code looks identical to me."

This note explains what each quantity means in plain language.

## 1. Residual similarity

### Plain-language definition

Residual similarity answers this question:

> After round-trip translation, how similar is the final C++ to the original C++?

### How this repository computes it

The implementation is in:

- `src/rttdist/fixed_point.py:27`
- `src/rttdist/normalize.py:64`

The steps are:

1. Normalize the original C++ into tokens
2. Normalize the round-trip C++ into tokens
3. Ignore comments and insignificant whitespace effects
4. Compare the two token multisets with Sorensen-Dice similarity

### Important consequence

This means:

- it is more robust than raw string comparison
- it is still syntax-level, not semantic proof
- `1.0` means the normalized token multiset is identical
- `1.0` does **not** necessarily mean the exact original formatting survived

## 2. What is Sorensen-Dice similarity?

### Intuition

Sorensen-Dice asks:

> How much overlap do two collections have, relative to their total size?

If two token collections are identical, the score is `1.0`.
If they barely overlap, the score approaches `0.0`.

### Current implementation detail

The current code uses **multiset** overlap, not simple set overlap.

That means repeated tokens still matter.

For example, if one program repeats `return` or `i` many times and the other does not, the score changes.

This is implemented in:

- `src/rttdist/normalize.py:64`

### Why this is useful

For code, multiset overlap is often better than plain set overlap because repeated operators, identifiers, and literals carry real structural information.

## 3. Fixed point

### Plain-language definition

Fixed point means:

> The round-trip translation has stabilized, so doing one more iteration does not change the normalized C++ anymore.

### How this repository computes it

Implementation:

- `src/rttdist/fixed_point.py:13`
- `src/rttdist/fixed_point.py:21`

The steps are:

1. Normalize the C++ tokens
2. Hash the normalized token sequence
3. Compare the newest two hashes
4. If they are equal, the status is `fixed_point`

So the repository uses **hash equality of normalized C++ tokens**, not a fuzzy threshold such as "less than 2% changed."

## 4. Oscillation

### Plain-language definition

Oscillation means:

> The translation does not settle to one stable output, but keeps bouncing between two forms.

### Current rule

Implementation:

- `src/rttdist/fixed_point.py:39`

The repository detects a 2-cycle:

- `A, B, A, B`
- with `A != B`

If that pattern appears in the normalized C++ hash history, the status becomes `oscillation`.

## 5. AST distance

### Plain-language definition

AST distance asks:

> How different are the program structures, ignoring many surface-level syntax details?

### How this repository computes it

Implementation:

- `src/rttdist/ast_ir.py`
- `src/rttdist/ast_metrics.py:30`

The steps are:

1. Parse each program using `tree-sitter`
2. Convert the language-specific AST into a shared IR
3. Compute tree edit distance with `apted`

This is important because comparing raw parser node labels across C++, Python, Java, and C would be noisy and language-specific.

## 6. Why a high residual similarity does not mean everything is the same

Suppose a report says:

- residual similarity: high
- AST distance: non-zero
- complexity deltas: non-zero

That means:

- the final round-trip C++ stayed close to the original at the token level
- but the intermediate target-language code still changed structure and complexity

So you should read the metrics together, not in isolation.

## 7. Change-count distance in the current repository

The repository now exposes a simple change-count distance.

Its definition is:

> `C++ -> target -> C++` 왕복 1회를 거리 1로 계산한다.

So if Python is the target language:

- first completed `C++ -> Python -> C++` cycle -> distance 1
- second completed cycle -> distance 2
- third completed cycle -> distance 3

This is easy to interpret, but it is intentionally simple.

It is **not** the same thing as:

- token edit count
- AST edit count for a single leg
- statement rewrite count

So you should treat it as a convergence-distance style number, not a fine-grained edit-distance number.

## 8. Practical reading guide

When you look at a result, read it like this:

### If `fixed_point` is reached quickly

- the translation stabilized quickly
- the two languages may be relatively easy for the current model to round-trip between

### If `residual_similarity` is high

- the final round-trip C++ stayed close to the seed C++

### If AST distance is still large

- the target-language representation may still be structurally quite different

### If semantic checks pass

- despite structural or lexical changes, the translated code still solves the sample tests

## 9. Suggested mental model

Use the current metrics like this:

- `iteration count` / `change_count_distance` -> stability distance in whole RTT cycles
- `residual similarity` -> seed vs final round-trip closeness
- `AST distance` -> structural difference
- `complexity delta` -> conciseness / control-flow difference
- `semantic summary` -> whether behavior still looks correct on samples

That is the safest way to interpret the current reports.
