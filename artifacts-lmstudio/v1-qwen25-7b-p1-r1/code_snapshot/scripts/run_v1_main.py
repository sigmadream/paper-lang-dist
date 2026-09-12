"""Run the preregistered main repetitions, then regenerate all machine-readable tables."""
import json
from pathlib import Path
import sys
from concurrent.futures import ThreadPoolExecutor

import yaml

from rttdist.config import load_experiment_config
from rttdist.experiment_v1 import run_experiment
from rttdist.reporting_v1 import report_runs


def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "lmstudio_v1.yaml")
    config = load_experiment_config(path)
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert raw["phase"] == "main"
    def repetition(repeat):
        run_id = f"v1-qwen25-7b-p1-r{repeat}"
        run_raw = {**raw, "repeat_index": repeat}
        existing = (config.output_root / run_id / "run_metadata.json").exists()
        results = run_experiment(config, run_raw, run_id, resume=existing)
        for recovery in range(raw["recovery"]["max_resumes_per_route"]):
            if all(r["status"] != "api_error" for r in results):
                break
            results = run_experiment(config, run_raw, run_id, resume=True)
        if any(r["status"] == "api_error" or r["details"].get("missing_toolchain") for r in results):
            raise RuntimeError(f"Unresolved infrastructure in {run_id}; preserve artifacts and report incomplete")
        report_runs(config.output_root, [run_id])
        print(f"REPETITION COMPLETE: {run_id}", flush=True)
        return run_id
    with ThreadPoolExecutor(max_workers=raw["execution_schedule"]["parallel_runs"]) as executor:
        runs = list(executor.map(repetition, (1, 2, 3)))
    report_runs(config.output_root, runs)
    print("ALL MAIN REPETITIONS COMPLETE", flush=True)


if __name__ == "__main__":
    main()
