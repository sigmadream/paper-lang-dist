"""Replace the three-repeat controller at a durable model-response checkpoint."""
from pathlib import Path
import hashlib
import subprocess
import sys
import time

import psutil

from rttdist.experiment_io import digest, read_json, timestamp, write_json


def main():
    workspace = Path(__file__).resolve().parents[1]
    root = workspace / "artifacts-lmstudio/v2-a-quality-1"
    revision_path = root / "execution_plan_revision.json"
    if revision_path.exists():
        raise RuntimeError("Plan already amended; do not launch a duplicate worker")
    previous = read_json(root / "continuation_status.json")
    supervisor = psutil.Process(previous["pid"])
    if "scripts/finish_v2.py" not in supervisor.cmdline():
        raise RuntimeError("Unexpected supervisor; refusing to stop it")
    workers = [p for p in supervisor.children(recursive=True)
               if "scripts/run_v2.py" in p.cmdline()]
    if len(workers) != 2:
        raise RuntimeError("Expected the Windows venv launcher and its Python worker")
    parent = next(p for p in workers if p.ppid() == supervisor.pid)
    worker = next(p for p in workers if p.ppid() == parent.pid)
    run_id = "v2-a-quality-1-r1"
    run_root = root / run_id
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        worker.suspend()
        keep_suspended = False
        try:
            requests = list(run_root.glob("*/cpp-to-*/attempt-*/iterations/iter-*/step-*/llm-request.json"))
            latest = max(requests, key=lambda p: p.stat().st_mtime_ns)
            if (latest.parent / "llm-response.json").exists():
                keep_suspended = True
                break
        finally:
            if not keep_suspended:
                worker.resume()
        time.sleep(.2)
    else:
        raise TimeoutError("No durable model response checkpoint reached; original experiment continues")
    try:
        revision = {"created_at": timestamp(), "reason": "User requested one main repetition for a faster preliminary result",
                    "original_main_repetitions": 3, "original_main_observations": 360,
                    "main_repetitions": 1, "main_observations": 120,
                    "retained_run_id": run_id, "cancelled_run_ids": ["v2-a-quality-1-r2", "v2-a-quality-1-r3"],
                    "original_design_hash": digest(read_json(root / "frozen_design.json")),
                    "condition_hash": read_json(run_root / "run_metadata.json")["condition_hash"],
                    "confirmation_cycles": 5, "max_iterations": 10,
                    "checkpoint_response": str(latest.parent / "llm-response.json"),
                    "interruption_policy": "Only stop after the latest model response is durable; resume cached completed steps",
                    "previous_supervisor_pid": supervisor.pid, "previous_worker_pid": worker.pid,
                    "new_driver": "scripts/run_v2_single.py",
                    "new_driver_sha256": hashlib.sha256((workspace / "scripts/run_v2_single.py").read_bytes()).hexdigest()}
        write_json(revision_path, revision)
        write_json(root / "single_driver_snapshot.json", {
            "source": (workspace / "scripts/run_v2_single.py").read_text(encoding="utf-8"),
            "sha256": revision["new_driver_sha256"]})
        children = parent.children(recursive=True)
        supervisor.terminate()
        supervisor.wait(timeout=5)
        for process in reversed(children):
            try:
                process.terminate()
            except psutil.NoSuchProcess:
                pass
        parent.terminate()
        _, alive = psutil.wait_procs([parent, *children], timeout=5)
        if alive:
            raise RuntimeError("Old worker has not stopped; refusing to run two controllers")
    except Exception:
        try:
            worker.resume()
        except psutil.NoSuchProcess:
            pass
        raise
    with (root / "single.stdout.log").open("ab") as out, (root / "single.stderr.log").open("ab") as err:
        child = subprocess.Popen([sys.executable, "-X", "utf8", "-u", "scripts/run_v2_single.py"],
                                 cwd=workspace, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                 creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    print(f"Started single-repetition controller launcher PID {child.pid}")
    print(f"Retained cached response: {latest.parent}")


if __name__ == "__main__":
    main()
