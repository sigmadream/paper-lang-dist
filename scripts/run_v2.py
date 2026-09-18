"""Execute and audit the frozen v2 pilot, then three serial main repetitions."""
import argparse
from dataclasses import replace
from datetime import datetime, timezone
import os
from pathlib import Path
import statistics
import sys
import time

import yaml

from rttdist.config import load_experiment_config
from rttdist.experiment_io import (code_provenance, digest, read_json, server_metadata,
                                   timestamp, validation_gate, validate_execute, write_json)
from rttdist.experiment_v1 import run_experiment
from rttdist.reporting_v1 import report_runs
from v1_checks import audit

PILOT = ("IPOP_1620", "IPOP_9663", "LC_0003", "LC_0063", "LC_0207")


def resource_report(root):
    responses = [read_json(p) for p in root.glob("*/cpp-to-*/attempt-*/iterations/iter-*/step-*/llm-response.json")]
    attempts = [read_json(p) for p in root.glob("*/cpp-to-*/attempt-*/iterations/iter-*/step-*/api-attempt-*.json")]
    times = [a["seconds"] for a in attempts]
    prompt = [r.get("usage", {}).get("prompt_tokens", 0) for r in responses]
    completion = [r.get("usage", {}).get("completion_tokens", 0) for r in responses]
    return {"logical_calls": len(responses), "api_attempts": len(attempts),
            "api_errors": sum(a["error"] is not None for a in attempts),
            "truncated": sum(any(c.get("finish_reason") == "length" for c in r.get("choices", [])) for r in responses),
            "prompt_tokens_total": sum(prompt), "completion_tokens_total": sum(completion),
            "prompt_tokens_max": max(prompt, default=0), "completion_tokens_max": max(completion, default=0),
            "api_seconds_total": sum(times), "api_seconds_mean": statistics.mean(times) if times else None,
            "api_seconds_max": max(times, default=0)}


def execute(config, raw, run_id):
    root = config.output_root / run_id
    existing = (root / "run_metadata.json").exists()
    results = run_experiment(config, raw, run_id, resume=existing)
    for _ in range(raw["recovery"]["max_resumes_per_route"]):
        if not any(r["status"] == "api_error" for r in results):
            break
        results = run_experiment(config, raw, run_id, resume=True)
    if len(results) != len(config.problem_ids)*len(config.target_languages) or any(
        r["status"] == "api_error" or r["details"].get("missing_toolchain") for r in results
    ):
        raise RuntimeError(f"Unresolved infrastructure: {run_id}")
    report_runs(config.output_root, [run_id])
    audit(root / "summary.json")
    resources = resource_report(root)
    write_json(root / "resources.json", resources)
    return resources


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("--config", default="lmstudio_v2.yaml")
    parser.add_argument("--stage", choices=("pilot", "main", "all"), default="all")
    args = parser.parse_args()
    workspace = Path(__file__).resolve().parents[1]
    os.environ["PATH"] = os.pathsep.join([str(workspace / ".tools/gcc/bin"),
                                         str(workspace / ".tools/R/bin/x64"), os.environ["PATH"]])
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", line_buffering=True)
    config_path = Path(args.config).resolve()
    config = load_experiment_config(config_path)
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if raw["execution_schedule"]["parallel_runs"] != 1 or raw["execution_schedule"]["parallel_routes_per_run"] != 1:
        raise ValueError("This driver requires serial execution")
    root = config.output_root
    root.mkdir(parents=True, exist_ok=True)
    state_path = root / "campaign_status.json"
    state = {"status": "preflight", "updated_at": timestamp(), "planned_main_observations": 360}
    write_json(state_path, state)
    try:
        if not (root / "corpus_validation.json").exists():
            validate_execute(config)
        _, validation = validation_gate(config)
        server = server_metadata(config.lmstudio.host, config.lmstudio.model)
        design = {"config": raw, "source": code_provenance(), "server": server["effective"],
                  "validation_hash": validation["validation_hash"], "pilot_problem_ids": PILOT,
                  "main_repetitions": 3, "main_observations": len(config.problem_ids)*len(config.target_languages)*3,
                  "pilot_max_logical_calls": 450, "main_max_logical_calls": 10800,
                  "max_output_tokens_per_logical_call": 4096,
                  "main_max_output_tokens_without_retries": 44236800,
                  "main_wall_hours": 24, "new_attempts_allowed": 0,
                  "sampling_verification": "Exact requested parameters retained; backend effective sampling not independently verified"}
        frozen_path = root / "frozen_design.json"
        if frozen_path.exists():
            if digest(read_json(frozen_path)) != digest(design):
                raise ValueError("Frozen design changed; refusing to mix conditions")
        else:
            write_json(frozen_path, design)
        pilot_id = raw["experiment_version"] + "-pilot"
        if args.stage in ("pilot", "all"):
            state.update(status="pilot_running", run_id=pilot_id, updated_at=timestamp())
            write_json(state_path, state)
            pilot_config = replace(config, problem_ids=PILOT)
            pilot_raw = {**raw, "phase": "pilot", "problem_ids": list(PILOT), "repeat_index": 1}
            resources = execute(pilot_config, pilot_raw, pilot_id)
            if resources["truncated"] or resources["prompt_tokens_max"] + config.lmstudio.max_tokens > 8192:
                raise RuntimeError("Pilot token/context gate failed; preserve pilot and revise protocol before main")
            write_json(root / "pilot_gate.json", {"passed": True, "created_at": timestamp(),
                       "design_hash": digest(design), "resources": resources,
                       "main_call_time_upper_estimate_seconds": resources["api_seconds_mean"]*10800,
                       "note": "API-only projection excludes execution/AST and is not a completion guarantee"})
            state.update(status="pilot_complete", updated_at=timestamp())
            write_json(state_path, state)
        if args.stage in ("main", "all"):
            gate = read_json(root / "pilot_gate.json")
            if not gate["passed"] or gate["design_hash"] != digest(design):
                raise ValueError("No matching passed pilot gate")
            campaign_path = root / "main_started.json"
            if not campaign_path.exists():
                write_json(campaign_path, {"started_at": timestamp()})
            started_at = read_json(campaign_path)["started_at"]
            runs = []
            for repeat in (1, 2, 3):
                if (datetime.now(timezone.utc) - datetime.fromisoformat(started_at)).total_seconds() >= 86400:
                    raise RuntimeError("Main campaign 24-hour deadline reached")
                run_id = raw["experiment_version"] + f"-r{repeat}"
                state.update(status="main_running", run_id=run_id, updated_at=timestamp())
                write_json(state_path, state)
                execute(config, {**raw, "repeat_index": repeat, "campaign_started_at": started_at}, run_id)
                runs.append(run_id)
            report_runs(root, runs)
            audit(root / "v2-combined/summary.json")
            state.update(status="complete", completed_main_observations=360, runs=runs, updated_at=timestamp())
            write_json(state_path, state)
    except Exception as exc:
        state.update(status="incomplete", error=f"{type(exc).__name__}: {exc}", updated_at=timestamp())
        write_json(state_path, state)
        raise


if __name__ == "__main__":
    main()
