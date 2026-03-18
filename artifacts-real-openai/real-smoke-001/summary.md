# Run Summary: real-smoke-001

| Problem | Language | Final status | Iterations | Change-count distance | Convergence | Residual similarity | MOSS similarity | Semantic | AST distance to seed |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- | --- |
| IPOP_1436 | c | success | 2 | 2 | fixed_point | 0.704082 | seed=0%, roundtrip=0% | pass | 18 |
| IPOP_1436 | java | compile_error | 1 | 1 | terminated_on_failure | unavailable (compile_error at roundtrip_execution) | seed=81%, roundtrip=86% | fail | 17 |
| IPOP_1436 | python | compile_error | 1 | 1 | terminated_on_failure | unavailable (compile_error at roundtrip_execution) | seed=0%, roundtrip=0% | fail | 28 |
| IPOP_2579 | c | success | 2 | 2 | fixed_point | 0.795970 | seed=30%, roundtrip=29% | pass | 33 |
| IPOP_2579 | java | compile_error | 1 | 1 | terminated_on_failure | unavailable (compile_error at roundtrip_execution) | seed=74%, roundtrip=80% | fail | 24 |
| IPOP_2579 | python | compile_error | 1 | 1 | terminated_on_failure | unavailable (compile_error at roundtrip_execution) | seed=61%, roundtrip=51% | fail | 48 |

## IPOP_1436 / c

- Final status: success
- Iteration count: 2
- Change-count distance (1 cycle = C++ -> target -> C++): 2
- Convergence outcome: fixed_point
- Residual similarity to seed C++: 0.704082
- MOSS similarity to seed C++: seed=0%, roundtrip=0%
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=18, distance_to_roundtrip_cpp=0
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=1, function_count=0, loc=-1, max_nesting_depth=1, token_count=1]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=1, function_count=0, loc=-1, max_nesting_depth=1, token_count=9]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]

## IPOP_1436 / java

- Final status: compile_error
- Iteration count: 1
- Change-count distance (1 cycle = C++ -> target -> C++): 1
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (compile_error at roundtrip_execution)
- MOSS similarity to seed C++: seed=81%, roundtrip=86%
- Semantic summary: fail (target=success, roundtrip_cpp=compile_error)
- AST distance: distance_to_seed_cpp=17, distance_to_roundtrip_cpp=17
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-2, max_nesting_depth=0, token_count=26]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-1, max_nesting_depth=0, token_count=-5]

## IPOP_1436 / python

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

## IPOP_2579 / c

- Final status: success
- Iteration count: 2
- Change-count distance (1 cycle = C++ -> target -> C++): 2
- Convergence outcome: fixed_point
- Residual similarity to seed C++: 0.795970
- MOSS similarity to seed C++: seed=30%, roundtrip=29%
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=33, distance_to_roundtrip_cpp=0
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=2, function_count=0, loc=-3, max_nesting_depth=0, token_count=-3]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=2, function_count=0, loc=-3, max_nesting_depth=0, token_count=3]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]

## IPOP_2579 / java

- Final status: compile_error
- Iteration count: 1
- Change-count distance (1 cycle = C++ -> target -> C++): 1
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (compile_error at roundtrip_execution)
- MOSS similarity to seed C++: seed=74%, roundtrip=80%
- Semantic summary: fail (target=success, roundtrip_cpp=compile_error)
- AST distance: distance_to_seed_cpp=24, distance_to_roundtrip_cpp=25
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-3, max_nesting_depth=0, token_count=40]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-3, max_nesting_depth=0, token_count=-15]

## IPOP_2579 / python

- Final status: compile_error
- Iteration count: 1
- Change-count distance (1 cycle = C++ -> target -> C++): 1
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (compile_error at roundtrip_execution)
- MOSS similarity to seed C++: seed=61%, roundtrip=51%
- Semantic summary: fail (target=success, roundtrip_cpp=compile_error)
- AST distance: distance_to_seed_cpp=48, distance_to_roundtrip_cpp=58
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=1, function_count=0, loc=-7, max_nesting_depth=4, token_count=-11]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=2, function_count=0, loc=-4, max_nesting_depth=3, token_count=30]
