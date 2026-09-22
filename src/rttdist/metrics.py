from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
from typing import Any

from rttdist.failure_taxonomy import FailureRecord
from rttdist.normalize import NormalizationError, normalize_cpp_tokens

COMPLEXITY_UNAVAILABLE_REASON = "optional_tool_not_configured_or_not_installed"
LEGACY_DISTANCE_METRICS_MISSING_REASON = "legacy_distance_metrics_missing"
LEGACY_RTT_DISTANCE_MISSING_REASON = "legacy_rtt_distance_missing"
NO_COMPLETED_ROUTE_REASON = "no_completed_route"
ZERO_TOKEN_DENOMINATOR_REASON = "zero_token_denominator"

_COMPLEXITY_SUBMETRICS = ("loc", "token_count", "cyclomatic", "function_count", "max_nesting")


def build_distance_metrics(
    *,
    rtt_distance: Mapping[str, Any] | None,
    evaluation_checks: Mapping[str, Any] | None,
    translation_steps: Sequence[Mapping[str, Any]],
    reference_source: str,
    candidate_source: str,
) -> dict[str, Any]:
    """Build the first-pass paper-facing language-distance metric block."""

    return {
        "schema_version": 1,
        "change_count": build_change_count_metric(rtt_distance),
        "residual_similarity": build_residual_similarity(reference_source, candidate_source),
        "semantic_preservation": build_semantic_preservation(
            evaluation_checks=evaluation_checks,
            translation_steps=translation_steps,
        ),
        "complexity_delta": build_complexity_delta_unavailable(),
    }


def build_change_count_metric(rtt_distance: Mapping[str, Any] | None) -> dict[str, Any]:
    if isinstance(rtt_distance, Mapping) and rtt_distance.get("availability") == "measured":
        value = rtt_distance.get("value")
        return {
            "available": True,
            "status": "measured",
            "value": value,
            "unit": rtt_distance.get("unit", "completed_full_routes"),
            "canonical_source": "rtt_distance",
        }

    reason = NO_COMPLETED_ROUTE_REASON
    if isinstance(rtt_distance, Mapping):
        reason_value = rtt_distance.get("reason")
        if isinstance(reason_value, str) and reason_value:
            reason = reason_value

    payload: dict[str, Any] = {
        "available": False,
        "status": "unavailable",
        "reason": reason,
        "unit": "completed_full_routes",
        "canonical_source": "rtt_distance",
    }
    if isinstance(rtt_distance, Mapping) and isinstance(rtt_distance.get("failure"), Mapping):
        payload["failure"] = dict(rtt_distance["failure"])
    return payload


def build_residual_similarity(reference_source: str, candidate_source: str) -> dict[str, Any]:
    base = {
        "metric": "sorensen_dice_token_multiset",
        "unit": "ratio",
        "source_language": "cpp",
        "reference": "iteration_input_seed_source",
        "candidate": "roundtrip_source",
    }
    try:
        reference_tokens = Counter(normalize_cpp_tokens(reference_source))
        candidate_tokens = Counter(normalize_cpp_tokens(candidate_source))
    except NormalizationError as exc:
        return {
            **base,
            "available": False,
            "status": "unavailable",
            "reason": _normalization_reason(exc),
            "message": str(exc),
        }

    denominator = sum(reference_tokens.values()) + sum(candidate_tokens.values())
    if denominator == 0:
        return {
            **base,
            "available": False,
            "status": "unavailable",
            "reason": ZERO_TOKEN_DENOMINATOR_REASON,
        }

    overlap = sum(
        min(reference_tokens[token], candidate_tokens[token])
        for token in reference_tokens.keys() | candidate_tokens.keys()
    )
    return {
        **base,
        "available": True,
        "status": "measured",
        "value": (2.0 * overlap) / denominator,
    }


def build_semantic_preservation(
    *,
    evaluation_checks: Mapping[str, Any] | None,
    translation_steps: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    steps = [dict(step) for step in translation_steps]
    evaluated_steps = [step for step in steps if _has_evaluation_result(step)]
    base: dict[str, Any] = {
        "canonical_source": "evaluation_checks",
        "compile": dict(evaluation_checks.get("compile", {}))
        if isinstance(evaluation_checks, Mapping)
        and isinstance(evaluation_checks.get("compile"), Mapping)
        else {},
        "functionality": dict(evaluation_checks.get("functionality", {}))
        if isinstance(evaluation_checks, Mapping)
        and isinstance(evaluation_checks.get("functionality"), Mapping)
        else {},
    }

    if not evaluated_steps:
        return {
            **base,
            "available": False,
            "status": "not_evaluated",
            "overall_passed": False,
            "final_roundtrip_passed": False,
            "route_had_degradation": False,
            "reason": "no_evaluation_results",
        }

    final_step = steps[-1] if steps else evaluated_steps[-1]
    final_roundtrip_passed = final_step.get("functionality_passed") is True
    route_had_degradation = any(_is_intermediate_degradation(step) for step in steps[:-1])

    if final_roundtrip_passed:
        if route_had_degradation:
            return {
                **base,
                "available": True,
                "status": "degraded",
                "overall_passed": False,
                "final_roundtrip_passed": True,
                "route_had_degradation": True,
                "reason": "route_degraded",
            }
        return {
            **base,
            "available": True,
            "status": "pass",
            "overall_passed": True,
            "final_roundtrip_passed": True,
            "route_had_degradation": False,
        }

    reason = _semantic_failure_reason(final_step)
    return {
        **base,
        "available": True,
        "status": "fail",
        "overall_passed": False,
        "final_roundtrip_passed": False,
        "route_had_degradation": route_had_degradation,
        "reason": reason,
    }


def build_complexity_delta_unavailable() -> dict[str, Any]:
    submetric = {
        "available": False,
        "status": "unavailable",
        "reason": COMPLEXITY_UNAVAILABLE_REASON,
    }
    return {
        "available": False,
        "status": "unavailable",
        "tool": "lizard",
        "reason": COMPLEXITY_UNAVAILABLE_REASON,
        "metrics": {name: dict(submetric) for name in _COMPLEXITY_SUBMETRICS},
    }


def build_unavailable_rtt_distance(failure_record: FailureRecord) -> dict[str, Any]:
    return {
        "availability": "unavailable",
        "reason": NO_COMPLETED_ROUTE_REASON,
        "unit": "completed_full_routes",
        "failure": {
            "status": failure_record.status.value,
            "stage": failure_record.stage,
        },
    }


def build_legacy_distance_metrics_fallback(
    *,
    rtt_distance: Mapping[str, Any] | None,
    evaluation_checks: Mapping[str, Any] | None = None,
    translation_steps: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    if isinstance(rtt_distance, Mapping):
        change_count = build_change_count_metric(rtt_distance)
    else:
        change_count = {
            "available": False,
            "status": "unavailable",
            "reason": LEGACY_RTT_DISTANCE_MISSING_REASON,
            "unit": "completed_full_routes",
            "canonical_source": "rtt_distance",
        }

    semantic_preservation = build_semantic_preservation(
        evaluation_checks=evaluation_checks,
        translation_steps=translation_steps,
    )
    if not translation_steps:
        semantic_preservation = {
            "available": False,
            "status": "not_evaluated",
            "overall_passed": False,
            "final_roundtrip_passed": False,
            "route_had_degradation": False,
            "reason": LEGACY_DISTANCE_METRICS_MISSING_REASON,
            "canonical_source": "evaluation_checks",
            "compile": dict(evaluation_checks.get("compile", {}))
            if isinstance(evaluation_checks, Mapping)
            and isinstance(evaluation_checks.get("compile"), Mapping)
            else {},
            "functionality": dict(evaluation_checks.get("functionality", {}))
            if isinstance(evaluation_checks, Mapping)
            and isinstance(evaluation_checks.get("functionality"), Mapping)
            else {},
        }

    return {
        "schema_version": 1,
        "change_count": change_count,
        "residual_similarity": {
            "available": False,
            "status": "unavailable",
            "metric": "sorensen_dice_token_multiset",
            "unit": "ratio",
            "source_language": "cpp",
            "reference": "iteration_input_seed_source",
            "candidate": "roundtrip_source",
            "reason": LEGACY_DISTANCE_METRICS_MISSING_REASON,
        },
        "semantic_preservation": semantic_preservation,
        "complexity_delta": build_complexity_delta_unavailable(),
    }


def _normalization_reason(exc: NormalizationError) -> str:
    message = str(exc)
    if "non-empty" in message:
        return "empty_or_whitespace_source"
    return "normalization_error"


def _has_evaluation_result(step: Mapping[str, Any]) -> bool:
    return _status_is_evaluated(step.get("compile_status")) or _status_is_evaluated(
        step.get("functionality_status")
    )


def _status_is_evaluated(value: Any) -> bool:
    return isinstance(value, str) and value not in {"", "not_evaluated"}


def _is_intermediate_degradation(step: Mapping[str, Any]) -> bool:
    return (
        step.get("status") == "completed_with_functionality_failure"
        or step.get("functionality_passed") is False
        and step.get("functionality_status") == "failed"
    )


def _semantic_failure_reason(final_step: Mapping[str, Any]) -> str:
    if not _has_evaluation_result(final_step):
        return "route_incomplete"
    functionality_check = final_step.get("functionality_check")
    if isinstance(functionality_check, Mapping):
        execution_status = functionality_check.get("execution_status")
        if isinstance(execution_status, str) and execution_status:
            return execution_status
    compile_status = final_step.get("compile_status")
    if compile_status == "failed":
        return "compile_failed"
    functionality_status = final_step.get("functionality_status")
    if isinstance(functionality_status, str) and functionality_status:
        return functionality_status
    step_status = final_step.get("status")
    if isinstance(step_status, str) and step_status:
        return step_status
    return "route_incomplete"
