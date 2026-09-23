"""One execution engine for model matrices and versioned RTT policies."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import importlib.metadata
import inspect
import functools
from pathlib import Path
import platform
import random
import shutil
import time
import uuid

from rttdist.experiment_io import command_info, digest, read_json, write_json
from rttdist.extract import extract_single_file_source_text, SourceExtractionError
from rttdist.fps_execution import evaluate
from rttdist.prompts import build_translation_prompt
from rttdist.providers import create_provider, ProviderError
from .config import LANGUAGES, provider_settings
from .metrics import METRICS, MetricContext, measure
from .policies import POLICIES, outcome
from .store import StoreError, event, exclusive_lock, immutable_json, immutable_bytes, seal, stage, trial_id, verify


def corpus_files(cfg):
    """Validate separate public examples and hidden evaluation inputs."""
    paths = {}
    for pid in cfg["problem_ids"]:
        problem = Path(cfg["corpus_root"]) / pid
        required = [problem / "statement.md"]
        required += [problem / ("reference." + LANGUAGES[l]) for l in {r[0] for r in cfg["routes"]}]
        sets = {}
        for name in ("prompt_examples", "evaluation"):
            inputs = sorted((problem / name).glob("*.inp"))
            outputs = sorted((problem / name).glob("*.out"))
            if not inputs or {p.stem for p in inputs} != {p.stem for p in outputs}:
                raise ValueError(f"Incomplete {name} pairs: {pid}")
            if name == "evaluation" and len(inputs) < cfg["runtime"]["minimum_evaluation_cases"]:
                raise ValueError(f"Insufficient evaluation cases: {pid}")
            required.extend(inputs + outputs)
            sets[name] = {p.read_text(encoding="utf-8").removesuffix("\n") for p in inputs}
        if sets["prompt_examples"] & sets["evaluation"]:
            raise ValueError(f"Prompt/evaluation input overlap: {pid}")
        for path in required:
            if not path.is_file():
                raise ValueError(f"Missing corpus file: {path}")
            paths[path.relative_to(Path(cfg["corpus_root"])).as_posix()] = digest(path.read_bytes())
    return paths


def implementation_hashes():
    package = Path(__file__).resolve().parents[1]
    hashes = {p.relative_to(package).as_posix(): digest(p.read_bytes()) for p in sorted(package.rglob("*.py"))}
    # Include extension implementations as well as their declared versions.
    from .aggregation import AGGREGATORS
    from rttdist.providers import PROVIDER_FACTORIES
    functions = [m.compute for m in METRICS.values()] + [p.decide for p in POLICIES.values()]
    functions += [a.compute for a in AGGREGATORS.values()] + list(PROVIDER_FACTORIES.values())
    for fn in functions:
        while isinstance(fn, functools.partial):
            fn = fn.func
        try:
            path = inspect.getsourcefile(fn)
        except TypeError:
            fn = type(fn)
            path = inspect.getsourcefile(fn)
        if path and Path(path).is_file():
            hashes["extension:" + fn.__module__] = digest(Path(path).read_bytes())
    return hashes


def _metric_tools(profile, *, scope="execution", required=True):
    files = {}
    for spec in profile[scope]["metrics"]:
        if spec["metric"] == "jplag":
            options = spec["options"]
            if not options.get("jar") or not options.get("java"):
                if required:
                    raise ValueError("Execution JPlag metric requires java and jar options")
                files[spec["id"]] = {"status": "not_configured"}
                continue
            jar = Path(options["jar"])
            if required and (not jar.is_file() or not shutil.which(options["java"])):
                raise ValueError("Execution JPlag tool is unavailable")
            files[spec["id"]] = {"jar": str(jar), "sha256": digest(jar.read_bytes()) if jar.is_file() else None,
                                  "java": command_info([options["java"], "--version"])}
    return files


def environment_metadata():
    return {"python": platform.python_version(), "platform": platform.platform(),
            "packages": {name: importlib.metadata.version(name) for name in ("PyYAML", "tree-sitter", "tree-sitter-cpp", "apted")}}


def toolchain_metadata(cfg):
    return {l: command_info([tool, "--version"]) for l, tool in cfg["runtime"]["tools"].items()}


def freeze(cfg, root):
    hashes = corpus_files(cfg)
    missing_tools = [language for language, tool in cfg["runtime"]["tools"].items() if not shutil.which(tool)]
    if missing_tools:
        raise ValueError(f"Missing runtime tools: {', '.join(missing_tools)}")
    contract = {"schema_version": 1, "config": cfg, "corpus_hashes": hashes,
                "implementation_hashes": implementation_hashes(), "metric_tools": _metric_tools(cfg["profile"]),
                "environment": environment_metadata(), "toolchains": toolchain_metadata(cfg)}
    immutable_json(root / "contract.json", contract)
    for name, expected in hashes.items():
        destination = root / "corpus" / name
        if destination.exists():
            if digest(destination.read_bytes()) != expected:
                raise StoreError("Frozen corpus changed")
        else:
            immutable_bytes(destination, (Path(cfg["corpus_root"]) / name).read_bytes())
    jobs = [{"id": trial_id(model, pid, route, repeat), "model_id": model, "problem_id": pid,
             "route": route, "repeat": repeat} for model in cfg["models"] for pid in cfg["problem_ids"]
            for route in cfg["routes"] for repeat in range(1, cfg["repeats"] + 1)]
    random.Random(cfg["schedule_seed"]).shuffle(jobs)
    immutable_json(root / "schedule.json", jobs)
    return contract, jobs


def step_measurements(specs, origin, previous, language, steps, folder):
    step = steps[-1]
    result = {}
    for spec in specs:
        if spec["scope"] == "roundtrip" and step["target_language"] != language:
            continue
        reference = origin if spec["reference"] == "origin" else (
            (steps[-2]["source"] if len(steps) > 1 else origin) if spec["scope"] == "step" else previous)
        context = MetricContext(reference, step["source"], step["target_language"], folder / spec["id"], step)
        contract = {"spec": spec, "reference": digest(reference.encode()), "candidate": step.get("source_sha256"),
                    "response": digest(step.get("response", {}))}
        result[spec["id"]] = stage(folder / (spec["id"] + ".json"), contract, lambda: measure(spec, context))
    return result


def _messages(cfg, problem, pid, source, a, b):
    example = sorted((problem / "prompt_examples").glob("*.inp"))[0]
    bundle = build_translation_prompt(problem_id=pid, source_language=a, target_language=b,
        problem_statement=(problem / "statement.md").read_text(encoding="utf-8"),
        sample_input=example.read_text(encoding="utf-8"),
        sample_output=example.with_suffix(".out").read_text(encoding="utf-8"),
        source_code=source, template_version=cfg["prompt_template_version"])
    return [m.to_dict() for m in bundle.messages]


def _translate(provider, payload, folder, model, timing):
    def call():
        remaining = model["min_interval_seconds"] - (time.monotonic() - timing[0])
        if remaining > 0:
            time.sleep(remaining)
        try:
            return provider.complete(payload, folder / "provider")
        finally:
            timing[0] = time.monotonic()
    return stage(folder / "response.json", {"payload": payload, "model": model}, call)


def _run_step(cfg, job, index, source, origin, previous, prior, folder, problem, provider, evaluator, timing):
    if (folder / "sealed.json").exists():
        verify(folder)
        record = read_json(folder / "step.json")
        if record["input_sha256"] != digest(source.encode()):
            raise StoreError("Step input lineage changed")
        return record
    a, b = job["route"] if index % 2 else list(reversed(job["route"]))
    model = cfg["models"][job["model_id"]]
    generation = deepcopy(model["generation"])
    if "seed" in generation:
        generation["seed"] += job["repeat"] - 1
    payload = {"model": model["model"], "messages": _messages(cfg, problem, job["problem_id"], source, a, b), **generation}
    base = {"schema_version": 1, "id": job["id"] + f"/{folder.parent.name}/step-{index:04d}", "index": index,
            "previous_step": index - 1 or None, "source_language": a, "target_language": b,
            "input_sha256": digest(source.encode()), "request_sha256": digest(payload), "source": None,
            "status": "infrastructure_error", "measurements": {}}
    folder.mkdir(parents=True, exist_ok=True)
    immutable_json(folder / "request.json", payload)
    event(folder, "translation_requested", index=index, request_sha256=digest(payload))
    response = _translate(provider, payload, folder, model, timing)
    base["response"] = {k: v for k, v in response.items() if k != "body"}
    actual = response.get("actual_model")
    if actual not in model["accepted_models"]:
        raise ProviderError("Response model is missing or not in accepted_models")
    try:
        choice = response["body"]["choices"][0]
        text = choice["message"]["content"]
        extracted = stage(folder / "extraction.json", {"response_sha256": digest(response)},
                          lambda: {"source": extract_single_file_source_text(text, preserve_unfenced=True)})
    except (SourceExtractionError, KeyError, IndexError, TypeError):
        base["status"] = "format_error"
    else:
        code = extracted["source"]
        path = folder / ("source." + LANGUAGES[b])
        immutable_bytes(path, code.encode("utf-8"))
        base.update(source=code, source_sha256=digest(code.encode()), finish_reason=choice.get("finish_reason"))
        evaluation = stage(folder / "execution.json", {"source_sha256": base["source_sha256"], "runtime": cfg["runtime"]},
                           lambda: evaluator(code, b, problem, folder / "execution", cfg["runtime"]))
        base.update(status=evaluation["status"], execution=evaluation)
    base["measurements"] = step_measurements(cfg["profile"]["execution"]["metrics"], origin, previous,
                                              job["route"][0], [*prior, base], folder / "measurements")
    immutable_json(folder / "step.json", base)
    seal(folder)
    event(folder, "step_completed", status=base["status"])
    return base


def _run_trial(cfg, root, job, provider, evaluator, timing, new_attempt):
    trial = root / "trials" / job["id"]
    trial.mkdir(parents=True, exist_ok=True)
    immutable_json(trial / "trial.json", job)
    attempts = sorted(trial.glob("attempt-*"))
    for folder in attempts:
        if (folder / "result.json").exists():
            if not (folder / "sealed.json").exists():
                _recover_commit(cfg, root, folder, job)
            verify(folder)
            return read_json(folder / "result.json")  # First evaluable attempt is final.
    if attempts and not new_attempt:
        folder = attempts[-1]
    else:
        folder = trial / f"attempt-{len(attempts) + 1:03d}"
    folder.mkdir(parents=True, exist_ok=True)
    problem = root / "corpus" / job["problem_id"]
    origin = (problem / ("reference." + LANGUAGES[job["route"][0]])).read_text(encoding="utf-8")
    source = previous = origin
    steps = []
    execution = cfg["profile"]["execution"]
    policy = POLICIES[execution["policy"]]
    decision = outcome()
    event(folder, "attempt_started", attempt=folder.name)
    for index in range(1, execution["max_steps"] + 1):
        try:
            step = _run_step(cfg, job, index, source, origin, previous, steps, folder / f"step-{index:04d}",
                             problem, provider, evaluator, timing)
        except (ProviderError, OSError) as exc:
            # Infrastructure interruptions are retained, never counted as code failures.
            interrupted = {"index": index, "target_language": job["route"][index % 2],
                           "status": "infrastructure_error", "source": None}
            decision = policy.decide(execution, origin, job["route"][0], [*steps, interrupted])
            decision["reason"] = type(exc).__name__
            write_json(folder / f"interruption-{uuid.uuid4().hex}.json", {"step": index, "reason": type(exc).__name__})
            event(folder, "attempt_interrupted", step=index, reason=type(exc).__name__)
            break
        steps.append(step)
        decision = policy.decide(execution, origin, job["route"][0], steps)
        if decision["terminal"]:
            break
        source = step["source"]
        if step["target_language"] == job["route"][0]:
            previous = source
    if not decision["terminal"]:
        decision = outcome("policy_error", category="invalid", reason="policy_did_not_terminate_at_budget")
    record = {**job, "attempt": folder.name, "decision": decision, "steps": steps,
              "artifact_path": folder.relative_to(root).as_posix(), "origin_sha256": digest(origin.encode())}
    write_json(folder / "progress.json", record)
    if decision["terminal"] and decision["category"] != "invalid":
        immutable_json(folder / "result.json", record)
        seal(folder)
    return record


def _recover_commit(cfg, root, folder, job):
    """Finish a crash between the atomic result write and the final seal."""
    record = read_json(folder / "result.json")
    if any(record.get(key) != value for key, value in job.items()):
        raise StoreError("Uncommitted trial identity changed")
    for step in record["steps"]:
        step_folder = folder / f"step-{step['index']:04d}"
        verify(step_folder)
        if read_json(step_folder / "step.json") != step:
            raise StoreError("Uncommitted result differs from step evidence")
    language = job["route"][0]
    origin = (root / "corpus" / job["problem_id"] / ("reference." + LANGUAGES[language])).read_text(encoding="utf-8")
    if record["origin_sha256"] != digest(origin.encode()) or record["artifact_path"] != folder.relative_to(root).as_posix():
        raise StoreError("Uncommitted result provenance changed")
    steps = list(record["steps"])
    if record["decision"]["status"] == "infrastructure_error":
        if not list(folder.glob("interruption-*.json")):
            raise StoreError("Missing interruption evidence")
        index = len(steps) + 1
        steps.append({"index": index, "source": None, "status": "infrastructure_error", "target_language": job["route"][index % 2]})
    execution = cfg["profile"]["execution"]
    decision = POLICIES[execution["policy"]].decide(execution, origin, language, steps)
    if any(decision.get(key) != record["decision"].get(key) for key in decision):
        raise StoreError("Uncommitted decision differs from step evidence")
    if not decision["terminal"] or decision["category"] == "invalid":
        raise StoreError("Only an evaluable terminal result can be committed")
    seal(folder)


def run_experiment(cfg, *, resume=False, new_attempt=False, provider_factory=create_provider, evaluator=evaluate):
    """Run each model serially; independent models may run in parallel.

    No prompt cache is shared between repeated trials or model aliases.
    """
    root = Path(cfg["output_root"]) / cfg["id"]
    with exclusive_lock(root):
        if (root / "contract.json").exists() and not resume:
            raise StoreError("Experiment already exists; use resume or a new id")
        if resume and not (root / "contract.json").exists():
            raise StoreError("No experiment to resume")
        contract, jobs = freeze(cfg, root)
        # Verify reference behavior before paying for any model calls.
        for pid in cfg["problem_ids"]:
            problem = root / "corpus" / pid
            for language in sorted({r[0] for r in cfg["routes"]}):
                source = (problem / ("reference." + LANGUAGES[language])).read_text(encoding="utf-8")
                checked = stage(root / "reference_checks" / pid / (language + ".json"),
                                {"source": digest(source.encode()), "corpus": contract["corpus_hashes"], "runtime": cfg["runtime"]},
                                lambda: evaluator(source, language, problem, root / "reference_checks" / pid / language, cfg["runtime"]))
                if checked["status"] != "success":
                    raise ValueError(f"Reference validation failed: {pid}/{language}")
        def run_model(alias):
            model = cfg["models"][alias]
            provider = provider_factory(provider_settings(model), ledger=root / "models" / alias / "costs.jsonl")
            records = []
            timing = [float("-inf")]
            for job in jobs:
                if job["model_id"] == alias:
                    records.append(_run_trial(cfg, root, job, provider, evaluator, timing, new_attempt))
                    write_json(root / "models" / alias / "progress.json", {"processed": len(records), "last_trial": job["id"]})
            return records
        aliases = list(cfg["models"])
        if cfg["parallel_models"] > 1:
            with ThreadPoolExecutor(max_workers=cfg["parallel_models"]) as pool:
                rows = [row for group in pool.map(run_model, aliases) for row in group]
        else:
            rows = [row for alias in aliases for row in run_model(alias)]
        write_json(root / "observations.json", rows)
        return rows
