# Run Summary: real-ollama-smoke-001

| Problem | Language | Final status | Iterations | Change-count distance | Convergence | Residual similarity | MOSS similarity | Semantic | AST distance to seed |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- | --- |
| IPOP_1436 | c | wrong_answer | 1 | 0 | terminated_on_failure | unavailable (wrong_answer at target_execution) | unavailable (wrong_answer at target_execution) | fail | unavailable (wrong_answer at target_execution) |
| IPOP_1436 | java | success | 2 | 2 | fixed_point | 0.872727 | seed=64%, roundtrip=76% | pass | 12 |
| IPOP_1436 | python | success | 2 | 2 | fixed_point | 0.812500 | seed=0%, roundtrip=0% | pass | 33 |

## IPOP_1436 / c

- Final status: wrong_answer
- Iteration count: 1
- Change-count distance (1 cycle = C++ -> target -> C++): 0
- Convergence outcome: terminated_on_failure
- Residual similarity to seed C++: unavailable (wrong_answer at target_execution)
- MOSS similarity to seed C++: unavailable (wrong_answer at target_execution)
- Semantic summary: fail (target=wrong_answer, roundtrip_cpp=not_evaluated)
- AST distance: unavailable (wrong_answer at target_execution)
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-3, max_nesting_depth=0, token_count=-16]
- Roundtrip C++ complexity deltas: unavailable (wrong_answer at target_execution)

## IPOP_1436 / java

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

## IPOP_1436 / python

- Final status: success
- Iteration count: 2
- Change-count distance (1 cycle = C++ -> target -> C++): 2
- Convergence outcome: fixed_point
- Residual similarity to seed C++: 0.812500
- MOSS similarity to seed C++: seed=0%, roundtrip=0%
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=33, distance_to_roundtrip_cpp=20
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-8, max_nesting_depth=0, token_count=-36]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=1, max_nesting_depth=0, token_count=5]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=1, function_count=1, loc=0, max_nesting_depth=0, token_count=8]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]
