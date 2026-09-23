"""Pure reducers over durable steps; policies never call a model or write files."""
from dataclasses import dataclass
import math
from typing import Callable

from rttdist.fps_state import FPSState


@dataclass(frozen=True)
class DecisionPolicy:
    name: str
    version: str
    validate: Callable
    decide: Callable


POLICIES: dict[str, DecisionPolicy] = {}


def register_policy(policy):
    if policy.name in POLICIES:
        raise ValueError(f"Policy already registered: {policy.name}")
    POLICIES[policy.name] = policy


def _threshold_validate(config):
    allowed = {"policy", "policy_version", "max_steps", "metric", "threshold", "metrics"}
    if config.get("policy") == "fps":
        allowed |= {"max_states", "thresholds"}
    if set(config) - allowed:
        raise ValueError("Unknown decision policy option")
    value = config.get("threshold")
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError("threshold must be in [0, 1]")
    spec = next((m for m in config["metrics"] if m["id"] == config.get("metric")), None)
    if spec is None or spec["scope"] != "roundtrip" or spec["reference"] != "previous":
        raise ValueError("Policy metric must compare adjacent roundtrips")


def _strict_validate(config):
    if set(config) - {"policy", "policy_version", "max_steps", "metrics", "confirmations"}:
        raise ValueError("Unknown decision policy option")
    n = config.get("confirmations", 0)
    if type(n) is not int or n < 0:
        raise ValueError("confirmations must be a nonnegative integer")


def _fps_validate(config):
    _threshold_validate(config)
    if type(config.get("max_states")) is not int or config["max_states"] < 2:
        raise ValueError("max_states must be at least two")
    values = config.get("thresholds", [config["threshold"]])
    if not isinstance(values, list) or any(type(v) not in (int, float) or not 0 <= v <= 1 for v in values):
        raise ValueError("thresholds must be a list in [0, 1]")
    values = set(values) | {config["threshold"]}
    if any(abs(v - round(v, 2)) > 1e-12 for v in values):
        raise ValueError("FPS thresholds support at most two decimal places")
    if len({f"{v:.2f}" for v in values}) != len(values):
        raise ValueError("FPS thresholds collide at two-decimal precision")


def outcome(status=None, *, reached=None, states=None, category=None, **extra):
    success = reached is not None
    return {"terminal": status is not None, "status": status,
            "category": category or ("success" if success else "incomplete"),
            "success": success, "reached_step": reached, "unique_state_count": states, **extra}


def _failure(step):
    status = step["status"]
    if status == "success":
        return None
    category = "invalid" if status in ("infrastructure_error", "measurement_error") else "functional_failure"
    return outcome(status, category=category)


def _threshold(config, origin, language, steps):
    measured = 0
    for step in steps:
        failure = _failure(step)
        if failure:
            return failure
        if step["target_language"] == language:
            metric = step.get("measurements", {}).get(config["metric"], {})
            if metric.get("status") == "measured":
                measured += 1
                if metric["value"] >= config["threshold"]:
                    return outcome("converged", reached=step["index"])
    if len(steps) >= config["max_steps"]:
        return outcome("translation_budget_reached", category="budget" if measured else "invalid",
                       reason=None if measured else "similarity_unavailable")
    return outcome()


def _strict(config, origin, language, steps):
    from rttdist.normalize import hash_normalized_cpp_tokens
    if language != "cpp":
        raise ValueError("normalized_fixed_point currently supports C++ seed code")
    hashes = [hash_normalized_cpp_tokens(origin)]
    candidate = None
    confirmations = 0
    for step in steps:
        failure = _failure(step)
        if failure:
            return failure
        if step["target_language"] != language:
            continue
        hashes.append(hash_normalized_cpp_tokens(step["source"]))
        if candidate is not None:
            if hashes[-1] != hashes[-2]:
                return outcome("confirmation_failed", category="unstable")
            confirmations += 1
        elif hashes[-1] == hashes[-2]:
            candidate = step["index"]
        else:
            for period in range(2, 5):
                if len(hashes) >= 2 * period and hashes[-period:] == hashes[-2 * period:-period]:
                    return outcome("oscillation", category="unstable")
        if candidate is not None and confirmations >= config.get("confirmations", 0):
            return outcome("converged", reached=candidate, confirmations=confirmations)
    if len(steps) >= config["max_steps"]:
        return outcome("translation_budget_reached", category="budget")
    return outcome()


def _fps(config, origin, language, steps):
    state = FPSState(language, origin, config["threshold"], config["max_states"],
                     config["max_steps"], thresholds=config.get("thresholds"))
    status = None
    measured = 0
    for step in steps:
        if step.get("source") is not None:
            state.add(step["target_language"], step["source"])
        if step["status"] != "success":
            status = step["status"]
            break
        metric = step.get("measurements", {}).get(config["metric"], {})
        available = metric.get("status") == "measured"
        measured += available
        status = state.decide(step["status"], step["target_language"] == language,
                              metric.get("value"), available)
        if status:
            break
    outcomes = state.outcomes(status)
    if not measured and status in ("translation_budget_reached", "max_distance_reached"):
        for result in outcomes.values():
            if not result["success"]:
                result["category"] = "invalid"
    primary = outcomes[f"{config['threshold']:.2f}"]
    return outcome(status, reached=primary["reached_step"], states=primary["d_n"],
                   category=primary["category"] if status else "incomplete",
                   outcomes=outcomes, states_at_stop=len(state.states))


register_policy(DecisionPolicy("threshold", "1", _threshold_validate, _threshold))
register_policy(DecisionPolicy("normalized_fixed_point", "1", _strict_validate, _strict))
register_policy(DecisionPolicy("fps", "2", _fps_validate, _fps))
