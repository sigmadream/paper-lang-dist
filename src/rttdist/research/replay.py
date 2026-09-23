"""Re-extract and evaluate saved responses without creating model requests."""
from pathlib import Path
import uuid

from rttdist.experiment_io import digest, read_json, write_json
from rttdist.extract import extract_single_file_source_text, SourceExtractionError
from rttdist.fps_execution import evaluate
from .analysis import load_observations
from .config import LANGUAGES
from .engine import implementation_hashes, step_measurements, _metric_tools, environment_metadata, toolchain_metadata
from .policies import POLICIES, outcome
from .profiles import identifier
from .store import exclusive_lock, immutable_json, stage, seal, verify, StoreError


def replay(root, *, replay_id=None, evaluator=evaluate):
    root = Path(root).resolve()
    replay_id = identifier(replay_id or ("replay-" + uuid.uuid4().hex[:12]))
    with exclusive_lock(root):
        contract, rows = load_observations(root)
        cfg = contract["config"]
        execution = cfg["profile"]["execution"]
        folder = root / "replays" / replay_id
        replay_contract = {"original_contract_sha256": digest(contract), "input_records_sha256": digest(rows),
                           "implementation_hashes": implementation_hashes(), "environment": environment_metadata(),
                           "toolchains": toolchain_metadata(cfg), "metric_tools": _metric_tools(cfg["profile"], required=False)}
        if (folder / "sealed.json").exists():
            verify(folder)
            if read_json(folder / "contract.json") != replay_contract:
                raise StoreError("Replay inputs changed; use a new replay id")
            return read_json(folder / "summary.json")
        immutable_json(folder / "contract.json", replay_contract)
        records = []
        for row in rows:
            problem = root / "corpus" / row["problem_id"]
            language = row["route"][0]
            origin = (problem / ("reference." + LANGUAGES[language])).read_text(encoding="utf-8")
            previous = origin
            steps = []
            decision = outcome()
            for old in row["steps"]:
                step_folder = folder / row["id"] / f"step-{old['index']:04d}"
                response = read_json(root / row["artifact_path"] / f"step-{old['index']:04d}" / "response.json")["result"]
                step = {k: v for k, v in old.items() if k not in ("source", "source_sha256", "execution", "measurements", "status")}
                step.update(status="format_error", source=None, measurements={})
                try:
                    text = response["body"]["choices"][0]["message"]["content"]
                    source = extract_single_file_source_text(text, preserve_unfenced=True)
                except (SourceExtractionError, KeyError, IndexError, TypeError):
                    pass
                else:
                    step.update(source=source, source_sha256=digest(source.encode()))
                    result = stage(step_folder / "execution.json", {"source_sha256": step["source_sha256"], "runtime": cfg["runtime"]},
                                   lambda: evaluator(source, step["target_language"], problem, step_folder / "execution", cfg["runtime"]))
                    step.update(status=result["status"], execution=result)
                steps.append(step)
                step["measurements"] = step_measurements(execution["metrics"], origin, previous, language, steps, step_folder / "measurements")
                decision = POLICIES[execution["policy"]].decide(execution, origin, language, steps)
                immutable_json(step_folder / "step.json", step)
                if decision["terminal"]:
                    break
                if step["target_language"] == language:
                    previous = step["source"]
            if not decision["terminal"]:
                decision["reason"] = "saved_history_exhausted"
            keys = ("status", "category", "success", "reached_step", "unique_state_count")
            records.append({"trial_id": row["id"], "decision": decision,
                            "matches_original": all(decision.get(k) == row["decision"].get(k) for k in keys),
                            "steps": steps})
        summary = {"replay_id": replay_id, "model_calls": 0, "recorded": len(records),
                   "matches_original": all(r["matches_original"] for r in records), "trials": records}
        write_json(folder / "summary.json", summary)
        seal(folder)
        return summary
