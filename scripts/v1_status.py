"""Read-only progress snapshot. A process/session poll is still required for liveness."""
from collections import Counter
from pathlib import Path
import json

root = Path("artifacts-lmstudio")
total = 0
for directory in sorted(root.glob("v1-qwen25-7b-p1-r*")):
    statuses = Counter()
    active = []
    for index_path in directory.glob("IPOP_*/cpp-to-*/attempts.json"):
        index = json.loads(index_path.read_text(encoding="utf-8"))
        entry = next(a for a in index["attempts"] if a["attempt_id"] == (index["selected_attempt_id"] or index["active_attempt_id"]))
        if index["selected_attempt_id"]:
            statuses[entry["status"]] += 1
            total += 1
        else:
            path = index_path.parent / entry["manifest_path"]
            manifest = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
            active.append({"problem": index_path.parent.parent.name, "route": index_path.parent.name,
                           "iterations_recorded": len(manifest.get("iterations", [])), "status": manifest.get("status", "starting")})
    print(json.dumps({"run": directory.name, "completed": sum(statuses.values()), "expected": 57,
                      "statuses": dict(statuses), "active": active}, ensure_ascii=False))
print(f"TOTAL {total}/171")
