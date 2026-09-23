"""Measurements are independent of termination decisions and aggregation."""
from __future__ import annotations

from dataclasses import dataclass, field
import math
from pathlib import Path
from typing import Callable

from rttdist.experiment_io import digest


@dataclass(frozen=True)
class MetricContext:
    reference: str
    candidate: str | None
    language: str
    folder: Path
    step: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Metric:
    name: str
    version: str
    unit: str
    compute: Callable[[MetricContext, dict], dict]
    languages: tuple[str, ...] = ()  # Empty means language independent.
    scopes: tuple[str, ...] = ("roundtrip",)
    requires: tuple[str, ...] = ("reference", "candidate")


METRICS: dict[str, Metric] = {}


def register_metric(metric: Metric) -> None:
    if metric.name in METRICS:
        raise ValueError(f"Metric already registered: {metric.name}")
    METRICS[metric.name] = metric


def validate_metric(spec: dict) -> None:
    if not isinstance(spec, dict) or set(spec) - {"id", "metric", "version", "scope", "reference", "options"}:
        raise ValueError("Invalid metric specification")
    metric = METRICS.get(spec.get("metric"))
    if metric is None:
        raise ValueError(f"Unknown metric: {spec.get('metric')}")
    if spec.get("version", metric.version) != metric.version:
        raise ValueError(f"Metric version mismatch: {metric.name}")
    if spec.get("scope", "roundtrip") not in metric.scopes:
        raise ValueError(f"Unsupported metric scope: {metric.name}")
    if spec.get("reference", "previous") not in ("previous", "origin"):
        raise ValueError("Metric reference must be previous or origin")
    if not isinstance(spec.get("options", {}), dict):
        raise ValueError("Metric options must be a mapping")


def measure(spec: dict, context: MetricContext) -> dict:
    validate_metric(spec)
    metric = METRICS[spec["metric"]]
    base = {
        "id": spec["id"], "metric": metric.name, "version": metric.version,
        "unit": metric.unit, "scope": spec.get("scope", "roundtrip"),
        "reference": spec.get("reference", "previous"), "language": context.language,
        "reference_sha256": digest(context.reference.encode()),
        "candidate_sha256": digest(context.candidate.encode()) if context.candidate is not None else None,
        "options": spec.get("options", {}), "value": None, "reason": None,
    }
    if metric.languages and context.language not in metric.languages:
        return {**base, "status": "not_applicable", "reason": "unsupported_language"}
    inputs = {"reference": context.reference, "candidate": context.candidate, **context.step}
    missing = [key for key in metric.requires if inputs.get(key) is None]
    if missing:
        return {**base, "status": "unavailable", "reason": "missing_inputs:" + ",".join(missing)}
    context.folder.mkdir(parents=True, exist_ok=True)
    try:
        result = metric.compute(context, spec.get("options", {}))
        if result.get("status") not in ("measured", "unavailable", "not_applicable", "error"):
            raise ValueError("Invalid measurement status")
        if result["status"] == "measured":
            value = result.get("value")
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError("A measured value must be finite and numeric")
        # A plugin cannot replace identity or provenance fields.
        return {**result, **base, "status": result["status"],
                "value": result.get("value") if result["status"] == "measured" else None,
                "reason": result.get("reason")}
    except Exception as exc:
        return {**base, "status": "error", "reason": type(exc).__name__}


def _tokens(context, options, sequence=False):
    from rttdist.normalize import normalize_cpp_tokens
    from rttdist.similarity import token_multiset_dice, token_sequence_ratio
    fn = token_sequence_ratio if sequence else token_multiset_dice
    return {"status": "measured", "value": fn(normalize_cpp_tokens(context.reference),
                                                normalize_cpp_tokens(context.candidate))}


def _jplag(context, options):
    from rttdist.jplag_similarity import measure as jplag
    if options.get("language", "cpp") != "text" and context.language != "cpp":
        return {"status": "not_applicable", "reason": "configure_text_mode_for_non_cpp"}
    if not options.get("jar") or not options.get("java"):
        return {"status": "unavailable", "reason": "jplag_not_configured"}
    return jplag(context.reference, context.candidate, context.folder,
                 config={"language": "cpp", "minimum_tokens": 9, **options})


def _ast(context, options):
    from rttdist.ast_similarity import ast_similarity
    return ast_similarity(context.reference, context.candidate, **options)


def _latency(context, options):
    value = context.step.get("response", {}).get("latency_seconds")
    return {"status": "measured" if value is not None else "unavailable", "value": value,
            "reason": None if value is not None else "provider_did_not_report"}


def _usage(context, options, key):
    value = (context.step.get("response", {}).get("usage") or {}).get(key)
    return {"status": "measured" if value is not None else "unavailable", "value": value,
            "reason": None if value is not None else "provider_did_not_report"}


register_metric(Metric("token_dice", "1", "similarity", _tokens, ("cpp",)))
register_metric(Metric("source_identity", "1", "similarity", lambda ctx, opts: {
    "status": "measured", "value": float(ctx.reference.replace("\r\n", "\n") == ctx.candidate.replace("\r\n", "\n"))}))
register_metric(Metric("token_sequence", "1", "similarity",
                       lambda ctx, opts: _tokens(ctx, opts, True), ("cpp",)))
register_metric(Metric("jplag", "1", "similarity", _jplag))
register_metric(Metric("ast_similarity", "1", "similarity", _ast, ("cpp",)))
register_metric(Metric("source_bytes_delta", "1", "bytes", lambda ctx, opts: {
    "status": "measured", "value": len(ctx.candidate.encode()) - len(ctx.reference.encode())},
    scopes=("step", "roundtrip")))
register_metric(Metric("llm_latency", "1", "seconds", _latency, scopes=("step",), requires=("response",)))
register_metric(Metric("prompt_tokens", "1", "tokens", lambda ctx, opts: _usage(ctx, opts, "prompt_tokens"),
                       scopes=("step",), requires=("response",)))
register_metric(Metric("completion_tokens", "1", "tokens", lambda ctx, opts: _usage(ctx, opts, "completion_tokens"),
                       scopes=("step",), requires=("response",)))
