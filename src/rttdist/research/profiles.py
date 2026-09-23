"""Resolve reusable profiles to explicit, serializable experiment contracts."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import math

import yaml

from rttdist.config import _yaml_safe_loader_with_duplicate_check
from .metrics import METRICS, validate_metric


PROFILES = {
    "paper-abstract-v1": {
        "id": "paper-abstract-v1", "version": 1,
        "execution": {"policy": "threshold", "metric": "adjacent", "threshold": .85,
                      "max_steps": 20, "metrics": [
                          {"id": "adjacent", "metric": "jplag", "reference": "previous"}]},
        "analysis": {"metrics": [{"id": "origin", "metric": "jplag", "reference": "origin"}],
                     "aggregator": "hop_distance", "weighting": "pooled"},
    },
    "strict-fixed-point-v1": {
        "id": "strict-fixed-point-v1", "version": 1,
        "execution": {"policy": "normalized_fixed_point", "confirmations": 5,
                      "max_steps": 30, "metrics": []},
        "analysis": {"metrics": [{"id": "origin", "metric": "token_dice", "reference": "origin"}],
                     "aggregator": "hop_distance", "weighting": "pooled"},
    },
    "fps-v2": {
        "id": "fps-v2", "version": 1,
        "execution": {"policy": "fps", "metric": "adjacent", "threshold": .85,
                      "thresholds": [.8, .85, .9], "max_states": 10, "max_steps": 20,
                      "metrics": [{"id": "adjacent", "metric": "jplag", "reference": "previous", "options": {"language": "text"}}]},
        "analysis": {"metrics": [], "aggregator": "fps_distance", "weighting": "problem",
                     "failure_penalty": 11},
    },
}


def register_profile(name, profile):
    identifier(name)
    if name in PROFILES:
        raise ValueError(f"Profile already registered: {name}")
    PROFILES[name] = deepcopy(profile)


def read_yaml(path):
    value = yaml.load(Path(path).read_text(encoding="utf-8"), Loader=_yaml_safe_loader_with_duplicate_check)
    if not isinstance(value, dict):
        raise ValueError("YAML root must be a mapping")
    return value


def merge(base, overrides):
    result = deepcopy(base)
    for key, value in overrides.items():
        result[key] = merge(result[key], value) if isinstance(value, dict) and isinstance(result.get(key), dict) else deepcopy(value)
    return result


def identifier(value):
    import re
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,99}", value):
        raise ValueError("Identifiers must contain only letters, numbers, dots, underscores or hyphens")
    return value


def resolve_metrics(specs):
    if not isinstance(specs, list):
        raise ValueError("metrics must be a list")
    resolved = []
    for spec in specs:
        validate_metric(spec)
        identifier(spec.get("id"))
        resolved.append({"version": METRICS[spec["metric"]].version, "scope": "roundtrip",
                         "reference": "previous", "options": {}, **deepcopy(spec)})
    if len({s["id"] for s in resolved}) != len(resolved):
        raise ValueError("Duplicate metric id")
    return resolved


def load_profile(value, base_dir=Path(".")):
    if isinstance(value, str):
        if value in PROFILES:
            raw = deepcopy(PROFILES[value])
        else:
            path = (Path(base_dir) / value).resolve()
            raw = read_yaml(path)
            base_dir = path.parent
    elif isinstance(value, dict):
        raw = deepcopy(value)
    else:
        raise ValueError("profile must be a name, YAML path or mapping")
    parent = raw.pop("extends", None)
    if parent:
        if parent not in PROFILES:
            raise ValueError("extends must name a built-in profile")
        raw = merge(PROFILES[parent], raw)
    if set(raw) - {"id", "version", "execution", "analysis"}:
        raise ValueError("Unknown profile field")
    identifier(raw.get("id"))
    if type(raw.get("version")) is not int or raw["version"] < 1:
        raise ValueError("profile version must be a positive integer")
    execution = raw.get("execution", {})
    analysis = raw.get("analysis", {})
    if not isinstance(execution, dict) or not isinstance(analysis, dict):
        raise ValueError("execution and analysis must be mappings")
    execution["metrics"] = resolve_metrics(execution.get("metrics", []))
    analysis["metrics"] = resolve_metrics(analysis.get("metrics", []))
    for scope in (execution, analysis):
        for spec in scope["metrics"]:
            for name in ("jar", "java"):
                if name in spec["options"]:
                    path = Path(spec["options"][name])
                    if name == "jar" or path.parent != Path("."):
                        spec["options"][name] = str((Path(base_dir) / path).resolve())
    from .policies import POLICIES
    policy = POLICIES.get(execution.get("policy"))
    if policy is None:
        raise ValueError("Unknown decision policy")
    if execution.get("policy_version", policy.version) != policy.version:
        raise ValueError("Decision policy version mismatch")
    execution["policy_version"] = policy.version
    if type(execution.get("max_steps")) is not int or execution["max_steps"] < 2:
        raise ValueError("max_steps must be at least two")
    policy.validate(execution)
    analysis.setdefault("aggregator", "hop_distance")
    analysis.setdefault("weighting", "pooled")
    analysis.setdefault("bootstrap_samples", 1000)
    analysis.setdefault("seed", 0)
    from .aggregation import AGGREGATORS
    if analysis["aggregator"] not in AGGREGATORS:
        raise ValueError("Unknown aggregator")
    if analysis["aggregator"] in ("hop_distance", "fps_distance") and set(analysis) - {
        "metrics", "aggregator", "aggregator_version", "weighting", "bootstrap_samples", "seed", "failure_penalty", "outcome_threshold"
    }:
        raise ValueError("Unknown analysis option")
    if analysis["aggregator"] == "fps_distance" and execution["policy"] != "fps":
        raise ValueError("fps_distance requires an FPS execution policy")
    if "outcome_threshold" in analysis:
        collected = set(execution.get("thresholds", [])) | {execution.get("threshold")}
        if type(analysis["outcome_threshold"]) not in (int, float) or execution["policy"] != "fps" or analysis["outcome_threshold"] not in collected:
            raise ValueError("outcome_threshold must be a threshold collected by the FPS execution")
    version = AGGREGATORS[analysis["aggregator"]].version
    if analysis.get("aggregator_version", version) != version:
        raise ValueError("Aggregator version mismatch")
    analysis["aggregator_version"] = version
    if analysis["weighting"] not in ("pooled", "problem"):
        raise ValueError("weighting must be pooled or problem")
    if type(analysis["bootstrap_samples"]) is not int or analysis["bootstrap_samples"] < 0:
        raise ValueError("bootstrap_samples must be a nonnegative integer")
    if type(analysis["seed"]) is not int:
        raise ValueError("analysis seed must be an integer")
    penalty = analysis.get("failure_penalty", 11)
    if type(penalty) not in (int, float) or not math.isfinite(penalty) or penalty <= 0:
        raise ValueError("failure_penalty must be positive")
    return {**raw, "execution": execution, "analysis": analysis}
