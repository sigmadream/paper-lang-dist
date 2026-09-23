"""Atomic stage checkpoints and integrity-checked, immutable evidence."""
from contextlib import contextmanager
import json
import os
from pathlib import Path

from rttdist.experiment_io import digest, read_json, write_json, timestamp
from .profiles import identifier


class StoreError(ValueError):
    pass


@contextmanager
def exclusive_lock(root):
    """OS lock releases on process death; a leftover file is not a live lock."""
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    with (root / ".lock").open("a+b") as stream:
        stream.seek(0, 2)
        if stream.tell() == 0:
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise StoreError("Experiment is locked by another process") from exc
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == "nt":
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)


def immutable_json(path, value):
    path = Path(path)
    if path.exists():
        if read_json(path) != value:
            raise StoreError(f"Immutable record changed: {path.name}")
    else:
        write_json(path, value)


def immutable_bytes(path, value):
    path = Path(path)
    if path.exists():
        if path.read_bytes() != value:
            raise StoreError(f"Immutable artifact changed: {path.name}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(value)
    os.replace(temporary, path)


def stage(path, contract, compute):
    path = Path(path)
    if path.exists():
        old = read_json(path)
        if old["contract"] != contract or old["result_sha256"] != digest(old["result"]):
            raise StoreError(f"Checkpoint mismatch: {path.name}")
        return old["result"]
    result = compute()
    write_json(path, {"contract": contract, "result": result, "result_sha256": digest(result)})
    return result


def event(folder, kind, **details):
    # Each trial has a single writer; model workers use independent event files.
    path = Path(folder) / "events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"at": timestamp(), "event": kind, **details}, ensure_ascii=False) + "\n")
        stream.flush()


def snapshot_files(folder):
    folder = Path(folder)
    return {p.relative_to(folder).as_posix(): digest(p.read_bytes()) for p in sorted(folder.rglob("*"))
            if p.is_file() and p.name not in ("sealed.json", "events.jsonl") and not p.name.endswith(".tmp")}


def seal(folder):
    immutable_json(Path(folder) / "sealed.json", snapshot_files(folder))


def verify(folder):
    folder = Path(folder)
    path = folder / "sealed.json"
    if not path.exists() or read_json(path) != snapshot_files(folder):
        raise StoreError(f"Artifact integrity check failed: {folder}")


def trial_id(model, problem, route, repeat):
    for part in [model, problem, *route]:
        identifier(part)
    return f"{model}/{problem}/{route[0]}-via-{route[1]}/repeat-{repeat:03d}"
