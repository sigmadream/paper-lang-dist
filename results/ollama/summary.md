# Run Summary: smoke-ollama-001

| Problem | Ordered pair | Final status | Iterations | Change-count distance | Convergence | Residual similarity | MOSS similarity | Semantic | AST distance to seed |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- | --- |
| IPOP_1436 | cpp->c | timeout | 1 | 0 | terminated_on_failure | unavailable (timeout at target_execution) | unavailable (timeout at target_execution) | fail | unavailable (timeout at target_execution) |
| IPOP_1436 | cpp->java | success | 2 | 2 | fixed_point | 0.872727 | seed=64%, roundtrip=76% | pass | 12 |
| IPOP_1436 | cpp->python | success | 3 | 3 | fixed_point | 0.812500 | seed=0%, roundtrip=0% | pass | 33 |
| IPOP_2110 | cpp->c | success | 2 | 2 | fixed_point | 0.863544 | seed=44%, roundtrip=39% | pass | 38 |
| IPOP_2110 | cpp->java | oscillation | 4 | 4 | oscillation | 0.841629 | seed=44%, roundtrip=47% | pass | 32 |
| IPOP_2110 | cpp->python | success | 3 | 3 | fixed_point | 0.897704 | seed=0%, roundtrip=0% | pass | 66 |
| IPOP_2217 | cpp->c | success | 2 | 2 | fixed_point | 0.827195 | seed=0%, roundtrip=0% | pass | 34 |
| IPOP_2217 | cpp->java | wrong_answer | 1 | 0 | terminated_on_failure | unavailable (wrong_answer at target_execution) | unavailable (wrong_answer at target_execution) | fail | unavailable (wrong_answer at target_execution) |
| IPOP_2217 | cpp->python | success | 2 | 2 | fixed_point | 0.881657 | seed=0%, roundtrip=0% | pass | 51 |
| IPOP_2579 | cpp->c | wrong_answer | 1 | 0 | terminated_on_failure | unavailable (wrong_answer at target_execution) | unavailable (wrong_answer at target_execution) | fail | unavailable (wrong_answer at target_execution) |
| IPOP_2579 | cpp->java | success | 2 | 2 | fixed_point | 0.932976 | seed=70%, roundtrip=76% | pass | 15 |
| IPOP_2579 | cpp->python | runtime_error | 2 | 1 | terminated_on_failure | unavailable (runtime_error at target_execution) | unavailable (runtime_error at target_execution) | fail | unavailable (runtime_error at target_execution) |
| IPOP_5567 | cpp->c | oscillation | 5 | 5 | oscillation | 0.853282 | seed=14%, roundtrip=12% | pass | 60 |
| IPOP_5567 | cpp->java | success | 3 | 3 | fixed_point | 0.928270 | seed=77%, roundtrip=85% | pass | 49 |
| IPOP_5567 | cpp->python | runtime_error | 1 | 0 | terminated_on_failure | unavailable (runtime_error at target_execution) | unavailable (runtime_error at target_execution) | fail | unavailable (runtime_error at target_execution) |

## Ordered-pair aggregates

| Ordered pair | Results | Divergence rate | Measured divergence count | Unavailable divergence count | Infrastructure divergence count |
| --- | ---: | --- | ---: | ---: | ---: |
| cpp->c | 5 | 0.333333 | 3 | 2 | 0 |
| cpp->java | 5 | 0.250000 | 4 | 1 | 0 |
| cpp->python | 5 | 0.000000 | 3 | 2 | 0 |

### Ordered pair: cpp->c

- Change-count distance aggregate: mean=1.800000, stddev=1.833030, measured=5, unavailable=0, infrastructure=0
- Residual similarity aggregate: mean=0.848007, stddev=0.015301, measured=3, unavailable=2, infrastructure=0
- Final similarity score aggregate: unavailable (measured=0, unavailable=5, infrastructure=0)
- Divergence aggregate: rate=0.333333, divergent=1, non_divergent=2, measured=3, unavailable=2, infrastructure=0

### Ordered pair: cpp->java

- Change-count distance aggregate: mean=2.200000, stddev=1.326650, measured=5, unavailable=0, infrastructure=0
- Residual similarity aggregate: mean=0.893901, stddev=0.038369, measured=4, unavailable=1, infrastructure=0
- Final similarity score aggregate: unavailable (measured=0, unavailable=5, infrastructure=0)
- Divergence aggregate: rate=0.250000, divergent=1, non_divergent=3, measured=4, unavailable=1, infrastructure=0

### Ordered pair: cpp->python

- Change-count distance aggregate: mean=1.800000, stddev=1.166190, measured=5, unavailable=0, infrastructure=0
- Residual similarity aggregate: mean=0.863953, stddev=0.036968, measured=3, unavailable=2, infrastructure=0
- Final similarity score aggregate: unavailable (measured=0, unavailable=5, infrastructure=0)
- Divergence aggregate: rate=0.000000, divergent=0, non_divergent=3, measured=3, unavailable=2, infrastructure=0

## IPOP_1436 / cpp->c

- Ordered pair: cpp->c
- Final status: timeout
- Iteration count: 1
- Change-count distance (1 cycle = C++ -> target -> C++): 0
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (timeout at target_execution)
- MOSS similarity to seed C++: unavailable (timeout at target_execution)
- Semantic summary: fail (target=timeout, roundtrip_cpp=not_evaluated)
- AST distance: unavailable (timeout at target_execution)
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-3, max_nesting_depth=0, token_count=-16]
- Roundtrip C++ complexity deltas: unavailable (timeout at target_execution)

## IPOP_1436 / cpp->java

- Ordered pair: cpp->java
- Final status: success
- Iteration count: 2
- Change-count distance (1 cycle = C++ -> target -> C++): 2
- Convergence outcome: fixed_point
- Residual similarity to seed C++: 0.872727
- MOSS similarity to seed C++: seed=64%, roundtrip=76%
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=12, distance_to_roundtrip_cpp=10
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-3, max_nesting_depth=0, token_count=4]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-3, max_nesting_depth=0, token_count=-16]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]

## IPOP_1436 / cpp->python

- Ordered pair: cpp->python
- Final status: success
- Iteration count: 3
- Change-count distance (1 cycle = C++ -> target -> C++): 3
- Convergence outcome: fixed_point
- Residual similarity to seed C++: 0.812500
- MOSS similarity to seed C++: seed=0%, roundtrip=0%
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=33, distance_to_roundtrip_cpp=20
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-8, max_nesting_depth=0, token_count=-36]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=1, function_count=1, loc=0, max_nesting_depth=0, token_count=8]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]

## IPOP_2110 / cpp->c

- Ordered pair: cpp->c
- Final status: success
- Iteration count: 2
- Change-count distance (1 cycle = C++ -> target -> C++): 2
- Convergence outcome: fixed_point
- Residual similarity to seed C++: 0.863544
- MOSS similarity to seed C++: seed=44%, roundtrip=39%
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=38, distance_to_roundtrip_cpp=13
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=1, loc=-1, max_nesting_depth=-1, token_count=5]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=1, loc=0, max_nesting_depth=-1, token_count=17]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]

## IPOP_2110 / cpp->java

- Ordered pair: cpp->java
- Final status: oscillation
- Iteration count: 4
- Change-count distance (1 cycle = C++ -> target -> C++): 4
- Convergence outcome: oscillation
- Residual similarity to seed C++: 0.841629
- MOSS similarity to seed C++: seed=44%, roundtrip=47%
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=32, distance_to_roundtrip_cpp=18
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=-1, function_count=0, loc=1, max_nesting_depth=-3, token_count=12]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=1, max_nesting_depth=0, token_count=6]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=-1, function_count=0, loc=-2, max_nesting_depth=-3, token_count=-30]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=-1, max_nesting_depth=0, token_count=1]

## IPOP_2110 / cpp->python

- Ordered pair: cpp->python
- Final status: success
- Iteration count: 3
- Change-count distance (1 cycle = C++ -> target -> C++): 3
- Convergence outcome: fixed_point
- Residual similarity to seed C++: 0.897704
- MOSS similarity to seed C++: seed=0%, roundtrip=0%
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=66, distance_to_roundtrip_cpp=60
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=-1, function_count=0, loc=-8, max_nesting_depth=1, token_count=-63]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=-1, function_count=0, loc=1, max_nesting_depth=-3, token_count=5]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]

## IPOP_2217 / cpp->c

- Ordered pair: cpp->c
- Final status: success
- Iteration count: 2
- Change-count distance (1 cycle = C++ -> target -> C++): 2
- Convergence outcome: fixed_point
- Residual similarity to seed C++: 0.827195
- MOSS similarity to seed C++: seed=0%, roundtrip=0%
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=34, distance_to_roundtrip_cpp=14
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=1, loc=-1, max_nesting_depth=-1, token_count=0]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=1, loc=0, max_nesting_depth=-1, token_count=17]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]

## IPOP_2217 / cpp->java

- Ordered pair: cpp->java
- Final status: wrong_answer
- Iteration count: 1
- Change-count distance (1 cycle = C++ -> target -> C++): 0
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (wrong_answer at target_execution)
- MOSS similarity to seed C++: unavailable (wrong_answer at target_execution)
- Semantic summary: fail (target=wrong_answer, roundtrip_cpp=not_evaluated)
- AST distance: unavailable (wrong_answer at target_execution)
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=-1, function_count=0, loc=-3, max_nesting_depth=-1, token_count=-9]
- Roundtrip C++ complexity deltas: unavailable (wrong_answer at target_execution)

## IPOP_2217 / cpp->python

- Ordered pair: cpp->python
- Final status: success
- Iteration count: 2
- Change-count distance (1 cycle = C++ -> target -> C++): 2
- Convergence outcome: fixed_point
- Residual similarity to seed C++: 0.881657
- MOSS similarity to seed C++: seed=0%, roundtrip=0%
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=51, distance_to_roundtrip_cpp=48
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=-2, function_count=0, loc=-9, max_nesting_depth=0, token_count=-65]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=-1, function_count=0, loc=-1, max_nesting_depth=-1, token_count=2]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]

## IPOP_2579 / cpp->c

- Ordered pair: cpp->c
- Final status: wrong_answer
- Iteration count: 1
- Change-count distance (1 cycle = C++ -> target -> C++): 0
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (wrong_answer at target_execution)
- MOSS similarity to seed C++: unavailable (wrong_answer at target_execution)
- Semantic summary: fail (target=wrong_answer, roundtrip_cpp=not_evaluated)
- AST distance: unavailable (wrong_answer at target_execution)
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=1, function_count=0, loc=-6, max_nesting_depth=0, token_count=-17]
- Roundtrip C++ complexity deltas: unavailable (wrong_answer at target_execution)

## IPOP_2579 / cpp->java

- Ordered pair: cpp->java
- Final status: success
- Iteration count: 2
- Change-count distance (1 cycle = C++ -> target -> C++): 2
- Convergence outcome: fixed_point
- Residual similarity to seed C++: 0.932976
- MOSS similarity to seed C++: seed=70%, roundtrip=76%
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=15, distance_to_roundtrip_cpp=13
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-4, max_nesting_depth=0, token_count=9]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-3, max_nesting_depth=0, token_count=-20]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]

## IPOP_2579 / cpp->python

- Ordered pair: cpp->python
- Final status: runtime_error
- Iteration count: 2
- Change-count distance (1 cycle = C++ -> target -> C++): 1
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (runtime_error at target_execution)
- MOSS similarity to seed C++: unavailable (runtime_error at target_execution)
- Semantic summary: fail (target=runtime_error, roundtrip_cpp=not_evaluated)
- AST distance: unavailable (runtime_error at target_execution)
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=-1, function_count=0, loc=-12, max_nesting_depth=1, token_count=-42]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=-2, max_nesting_depth=-1, token_count=-4]
- Roundtrip C++ complexity deltas: unavailable (runtime_error at target_execution)

## IPOP_5567 / cpp->c

- Ordered pair: cpp->c
- Final status: oscillation
- Iteration count: 5
- Change-count distance (1 cycle = C++ -> target -> C++): 5
- Convergence outcome: oscillation
- Residual similarity to seed C++: 0.853282
- MOSS similarity to seed C++: seed=14%, roundtrip=12%
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=60, distance_to_roundtrip_cpp=43
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=1, function_count=0, loc=-2, max_nesting_depth=-1, token_count=7]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=1, max_nesting_depth=0, token_count=2]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-3, max_nesting_depth=-1, token_count=16]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=-1, max_nesting_depth=0, token_count=12]

## IPOP_5567 / cpp->java

- Ordered pair: cpp->java
- Final status: success
- Iteration count: 3
- Change-count distance (1 cycle = C++ -> target -> C++): 3
- Convergence outcome: fixed_point
- Residual similarity to seed C++: 0.928270
- MOSS similarity to seed C++: seed=77%, roundtrip=85%
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=49, distance_to_roundtrip_cpp=50
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=1, max_nesting_depth=-1, token_count=57]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=-1, function_count=0, loc=-2, max_nesting_depth=-1, token_count=-25]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]

## IPOP_5567 / cpp->python

- Ordered pair: cpp->python
- Final status: runtime_error
- Iteration count: 1
- Change-count distance (1 cycle = C++ -> target -> C++): 0
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (runtime_error at target_execution)
- MOSS similarity to seed C++: unavailable (runtime_error at target_execution)
- Semantic summary: fail (target=runtime_error, roundtrip_cpp=not_evaluated)
- AST distance: unavailable (runtime_error at target_execution)
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-14, max_nesting_depth=3, token_count=-69]
- Roundtrip C++ complexity deltas: unavailable (runtime_error at target_execution)
