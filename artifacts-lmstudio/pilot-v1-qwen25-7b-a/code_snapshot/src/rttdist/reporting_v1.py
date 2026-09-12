"""Problem-cluster inference from selected attempts, with paired route resampling."""
from collections import Counter
import csv
import math
from pathlib import Path
import random
import statistics

from rttdist.ast_similarity import ast_similarity
from rttdist.experiment_io import read_json, write_json
from rttdist.experiment_v1 import sf_success
from rttdist.failure_taxonomy import paper_category

METRICS = ("token_multiset_dice", "token_sequence_ratio", "ast_tsed")


def quantile(values, p):
    values = sorted(values)
    if not values:
        return None
    pos = (len(values)-1)*p
    lo = int(pos)
    hi = min(lo+1, len(values)-1)
    return values[lo] + (values[hi]-values[lo])*(pos-lo)


def interval(values, *, required=2000):
    values = [v for v in values if v is not None]
    if len(values) < required*.95:
        return None, "unavailable"
    ci = [quantile(values, .025), quantile(values, .975)]
    return ci, "degenerate" if ci[0] == ci[1] else "measured"


def wilson(k, n):
    if not n:
        return None
    z = 1.959963984540054
    p, denominator = k/n, 1+z*z/n
    middle = (p+z*z/(2*n))/denominator
    margin = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/denominator
    return [middle-margin, middle+margin]


def descriptive(values, samples):
    values = [v for v in values if v is not None]
    ci, status = interval(samples)
    return {"n": len(values), "median": statistics.median(values) if values else None,
            "q1": quantile(values, .25), "q3": quantile(values, .75),
            "min": min(values) if values else None, "max": max(values) if values else None,
            "median_ci95": ci, "ci_status": status,
            "valid_resamples": sum(v is not None for v in samples)}


def load_selected(output_root, runs, *, postprocess=True):
    metadata = [read_json(output_root / r / "run_metadata.json") for r in runs]
    if len(set(runs)) != len(runs):
        raise ValueError("Duplicate run IDs")
    if len({m["condition_hash"] for m in metadata}) != 1:
        raise ValueError("Mixed conditions are not poolable")
    if len(runs) > 1 and any(m["phase"] != "main" for m in metadata):
        raise ValueError("Pilot results cannot be pooled into main results")
    rows, exclusions = [], []
    for run, meta in zip(runs, metadata):
        for problem in meta["problem_ids"]:
            for target in meta["target_languages"]:
                root = output_root / run / problem / f"cpp-to-{target}"
                index = read_json(root / "attempts.json")
                attempts = index["attempts"]
                if len({a["attempt_id"] for a in attempts}) != len(attempts):
                    raise ValueError("Duplicate attempt ID")
                if index["condition_hash"] != meta["condition_hash"]:
                    raise ValueError("Attempt index condition mismatch")
                selected = index["selected_attempt_id"]
                if selected is None:
                    exclusions.append({"run_id": run, "problem_id": problem, "target": target,
                                       "reason": "infrastructure_or_incomplete"})
                    continue
                matches = [a for a in attempts if a["attempt_id"] == selected]
                if len(matches) != 1:
                    raise ValueError("Invalid selected attempt")
                relative = Path(matches[0]["manifest_path"])
                path = (root / relative).resolve()
                if relative.is_absolute() or not path.is_relative_to(root.resolve()):
                    raise ValueError("Attempt path escapes route")
                manifest = read_json(path)
                if (manifest["condition_hash"] != meta["condition_hash"] or
                    manifest["validation_hash"] != meta["validation_hash"] or
                    manifest["attempt_id"] != selected or manifest["manifest_version"] != 3 or
                    manifest["run_id"] != run or manifest["problem_id"] != problem or
                    manifest["target_language"] != target):
                    raise ValueError("Selected manifest identity mismatch")
                if manifest["status"] in ("running", "api_error") or manifest["details"].get("missing_toolchain"):
                    raise ValueError("Unevaluable attempt selected")
                metrics = manifest["distance_metrics"]
                if metrics["schema_version"] != 2:
                    raise ValueError("Legacy schema in SF report")
                if metrics["stabilization"]["tau_candidate"] is not None and postprocess:
                    if "ast_tsed" not in metrics["delta_0"]:
                        reference = (path.parent / "seed.cpp").read_text(encoding="utf-8")
                        candidate = Path(manifest["candidate_source_path"]).read_text(encoding="utf-8")
                        result = ast_similarity(reference, candidate, **meta["ast"])
                        if result["value"] is not None:
                            result["value"] = 1-result["value"]
                        result.update(reference="seed_source", candidate="stabilized_source")
                        metrics["delta_0"]["ast_tsed"] = result
                        write_json(path, manifest)
                cmax = meta["runtime"]["confirmation_cycles"]
                rows.append({"run_id": run, "problem_id": problem, "route": manifest["route"],
                             "attempt_id": selected, "status": manifest["status"],
                             "category": paper_category(manifest), "distance_metrics": metrics,
                             "tau": metrics["stabilization"]["tau_candidate"],
                             "success": {str(c): sf_success(metrics, c) for c in range(cmax+1)},
                             "iterations": manifest["iterations"], "hash_history": manifest["hash_history"],
                             "manifest_path": str(path)})
    return metadata, rows, exclusions


def aggregate(rows, metadata, exclusions=()):
    meta = metadata[0]
    problems = list(meta["problem_ids"])
    runs = [m["run_id"] for m in metadata]
    cmax = meta["runtime"]["confirmation_cycles"]
    rng = random.Random(20260911)
    clusters = [rng.choices(problems, k=len(problems)) for _ in range(2000)]
    aggregates, route_samples = {}, {}
    for target in meta["target_languages"]:
        route = f"cpp-to-{target}"
        group = [r for r in rows if r["route"] == route]
        by_problem = {p: [r for r in group if r["problem_id"] == p] for p in problems}
        samples = [[r for p in draw for r in by_problem[p]] for draw in clusters]
        agg = {"experiment_version": meta["experiment_version"], "condition_hash": meta["condition_hash"],
               "problem_count": len(problems), "run_count": len(runs), "evaluable_count": len(group),
               "excluded_infrastructure_count": sum(e["target"] == target for e in exclusions),
               "incomplete_count": sum(e["target"] == target for e in exclusions),
               "excluded_seed_failure_count": sum(p["status"] != "success" for p in meta["validation_snapshot"]["problems"].values()),
               "parse_error_count": sum(r["status"] == "parse_error" for r in group),
               "by_confirmation": {}, "conditional": {}, "per_run": {}, "repeatability": {"by_confirmation": {}},
               "bootstrap": {"unit": "problem", "resamples": 2000, "seed": 20260911, "paired_routes": True, "interval": "percentile"}}
        route_samples[route] = {}
        for c in range(cmax+1):
            key = str(c)
            successes = [r for r in group if r["success"][key]]
            k, n = len(successes), len(group)
            sampled_p = [sum(r["success"][key] for r in s)/len(s) if s else None for s in samples]
            route_samples[route][key] = sampled_p
            ci, ci_status = interval(sampled_p)
            sensitivity = [r for r in group if r["status"] != "parse_error"]
            sensitivity_k = sum(r["success"][key] for r in sensitivity)
            rate = sensitivity_k/len(sensitivity) if sensitivity else None
            agg["by_confirmation"][key] = {"success_count": k, "p_sf": k/n if n else None, "d_sf": 1-k/n if n else None,
                "p_sf_ci95": ci, "d_sf_ci95": [1-ci[1], 1-ci[0]] if ci else None,
                "ci_method": "problem_cluster_bootstrap", "ci_status": ci_status,
                "p_sf_excluding_parse_error": rate, "d_sf_excluding_parse_error": 1-rate if rate is not None else None,
                "sensitivity_evaluable_count": len(sensitivity), "sensitivity_excluded_success_count": k-sensitivity_k}
            conditional = {"success_count": k, "delta_0": {}}
            success_samples = [[r for r in s if r["success"][key]] for s in samples]
            conditional["tau"] = descriptive([r["tau"] for r in successes],
                [statistics.median(r["tau"] for r in s) if s else None for s in success_samples])
            for metric in METRICS:
                def value(row):
                    m = row["distance_metrics"]["delta_0"].get(metric, {})
                    return m.get("value") if m.get("status") == "measured" else None
                values = [value(r) for r in successes]
                sampled_values = [[value(r) for r in s if value(r) is not None] for s in success_samples]
                stat = descriptive(values, [statistics.median(s) if s else None for s in sampled_values])
                stat["measurement_rate"] = stat["n"]/k if k else None
                stat["excluded_by_reason"] = dict(Counter(r["distance_metrics"]["delta_0"].get(metric, {}).get("reason", "not_processed") for r in successes if value(r) is None))
                conditional["delta_0"][metric] = stat
            agg["conditional"][key] = conditional
            rates = []
            for run in runs:
                g = [r for r in group if r["run_id"] == run]
                count = sum(r["success"][key] for r in g)
                p = count/len(g) if g else None
                agg["per_run"].setdefault(run, {"by_confirmation": {}})["by_confirmation"][key] = {
                    "success_count": count, "evaluable_count": len(g), "p_sf": p, "p_sf_wilson_ci95": wilson(count, len(g))}
                if p is not None:
                    rates.append(p)
            agg["repeatability"]["by_confirmation"][key] = {"p_sf_mean": statistics.mean(rates) if rates else None,
                "p_sf_min": min(rates) if rates else None, "p_sf_max": max(rates) if rates else None}
        categories = Counter(r["category"] for r in group if not r["success"][str(cmax)])
        agg["failures"] = {"confirmation": cmax, "denominator": len(group),
            "categories": {category: {"count": categories[category], "rate": categories[category]/len(group) if group else None}
                           for category in ("functionality_error", "oscillation", "max_iterations", "confirmation_failed", "format_error")}}
        aggregates[route] = agg
    differences = {}
    routes = list(aggregates)
    for i, a in enumerate(routes):
        for b in routes[i+1:]:
            differences[a+" minus "+b] = {}
            for c in range(cmax+1):
                key = str(c)
                values = [x-y if x is not None and y is not None else None for x,y in zip(route_samples[a][key], route_samples[b][key])]
                ci, status = interval(values)
                differences[a+" minus "+b][key] = {"p_sf_difference_ci95": ci, "ci_status": status}
    return aggregates, differences


def hash_repeatability(rows, runs):
    grouped = {}
    for row in rows:
        grouped.setdefault((row["problem_id"], row["route"]), {})[row["run_id"]] = row
    comparable, matched, unreached, phase_mismatch = 0, 0, 0, 0
    for group in grouped.values():
        maximum = max(len(r["iterations"]) for r in group.values())
        for t in range(maximum):
            items = [group[r]["iterations"][t] if r in group and len(group[r]["iterations"]) > t else None for r in runs]
            if any(it is None or it["roundtrip_hash"] is None for it in items):
                unreached += 1
                continue
            comparable += 1
            matched += len({it["roundtrip_hash"] for it in items}) == 1
            phase_mismatch += len({(it["phase"], it["confirmation_index"]) for it in items}) > 1
    return {"comparable_positions": comparable, "matched_positions": matched,
            "all_run_hash_match_rate": matched/comparable if comparable else None,
            "unreached_or_failed_positions": unreached, "phase_mismatch_positions": phase_mismatch}


def report_runs(output_root, runs):
    output_root = Path(output_root)
    metadata, rows, exclusions = load_selected(output_root, runs)
    aggregates, differences = aggregate(rows, metadata, exclusions)
    directory = output_root / (runs[0] if len(runs) == 1 else "v1-combined")
    summary = {"schema_version": 2, "run_metadata": metadata, "observations": rows,
               "rtt_route_aggregates": aggregates, "paired_route_differences": differences,
               "exclusions": exclusions, "complete": not exclusions,
               "hash_repeatability": hash_repeatability(rows, runs) if len(runs) > 1 else None}
    write_json(directory / "summary.json", summary)
    with (directory / "observations.csv").open("w", encoding="utf-8", newline="") as f:
        fields = ["problem_id", "route", "run_id", "attempt_id", "c", "success", "tau", *METRICS, "ast_status"]
        writer = csv.DictWriter(f, fields)
        writer.writeheader()
        for row in rows:
            for c, success in row["success"].items():
                writer.writerow({**{k: row[k] for k in fields[:4]}, "c": c, "success": int(success),
                    "tau": row["tau"] if success else None,
                    **{m: row["distance_metrics"]["delta_0"].get(m, {}).get("value") if success else None for m in METRICS},
                    "ast_status": row["distance_metrics"]["delta_0"].get("ast_tsed", {}).get("status", "not_applicable")})
    lines = ["# SF experiment summary", "", "| Route | c | success/n | p_SF | d_SF | 95% CI p_SF |", "|---|---:|---:|---:|---:|---|"]
    for route, agg in aggregates.items():
        for c, stat in agg["by_confirmation"].items():
            lines.append(f"| {route} | {c} | {stat['success_count']}/{agg['evaluable_count']} | {stat['p_sf']} | {stat['d_sf']} | {stat['p_sf_ci95']} ({stat['ci_status']}) |")
    lines.extend(["", "Conditional statistics and failure categories are preserved in summary.json.", ""])
    (directory / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    print(directory / "summary.json", flush=True)
    return summary
