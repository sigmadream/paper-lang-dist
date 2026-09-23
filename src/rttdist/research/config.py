"""Provider-neutral campaign configuration, validated before any generation."""
from copy import deepcopy
from pathlib import Path
import math

from rttdist.providers import create_provider, PROVIDER_FACTORIES
from .profiles import identifier, load_profile, read_yaml

LANGUAGES = {"cpp": "cpp", "c": "c", "python": "py", "java": "java", "haskell": "hs", "prolog": "pl"}


def positive_integer(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return value


def load_config(path):
    path = Path(path).resolve()
    return resolve_config(read_yaml(path), path.parent)


def resolve_config(raw, base_dir=Path(".")):
    cfg = deepcopy(raw)
    allowed = {"schema_version", "id", "corpus_root", "output_root", "problem_ids", "routes",
               "repeats", "schedule_seed", "models", "profile", "runtime", "prompt_template_version", "parallel_models"}
    if set(cfg) - allowed:
        raise ValueError(f"Unknown experiment fields: {sorted(set(cfg) - allowed)}")
    if type(cfg.get("schema_version")) is not int or cfg["schema_version"] != 1:
        raise ValueError("Research config schema_version must be 1")
    identifier(cfg.get("id"))
    for key in ("corpus_root", "output_root"):
        if not isinstance(cfg.get(key), str) or not cfg[key]:
            raise ValueError(f"{key} is required")
        cfg[key] = str((Path(base_dir) / cfg[key]).resolve())
    ids = cfg.get("problem_ids")
    if not isinstance(ids, list) or not ids or len(set(ids)) != len(ids):
        raise ValueError("problem_ids must be a nonempty unique list")
    for pid in ids:
        identifier(pid)
    routes = cfg.get("routes")
    if not isinstance(routes, list) or not routes:
        raise ValueError("routes must be a nonempty list of [seed, intermediate] pairs")
    for route in routes:
        if not isinstance(route, list) or len(route) != 2 or route[0] == route[1] or any(l not in LANGUAGES for l in route):
            raise ValueError("Invalid language route")
    if len({tuple(r) for r in routes}) != len(routes):
        raise ValueError("Duplicate route")
    cfg["repeats"] = positive_integer(cfg.get("repeats", 1), "repeats")
    cfg.setdefault("schedule_seed", 0)
    if type(cfg["schedule_seed"]) is not int:
        raise ValueError("schedule_seed must be an integer")
    cfg["parallel_models"] = positive_integer(cfg.get("parallel_models", 1), "parallel_models")
    cfg["profile"] = load_profile(cfg.get("profile", "paper-abstract-v1"), base_dir)
    from .metrics import METRICS
    control_id = cfg["profile"]["execution"].get("metric")
    for spec in cfg["profile"]["execution"]["metrics"]:
        if spec["id"] == control_id:
            languages = METRICS[spec["metric"]].languages
            if languages and any(route[0] not in languages for route in routes):
                raise ValueError("Decision metric does not support a configured seed language")
            if spec["metric"] == "jplag" and spec["options"].get("language", "cpp") != "text" and any(r[0] != "cpp" for r in routes):
                raise ValueError("JPlag needs text mode for non-C++ seed languages")
    if cfg["profile"]["execution"]["policy"] == "normalized_fixed_point" and any(r[0] != "cpp" for r in routes):
        raise ValueError("normalized_fixed_point requires C++ seeds")
    models = cfg.get("models")
    if not isinstance(models, dict) or not models:
        raise ValueError("models must be a nonempty mapping")
    for alias, model in models.items():
        identifier(alias)
        if not isinstance(model, dict):
            raise ValueError("Each model must be a mapping")
        if set(model) - {"provider", "model", "endpoint", "generation", "api_key_env", "request_timeout", "retries",
                         "pricing", "cost_cap_usd", "expected_model", "accepted_models", "min_interval_seconds"}:
            raise ValueError("Unknown model setting; adapters receive normalized provider configuration")
        model.setdefault("provider", "lmstudio")
        if model["provider"] not in PROVIDER_FACTORIES:
            raise ValueError(f"Unregistered provider: {model['provider']}")
        if model["provider"] == "lmstudio":
            model.setdefault("endpoint", "http://localhost:1234/v1")
        if not isinstance(model.get("model"), str) or not model["model"].strip():
            raise ValueError("Every model needs an explicit model ID")
        model.setdefault("generation", {"temperature": 0})
        if not isinstance(model["generation"], dict):
            raise ValueError("generation must be a mapping")
        for key, value in model["generation"].items():
            if key in ("temperature", "top_p", "repeat_penalty"):
                if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
                    raise ValueError(f"Invalid generation option: {key}")
                if key == "top_p" and value > 1:
                    raise ValueError("top_p must not exceed 1")
            if key in ("max_tokens", "top_k"):
                positive_integer(value, key)
            if key == "seed" and type(value) is not int:
                raise ValueError("seed must be an integer")
        model.setdefault("request_timeout", 300)
        model.setdefault("retries", 0)
        model.setdefault("min_interval_seconds", 0)
        positive_integer(model["request_timeout"], "request_timeout")
        if type(model["retries"]) is not int or model["retries"] < 0:
            raise ValueError("retries must be a nonnegative integer")
        interval = model["min_interval_seconds"]
        if type(interval) not in (int, float) or not math.isfinite(interval) or interval < 0:
            raise ValueError("min_interval_seconds must be nonnegative")
        accepted = model.setdefault("accepted_models", [model.get("expected_model") or model["model"]])
        if not isinstance(accepted, list) or not accepted or any(not isinstance(v, str) or not v for v in accepted):
            raise ValueError("accepted_models must be a nonempty model ID list")
        pricing = model.get("pricing")
        if pricing is not None:
            if not isinstance(pricing, dict) or any(type(v) not in (int, float) or not math.isfinite(v) or v < 0 for v in pricing.values()):
                raise ValueError("pricing must contain finite nonnegative rates")
        cap = model.get("cost_cap_usd")
        if cap is not None and (type(cap) not in (int, float) or not math.isfinite(cap) or cap <= 0):
            raise ValueError("cost_cap_usd must be positive")
        create_provider(provider_settings(model))  # Local validation; no network request.
    cfg.setdefault("prompt_template_version", "rtt.prompts.v2")
    if cfg["prompt_template_version"] not in ("rtt.prompts.v1", "rtt.prompts.v2", "rtt.prompts.abs.v1"):
        raise ValueError("Unknown prompt template version")
    runtime = cfg.setdefault("runtime", {})
    if not isinstance(runtime, dict) or set(runtime) - {"tools", "compile_timeout", "fixture_timeout", "minimum_evaluation_cases"}:
        raise ValueError("Invalid runtime settings")
    runtime.setdefault("compile_timeout", 60)
    runtime.setdefault("fixture_timeout", 10)
    runtime.setdefault("minimum_evaluation_cases", 1)
    for key in ("compile_timeout", "fixture_timeout", "minimum_evaluation_cases"):
        positive_integer(runtime[key], key)
    default_tools = {"cpp": "g++", "c": "gcc", "python": "python", "java": "javac", "haskell": "ghc", "prolog": "swipl"}
    from shutil import which
    tools = runtime.setdefault("tools", {})
    if not isinstance(tools, dict):
        raise ValueError("runtime.tools must be a mapping")
    for language in {l for route in routes for l in route}:
        tool = tools.get(language, default_tools[language])
        if not isinstance(tool, str) or not tool:
            raise ValueError("Runtime tool must be a path or executable name")
        tools[language] = str((Path(base_dir) / tool).resolve()) if Path(tool).parent != Path(".") else (which(tool) or tool)
    return cfg


def provider_settings(model):
    return {k: v for k, v in model.items() if k not in ("min_interval_seconds", "accepted_models")}
