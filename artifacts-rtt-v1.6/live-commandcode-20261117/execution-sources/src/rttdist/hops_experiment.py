"""v1.6 설정·계약과 홉 기반 관측 실행을 연결합니다."""

from copy import deepcopy
from pathlib import Path
import json
import random
import shutil
import subprocess
import sys
import time

import yaml

from rttdist.experiment_io import digest, read_json, write_json
from rttdist.fps_experiment import SYSTEM
from rttdist.extract import extract_single_file_source_text, SourceExtractionError
from rttdist.fps_execution import evaluate, EXTENSIONS, canonical_output
from rttdist.hops_state import HopsState, threshold_key
from rttdist.jplag_similarity import measure
from rttdist.providers import create_provider, ProviderError, CostCapReached

PROTOCOL = "rtt-hops-v1.6"
SCHEMA = "observation-v1.6"
PROMPT_VERSION = "hops.translation.v1.6"
PROBLEM_IDS = (
    "IPOP_11729",
    "IPOP_2110",
    "IPOP_1992",
    "IPOP_2579",
    "IPOP_5567",
    "IPOP_10988",
    "IPOP_1929",
    "IPOP_2609",
    "IPOP_9012",
    "LC_0053",
    "LC_0062",
    "IPOP_9663",
    "LC_0242",
    "LC_0283",
    "LC_0338",
)
PILOT_IDS = ("IPOP_11729", "IPOP_1992", "LC_0053")
ROUTES = [["cpp", language] for language in ("python", "java", "haskell", "prolog")]
VALIDATOR_SOURCES = ("scripts/prepare_v16_corpus.py", "scripts/validate_v16_corpus.py")
INDEPENDENT_SOURCES = (
    "problem/metadata/ipop19/tools/oracles.py",
    "problem/metadata/leetcode21/tools/oracles.py",
)


def _source_hashes(paths):
    repo = Path(__file__).resolve().parents[2]
    try:
        return {name: digest((repo / name).read_bytes()) for name in paths}
    except OSError as exc:
        raise ValueError(
            "알려진 검증기·독립 계산기 소스를 확인할 수 없습니다."
        ) from exc


def load_hops_config(path, provider_path=None):
    path = Path(path).resolve()
    cfg = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(cfg, dict):
        raise ValueError("설정은 매핑이어야 합니다.")
    fixed = {
        "manuscript_version": "v1.6",
        "experiment_version": PROTOCOL,
        "schema_version": SCHEMA,
        "repeats": 5,
        "pilot_repeats": 1,
        "threshold": 0.85,
        "max_hops": 10,
        "confirmation_roundtrips": 1,
        "schedule_seed": 20261117,
        "observation_wall_seconds": 900,
        "confirmation_wall_seconds": 300,
    }
    for key, value in fixed.items():
        if cfg.get(key) != value or isinstance(cfg.get(key), bool):
            raise ValueError(f"고정 설정이 다릅니다: {key}")
    ids = cfg.get("problem_ids", [])
    if len(ids) != 15 or len(set(ids)) != 15 or set(ids) != set(PROBLEM_IDS):
        raise ValueError("설계에 지정한 서로 다른 15문제가 필요합니다.")
    if cfg.get("pilot_problem_ids") != list(PILOT_IDS):
        raise ValueError("파일럿 문제 목록이 다릅니다.")
    routes = [
        r.split("-via-") if isinstance(r, str) else r for r in cfg.get("routes", [])
    ]
    if sorted(routes) != sorted(ROUTES):
        raise ValueError("고정된 C++ 출발 4경로가 필요합니다.")
    cfg["routes"] = routes
    if sorted(cfg.get("thresholds", [])) != [0.8, 0.85, 0.9]:
        raise ValueError("세 임계치를 모두 지정해 주십시오.")
    cfg["thresholds"] = [0.8, 0.85, 0.9]
    runtime = cfg.get("runtime", {})
    if any(
        runtime.get(k) != v
        for k, v in {
            "fixture_timeout": 5,
            "compile_timeout": 180,
            "minimum_evaluation_cases": 13,
        }.items()
    ) or set(runtime.get("tools", {})) != {
        "cpp",
        "python",
        "java",
        "haskell",
        "prolog",
    }:
        raise ValueError("13개 평가와 고정 실행 제한, 5언어 도구가 필요합니다.")
    similarity = cfg.get("similarity", {})
    if (
        similarity.get("minimum_tokens") != 9
        or similarity.get("normalize") is not False
        or similarity.get("similarity_field") != "averageSimilarity"
    ):
        raise ValueError("JPlag 고정 설정이 다릅니다.")
    for name in ("selection", "corpus_root", "validation", "output_root"):
        cfg[name] = str((path.parent / cfg[name]).resolve())
    cfg["similarity"]["jar"] = str((path.parent / similarity["jar"]).resolve())
    for name in ("campaign_id", "profile_id"):
        value = cfg.get(name)
        if (
            not isinstance(value, str)
            or not value
            or value in (".", "..")
            or "/" in value
            or "\\" in value
        ):
            raise ValueError(f"안전한 실행 식별자가 필요합니다: {name}")
    provider_path = (
        Path(provider_path).resolve()
        if provider_path
        else (
            (path.parent / cfg["provider_config"]).resolve()
            if cfg.get("provider_config")
            else None
        )
    )
    if provider_path:
        provider = yaml.safe_load(provider_path.read_text(encoding="utf-8"))
        forbidden = set(cfg) - {"llm", "profile_id", "provider_config"}
        if not isinstance(provider, dict) or forbidden.intersection(provider):
            raise ValueError("공급자 파일은 공통 실험 조건을 변경할 수 없습니다.")
        llm = provider.get("llm", provider)
        if llm.get("protocol") == "copilot_sdk" and not isinstance(
            llm.get("generation"), dict
        ):
            raise ValueError("SDK 공급자는 generation 딕셔너리를 명시해야 합니다.")
        cfg["llm"] = {**cfg.get("llm", {}), **llm}
        if provider.get("profile_id"):
            cfg["profile_id"] = provider["profile_id"]
    return cfg


def build_run_contract(cfg, manifest, environment):
    root = Path(__file__).resolve().parent
    names = [
        "__main__.py",
        "cli.py",
        "hops_experiment.py",
        "hops_state.py",
        "hops_reporting.py",
        "providers.py",
        "provider_protocols.py",
        "copilot_provider.py",
        "fps_execution.py",
        "jplag_similarity.py",
        "extract.py",
    ]
    implementations = {
        name: digest((root / name).read_bytes()) if (root / name).is_file() else None
        for name in names
    }
    implementations.update(_source_hashes((*VALIDATOR_SOURCES, *INDEPENDENT_SOURCES)))
    contract = {
        "protocol": PROTOCOL,
        "schema_version": SCHEMA,
        "schema": SCHEMA,
        "problem_ids": list(cfg["problem_ids"]),
        "routes": deepcopy(cfg["routes"]),
        "repeats": cfg["repeats"],
        "thresholds": list(cfg["thresholds"]),
        "primary_threshold": cfg["threshold"],
        "config": deepcopy(cfg),
        "manifest": deepcopy(manifest),
        "environment": deepcopy(environment),
        "implementation_hashes": implementations,
        "prompt_version": PROMPT_VERSION,
        "system_prompt": SYSTEM,
        "stop_rules": {
            key: cfg[key]
            for key in (
                "max_hops",
                "confirmation_roundtrips",
                "threshold",
                "thresholds",
                "observation_wall_seconds",
                "confirmation_wall_seconds",
            )
        },
        "requested_generation": deepcopy(cfg.get("llm", {}).get("generation")),
        "effective_generation": None,
        "effective_generation_missing_reason": "server_not_reported",
    }
    contract["hashes"] = {
        "code": digest(implementations),
        "aggregator": implementations["hops_reporting.py"],
        "prompt": digest({"version": PROMPT_VERSION, "system": SYSTEM}),
        "data": digest(manifest),
        "tools": digest(environment),
        "provider": digest(cfg.get("llm", {})),
        "generation": digest(contract["requested_generation"]),
        "stop_rules": digest(contract["stop_rules"]),
    }
    repo = root.parents[1]
    contract["dependency_hashes"] = {
        name: digest((repo / name).read_bytes()) if (repo / name).is_file() else None
        for name in ("pyproject.toml", "uv.lock")
    }
    contract["contract_hash"] = digest(contract)
    return contract


def campaign_root(cfg):
    return Path(cfg["output_root"]) / cfg["campaign_id"]


def build_hops_schedule(cfg, phase, shard=None):
    if phase not in ("pilot", "main"):
        raise ValueError("실행 단계는 pilot 또는 main이어야 합니다.")
    ids = cfg["pilot_problem_ids"] if phase == "pilot" else cfg["problem_ids"]
    repeats = cfg["pilot_repeats"] if phase == "pilot" else cfg["repeats"]
    jobs = [
        {
            "campaign_id": cfg["campaign_id"],
            "phase": phase,
            "problem_id": pid,
            "route": f"{a}-via-{b}",
            "seed_language": a,
            "target_language": b,
            "repeat": repeat,
        }
        for pid in ids
        for a, b in cfg["routes"]
        for repeat in range(1, repeats + 1)
    ]
    random.Random(cfg["schedule_seed"]).shuffle(jobs)
    if shard:
        try:
            index, total = (int(part) for part in str(shard).split("/"))
        except ValueError, TypeError:
            raise ValueError("샤드는 i/k 형식이어야 합니다.") from None
        if not 1 <= index <= total:
            raise ValueError("샤드는 1 <= i <= k를 만족해야 합니다.")
        jobs = [job for n, job in enumerate(jobs) if n % total == index - 1]
    return jobs


def _prompt(problem, source, source_language, target_language):
    examples = []
    for path in sorted((problem / "prompt_examples").glob("*.inp")):
        pair = {
            "input": path.read_text(encoding="utf-8"),
            "output": path.with_suffix(".out").read_text(encoding="utf-8"),
        }
        if pair not in examples:
            examples.append(pair)
        if len(examples) == 2:
            break
    content = (
        f"Source language: {source_language}\nTarget language: {target_language}\nSpecification:\n"
        + (problem / "statement.md").read_text(encoding="utf-8")
        + "\nPublic examples:\n"
        + json.dumps(examples, ensure_ascii=False)
        + "\nSource code:\n"
        + source
    )
    return [{"role": "system", "content": SYSTEM}, {"role": "user", "content": content}]


def _local_measure(a, b, folder, cfg):
    attempts = []
    for index in range(2):
        destination = folder if index == 0 else folder.with_name(folder.name + "-retry")
        try:
            result = measure(a, b, destination, config=cfg["similarity"])
        except (OSError, ValueError, RuntimeError) as exc:
            result = {
                "status": "unavailable",
                "value": None,
                "reason": type(exc).__name__,
            }
        attempts.append(result)
        if result.get("status") == "measured" and result.get("value") is not None:
            break
    return {**result, "attempts": attempts}


def _observation_contract(cfg, job, problem):
    hashes = {
        path.relative_to(problem).as_posix(): digest(path.read_bytes())
        for path in sorted(problem.rglob("*"))
        if path.is_file()
    }
    return build_run_contract(
        {k: v for k, v in cfg.items() if not k.startswith("_")},
        {"job": job, "file_hashes": hashes},
        cfg.get("_environment", {}),
    )


def _response_for_step(provider, payload, folder):
    path = folder / "provider_result.json"
    if path.is_file():
        return read_json(path)
    started = folder / "request_started.json"
    recoverable = any(
        (folder / name).is_file() for name in ("response.json", "response_body.txt")
    )
    if started.is_file() and not recoverable:
        raise ProviderError("request_outcome_unknown")
    write_json(
        started,
        {
            "call_id": digest(payload["logical_request"]),
            "logical_request": payload["logical_request"],
        },
    )
    response = provider.complete(payload, folder)
    write_json(path, response)
    return response


def _process_step(
    cfg,
    problem,
    folder,
    response,
    language,
    origin,
    previous,
    current,
    step,
    checkpoint,
):
    path = folder / "processed.json"
    if path.is_file():
        cached = read_json(path)
        if "deadline_reason" not in cached:
            raise ValueError(
                "단계 시간 판정 근거가 없습니다. 새 campaign이 필요합니다."
            )
        return cached
    result = {
        "source": "",
        "evaluation_status": "infrastructure_error",
        "sym_adj": None,
        "sym_origin": None,
        "sym_status": None,
    }

    def check(stage):
        timing = checkpoint(stage)
        result["timing"] = timing
        result["deadline_reason"] = timing["deadline_reason"]
        result["accepted_within_deadline"] = timing["deadline_reason"] is None
        if timing["deadline_reason"]:
            result["reason"] = timing["deadline_reason"]
        return timing["deadline_reason"] is not None

    def save():
        write_json(path, result)
        return result

    if check("response"):
        return save()
    evidence = response.get("model_evidence")
    actual = response.get("actual_model")
    allowed = [cfg["llm"]["model"], *cfg["llm"].get("allowed_response_models", [])]
    sdk = cfg["llm"].get("protocol") == "copilot_sdk"
    if actual is not None and actual not in allowed:
        result["reason"] = "model_mismatch"
        return save()
    if actual is None and not sdk:
        result["reason"] = "model_missing"
        return save()
    if isinstance(evidence, dict) and evidence.get("status") == "mismatch":
        result["reason"] = "model_mismatch"
        return save()
    try:
        if response.get("finish_reason") in (
            "length",
            "max_tokens",
            "max_output_tokens",
            "content_filter",
        ):
            raise SourceExtractionError("출력이 잘렸습니다.")
        source = extract_single_file_source_text(
            response.get("text"), preserve_unfenced=True
        )
    except SourceExtractionError:
        result.update(evaluation_status="format_error", reason="format_error")
        check("extraction")
        return save()
    source_path = folder / ("source." + EXTENSIONS[language])
    source_path.write_text(source, encoding="utf-8", newline="")
    try:
        evaluation = evaluate(
            source, language, problem, folder / "evaluation", cfg["runtime"]
        )
    except (OSError, ValueError, RuntimeError) as exc:
        evaluation = {"status": "infrastructure_error", "reason": type(exc).__name__}
    result.update(
        source=source,
        source_path=str(source_path),
        evaluation_status=evaluation["status"],
        evaluation=evaluation,
    )
    if check("evaluation"):
        return save()
    if evaluation["status"] == "success" and step % 2 == 0:
        adjacent = _local_measure(previous, source, folder / "sym_adj", cfg)
        result.update(
            sym_adj=adjacent.get("value"),
            sym_status=adjacent.get("status"),
            similarity={"adjacent": adjacent},
        )
        if check("sym_adj"):
            return save()
        original = _local_measure(origin, source, folder / "sym_origin", cfg)
        result.update(
            sym_adj=adjacent.get("value"),
            sym_origin=original.get("value"),
            sym_status=adjacent.get("status"),
            similarity={"adjacent": adjacent, "origin": original},
        )
        if original.get("status") != "measured":
            result["sym_status"] = "unavailable"
            result["sym_origin_missing_reason"] = (
                original.get("reason") or "similarity_unavailable"
            )
        check("sym_origin")
    return save()


def _step_decision(folder, processed, checkpoint):
    path = folder / "decision.json"
    if path.is_file():
        decision = read_json(path)
    else:
        timing = checkpoint("decision")
        reason = processed.get("deadline_reason") or timing["deadline_reason"]
        decision = {
            "timing": {**timing, "deadline_reason": reason},
            "deadline_reason": reason,
            "accepted_within_deadline": reason is None,
            "reason": reason or processed.get("reason"),
        }
        write_json(path, decision)
    return {**processed, **decision}


def run_hops_observation(cfg, job, provider, folder):
    folder = Path(folder).resolve()
    problem = Path(cfg["corpus_root"]) / job["problem_id"]
    contract = _observation_contract(cfg, job, problem)
    contract_path = folder / "contract.json"
    if contract_path.exists() and read_json(contract_path) != contract:
        raise ValueError("관측 계약이 변경되었습니다. 새 campaign이 필요합니다.")
    write_json(contract_path, contract)
    if (folder / "observation.json").is_file():
        return read_json(folder / "observation.json")
    origin = (problem / "reference.cpp").read_text(encoding="utf-8")
    current = previous = origin
    state = HopsState(
        origin,
        cfg["thresholds"],
        cfg["threshold"],
        cfg["max_hops"],
        cfg["confirmation_roundtrips"],
    )
    generation = deepcopy(cfg["llm"].get("generation", {}))
    if generation.get("seed") is not None:
        generation["seed"] += job["repeat"] - 1
    steps = []
    started = time.monotonic()
    confirmation_started = None
    elapsed_base = 0
    confirmation_base = 0
    clock_abort_path = folder / "clock_abort.json"
    clock_regressed = clock_abort_path.is_file()
    if (folder / "timing.json").is_file():
        timing = read_json(folder / "timing.json")
        clock_regressed = clock_regressed or (
            timing.get("deadline_reason") == "observation_clock_unavailable"
            or started < timing.get("checkpoint_monotonic", started)
        )
        gap = max(0, started - timing.get("checkpoint_monotonic", started))
        elapsed_base = timing.get("elapsed_seconds", 0) + gap
        confirmation_base = timing.get("confirmation_seconds", 0)
        if timing.get("active_kind") == "confirmation":
            confirmation_base += gap
    if clock_regressed and not clock_abort_path.is_file():
        write_json(clock_abort_path, {"reason": "observation_clock_unavailable"})
    while state.next_step_kind() != "stop":
        kind = state.next_step_kind()
        number = state.translation_steps + 1
        stepfolder = folder / f"step-{number:02}"
        replay = (stepfolder / "processed.json").is_file()
        has_response = any(
            (stepfolder / name).is_file()
            for name in ("provider_result.json", "response.json", "response_body.txt")
        )
        now = time.monotonic()
        if clock_regressed and not replay and not has_response:
            state.abort("observation_clock_unavailable")
            break
        if kind == "confirmation" and confirmation_started is None:
            confirmation_started = now
            if confirmation_base == 0:
                boundary = read_json(
                    folder / f"step-{cfg['max_hops']:02}/decision.json"
                )
                confirmation_started = min(
                    now, boundary["timing"]["checkpoint_monotonic"]
                )
        if (
            not replay
            and not has_response
            and kind == "discovery"
            and now - started + elapsed_base >= cfg["observation_wall_seconds"]
        ):
            state.abort("observation_wall_clock")
            break
        if (
            not replay
            and not has_response
            and kind == "confirmation"
            and now - confirmation_started + confirmation_base
            >= cfg["confirmation_wall_seconds"]
        ):
            state.abort("confirmation_wall_clock")
            break

        def checkpoint(stage):
            checked_at = time.monotonic()
            elapsed = checked_at - started + elapsed_base
            confirmation_elapsed = confirmation_base + (
                checked_at - confirmation_started
                if confirmation_started is not None
                else 0
            )
            reason = "observation_clock_unavailable" if clock_regressed else None
            if (
                reason is None
                and kind == "discovery"
                and elapsed >= cfg["observation_wall_seconds"]
            ):
                reason = "observation_wall_clock"
            elif (
                reason is None
                and kind == "confirmation"
                and confirmation_elapsed >= cfg["confirmation_wall_seconds"]
            ):
                reason = "confirmation_wall_clock"
            snapshot = {
                "elapsed_seconds": elapsed,
                "confirmation_seconds": confirmation_elapsed,
                "checkpoint_monotonic": checked_at,
                "active_kind": kind,
                "stage": stage,
                "deadline_reason": reason,
            }
            write_json(folder / "timing.json", snapshot)
            write_json(stepfolder / "timing.json", snapshot)
            return snapshot

        if not replay:
            start_timing = checkpoint("start")
            if start_timing["deadline_reason"] and not has_response:
                state.abort(start_timing["deadline_reason"])
                break
        language = job["target_language"] if number % 2 else "cpp"
        source_language = "cpp" if number % 2 else job["target_language"]
        logical = {
            "campaign": job["campaign_id"],
            "phase": job["phase"],
            "problem": job["problem_id"],
            "route": job["route"],
            "repeat": job["repeat"],
            "step": number,
        }
        call_id = "/".join(
            str(logical[key])
            for key in ("campaign", "phase", "problem", "route", "repeat", "step")
        )
        payload = {
            "model": cfg["llm"]["model"],
            "messages": _prompt(problem, current, source_language, language),
            "generation": generation,
            "logical_request": logical,
        }
        try:
            response = _response_for_step(provider, payload, stepfolder)
        except ProviderError as exc:
            reason = (
                "request_outcome_unknown"
                if str(exc) == "request_outcome_unknown"
                else (
                    "cost_cap_reached"
                    if isinstance(exc, CostCapReached)
                    else "provider_error"
                )
            )
            state.abort(reason)
            write_json(
                stepfolder / "infrastructure_error.json",
                {"reason": reason, "exception_type": type(exc).__name__},
            )
            break
        processed = _process_step(
            cfg,
            problem,
            stepfolder,
            response,
            language,
            origin,
            previous,
            current,
            number,
            checkpoint,
        )
        processed = _step_decision(stepfolder, processed, checkpoint)
        transition = state.record_step(
            language,
            processed["source"],
            (
                "infrastructure_error"
                if processed.get("deadline_reason")
                else processed["evaluation_status"]
            ),
            {
                "sym_adj": processed.get("sym_adj"),
                "sym_origin": processed.get("sym_origin"),
            },
            processed.get("sym_status"),
        )
        if processed.get("reason") and state.terminal_status == "infrastructure_error":
            state.reason = processed["reason"]
            if state.confirmation_status == "unavailable":
                state.confirmation_reason = processed["reason"]
            for outcome in state._outcomes.values():
                if outcome["category"] == "invalid":
                    outcome["reason"] = processed["reason"]
        item = {
            **{k: v for k, v in processed.items() if k != "source"},
            **transition,
            "language": language,
            "direction": f"{source_language}-to-{language}",
            "phase": "search" if kind == "discovery" else "confirmation",
            "call_id": call_id,
            "response_path": str(stepfolder / "provider_result.json"),
        }
        for key in (
            "finish_reason",
            "actual_model",
            "model_evidence",
            "usage",
            "usage_raw",
            "cost_usd",
            "cost_source",
            "request_id",
            "requested_generation",
            "sent_generation",
            "effective_generation",
            "raw_response_path",
            "latency_seconds",
        ):
            item[key] = response.get(key)
        item["effective_generation_missing_reason"] = response.get(
            "effective_generation_missing_reason"
        ) or (
            "server_not_reported"
            if response.get("effective_generation") is None
            else None
        )
        write_json(stepfolder / "step.json", item)
        steps.append(item)
        current = processed["source"]
        if number % 2 == 0:
            previous = current
    outcomes = state.outcomes()
    primary = outcomes[threshold_key(cfg["threshold"])]
    comparison = (
        "sdk_exploratory"
        if cfg["llm"].get("protocol") == "copilot_sdk"
        else "direct_api"
    )
    record = {
        **job,
        "schema_version": SCHEMA,
        "protocol": PROTOCOL,
        "profile_id": cfg["profile_id"],
        "contract_hash": cfg.get("_contract_hash", contract["contract_hash"]),
        "observation_contract_hash": contract["contract_hash"],
        "attempt": job["repeat"],
        "seed": generation.get("seed"),
        "primary_threshold": threshold_key(cfg["threshold"]),
        "outcomes": outcomes,
        "terminal_status": state.terminal_status,
        "status": state.terminal_status,
        "reason": state.reason,
        "confirmation_status": state.confirmation_status,
        "confirmation_reason": state.confirmation_reason,
        "translation_steps": state.translation_steps,
        "steps": steps,
        "comparison_class": comparison,
        "execution_class": comparison,
        "complete_by_threshold": {
            key: value["category"] in ("success", "functional_failure", "hop_limit")
            for key, value in outcomes.items()
        },
        "success": primary["success"],
        "category": primary["category"],
        "evaluable": primary["category"]
        in ("success", "functional_failure", "hop_limit"),
        "states": [
            {"language": key[0], "sha256": key[1], "first_seen_step": value}
            for key, value in state.states.items()
        ],
        "cost_usd": (
            sum(s["cost_usd"] for s in steps)
            if steps and all(s["cost_usd"] is not None for s in steps)
            else None
        ),
        "known_cost_usd": sum(
            s["cost_usd"] for s in steps if s["cost_usd"] is not None
        ),
    }
    write_json(folder / "observation.json", record)
    return record


def audit_observation(record, contract):
    errors = []
    cfg = contract.get("config", contract)
    if record.get("schema_version") != SCHEMA or record.get("protocol") != PROTOCOL:
        errors.append("관측 버전이 다릅니다.")
    steps = record.get("steps", [])
    if record.get("translation_steps") != len(steps) or len(steps) > 12:
        errors.append("번역 단계 수가 다릅니다.")
    if [s.get("step") for s in steps] != list(range(1, len(steps) + 1)):
        errors.append("단계 순서가 다릅니다.")
    for value in record.get("outcomes", {}).values():
        if value.get("success"):
            reached = value.get("reached_step")
            if reached not in (2, 4, 6, 8, 10) or reached > len(steps):
                errors.append("도달 홉이 유효하지 않습니다.")
            elif any(s.get("evaluation_status") != "success" for s in steps[:reached]):
                errors.append("도달 전 기능 실패가 있습니다.")
    if len(record.get("outcomes", {})) != len(cfg.get("thresholds", [0.8, 0.85, 0.9])):
        errors.append("임계치 결과가 누락되었습니다.")
    return {"passed": not errors, "errors": errors}


def collect_hops_environment(cfg):
    tools = {}
    commands = {**cfg["runtime"]["tools"], "similarity_java": cfg["similarity"]["java"]}
    for language, command in commands.items():
        resolved = shutil.which(command)
        if not resolved:
            raise ValueError(f"필수 실행 도구가 없습니다: {language}")
        process = subprocess.run(
            [resolved, "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
        if process.returncode != 0:
            raise ValueError(f"도구 버전을 확인하지 못했습니다: {language}")
        tools[language] = {
            "path": str(Path(resolved).resolve()),
            "version": (process.stdout + process.stderr).strip(),
        }
    jar = Path(cfg["similarity"]["jar"])
    if not jar.is_file():
        raise ValueError("JPlag jar 파일이 없습니다.")
    jar_hash = digest(jar.read_bytes())
    if cfg["similarity"].get("jar_sha256") not in (None, jar_hash):
        raise ValueError("JPlag jar 해시가 변경되었습니다.")
    return {
        "python": sys.version,
        "python_executable": sys.executable,
        "tools": tools,
        "jplag_jar_sha256": jar_hash,
    }


def _validated_inputs(cfg, validation):
    if (
        validation.get("passed") is not True
        or validation.get("runtime") != cfg["runtime"]
    ):
        raise ValueError("기준 구현 검증 또는 실행 환경이 유효하지 않습니다.")
    if validation.get("validator_source_hashes") != _source_hashes(VALIDATOR_SOURCES):
        raise ValueError(
            "검증기 소스 계약이 변경되었거나 누락되었습니다. 재검증이 필요합니다."
        )
    independent = validation.get("independent_checks")
    if (
        not isinstance(independent, dict)
        or independent.get("passed") is not True
        or independent.get("source_hashes") != _source_hashes(INDEPENDENT_SOURCES)
    ):
        raise ValueError("독립 계산기 소스 계약 또는 통과 근거가 유효하지 않습니다.")
    results = validation.get("results", [])
    pairs = {(r.get("problem_id"), r.get("language")) for r in results}
    expected = {
        (pid, language)
        for pid in cfg["problem_ids"]
        for language in cfg["runtime"]["tools"]
    }
    if (
        len(results) != 75
        or pairs != expected
        or any(
            r.get("status") != "success"
            or r.get("case_count") != 13
            or r.get("passed_cases") != 13
            for r in results
        )
        or validation.get("executed_cases") != 975
        or validation.get("passed_cases") != 975
    ):
        raise ValueError("75개 기준 구현과 975개 평가 성공이 필요합니다.")
    hashes = validation.get("file_hashes")
    if not hashes:
        raise ValueError("자료 파일 해시가 필요합니다.")
    root = Path(cfg["corpus_root"]).resolve()
    for name, expected_hash in hashes.items():
        path = (root / name).resolve()
        if (
            not path.is_relative_to(root)
            or not path.is_file()
            or digest(path.read_bytes()) != expected_hash
        ):
            raise ValueError(f"검증 후 자료가 변경되었습니다: {name}")
    manifest = read_json(root / "manifest.json")
    expected_hashes = {
        **manifest.get("file_hashes", {}),
        "manifest.json": digest((root / "manifest.json").read_bytes()),
    }
    actual_hashes = {
        path.relative_to(root).as_posix(): digest(path.read_bytes())
        for path in root.rglob("*")
        if path.is_file()
    }
    if expected_hashes != hashes or actual_hashes != hashes:
        raise ValueError("매니페스트와 검증 해시가 다릅니다.")
    selection = read_json(cfg["selection"])
    if {p["problem_id"] for p in selection["problems"]} != set(cfg["problem_ids"]):
        raise ValueError("문제 선택 목록이 다릅니다.")
    if manifest.get("selection_sha256") and manifest["selection_sha256"] != digest(
        Path(cfg["selection"]).read_bytes()
    ):
        raise ValueError("문제 선택 해시가 변경되었습니다.")
    _check_independent_results(cfg, independent, root)
    return manifest


def _check_independent_results(cfg, independent, root):
    results = independent.get("results")
    if not isinstance(results, list) or len(results) != 195:
        raise ValueError("독립 검증 195건의 근거가 필요합니다.")
    expected = {}
    for pid in cfg["problem_ids"]:
        inputs = sorted((root / pid / "evaluation").glob("*.inp"))
        if len(inputs) != 13 or any(
            not path.with_suffix(".out").is_file() for path in inputs
        ):
            raise ValueError("독립 검증에는 문제별 13개 완전한 평가 쌍이 필요합니다.")
        for inp in inputs:
            output = inp.with_suffix(".out")
            expected[(pid, inp.stem)] = {
                "input_sha256": digest(inp.read_bytes()),
                "expected_sha256": digest(output.read_bytes()),
                "computed_sha256": digest(
                    canonical_output(output.read_text(encoding="utf-8")).encode("utf-8")
                ),
            }
    seen = set()
    for result in results:
        if (
            not isinstance(result, dict)
            or not isinstance(result.get("problem_id"), str)
            or not isinstance(result.get("case"), str)
        ):
            raise ValueError("독립 검증의 문제·사례 키가 유효하지 않습니다.")
        key = (result["problem_id"], result["case"])
        methods = result.get("methods")
        methods_valid = (isinstance(methods, str) and bool(methods.strip())) or (
            isinstance(methods, list)
            and bool(methods)
            and all(isinstance(method, str) and method.strip() for method in methods)
        )
        if (
            key not in expected
            or key in seen
            or result.get("passed") is not True
            or result.get("error")
            or not methods_valid
        ):
            raise ValueError("독립 검증 사례가 중복·누락되었거나 실패 근거가 있습니다.")
        if any(result.get(name) != value for name, value in expected[key].items()):
            raise ValueError("독립 검증 사례의 입력·정답·계산 결과 해시가 다릅니다.")
        seen.add(key)
    if seen != set(expected):
        raise ValueError("독립 검증 사례 집합이 평가 자료와 다릅니다.")


def _budget_config(cfg):
    budget = cfg.get("budget", {})
    calls = budget.get("max_logical_requests")
    transports = budget.get("max_transport_attempts")
    if (
        type(calls) is not int
        or calls < 1
        or type(transports) is not int
        or transports < 1
    ):
        raise ValueError("논리 요청·통신 전송 상한을 지정해 주십시오.")
    llm = deepcopy(cfg["llm"])
    llm.update(max_calls=calls, max_transport_attempts=transports)
    cap = budget.get("cost_cap_usd", llm.get("cost_cap_usd"))
    if cap is not None:
        if isinstance(cap, bool) or not isinstance(cap, (int, float)) or cap <= 0:
            raise ValueError("비용 상한은 양수여야 합니다.")
        if not llm.get("pricing") and llm.get("max_request_cost_usd") is None:
            raise ValueError("달러 상한에는 단가 또는 최대 요청 비용이 필요합니다.")
        llm["cost_cap_usd"] = cap
    return llm


def _check_validation_environment(validation, environment):
    for language, saved in validation.get("tool_versions", {}).items():
        if language == "java_runtime":
            language = "similarity_java"
        current = environment.get("tools", {}).get(language)
        version = (saved.get("stdout", "") + saved.get("stderr", "")).strip()
        if current is None or not version or version != current.get("version"):
            raise ValueError(
                f"기준 구현 검증 후 도구 버전이 변경되었습니다: {language}"
            )


def freeze_main_design(cfg, pilot_audit, validation, provider_preflight):
    manifest = _validated_inputs(cfg, validation)
    llm = _budget_config(cfg)
    profile = cfg["llm"].get("generation_profile")
    sdk = cfg["llm"].get("protocol") == "copilot_sdk"
    generation = cfg["llm"].get("generation")
    if not profile or not isinstance(generation, dict) or (not sdk and not generation):
        raise ValueError("생성 프로파일과 요청 설정이 필요합니다.")
    if sdk:
        from rttdist.provider_protocols import validate_generation

        if (
            not isinstance(profile, dict)
            or not profile.get("name")
            or not isinstance(profile.get("supported_options"), list)
        ):
            raise ValueError("유효한 SDK 생성 프로파일이 필요합니다.")
        validate_generation(profile, generation)
    if (
        provider_preflight.get("passed") is not True
        or provider_preflight.get("live") is not True
    ):
        raise ValueError("실접속이 확인된 공급자 사전 점검이 필요합니다.")
    if provider_preflight.get("generation_profile") != profile:
        raise ValueError("생성 프로파일이 사전 점검과 다릅니다.")
    actual = provider_preflight.get("actual_model")
    evidence = provider_preflight.get("model_evidence", {})
    status = evidence.get("status") if isinstance(evidence, dict) else evidence
    allowed = [cfg["llm"]["model"], *cfg["llm"].get("allowed_response_models", [])]
    if status == "mismatch" or (actual is not None and actual not in allowed):
        raise ValueError("응답 모델이 요청과 다릅니다.")
    if not sdk and (actual is None or status not in ("exact", "alias")):
        raise ValueError("직접 API는 실제 모델 ID 확인이 필요합니다.")
    environment = collect_hops_environment(cfg)
    _check_validation_environment(validation, environment)
    contract = build_run_contract(cfg, manifest, environment)
    if (
        pilot_audit.get("passed") is not True
        or pilot_audit.get("observation_count", pilot_audit.get("observed")) != 12
    ):
        raise ValueError("12개 파일럿 관측의 감사 통과가 필요합니다.")
    completeness = pilot_audit.get("complete_by_threshold")
    if not isinstance(completeness, dict) or any(
        completeness.get(threshold_key(value)) is not True
        for value in cfg["thresholds"]
    ):
        raise ValueError("파일럿의 모든 필수 임계치가 완전해야 합니다.")
    if pilot_audit.get("contract_hash") != contract["contract_hash"]:
        raise ValueError("파일럿과 본 실험 계약이 다릅니다.")
    root = campaign_root(cfg)
    root.mkdir(parents=True, exist_ok=True)
    disk_free = shutil.disk_usage(root).free
    minimum = cfg.get("minimum_free_bytes", 64 * 1024 * 1024)
    if disk_free < minimum:
        raise ValueError("원자료를 보존할 디스크 여유 공간이 부족합니다.")
    path = root / "main_design.json"
    identity = {
        "contract": contract["contract_hash"],
        "pilot": digest(pilot_audit),
        "validation": digest(validation),
        "preflight": digest(provider_preflight),
    }
    if path.is_file():
        previous = read_json(path)
        if previous.get("identity") != identity:
            raise ValueError(
                "동결 이후 조건이 변경되었습니다. 새 campaign이 필요합니다."
            )
        return previous
    design = {
        "schema_version": "main-design-v1.6",
        "approved_for_main": True,
        "confirmatory": not sdk,
        "comparison_class": "sdk_exploratory" if sdk else "direct_api",
        "identity": identity,
        "contract_hash": contract["contract_hash"],
        "contract": contract,
        "approval_basis": "고정된 자료·파일럿 감사·모델 확인·예산 관문을 통과하였습니다.",
        "main_attempts": 300,
        "pilot_attempts": 12,
        "max_logical_requests": 3600,
        "max_transport_attempts": 10800,
        "configured_budget": cfg["budget"],
        "generation_profile": profile,
        "model_evidence": evidence,
        "pilot_reuse": False,
        "output_path": str(root / "main"),
        "disk_free_bytes_at_freeze": disk_free,
        "minimum_free_bytes": minimum,
        "estimated_cost_usd": (
            3600 * llm["max_request_cost_usd"]
            if llm.get("max_request_cost_usd")
            else None
        ),
        "cost_missing_reason": (
            None
            if llm.get("max_request_cost_usd")
            else "요청별 최대 단가가 보고되지 않았습니다."
        ),
        "maximum_observation_seconds": 1200,
        "serial_wall_seconds_upper_bound": 360000,
        "observability": {
            "comparison_class": "sdk_exploratory" if sdk else "direct_api",
            "effective_generation": "공급자 보고값만 사용합니다.",
        },
        "instructions": [
            "파일럿 응답은 본 실험에 복사하지 않으며 새로운 main 요청 키를 사용합니다.",
            "중단 후 동일 설정과 campaign으로 --action resume를 실행해 주십시오.",
            "자료·도구·코드·공급자·설정을 변경하시면 새 campaign을 사용해 주십시오.",
            "요청 결과가 불명확하면 자동 재생성하지 않으며 저장된 근거를 확인해 주십시오.",
        ],
    }
    write_json(path, design)
    return design


def _prepare_campaign(cfg, phase):
    validation = read_json(cfg["validation"])
    manifest = _validated_inputs(cfg, validation)
    environment = collect_hops_environment(cfg)
    _check_validation_environment(validation, environment)
    contract = build_run_contract(cfg, manifest, environment)
    root = campaign_root(cfg) / phase
    if phase == "main":
        design_path = campaign_root(cfg) / "main_design.json"
        if not design_path.is_file():
            raise ValueError("본 실험 동결 파일이 필요합니다.")
        design = read_json(design_path)
        if (
            not design.get("approved_for_main")
            or design.get("contract_hash") != contract["contract_hash"]
        ):
            raise ValueError("본 실험 계약이 변경되었습니다. 새 campaign이 필요합니다.")
    path = root / "contract.json"
    if path.is_file() and read_json(path) != contract:
        raise ValueError("캠페인 계약이 변경되었습니다. 새 campaign이 필요합니다.")
    write_json(path, contract)
    return contract, root, environment


def run_hops_campaign(cfg, phase, shard=None):
    jobs = build_hops_schedule(cfg, phase, shard)
    llm = _budget_config(cfg)
    contract, root, environment = _prepare_campaign(cfg, phase)
    provider = create_provider(llm, ledger=root / "provider_ledger.jsonl")
    execution_cfg = {
        **cfg,
        "_contract_hash": contract["contract_hash"],
        "_environment": environment,
    }
    records = []
    for job in jobs:
        folder = root / job["problem_id"] / job["route"] / f"attempt-{job['repeat']:02}"
        record = run_hops_observation(execution_cfg, job, provider, folder)
        records.append(record)
    all_records = [
        read_json(path) for path in sorted(root.glob("*/*/attempt-*/observation.json"))
    ]
    planned = build_hops_schedule(cfg, phase)
    valid_categories = {"success", "functional_failure", "hop_limit"}
    complete = {
        threshold_key(t): len(all_records) == len(planned)
        and all(
            record.get("outcomes", {}).get(threshold_key(t), {}).get("category")
            in valid_categories
            for record in all_records
        )
        for t in cfg["thresholds"]
    }
    audits = [audit_observation(record, contract) for record in all_records]
    audit = {
        "passed": len(all_records) == len(planned) and all(a["passed"] for a in audits),
        "collection_finished": len(all_records) == len(planned),
        "observation_count": len(all_records),
        "planned": len(planned),
        "contract_hash": contract["contract_hash"],
        "complete_by_threshold": complete,
        "incomplete_slots": len(planned) - len(all_records),
        "errors": [error for a in audits for error in a["errors"]],
    }
    # 샤드가 순서대로 완료될 때마다 파일을 다시 계산합니다. 원자료는 샤드별 파일로 보존됩니다.
    write_json(root / "completion_audit.json", audit)
    return records


def report_hops_campaign(cfg, phase):
    from rttdist.hops_reporting import summarize_hops
    from scripts.report_v16 import write_v16_report

    root = campaign_root(cfg) / phase
    contract = read_json(root / "contract.json")
    records = [
        read_json(path) for path in sorted(root.glob("*/*/attempt-*/observation.json"))
    ]
    manifest = read_json(cfg["selection"])
    reporting_contract = deepcopy(contract)
    if phase == "pilot":
        reporting_contract.update(problem_ids=cfg["pilot_problem_ids"], repeats=1)
    summary = summarize_hops(records, manifest, reporting_contract)
    write_json(root / "summary.json", summary)
    write_v16_report(summary, root / "report")
    return summary
