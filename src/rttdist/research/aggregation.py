"""Model-separated statistics with explicit denominators and sampling units."""
from collections import Counter, defaultdict
from dataclasses import dataclass
import random
import statistics
from typing import Callable


@dataclass(frozen=True)
class Aggregator:
    name: str
    version: str
    compute: Callable


AGGREGATORS: dict[str, Aggregator] = {}


def register_aggregator(aggregator):
    if aggregator.name in AGGREGATORS:
        raise ValueError(f"Aggregator already registered: {aggregator.name}")
    AGGREGATORS[aggregator.name] = aggregator


def _mean(values):
    return statistics.mean(values) if values else None


def _estimates(rows, config):
    valid = [r for r in rows if r["decision"]["terminal"] and r["decision"]["category"] != "invalid"]
    success = [r for r in valid if r["decision"]["success"]]
    by_problem = defaultdict(list)
    for row in valid:
        by_problem[row["problem_id"]].append(row)
    pooled = len(success) / len(valid) if valid else None
    rate = pooled if config["weighting"] == "pooled" else _mean([
        sum(r["decision"]["success"] for r in rs) / len(rs) for rs in by_problem.values()])
    hops = _mean([r["decision"]["reached_step"] for r in success])
    states = _mean([r["decision"]["unique_state_count"] for r in success
                    if r["decision"].get("unique_state_count") is not None])
    return {"success_rate": rate, "pooled_success_rate": pooled, "mean_hops": hops,
            "mean_unique_state_count": states,
            "hop_adjusted_distance": hops / rate if hops is not None and rate else None}


def _summary(rows, config):
    estimate = _estimates(rows, config)
    categories = Counter(r["decision"]["category"] for r in rows)
    valid = sum(r["decision"]["terminal"] and r["decision"]["category"] != "invalid" for r in rows)
    result = {**estimate, "recorded": len(rows), "valid": valid,
              "success": sum(r["decision"]["success"] for r in rows), "categories": dict(categories),
              "distance_unavailable_reason": "no_valid_trials" if not valid else
                  "no_successful_trials" if estimate["mean_hops"] is None else None,
              "weighting": config["weighting"], "sampling_unit": "problem",
              "invalid_reasons": dict(Counter(r.get("reason") or r["decision"].get("reason") or r["decision"]["status"]
                                              for r in rows if r["decision"]["category"] == "invalid"))}
    # Cluster bootstrap: all repetitions of a sampled problem stay together.
    by_problem = defaultdict(list)
    for row in rows:
        by_problem[row["problem_id"]].append(row)
    ids = sorted(by_problem)
    draws = defaultdict(list)
    rng = random.Random(config["seed"])
    for _ in range(config["bootstrap_samples"]):
        sampled = []
        for index, pid in enumerate(rng.choices(ids, k=len(ids))):
            sampled.extend({**r, "problem_id": str(index)} for r in by_problem[pid])
        for name, value in _estimates(sampled, config).items():
            if value is not None:
                draws[name].append(value)
    result["bootstrap95"] = {}
    for name in estimate:
        values = sorted(draws[name])
        result["bootstrap95"][name] = {
            "interval": [_quantile(values, .025), _quantile(values, .975)] if values else None,
            "valid_replicates": len(values), "requested_replicates": config["bootstrap_samples"],
            "degenerate": len(set(values)) == 1 if values else None}
    measurements = defaultdict(list)
    statuses = defaultdict(Counter)
    for row in rows:
        for step in row.get("steps", []):
            for name, metric in step.get("analysis_measurements", {}).items():
                statuses[name][metric["status"]] += 1
                if metric["status"] == "measured":
                    measurements[name].append(metric["value"])
    result["measurements"] = {name: {"mean": _mean(measurements[name]), "n": len(measurements[name]),
                                      "statuses": dict(status)} for name, status in statuses.items()}
    return result


def _quantile(values, q):
    pos = (len(values) - 1) * q
    i = int(pos)
    return values[i] + (values[min(i + 1, len(values) - 1)] - values[i]) * (pos - i)


def _fps_summary(rows, config):
    result = _summary(rows, config)
    penalty = config.get("failure_penalty", 11)
    by_problem = defaultdict(list)
    for r in rows:
        d = r["decision"]
        if d["terminal"] and d["category"] != "invalid":
            by_problem[r["problem_id"]].append(d["unique_state_count"] if d["success"] else penalty)
    values = [v for vs in by_problem.values() for v in vs] if config["weighting"] == "pooled" else [_mean(vs) for vs in by_problem.values()]
    return {**result, "penalized_state_distance": _mean(values), "failure_penalty": penalty}


def aggregate(rows, config):
    groups = defaultdict(list)
    for row in rows:
        if "outcome_threshold" in config:
            key = f"{config['outcome_threshold']:.2f}"
            observed = row["decision"].get("outcomes", {}).get(key)
            if observed is None:
                raise ValueError("Requested threshold was not recorded")
            row = {**row, "decision": {**row["decision"], "category": observed["category"],
                                       "success": observed["success"], "reached_step": observed["reached_step"],
                                       "unique_state_count": observed["d_n"]}}
        groups[(row["model_id"], tuple(row["route"]))].append(row)
    fn = AGGREGATORS[config["aggregator"]].compute
    return [{"model_id": model, "route": list(route), **fn(group, config)}
            for (model, route), group in sorted(groups.items())]


register_aggregator(Aggregator("hop_distance", "1", _summary))
register_aggregator(Aggregator("fps_distance", "1", _fps_summary))
