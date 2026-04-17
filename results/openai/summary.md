# Run Summary: smoke-openai-001

| Problem | Ordered pair | Final status | Iterations | Change-count distance | Convergence | Residual similarity | MOSS similarity | Semantic | AST distance to seed |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- | --- |
| IPOP_1436 | cpp->c | success | 2 | 2 | fixed_point | 0.564103 | seed=0%, roundtrip=0% | pass | 42 |
| IPOP_1436 | cpp->java | compile_error | 2 | 2 | terminated_on_failure | unavailable (compile_error at roundtrip_execution) | seed=81%, roundtrip=86% | fail | 17 |
| IPOP_1436 | cpp->python | compile_error | 1 | 1 | terminated_on_failure | unavailable (compile_error at roundtrip_execution) | seed=0%, roundtrip=0% | fail | 28 |
| IPOP_2110 | cpp->c | success | 4 | 4 | fixed_point | 0.826613 | seed=44%, roundtrip=40% | pass | 51 |
| IPOP_2110 | cpp->java | parse_error | 1 | 0 | terminated_on_failure | unavailable (parse_error at target_to_cpp_translation) | unavailable (parse_error at target_to_cpp_translation) | fail | unavailable (parse_error at target_to_cpp_translation) |
| IPOP_2110 | cpp->python | compile_error | 1 | 1 | terminated_on_failure | unavailable (compile_error at roundtrip_execution) | seed=33%, roundtrip=32% | fail | 71 |
| IPOP_2217 | cpp->c | success | 16 | 16 | fixed_point | 0.765027 | seed=31%, roundtrip=26% | pass | 41 |
| IPOP_2217 | cpp->java | compile_error | 1 | 1 | terminated_on_failure | unavailable (compile_error at roundtrip_execution) | seed=0%, roundtrip=0% | fail | 93 |
| IPOP_2217 | cpp->python | compile_error | 1 | 1 | terminated_on_failure | unavailable (compile_error at roundtrip_execution) | seed=34%, roundtrip=36% | fail | 54 |
| IPOP_2579 | cpp->c | success | 2 | 2 | fixed_point | 0.782178 | seed=52%, roundtrip=49% | pass | 26 |
| IPOP_2579 | cpp->java | parse_error | 1 | 0 | terminated_on_failure | unavailable (parse_error at target_to_cpp_translation) | unavailable (parse_error at target_to_cpp_translation) | fail | unavailable (parse_error at target_to_cpp_translation) |
| IPOP_2579 | cpp->python | compile_error | 1 | 1 | terminated_on_failure | unavailable (compile_error at roundtrip_execution) | seed=61%, roundtrip=53% | fail | 49 |
| IPOP_5567 | cpp->c | success | 3 | 3 | fixed_point | 0.544489 | seed=0%, roundtrip=0% | pass | 125 |
| IPOP_5567 | cpp->java | compile_error | 1 | 1 | terminated_on_failure | unavailable (compile_error at roundtrip_execution) | seed=29%, roundtrip=90% | fail | 121 |
| IPOP_5567 | cpp->python | compile_error | 1 | 1 | terminated_on_failure | unavailable (compile_error at roundtrip_execution) | seed=54%, roundtrip=37% | fail | 81 |

## Ordered-pair aggregates

| Ordered pair | Results | Divergence rate | Measured divergence count | Unavailable divergence count | Infrastructure divergence count |
| --- | ---: | --- | ---: | ---: | ---: |
| cpp->c | 5 | 0.000000 | 5 | 0 | 0 |
| cpp->java | 5 | unavailable | 0 | 5 | 0 |
| cpp->python | 5 | unavailable | 0 | 5 | 0 |

### Ordered pair: cpp->c

- Change-count distance aggregate: mean=5.400000, stddev=5.351635, measured=5, unavailable=0, infrastructure=0
- Residual similarity aggregate: mean=0.696482, stddev=0.117985, measured=5, unavailable=0, infrastructure=0
- Final similarity score aggregate: mean=0.857056, stddev=0.028325, measured=5, unavailable=0, infrastructure=0
- Divergence aggregate: rate=0.000000, divergent=0, non_divergent=5, measured=5, unavailable=0, infrastructure=0

### Ordered pair: cpp->java

- Change-count distance aggregate: mean=0.800000, stddev=0.748331, measured=5, unavailable=0, infrastructure=0
- Residual similarity aggregate: unavailable (measured=0, unavailable=5, infrastructure=0)
- Final similarity score aggregate: mean=0.625492, stddev=0.353565, measured=3, unavailable=2, infrastructure=0
- Divergence aggregate: unavailable (measured=0, unavailable=5, infrastructure=0)

### Ordered pair: cpp->python

- Change-count distance aggregate: mean=1.000000, stddev=0.000000, measured=5, unavailable=0, infrastructure=0
- Residual similarity aggregate: unavailable (measured=0, unavailable=5, infrastructure=0)
- Final similarity score aggregate: mean=0.923921, stddev=0.038034, measured=5, unavailable=0, infrastructure=0
- Divergence aggregate: unavailable (measured=0, unavailable=5, infrastructure=0)

## IPOP_1436 / cpp->c

- Ordered pair: cpp->c
- Final status: success
- Iteration count: 2
- Change-count distance (1 cycle = C++ -> target -> C++): 2
- Convergence outcome: fixed_point
- Residual similarity to seed C++: 0.564103
- MOSS similarity to seed C++: seed=0%, roundtrip=0%
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=42, distance_to_roundtrip_cpp=0
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=6, function_count=1, loc=10, max_nesting_depth=1, token_count=47]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=6, function_count=1, loc=10, max_nesting_depth=1, token_count=51]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]

## IPOP_1436 / cpp->java

- Ordered pair: cpp->java
- Final status: compile_error
- Iteration count: 2
- Change-count distance (1 cycle = C++ -> target -> C++): 2
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (compile_error at roundtrip_execution)
- MOSS similarity to seed C++: seed=81%, roundtrip=86%
- Semantic summary: fail (target=success, roundtrip_cpp=compile_error)
- AST distance: distance_to_seed_cpp=17, distance_to_roundtrip_cpp=17
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-2, max_nesting_depth=0, token_count=26]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-1, max_nesting_depth=0, token_count=-5]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=-1, max_nesting_depth=0, token_count=-2]

## IPOP_1436 / cpp->python

- Ordered pair: cpp->python
- Final status: compile_error
- Iteration count: 1
- Change-count distance (1 cycle = C++ -> target -> C++): 1
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (compile_error at roundtrip_execution)
- MOSS similarity to seed C++: seed=0%, roundtrip=0%
- Semantic summary: fail (target=success, roundtrip_cpp=compile_error)
- AST distance: distance_to_seed_cpp=28, distance_to_roundtrip_cpp=34
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-6, max_nesting_depth=0, token_count=-17]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=1, function_count=0, loc=0, max_nesting_depth=1, token_count=16]

## IPOP_2110 / cpp->c

- Ordered pair: cpp->c
- Final status: success
- Iteration count: 4
- Change-count distance (1 cycle = C++ -> target -> C++): 4
- Convergence outcome: fixed_point
- Residual similarity to seed C++: 0.826613
- MOSS similarity to seed C++: seed=44%, roundtrip=40%
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=51, distance_to_roundtrip_cpp=19
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=4, function_count=1, loc=5, max_nesting_depth=1, token_count=72]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=1, function_count=0, loc=-1, max_nesting_depth=1, token_count=17]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]

## IPOP_2110 / cpp->java

- Ordered pair: cpp->java
- Final status: parse_error
- Iteration count: 1
- Change-count distance (1 cycle = C++ -> target -> C++): 0
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (parse_error at target_to_cpp_translation)
- MOSS similarity to seed C++: unavailable (parse_error at target_to_cpp_translation)
- Semantic summary: fail (target=success, roundtrip_cpp=not_evaluated)
- AST distance: unavailable (parse_error at target_to_cpp_translation)
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=9, function_count=2, loc=32, max_nesting_depth=1, token_count=229]
- Roundtrip C++ complexity deltas: unavailable (parse_error at target_to_cpp_translation)

## IPOP_2110 / cpp->python

- Ordered pair: cpp->python
- Final status: compile_error
- Iteration count: 1
- Change-count distance (1 cycle = C++ -> target -> C++): 1
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (compile_error at roundtrip_execution)
- MOSS similarity to seed C++: seed=33%, roundtrip=32%
- Semantic summary: fail (target=success, roundtrip_cpp=compile_error)
- AST distance: distance_to_seed_cpp=71, distance_to_roundtrip_cpp=71
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=-1, function_count=0, loc=-7, max_nesting_depth=1, token_count=-53]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-2, max_nesting_depth=0, token_count=2]

## IPOP_2217 / cpp->c

- Ordered pair: cpp->c
- Final status: success
- Iteration count: 16
- Change-count distance (1 cycle = C++ -> target -> C++): 16
- Convergence outcome: fixed_point
- Residual similarity to seed C++: 0.765027
- MOSS similarity to seed C++: seed=31%, roundtrip=26%
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=41, distance_to_roundtrip_cpp=7
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=2, function_count=1, loc=3, max_nesting_depth=1, token_count=41]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=2, function_count=1, loc=2, max_nesting_depth=1, token_count=26]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]

## IPOP_2217 / cpp->java

- Ordered pair: cpp->java
- Final status: compile_error
- Iteration count: 1
- Change-count distance (1 cycle = C++ -> target -> C++): 1
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (compile_error at roundtrip_execution)
- MOSS similarity to seed C++: seed=0%, roundtrip=0%
- Semantic summary: fail (target=success, roundtrip_cpp=compile_error)
- AST distance: distance_to_seed_cpp=93, distance_to_roundtrip_cpp=109
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=9, function_count=3, loc=36, max_nesting_depth=0, token_count=209]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=-2, function_count=0, loc=-15, max_nesting_depth=0, token_count=-108]

## IPOP_2217 / cpp->python

- Ordered pair: cpp->python
- Final status: compile_error
- Iteration count: 1
- Change-count distance (1 cycle = C++ -> target -> C++): 1
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (compile_error at roundtrip_execution)
- MOSS similarity to seed C++: seed=34%, roundtrip=36%
- Semantic summary: fail (target=success, roundtrip_cpp=compile_error)
- AST distance: distance_to_seed_cpp=54, distance_to_roundtrip_cpp=54
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=-1, function_count=0, loc=-8, max_nesting_depth=1, token_count=-50]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-6, max_nesting_depth=2, token_count=-12]

## IPOP_2579 / cpp->c

- Ordered pair: cpp->c
- Final status: success
- Iteration count: 2
- Change-count distance (1 cycle = C++ -> target -> C++): 2
- Convergence outcome: fixed_point
- Residual similarity to seed C++: 0.782178
- MOSS similarity to seed C++: seed=52%, roundtrip=49%
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=26, distance_to_roundtrip_cpp=0
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=3, function_count=1, loc=-2, max_nesting_depth=0, token_count=4]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=3, function_count=1, loc=-2, max_nesting_depth=0, token_count=10]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]

## IPOP_2579 / cpp->java

- Ordered pair: cpp->java
- Final status: parse_error
- Iteration count: 1
- Change-count distance (1 cycle = C++ -> target -> C++): 0
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (parse_error at target_to_cpp_translation)
- MOSS similarity to seed C++: unavailable (parse_error at target_to_cpp_translation)
- Semantic summary: fail (target=success, roundtrip_cpp=not_evaluated)
- AST distance: unavailable (parse_error at target_to_cpp_translation)
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=8, function_count=3, loc=32, max_nesting_depth=1, token_count=223]
- Roundtrip C++ complexity deltas: unavailable (parse_error at target_to_cpp_translation)

## IPOP_2579 / cpp->python

- Ordered pair: cpp->python
- Final status: compile_error
- Iteration count: 1
- Change-count distance (1 cycle = C++ -> target -> C++): 1
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (compile_error at roundtrip_execution)
- MOSS similarity to seed C++: seed=61%, roundtrip=53%
- Semantic summary: fail (target=success, roundtrip_cpp=compile_error)
- AST distance: distance_to_seed_cpp=49, distance_to_roundtrip_cpp=58
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=1, function_count=0, loc=-7, max_nesting_depth=4, token_count=-9]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=2, function_count=0, loc=-4, max_nesting_depth=3, token_count=24]

## IPOP_5567 / cpp->c

- Ordered pair: cpp->c
- Final status: success
- Iteration count: 3
- Change-count distance (1 cycle = C++ -> target -> C++): 3
- Convergence outcome: fixed_point
- Residual similarity to seed C++: 0.544489
- MOSS similarity to seed C++: seed=0%, roundtrip=0%
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=125, distance_to_roundtrip_cpp=0
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=3, function_count=0, loc=28, max_nesting_depth=0, token_count=230]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=3, function_count=0, loc=28, max_nesting_depth=0, token_count=249]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]

## IPOP_5567 / cpp->java

- Ordered pair: cpp->java
- Final status: compile_error
- Iteration count: 1
- Change-count distance (1 cycle = C++ -> target -> C++): 1
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (compile_error at roundtrip_execution)
- MOSS similarity to seed C++: seed=29%, roundtrip=90%
- Semantic summary: fail (target=success, roundtrip_cpp=compile_error)
- AST distance: distance_to_seed_cpp=121, distance_to_roundtrip_cpp=147
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=11, function_count=4, loc=38, max_nesting_depth=1, token_count=271]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=-3, function_count=0, loc=-24, max_nesting_depth=-1, token_count=-164]

## IPOP_5567 / cpp->python

- Ordered pair: cpp->python
- Final status: compile_error
- Iteration count: 1
- Change-count distance (1 cycle = C++ -> target -> C++): 1
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (compile_error at roundtrip_execution)
- MOSS similarity to seed C++: seed=54%, roundtrip=37%
- Semantic summary: fail (target=success, roundtrip_cpp=compile_error)
- AST distance: distance_to_seed_cpp=81, distance_to_roundtrip_cpp=103
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=1, function_count=0, loc=-7, max_nesting_depth=4, token_count=-24]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=8, function_count=0, loc=5, max_nesting_depth=4, token_count=94]
