"""Versioned experiment provenance and corpus execution gates."""
from dataclasses import asdict
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
from urllib.request import urlopen

from rttdist.ast_similarity import parser_smoke
from rttdist.corpus import validate_corpus
from rttdist.exec.adapters import evaluate_source


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def serial(value):
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    raise TypeError(type(value))


def digest(value):
    raw = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True, ensure_ascii=False, default=serial).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False, default=serial) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def command_info(command):
    resolved = shutil.which(command[0])
    if not resolved:
        return {"path": None, "missing_toolchain": command[0]}
    proc = subprocess.run([resolved, *command[1:]], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
    return {"path": resolved, "version": (proc.stdout+proc.stderr).strip(), "exit_code": proc.returncode}


def environment():
    return {"os": platform.platform(), "python_executable": sys.executable, "python_version": sys.version,
            "toolchains": {name: command_info([name, flag]) for name, flag in (("g++", "--version"), ("gcc", "--version"), ("javac", "-version"), ("java", "-version"), ("uv", "--version"), ("Rscript", "--version"))},
            "ast_packages": parser_smoke(), "compile_options": {"cpp": ["-O2", "-std=c++17"], "c": ["-O2", "-std=c11"], "java": ["-encoding", "UTF-8"]}}


def corpus_hashes(entries):
    return {e.problem_id: {str(path.resolve()): digest(path.read_bytes()) for path in
            [e.seed_path, e.statement_path, *[p for pair in (*e.fixture_pairs, *(e.prompt_examples or ()))
                                           for p in (pair.input_path, pair.output_path)]]} for e in entries}


def validate_execute(config):
    entries = validate_corpus(config)
    env = environment()
    missing = [name for name in ("g++", "gcc", "java", "javac") if env["toolchains"][name].get("missing_toolchain")]
    if missing:
        raise ValueError(f"Missing toolchains: {missing}")
    result = {"schema_version": 2, "validator_version": "execute-v1", "created_at": timestamp(),
              "environment": env, "timeout_seconds": config.runtime.timeout_seconds,
              "content_hashes": corpus_hashes(entries), "problems": {}}
    root = config.output_root / "validation" / result["created_at"].replace(":", "-")
    for entry in entries:
        evaluation = evaluate_source(language="cpp", source_path=entry.seed_path, problem=entry,
                                     workspace_root=root, timeout_seconds=config.runtime.timeout_seconds)
        result["problems"][entry.problem_id] = asdict(evaluation)
        print(f"seed {entry.problem_id}: {evaluation.status.value}", flush=True)
    result["validation_hash"] = digest(result)
    write_json(config.output_root / "corpus_validation.json", result)
    return result


def validation_gate(config):
    saved = read_json(config.output_root / "corpus_validation.json")
    check = dict(saved)
    claimed = check.pop("validation_hash")
    if digest(check) != claimed:
        raise ValueError("Validation content hash mismatch")
    entries = validate_corpus(config)
    current = corpus_hashes(entries)
    if any(saved["content_hashes"].get(k) != v for k, v in current.items()):
        raise ValueError("Corpus changed; rerun validate-corpus --execute")
    env = environment()
    if saved["timeout_seconds"] != config.runtime.timeout_seconds or saved["environment"] != env:
        raise ValueError("Validation environment changed; revalidate")
    failed = [e.problem_id for e in entries if saved["problems"][e.problem_id]["status"] != "success"]
    if failed:
        raise ValueError(f"Selected seed failures must be excluded from all routes: {failed}")
    return entries, saved


def server_metadata(host, model):
    base = host.removesuffix("/v1").rstrip("/")
    with urlopen(base + "/api/v1/models", timeout=15) as response:
        native = json.load(response)
    with urlopen(host.rstrip("/") + "/models", timeout=15) as response:
        compatibility = json.load(response)
    matches = [(m, instance) for m in native["models"] for instance in m.get("loaded_instances", []) if instance["id"] == model]
    if len(matches) != 1:
        raise ValueError(f"Configured model must identify exactly one loaded instance: {model}")
    m, instance = matches[0]
    # Version from the installed executable, never inferred from a model filename.
    exe = Path.home() / "scoop/apps/lmstudio/current/LM Studio.exe"
    version = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-Item -LiteralPath '"+str(exe).replace("'", "''")+"').VersionInfo.ProductVersion"], capture_output=True, text=True, timeout=15).stdout.strip()
    return {"native_response": native, "models_response": compatibility,
            "effective": {"model": model, "key": m["key"], "publisher": m["publisher"],
                          "quantization": m["quantization"], "size_bytes": m["size_bytes"],
                          "config": instance["config"], "lmstudio_version": version,
                          "version_source": str(exe)}}


def code_provenance():
    root = Path(__file__).resolve().parents[2]
    paths = sorted((root / "src/rttdist").rglob("*.py")) + [root / "pyproject.toml", root / "uv.lock"]
    for name in ("run_v1_main.py", "run_v2.py", "v1_checks.py"):
        driver = root / "scripts" / name
        if driver.exists():
            paths.append(driver)
    hashes = {p.relative_to(root).as_posix(): digest(p.read_bytes()) for p in paths}
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True, check=True).stdout.strip()
    return {"commit": commit, "file_hashes": hashes, "source_hash": digest(hashes),
            "prompt_template_hash": hashes["src/rttdist/prompts.py"], "extractor_hash": hashes["src/rttdist/extract.py"], "lock_hash": hashes["uv.lock"]}
