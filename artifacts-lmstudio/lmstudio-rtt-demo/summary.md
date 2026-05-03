# Run Summary: lmstudio-rtt-demo

| Problem | RTT route | Final status | RTT cycles | Conversions/cycle | Completed conversions | Convergence | Semantic |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| IPOP_1436 | cpp->c->cpp | success | 2 | 2 | 2 | fixed_point | pass |
| IPOP_1436 | cpp->java->cpp | success | 2 | 2 | 2 | fixed_point | pass |
| IPOP_1436 | cpp->python->cpp | success | 2 | 2 | 2 | fixed_point | pass |

## RTT route aggregates

| RTT route | Results | Divergence rate | Measured divergence count | Unavailable divergence count | Infrastructure divergence count |
| --- | ---: | --- | ---: | ---: | ---: |
| cpp->c->cpp | 1 | 0.000000 | 1 | 0 | 0 |
| cpp->java->cpp | 1 | 0.000000 | 1 | 0 | 0 |
| cpp->python->cpp | 1 | 0.000000 | 1 | 0 | 0 |

## IPOP_1436 / cpp->c->cpp

- RTT route: cpp->c->cpp
- Final status: success
- RTT cycle count: 2
- Translations per RTT cycle: 2
- Attempted translations in final iteration: 2
- Completed translations in final iteration: 2
- Failed translations in final iteration: 0
- Conversion log: lmstudio-rtt-demo/IPOP_1436/cpp-to-c/iterations/iter-002/conversion.log
- Convergence outcome: fixed_point
- Semantic preservation: pass
- Legacy semantic summary (raw execution): pass
- Residual similarity: measured 1.000000
- Complexity delta: unavailable (optional_tool_not_configured_or_not_installed)

## IPOP_1436 / cpp->java->cpp

- RTT route: cpp->java->cpp
- Final status: success
- RTT cycle count: 2
- Translations per RTT cycle: 2
- Attempted translations in final iteration: 2
- Completed translations in final iteration: 2
- Failed translations in final iteration: 0
- Conversion log: lmstudio-rtt-demo/IPOP_1436/cpp-to-java/iterations/iter-002/conversion.log
- Convergence outcome: fixed_point
- Semantic preservation: pass
- Legacy semantic summary (raw execution): pass
- Residual similarity: measured 1.000000
- Complexity delta: unavailable (optional_tool_not_configured_or_not_installed)

## IPOP_1436 / cpp->python->cpp

- RTT route: cpp->python->cpp
- Final status: success
- RTT cycle count: 2
- Translations per RTT cycle: 2
- Attempted translations in final iteration: 2
- Completed translations in final iteration: 2
- Failed translations in final iteration: 0
- Conversion log: lmstudio-rtt-demo/IPOP_1436/cpp-to-python/iterations/iter-002/conversion.log
- Convergence outcome: fixed_point
- Semantic preservation: pass
- Legacy semantic summary (raw execution): pass
- Residual similarity: measured 1.000000
- Complexity delta: unavailable (optional_tool_not_configured_or_not_installed)
