"""Audit exact responses, execution cost, AST cost and legacy observations."""
from collections import Counter
import difflib
import json
from pathlib import Path
import statistics
import sys

from rttdist.ast_similarity import ast_similarity
from rttdist.experiment_io import read_json, write_json
from rttdist.normalize import hash_normalized_cpp_tokens


def diagnostics(run_dir, ast_all=False):
    run_dir = Path(run_dir)
    calls, truncations, formats, execution, ast = [], [], [], [], {}
    for p in sorted(run_dir.glob("IPOP_*/cpp-to-*/attempt-*/iterations/iter-*/step-*/api-attempt-*.json")):
        a = read_json(p)
        a["path"] = str(p)
        if a["raw_response"] and a["http_status"] == 200:
            response = json.loads(a["raw_response"])
            a["usage"] = response.get("usage", {})
            for choice in response.get("choices", []):
                if choice.get("finish_reason") == "length":
                    truncations.append({"path": str(p), "choice_index": choice.get("index"), "usage": a["usage"]})
        calls.append({k: a.get(k) for k in ("path", "seconds", "error", "http_status", "usage")})
    for p in sorted(run_dir.glob("IPOP_*/cpp-to-*/attempt-*/iterations/iter-*/step-*/step.json")):
        s = read_json(p)
        if s["status"] == "parse_error":
            response = read_json(p.parent / "llm-response.json")
            formats.append({"path": str(p), "error": s["error"], "truncated": s["truncated"],
                            "raw_response": response, "audit": "Review all choices against the pinned single-file extractor."})
        if "execution" in s:
            e = s["execution"]
            execution.append({"path": str(p), "language": s["target_language"], "status": s["status"],
                "compile_seconds": e["compile_result"]["duration_seconds"] if e["compile_result"] else 0,
                "fixture_seconds": [f["duration_seconds"] for f in e["fixture_results"]],
                "failed_fixtures": [{k: f[k] for k in ("fixture_stem", "status", "duration_seconds", "stdout", "stderr")} for f in e["fixture_results"] if f["status"] != "success"]})
        if ast_all and s.get("source_path") and s["target_language"] == "cpp":
            source = Path(s["source_path"]).read_text(encoding="utf-8")
            input_source = (p.parent.parent / "input.cpp").read_text(encoding="utf-8")
            ast[str(p)] = ast_similarity(input_source, source)
    durations = [a["seconds"] for a in calls]
    broken = []
    for p in run_dir.glob("IPOP_*/cpp-to-*/attempt-*/run.json"):
        r = read_json(p)
        if r["status"] == "confirmation_failed":
            t = r["iterations"][-1]["iteration_index"]
            previous = Path(r["candidate_source_path"]).read_text(encoding="utf-8")
            changed = (p.parent / "iterations" / f"iter-{t:03d}" / "roundtrip.cpp").read_text(encoding="utf-8")
            delta = list(difflib.unified_diff(previous.splitlines(), changed.splitlines(), fromfile="candidate", tofile="confirmation"))
            broken.append({"problem_id": r["problem_id"], "route": r["route"],
                           "confirmation_index": r["details"]["confirmation_index"], "diff": delta,
                           "delta_step": r["iterations"][-1].get("delta_step")})
    result = {"api_attempt_count": len(calls), "logical_requests": len(list(run_dir.glob("IPOP_*/cpp-to-*/attempt-*/iterations/iter-*/step-*/llm-request.json"))),
              "call_seconds_total": sum(durations), "call_seconds_mean": statistics.mean(durations) if durations else None,
              "call_seconds_median": statistics.median(durations) if durations else None,
              "call_seconds_max": max(durations) if durations else None,
              "prompt_tokens": sum(a.get("usage", {}).get("prompt_tokens", 0) for a in calls if a.get("usage")),
              "completion_tokens": sum(a.get("usage", {}).get("completion_tokens", 0) for a in calls if a.get("usage")),
              "api_errors": [a for a in calls if a["error"]], "truncations": truncations,
              "parse_error_audit": formats, "calls": calls, "execution": execution,
              "generated_ast": ast, "confirmation_diffs": broken}
    write_json(run_dir / "diagnostics.json", result)
    print({k: v for k,v in result.items() if k not in ("calls", "execution", "generated_ast", "confirmation_diffs", "parse_error_audit")})
    return result


def legacy():
    root = Path("artifacts-lmstudio/lmstudio-rtt-demo")
    rows = []
    for path in sorted(root.glob("IPOP_*/*/run.json")):
        manifest = read_json(path)
        sources = [path.parent / "seed/reference.cpp"] + sorted(path.parent.glob("iterations/*/roundtrip.cpp"))
        row = {"path": str(path), "confirmed": "unavailable", "c_ge_1": None,
               "candidate_c0": None, "reason": None}
        if not all(p.exists() and p.read_text(encoding="utf-8").strip() for p in sources):
            row["reason"] = "missing_hash_evidence"
        else:
            hashes = [hash_normalized_cpp_tokens(p.read_text(encoding="utf-8")) for p in sources]
            tau = next((t for t in range(1, len(hashes)) if hashes[t] == hashes[t-1]), None)
            steps = [step for it in manifest["iterations"][:tau] for step in it.get("route_steps", [])] if tau else []
            complete = tau is not None and len(steps) == tau*2 and all("functionality_passed" in s and "compile_passed" in s for s in steps)
            row.update(tau_candidate=tau,
                       candidate_c0=all(s["functionality_passed"] and s["compile_passed"] for s in steps) if complete else None,
                       reason=None if complete else "missing_step_evidence_or_no_candidate")
        row["seed_validation"] = "historical_prevalidation_unavailable"
        row["included_in_main"] = False
        rows.append(row)
    write_json(root / "legacy_sf_reassessment.json", rows)
    return rows


if __name__ == "__main__":
    if sys.argv[1] == "legacy":
        print(legacy())
    else:
        diagnostics(sys.argv[1], ast_all="--ast-all" in sys.argv)
