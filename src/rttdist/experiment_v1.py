"""SF experiment runner. Legacy artifacts remain readable by the original runner.

Every model request, execution and completed step is checkpointed independently.
Only the first evaluable attempt is selected, regardless of its outcome.
"""
from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path
import time
from urllib import error, request

from rttdist.experiment_io import (code_provenance, digest, read_json, server_metadata,
                                  timestamp, validation_gate, write_json)
from rttdist.exec.adapters import evaluate_source
from rttdist.extract import SourceExtractionError, extract_single_file_source_text
from rttdist.normalize import hash_normalized_cpp_tokens
from rttdist.prompts import build_translation_prompt, PROMPT_TEMPLATE_VERSION
from rttdist.similarity import token_deltas

MANIFEST_VERSION = 3


def sf_success(metrics, c):
    s = metrics["stabilization"]
    return (s["tau_candidate"] is not None and
            metrics["route_preservation"]["candidate_phase_all_passed"] is True and
            s["confirmations_held"] >= c)


def convergence(hashes):
    if len(hashes) >= 2 and hashes[-1] == hashes[-2]:
        return "fixed_point_candidate"
    for period in range(2, 5):
        if len(hashes) >= 2*period and hashes[-period:] == hashes[-2*period:-period]:
            return "oscillation"
    return "continue"


def initial_metrics():
    return {"schema_version": 2,
            "stabilization": {"tau_candidate": None, "confirmation_cycles_run": 0,
                "confirmations_held": 0, "first_broken_confirmation": None, "first_break_reason": None},
            "route_preservation": {"candidate_phase_all_passed": None,
                "first_failed_step": None, "evaluated_step_count": 0, "per_confirmation": []},
            "delta_0": {}}


def apply_iteration(metrics, iteration, hashes, cmax):
    """Pure reduction over durable iteration records, also used during resume."""
    s, p = metrics["stabilization"], metrics["route_preservation"]
    ci = iteration["confirmation_index"]
    status = iteration["status"]
    p["evaluated_step_count"] += sum("execution" in step for step in iteration["steps"])
    bad = next((step for step in iteration["steps"] if step["status"] != "success"), None)
    if bad and p["first_failed_step"] is None:
        p["first_failed_step"] = {"iteration_index": iteration["iteration_index"],
            "step_index": bad["step_index"], "target_language": bad["target_language"], "status": bad["status"]}
    if ci:
        held = iteration["hash_unchanged"] is True and iteration["all_steps_passed"] is True
        p["per_confirmation"].append({k: iteration[k] for k in ("confirmation_index", "hash_unchanged", "all_steps_passed", "status")})
        # A format/compile failure is an observed terminal confirmation, but not a completed round trip.
        s["confirmation_cycles_run"] += iteration.get("roundtrip_hash") is not None
        if held:
            s["confirmations_held"] += 1
        else:
            s["first_broken_confirmation"] = ci
            s["first_break_reason"] = "format_error" if status == "parse_error" else "test_failed" if status != "confirmation_failed" else "hash_changed"
        if status != "success":
            return status
        return "success" if s["confirmations_held"] == cmax else None
    if status != "success":
        return status
    state = convergence(hashes)
    if state == "fixed_point_candidate":
        s["tau_candidate"] = iteration["iteration_index"]
        p["candidate_phase_all_passed"] = p["first_failed_step"] is None
        return "success" if cmax == 0 else None
    return "oscillation" if state == "oscillation" else None


def request_translation(payload, host, folder, *, retries=3, timeout=300):
    """Persist the exact wire request/response and every transient retry."""
    folder.mkdir(parents=True, exist_ok=True)
    write_json(folder / "llm-request.json", payload)
    cached = folder / "llm-response.json"
    if cached.exists():
        return read_json(cached)
    start_index = len(list(folder.glob("api-attempt-*.json"))) + 1
    for offset in range(retries + 1):
        started, tick = timestamp(), time.perf_counter()
        raw, http_status, retry = None, None, False
        failure = None
        try:
            req = request.Request(host.rstrip("/") + "/chat/completions", data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
            with request.urlopen(req, timeout=timeout) as response:
                http_status = response.status
                raw = response.read().decode("utf-8")
            parsed = json.loads(raw)
        except error.HTTPError as exc:
            http_status = exc.code
            raw = exc.read().decode("utf-8", errors="replace")
            retry = exc.code >= 500
            failure = str(exc)
        except (error.URLError, OSError, TimeoutError) as exc:
            retry, failure = True, str(exc)
        except (ValueError, TypeError) as exc:
            failure = str(exc)
        write_json(folder / f"api-attempt-{start_index+offset:03d}.json",
                   {"started_at": started, "seconds": time.perf_counter()-tick,
                    "request": payload, "http_status": http_status, "raw_response": raw,
                    "error": failure, "will_retry": bool(failure and retry and offset < retries)})
        if failure is None:
            write_json(cached, parsed)
            return parsed
        if not retry or offset == retries:
            raise RuntimeError(failure)
        time.sleep(2**offset)


def run_route(config, problem, target, run_id, metadata, *, resume=False, new_attempt=False):
    route = f"cpp-to-{target}"
    root = config.output_root / run_id / problem.problem_id / route
    index_path = root / "attempts.json"
    if index_path.exists():
        index = read_json(index_path)
        if index["condition_hash"] != metadata["condition_hash"]:
            raise ValueError("Attempt condition mismatch")
        if index["selected_attempt_id"]:
            chosen = [a for a in index["attempts"] if a["attempt_id"] == index["selected_attempt_id"]]
            if len(chosen) != 1:
                raise ValueError("Invalid selected attempt index")
            return read_json(root / chosen[0]["manifest_path"])
        if not resume:
            raise ValueError("Existing incomplete attempt; use resume")
        reruns = read_json(root / "rerun_log.json")
        if len(reruns) >= metadata["recovery"]["max_resumes_per_route"]:
            raise ValueError("Route recovery budget exhausted")
        previous = index["active_attempt_id"]
        if new_attempt:
            attempt_id = f"attempt-{len(index['attempts'])+1:03d}"
            index["active_attempt_id"] = attempt_id
            index["attempts"].append({"attempt_id": attempt_id, "manifest_path": attempt_id+"/run.json", "status": "running"})
            write_json(index_path, index)
        reruns.append({"previous_attempt": previous, "new_attempt": index["active_attempt_id"],
                       "cause": "unresumable_infrastructure_new_attempt" if new_attempt else "resume_infrastructure_or_interruption", "at": timestamp(),
                       "condition_hash": metadata["condition_hash"], "selected": False})
        write_json(root / "rerun_log.json", reruns)
    else:
        index = {"schema_version": 1, "condition_hash": metadata["condition_hash"],
                 "active_attempt_id": "attempt-001", "selected_attempt_id": None,
                 "attempts": [{"attempt_id": "attempt-001", "manifest_path": "attempt-001/run.json", "status": "running"}]}
        write_json(index_path, index)
        write_json(root / "rerun_log.json", [])
    attempt = root / index["active_attempt_id"]
    active = next(a for a in index["attempts"] if a["attempt_id"] == index["active_attempt_id"])
    attempt.mkdir(parents=True, exist_ok=True)
    seed = problem.seed_path.read_text(encoding="utf-8").rstrip()
    (attempt / "seed.cpp").write_text(seed + "\n", encoding="utf-8")
    current, hashes = seed, [hash_normalized_cpp_tokens(seed)]
    metrics = initial_metrics()
    manifest = {"manifest_version": MANIFEST_VERSION, "run_id": run_id, "problem_id": problem.problem_id,
                "route": route, "target_language": target, "attempt_id": index["active_attempt_id"],
                "condition_hash": metadata["condition_hash"], "validation_hash": metadata["validation_hash"],
                "distance_metrics": metrics, "iterations": [], "status": "running", "details": {}}
    final = None
    for t in range(1, config.runtime.max_iterations + config.runtime.confirmation_cycles + 1):
        tau = metrics["stabilization"]["tau_candidate"]
        if tau is None and t > config.runtime.max_iterations:
            final = "max_iter_no_convergence"
            break
        ci = t - tau if tau else None
        folder = attempt / "iterations" / f"iter-{t:03d}"
        iteration_path = folder / "iteration.json"
        if iteration_path.exists():
            it = read_json(iteration_path)
        else:
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "input.cpp").write_text(current + "\n", encoding="utf-8")
            it = {"iteration_index": t, "phase": "confirmation" if ci else "candidate",
                  "confirmation_index": ci, "steps": [], "status": "success", "hash_unchanged": None,
                  "all_steps_passed": None, "roundtrip_hash": None}
            working = current
            for step_index, (source_lang, language) in enumerate((("cpp", target), (target, "cpp")), 1):
                step_dir = folder / f"step-{step_index:03d}"
                step_dir.mkdir(parents=True, exist_ok=True)
                step_path = step_dir / "step.json"
                if step_path.exists():
                    step = read_json(step_path)
                else:
                    elapsed = (datetime.now(timezone.utc) - datetime.fromisoformat(metadata["started_at"])).total_seconds()
                    if elapsed > metadata["recovery"]["max_wall_hours"]*3600:
                        raise ValueError("Run wall-clock recovery deadline reached")
                    prompt = build_translation_prompt(problem_id=problem.problem_id,
                        source_language=source_lang, target_language=language,
                        problem_statement=problem.statement_path.read_text(encoding="utf-8"),
                        sample_input=problem.prompt_sample.input_path.read_text(encoding="utf-8"),
                        sample_output=problem.prompt_sample.output_path.read_text(encoding="utf-8"),
                        source_code=working, direction="seed_to_target" if step_index == 1 else "target_to_seed")
                    payload = {"model": config.lmstudio.model, "messages": [m.to_dict() for m in prompt.messages],
                               "temperature": 0, "max_tokens": config.lmstudio.max_tokens, "stream": False,
                               **metadata["decoding"]}
                    step = {"step_index": step_index, "source_language": source_lang,
                            "target_language": language, "status": "success"}
                    print(f"{run_id} {problem.problem_id}/{target} t={t} c={ci or 0} step={step_index}", flush=True)
                    try:
                        response = request_translation(payload, config.lmstudio.host, step_dir)
                    except RuntimeError as exc:
                        # No terminal iteration is written: completed step checkpoints survive resume.
                        manifest.update(status="api_error", details={"error": str(exc), "iteration_index": t, "step_index": step_index})
                        write_json(attempt / "run.json", manifest)
                        active["status"] = "api_error"
                        write_json(index_path, index)
                        return manifest
                    step["truncated"] = any(ch.get("finish_reason") == "length" for ch in response.get("choices", []))
                    try:
                        translated = extract_single_file_source_text(response["choices"][0]["message"]["content"])
                    except (SourceExtractionError, KeyError, IndexError, TypeError) as exc:
                        step.update(status="parse_error", error=str(exc))
                    else:
                        extension = {"cpp": "cpp", "c": "c", "java": "java", "python": "py"}[language]
                        source_path = step_dir / ("source." + extension)
                        source_path.write_text(translated.rstrip()+"\n", encoding="utf-8")
                        step["source_path"] = str(source_path.resolve())
                        evaluation = evaluate_source(language=language, source_path=source_path, problem=problem,
                            workspace_root=step_dir, timeout_seconds=config.runtime.timeout_seconds)
                        step.update(status=evaluation.status.value, execution=asdict(evaluation), details=evaluation.details)
                    write_json(step_path, step)
                it["steps"].append(step)
                if step["status"] != "success":
                    it["status"] = step["status"]
                    break
                working = Path(step["source_path"]).read_text(encoding="utf-8").rstrip()
            it["all_steps_passed"] = len(it["steps"]) == 2 and all(s["status"] == "success" for s in it["steps"])
            # A restored source can be hashed even when its fixture evaluation fails.
            # Preserve both observations independently instead of treating failed tests as a missing hash.
            if len(it["steps"]) == 2 and it["steps"][-1].get("source_path"):
                working = Path(it["steps"][-1]["source_path"]).read_text(encoding="utf-8").rstrip()
                (folder / "roundtrip.cpp").write_text(working+"\n", encoding="utf-8")
                it["roundtrip_hash"] = hash_normalized_cpp_tokens(working)
                it["delta_step"] = token_deltas(current, working)
                for value in it["delta_step"].values():
                    value.update(reference="previous_source", candidate="roundtrip_source")
                if ci:
                    it["hash_unchanged"] = it["roundtrip_hash"] == hashes[tau]
                    if not it["hash_unchanged"] and it["all_steps_passed"]:
                        it["status"] = "confirmation_failed"
            write_json(iteration_path, it)
        if it["roundtrip_hash"]:
            hashes.append(it["roundtrip_hash"])
            current = (folder / "roundtrip.cpp").read_text(encoding="utf-8").rstrip()
        final = apply_iteration(metrics, it, hashes, config.runtime.confirmation_cycles)
        manifest["iterations"].append(it)
        if metrics["stabilization"]["tau_candidate"] == t:
            metrics["delta_0"] = token_deltas(seed, current)
            manifest["candidate_source_path"] = str((folder / "roundtrip.cpp").resolve())
        manifest.update(hash_history=hashes, status=final or "running")
        write_json(attempt / "run.json", manifest)
        if final:
            break
    manifest.update(status=final or "max_iter_no_convergence", finished_at=timestamp())
    if manifest["iterations"]:
        last = manifest["iterations"][-1]
        manifest["details"] = {"confirmation_index": last["confirmation_index"],
                               **next((s.get("details", {}) for s in last["steps"] if s["status"] != "success"), {})}
    write_json(attempt / "run.json", manifest)
    active["status"] = manifest["status"]
    if not manifest["details"].get("missing_toolchain"):
        index["selected_attempt_id"] = index["active_attempt_id"]
    write_json(index_path, index)
    return manifest


def run_experiment(config, raw, run_id, *, resume=False, new_attempt=False):
    if config.lmstudio.max_tokens is None or not config.runtime.stop_on_intermediate_failure:
        raise ValueError("SF experiments require explicit max_tokens and stop_on_intermediate_failure=true")
    entries, validation = validation_gate(config)
    server = server_metadata(config.lmstudio.host, config.lmstudio.model)
    provenance = code_provenance()
    conditions = {"experiment_version": raw["experiment_version"], "problem_ids": config.problem_ids,
                  "target_languages": config.target_languages, "runtime": asdict(config.runtime),
                  "lmstudio": asdict(config.lmstudio), "server": server["effective"],
                  "decoding": raw.get("decoding", {}), "validation_hash": validation["validation_hash"],
                  "execution_schedule": raw.get("execution_schedule", {"parallel_runs": 1, "parallel_routes_per_run": 1}),
                  "code": provenance, "ast": raw["ast"], "recovery": raw["recovery"]}
    metadata = {**conditions, "condition_hash": digest(conditions), "phase": raw["phase"],
                "run_id": run_id, "repeat_index": raw.get("repeat_index"), "started_at": timestamp(),
                "server_snapshot": server, "validation_snapshot": validation,
                "prompt_template_version": PROMPT_TEMPLATE_VERSION}
    path = config.output_root / run_id / "run_metadata.json"
    if path.exists():
        old = read_json(path)
        if old["condition_hash"] != metadata["condition_hash"]:
            raise ValueError("Resume refused: code, corpus, model or conditions changed")
        metadata = old
    else:
        write_json(path, metadata)
        source_root = Path(__file__).resolve().parents[2]
        for relative in provenance["file_hashes"]:
            snapshot = path.parent / "code_snapshot" / relative
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            snapshot.write_bytes((source_root / relative).read_bytes())
        write_json(path.parent / "config_snapshot.json", raw)
    results = []
    for entry in entries:
        for target in config.target_languages:
            results.append(run_route(config, entry, target, run_id, metadata, resume=resume, new_attempt=new_attempt))
    return results
