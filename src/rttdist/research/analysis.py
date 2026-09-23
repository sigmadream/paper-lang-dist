"""Offline analysis of immutable observations; this module never constructs a provider."""
from copy import deepcopy
from pathlib import Path
import uuid

from rttdist.experiment_io import digest, read_json, write_json
from .aggregation import aggregate
from .config import LANGUAGES
from .engine import implementation_hashes, step_measurements, _metric_tools, environment_metadata
from .profiles import identifier, load_profile, read_yaml
from .store import StoreError, exclusive_lock, immutable_json, seal, verify


def load_observations(root):
    root = Path(root)
    contract = read_json(root / "contract.json")
    for name, expected in contract["corpus_hashes"].items():
        path = root / "corpus" / name
        if digest(path.read_bytes()) != expected:
            raise StoreError("Frozen corpus integrity check failed")
    records = []
    for job in read_json(root / "schedule.json"):
        trial = root / "trials" / job["id"]
        selected = None
        for folder in sorted(trial.glob("attempt-*")):
            if (folder / "result.json").exists():
                verify(folder)
                selected = read_json(folder / "result.json")
                break
            if (folder / "progress.json").exists():
                selected = read_json(folder / "progress.json")
                for step in selected["steps"]:
                    verify(folder / f"step-{step['index']:04d}")
        if selected is not None:
            if any(selected[k] != v for k, v in job.items()):
                raise StoreError("Trial identity mismatch")
            records.append(selected)
    return contract, records


def analyze(root, *, profile=None, analysis_id=None):
    """A profile may override analysis, but cannot invent a different execution history."""
    root = Path(root).resolve()
    analysis_id = identifier(analysis_id or ("analysis-" + uuid.uuid4().hex[:12]))
    with exclusive_lock(root):
        contract, records = load_observations(root)
        original = contract["config"]["profile"]
        if profile is None:
            resolved = original
        else:
            base_dir = Path(".")
            raw = deepcopy(profile)
            if isinstance(profile, (str, Path)) and Path(profile).is_file():
                path = Path(profile).resolve()
                raw = read_yaml(path)
                base_dir = path.parent
            if isinstance(raw, dict) and "execution" not in raw and "extends" not in raw:
                raw = {**deepcopy(original), "analysis": {**original["analysis"], **raw.get("analysis", raw)}}
            resolved = load_profile(raw, base_dir)
            if resolved["execution"] != original["execution"]:
                raise ValueError("Offline analysis cannot change execution policy; run a new experiment")
        folder = root / "analyses" / analysis_id
        manifest = {"schema_version": 1, "experiment_sha256": digest(contract), "profile": resolved,
                    "input_records_sha256": digest(records), "implementation_hashes": implementation_hashes(),
                    "metric_tools": _metric_tools(resolved, scope="analysis", required=False), "environment": environment_metadata()}
        if (folder / "sealed.json").exists():
            verify(folder)
            if read_json(folder / "contract.json") != manifest:
                raise StoreError("Analysis conditions changed; use a new analysis id")
            return read_json(folder / "summary.json")
        immutable_json(folder / "contract.json", manifest)
        analyzed = []
        for record in records:
            row = deepcopy(record)
            language = row["route"][0]
            origin = (root / "corpus" / row["problem_id"] / ("reference." + LANGUAGES[language])).read_text(encoding="utf-8")
            previous = origin
            for i, step in enumerate(row["steps"]):
                step["analysis_measurements"] = step_measurements(resolved["analysis"]["metrics"], origin, previous,
                    language, row["steps"][:i + 1], folder / "measurements" / row["id"] / f"step-{step['index']:04d}")
                if step["target_language"] == language and step.get("source") is not None:
                    previous = step["source"]
            analyzed.append(row)
        expected = len(read_json(root / "schedule.json"))
        summary = {"schema_version": 1, "experiment_id": contract["config"]["id"], "analysis_id": analysis_id,
                   "profile": resolved, "planned": expected, "recorded": len(records),
                   "complete": len(records) == expected and all(r["decision"]["terminal"] and r["decision"]["category"] != "invalid" for r in records),
                   "groups": aggregate(analyzed, resolved["analysis"])}
        write_json(folder / "observations.json", analyzed)
        write_json(folder / "summary.json", summary)
        import csv
        with (folder / "summary.csv").open("w", encoding="utf-8", newline="") as stream:
            names = ["model_id", "route", "recorded", "valid", "success", "success_rate", "mean_hops",
                     "hop_adjusted_distance", "mean_unique_state_count", "penalized_state_distance"]
            writer = csv.DictWriter(stream, fieldnames=names, extrasaction="ignore")
            writer.writeheader()
            writer.writerows({**group, "route": "-via-".join(group["route"])} for group in summary["groups"])
        seal(folder)
        return summary


def status(root):
    root = Path(root)
    _, rows = load_observations(root)
    from collections import Counter
    return {"planned": len(read_json(root / "schedule.json")), "recorded": len(rows),
            "categories": dict(Counter(r["decision"]["category"] for r in rows))}
