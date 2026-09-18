"""Read the durable v2 progress; process liveness must be checked separately."""
from collections import Counter
from pathlib import Path
import argparse
import json


def snapshot(root):
    read = lambda p: json.loads(p.read_text(encoding="utf-8"))
    state = read(root / "campaign_status.json")
    runs = []
    total = 0
    for path in sorted(root.glob("*/run_metadata.json")):
        meta = read(path)
        counts = Counter()
        active = []
        for index_path in path.parent.glob("*/cpp-to-*/attempts.json"):
            index = read(index_path)
            selected = index["selected_attempt_id"]
            attempt = next(a for a in index["attempts"] if a["attempt_id"] == (selected or index["active_attempt_id"]))
            if selected:
                counts[attempt["status"]] += 1
            else:
                manifest = index_path.parent / attempt["manifest_path"]
                value = read(manifest) if manifest.exists() else {}
                active.append({"problem": index_path.parent.parent.name, "route": index_path.parent.name,
                               "status": value.get("status", "starting"),
                               "iterations_recorded": len(value.get("iterations", []))})
        completed = sum(counts.values())
        if meta["phase"] == "main":
            total += completed
        runs.append({"run": meta["run_id"], "phase": meta["phase"], "completed": completed,
                     "expected": len(meta["problem_ids"])*len(meta["target_languages"]),
                     "statuses": dict(counts), "active": active})
    revision = root / "execution_plan_revision.json"
    expected = read(revision)["main_observations"] if revision.exists() else 360
    return {"campaign": state, "runs": runs, "main_completed": total, "main_expected": expected}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("--root", type=Path, default=Path("artifacts-lmstudio/v2-a-quality-1"))
    args = parser.parse_args()
    print(json.dumps(snapshot(args.root), indent=2, ensure_ascii=False))
