# Run Summary: real-smoke-003

| Problem | Language | Final status | Iterations | Change-count distance | Convergence | Residual similarity | Semantic | AST distance to seed |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| IPOP_1436 | python | success | 2 | 2 | fixed_point | 0.852273 | pass | 23 |

## IPOP_1436 / python

- Final status: success
- Iteration count: 2
- Change-count distance (1 cycle = C++ -> target -> C++): 2
- Convergence outcome: fixed_point
- Residual similarity to seed C++: 0.852273
- Semantic summary: pass (target=success, roundtrip_cpp=success)
- AST distance: distance_to_seed_cpp=23, distance_to_roundtrip_cpp=23
- Target complexity deltas: vs_seed_cpp[cyclomatic_complexity=-3, function_count=-1, loc=-10, max_nesting_depth=-2, token_count=-42]; vs_previous[cyclomatic_complexity=-3, function_count=-1, loc=-4, max_nesting_depth=-2, token_count=-16]
- Roundtrip C++ complexity deltas: vs_seed_cpp[cyclomatic_complexity=0, function_count=0, loc=-3, max_nesting_depth=0, token_count=-8]; vs_previous[cyclomatic_complexity=0, function_count=0, loc=0, max_nesting_depth=0, token_count=0]
