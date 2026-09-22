from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Any, TYPE_CHECKING

from rttdist.failure_taxonomy import FailureRecord, failure_record_from_dict
from rttdist.metrics import (
    LEGACY_RTT_DISTANCE_MISSING_REASON,
    build_legacy_distance_metrics_fallback,
)

if TYPE_CHECKING:
    from rttdist.pipeline import RTTRunResult


class ReportingError(RuntimeError):
    pass



@dataclass(frozen=True)
class RunSummaryArtifacts:
    summary_json_path: Path
    summary_markdown_path: Path


def generate_run_summary(
    *,
    output_root: Path,
    run_id: str,
    run_results: Sequence[RTTRunResult] | None = None,
) -> dict[str, Any]:
    normalized_output_root = Path(output_root).resolve()
    normalized_run_id = (
        _resolve_run_id_within_output_root(
            output_root=normalized_output_root,
            run_id=run_id,
        )
        .relative_to(normalized_output_root)
        .as_posix()
    )
    entries = [
        _build_summary_entry(output_root=normalized_output_root, manifest_path=path)
        for path in _collect_run_manifest_paths(
            output_root=normalized_output_root,
            run_id=normalized_run_id,
            run_results=run_results,
        )
    ]
    entries.sort(key=lambda item: (item["problem_id"], item["rtt_route_key"]))
    return {
        "schema_version": "report_summary.rtt.v1",
        "run_id": normalized_run_id,
        "result_count": len(entries),
        "results": entries,
        "rtt_route_aggregates": _build_rtt_route_aggregates(entries),
    }


def write_run_summary(
    *,
    output_root: Path,
    run_id: str,
    run_results: Sequence[RTTRunResult] | None = None,
) -> RunSummaryArtifacts:
    normalized_output_root = Path(output_root).resolve()
    run_root = _resolve_run_id_within_output_root(
        output_root=normalized_output_root,
        run_id=run_id,
    )
    run_root.mkdir(parents=True, exist_ok=True)
    summary = generate_run_summary(
        output_root=normalized_output_root,
        run_id=run_id,
        run_results=run_results,
    )
    summary_json_path = run_root / "summary.json"
    summary_markdown_path = run_root / "summary.md"
    summary_json_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    summary_markdown_path.write_text(render_run_summary_markdown(summary), encoding="utf-8")
    return RunSummaryArtifacts(summary_json_path=summary_json_path, summary_markdown_path=summary_markdown_path)


def render_run_summary_markdown(summary: dict[str, Any]) -> str:
    run_id = str(summary["run_id"])
    results = list(_require_list(summary.get("results"), field_name="results"))
    aggregates = _require_mapping(
        summary.get("rtt_route_aggregates"), field_name="rtt_route_aggregates"
    )
    lines = [
        f"# Run Summary: {run_id}",
        "",
        "| Problem | RTT route | Final status | RTT cycles | Conversions/cycle | Completed conversions | Convergence | Semantic |",
        "| --- | --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for entry in results:
        lines.append(
            "| {problem} | {route} | {status} | {cycles} | {per_cycle} | {completed} | {convergence} | {semantic} |".format(
                problem=entry["problem_id"],
                route=entry["rtt_route_key"],
                status=entry["final_status"],
                cycles=_format_measurement(entry["rtt_distance"]),
                per_cycle=entry["translation_count_per_cycle"],
                completed=entry["completed_translation_count"],
                convergence=entry["convergence_outcome"],
                semantic=_paper_semantic_status(entry),
            )
        )

    lines.extend([
        "",
        "## RTT route aggregates",
        "",
        "| RTT route | Results | Divergence rate | Measured divergence count | Unavailable divergence count | Infrastructure divergence count |",
        "| --- | ---: | --- | ---: | ---: | ---: |",
    ])
    for _, aggregate_value in sorted(aggregates.items()):
        aggregate = _require_mapping(aggregate_value, field_name="aggregate")
        divergence = _require_mapping(aggregate.get("divergence"), field_name="divergence")
        lines.append(
            "| {route} | {count} | {rate} | {measured} | {unavailable} | {infra} |".format(
                route=aggregate.get("rtt_route_key"),
                count=aggregate.get("result_count", 0),
                rate=_format_aggregate_rate(divergence),
                measured=divergence.get("measured_count", 0),
                unavailable=divergence.get("unavailable_count", 0),
                infra=divergence.get("infrastructure_count", 0),
            )
        )

    for entry in results:
        lines.extend([
            "",
            f"## {entry['problem_id']} / {entry['rtt_route_key']}",
            "",
            f"- RTT route: {entry['rtt_route_key']}",
            f"- Final status: {entry['final_status']}",
            f"- RTT cycle count: {_format_measurement(entry['rtt_distance'])}",
            f"- Translations per RTT cycle: {entry['translation_count_per_cycle']}",
            f"- Attempted translations in final iteration: {entry['attempted_translation_count']}",
            f"- Completed translations in final iteration: {entry['completed_translation_count']}",
            f"- Failed translations in final iteration: {entry['failed_translation_count']}",
            f"- Conversion log: {entry['artifacts']['final_conversion_log_path']}",
            f"- Convergence outcome: {entry['convergence_outcome']}",
            f"- Semantic preservation: {_paper_semantic_status(entry)}",
            f"- Legacy semantic summary (raw execution): {entry['semantic_summary']['overall']}",
            f"- Residual similarity: {_format_distance_metric(entry['distance_metrics'].get('residual_similarity'))}",
            f"- Complexity delta: {_format_distance_metric(entry['distance_metrics'].get('complexity_delta'))}",
        ])
    lines.append("")
    return "\n".join(lines)


def _build_summary_entry(*, output_root: Path, manifest_path: Path) -> dict[str, Any]:
    manifest = _require_mapping(_load_json_file(manifest_path), field_name="manifest")
    metadata = _require_mapping(manifest.get("metadata"), field_name="metadata")
    problem = _require_mapping(metadata.get("problem"), field_name="metadata.problem")
    iterations = _require_list(manifest.get("iterations"), field_name="iterations")
    if not iterations:
        raise ReportingError(f"Run manifest has no iterations: {manifest_path.as_posix()}")
    final_record = failure_record_from_dict(_require_mapping(manifest.get("final"), field_name="final"))
    final_iteration = _require_mapping(iterations[-1], field_name="iterations[-1]")
    artifact_paths = _require_mapping(final_iteration.get("artifact_paths"), field_name="artifact_paths")
    metrics_payload = _load_optional_json(
        _resolve_path_within_output_root(
            output_root=output_root,
            relative_path=_require_text(artifact_paths.get("metrics_path"), field_name="metrics_path"),
            field_name="metrics_path",
        )
    )
    execution_payload = _load_optional_json(
        _resolve_path_within_output_root(
            output_root=output_root,
            relative_path=_require_text(artifact_paths.get("execution_result_path"), field_name="execution_result_path"),
            field_name="execution_result_path",
        )
    )
    seed_language = _optional_text(metadata.get("seed_language")) or "cpp"
    target_language = _require_text(metadata.get("target_language"), field_name="target_language")
    language_route = _normalize_language_route(metadata.get("language_route"), seed_language, target_language)
    route_key = _optional_text(metadata.get("route_key")) or "->".join(language_route)
    completed_cycles = _count_completed_rtt_cycles(output_root=output_root, iterations=iterations)
    rtt_distance_summary = _build_rtt_distance_summary(
        completed_cycle_count=completed_cycles,
        metrics_payload=metrics_payload,
    )
    translation_summary = _build_translation_count_summary(
        language_route=language_route,
        final_iteration=final_iteration,
        metrics_payload=metrics_payload,
    )
    semantic_summary = _build_semantic_summary(execution_payload)
    distance_metrics_summary = _build_distance_metrics_summary(
        metrics_payload=metrics_payload,
        rtt_distance=rtt_distance_summary,
        evaluation_checks=translation_summary.get("evaluation_checks"),
        translation_steps=translation_summary.get("translation_steps", []),
    )
    return {
        "problem_id": _require_text(problem.get("problem_id"), field_name="problem_id"),
        "seed_language": seed_language,
        "target_language": target_language,
        "language_route": list(language_route),
        "rtt_route_key": route_key,
        "final_status": final_record.status.value,
        "iteration_count": len(iterations),
        "rtt_distance": rtt_distance_summary,
        **translation_summary,
        "final_iteration_index": final_record.iteration_index,
        "convergence_outcome": _convergence_outcome(final_record),
        "semantic_summary": semantic_summary,
        "distance_metrics": distance_metrics_summary,
        "artifacts": {
            "run_manifest_path": _relative_to(output_root, manifest_path),
            "final_iteration_directory": _require_text(artifact_paths.get("iteration_directory"), field_name="iteration_directory"),
            "final_execution_path": _require_text(artifact_paths.get("execution_result_path"), field_name="execution_result_path"),
            "final_metrics_path": _require_text(artifact_paths.get("metrics_path"), field_name="metrics_path"),
            "final_conversion_log_path": _conversion_log_path(final_iteration, artifact_paths),
        },
    }


def _normalize_language_route(value: Any, seed_language: str, target_language: str) -> tuple[str, ...]:
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return tuple(item.strip().lower() for item in value if item.strip())
    return (seed_language, target_language, seed_language)


def _build_rtt_distance_summary(*, completed_cycle_count: int, metrics_payload: dict[str, Any] | None) -> dict[str, Any]:
    if isinstance(metrics_payload, dict) and isinstance(metrics_payload.get("rtt_distance"), dict):
        return _require_mapping(metrics_payload["rtt_distance"], field_name="rtt_distance")
    if isinstance(metrics_payload, dict) and "rtt_distance" in metrics_payload:
        return {
            "availability": "unavailable",
            "reason": LEGACY_RTT_DISTANCE_MISSING_REASON,
            "unit": "completed_full_routes",
        }
    return {
        "availability": "measured",
        "value": int(completed_cycle_count),
        "unit": "completed_full_routes",
        "definition": "one route = configured language_route",
    }


def _build_distance_metrics_summary(
    *,
    metrics_payload: dict[str, Any] | None,
    rtt_distance: dict[str, Any],
    evaluation_checks: Any,
    translation_steps: Any,
) -> dict[str, Any]:
    if isinstance(metrics_payload, dict) and isinstance(metrics_payload.get("distance_metrics"), dict):
        return dict(metrics_payload["distance_metrics"])
    steps = translation_steps if isinstance(translation_steps, list) else []
    checks = evaluation_checks if isinstance(evaluation_checks, dict) else {}
    return build_legacy_distance_metrics_fallback(
        rtt_distance=rtt_distance,
        evaluation_checks=checks,
        translation_steps=[step for step in steps if isinstance(step, dict)],
    )


def _build_translation_count_summary(
    *,
    language_route: Sequence[str],
    final_iteration: dict[str, Any],
    metrics_payload: dict[str, Any] | None,
) -> dict[str, Any]:
    fallback_per_cycle = max(len(tuple(language_route)) - 1, 0)
    if isinstance(metrics_payload, dict):
        translation_count = metrics_payload.get("translation_count")
        if isinstance(translation_count, dict):
            return {
                "translation_count_per_cycle": _coerce_int(
                    translation_count.get("per_cycle"), fallback_per_cycle
                ),
                "attempted_translation_count": _coerce_int(
                    translation_count.get("attempted"), 0
                ),
                "completed_translation_count": _coerce_int(
                    translation_count.get("completed"), 0
                ),
                "failed_translation_count": _coerce_int(
                    translation_count.get("failed"), 0
                ),
                "translation_steps": _optional_list(
                    metrics_payload.get("translation_steps")
                ),
                "evaluation_checks": _optional_mapping(
                    metrics_payload.get("evaluation_checks")
                ),
            }
        return {
            "translation_count_per_cycle": _coerce_int(
                metrics_payload.get("translation_count_per_cycle"), fallback_per_cycle
            ),
            "attempted_translation_count": _coerce_int(
                metrics_payload.get("attempted_translation_count"), 0
            ),
            "completed_translation_count": _coerce_int(
                metrics_payload.get("completed_translation_count"), 0
            ),
            "failed_translation_count": _coerce_int(
                metrics_payload.get("failed_translation_count"), 0
            ),
            "translation_steps": _optional_list(
                metrics_payload.get("translation_steps")
            ),
            "evaluation_checks": _optional_mapping(
                metrics_payload.get("evaluation_checks")
            ),
        }
    return {
        "translation_count_per_cycle": _coerce_int(
            final_iteration.get("translation_count_per_cycle"), fallback_per_cycle
        ),
        "attempted_translation_count": _coerce_int(
            final_iteration.get("attempted_translation_count"), 0
        ),
        "completed_translation_count": _coerce_int(
            final_iteration.get("completed_translation_count"), 0
        ),
        "failed_translation_count": _coerce_int(
            final_iteration.get("failed_translation_count"), 0
        ),
        "translation_steps": [],
        "evaluation_checks": {},
    }


def _conversion_log_path(
    final_iteration: dict[str, Any], artifact_paths: dict[str, Any]
) -> str:
    value = final_iteration.get("conversion_log_path")
    if isinstance(value, str) and value.strip():
        return value.strip()
    metrics_payload_path = _require_text(
        artifact_paths.get("metrics_path"), field_name="metrics_path"
    )
    return (Path(metrics_payload_path).parent / "conversion.log").as_posix()


def _coerce_int(value: Any, fallback: int) -> int:
    if isinstance(value, bool):
        return fallback
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return fallback


def _optional_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _optional_mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _count_completed_rtt_cycles(*, output_root: Path, iterations: Sequence[Any]) -> int:
    completed = 0
    for index, item in enumerate(iterations):
        iteration = _require_mapping(item, field_name=f"iterations[{index}]")
        artifact_paths = _require_mapping(iteration.get("artifact_paths"), field_name="artifact_paths")
        roundtrip_path = _require_text(artifact_paths.get("roundtrip_source_path"), field_name="roundtrip_source_path")
        path = _resolve_path_within_output_root(output_root=output_root, relative_path=roundtrip_path, field_name="roundtrip_source_path")
        if path.is_file() and path.read_text(encoding="utf-8").strip():
            completed += 1
    return completed


def _build_semantic_summary(execution_payload: dict[str, Any] | None) -> dict[str, Any]:
    if execution_payload is None:
        return {"overall": "unknown", "steps": []}
    steps = execution_payload.get("steps")
    if isinstance(steps, list) and steps:
        step_summaries = [_semantic_stage_summary(step) for step in steps]
        overall = "pass" if all(step.get("status") == "success" for step in step_summaries) else "fail"
        return {"overall": overall, "steps": step_summaries}
    target = _semantic_stage_summary(execution_payload.get("target"))
    roundtrip_cpp = _semantic_stage_summary(execution_payload.get("roundtrip_cpp"))
    overall = "pass" if target["status"] == "success" and roundtrip_cpp["status"] == "success" else "fail"
    return {"overall": overall, "target": target, "roundtrip_cpp": roundtrip_cpp, "steps": [target, roundtrip_cpp]}


def _semantic_stage_summary(stage_payload: Any) -> dict[str, Any]:
    if not isinstance(stage_payload, dict):
        return {"available": False, "status": "not_evaluated", "passed": False, "fixture_pass_count": 0, "fixture_fail_count": 0, "message": "stage_not_executed"}
    fixture_results = stage_payload.get("fixture_results")
    fixtures = fixture_results if isinstance(fixture_results, list) else []
    pass_count = sum(1 for item in fixtures if isinstance(item, dict) and item.get("status") == "success")
    fail_count = len(fixtures) - pass_count
    status = str(stage_payload.get("status", "unknown"))
    return {"available": True, "status": status, "passed": status == "success", "fixture_pass_count": pass_count, "fixture_fail_count": fail_count, "message": stage_payload.get("message")}


def _build_rtt_route_aggregates(entries: Sequence[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        grouped.setdefault(str(entry["rtt_route_key"]), []).append(entry)
    return {
        key: {
            "rtt_route_key": key,
            "result_count": len(items),
            "rtt_distance": _build_numeric_aggregate(items),
            "divergence": _build_divergence_aggregate(items),
        }
        for key, items in sorted(grouped.items())
    }


def _build_numeric_aggregate(entries: Sequence[dict[str, Any]]) -> dict[str, Any]:
    values: list[float] = []
    unavailable_count = 0
    infrastructure_count = 0
    for entry in entries:
        measurement = entry.get("rtt_distance")
        if not isinstance(measurement, dict) or measurement.get("availability") != "measured":
            unavailable_count += 1
            if isinstance(measurement, dict) and _is_infrastructure_measurement_failure(measurement):
                infrastructure_count += 1
            continue
        value = measurement.get("value")
        if isinstance(value, (int, float)):
            values.append(float(value))
        else:
            unavailable_count += 1
    payload = {"measured_count": len(values), "unavailable_count": unavailable_count, "infrastructure_count": infrastructure_count, "denominator": len(values)}
    if not values:
        return {**payload, "availability": "unavailable", "reason": "no_measured_values"}
    return {**payload, "availability": "measured", "mean": sum(values) / len(values), "stddev": _population_stddev(values)}


def _build_divergence_aggregate(entries: Sequence[dict[str, Any]]) -> dict[str, Any]:
    divergent_count = 0
    non_divergent_count = 0
    unavailable_count = 0
    infrastructure_count = 0
    for entry in entries:
        status = str(entry.get("final_status", ""))
        if _is_infrastructure_failure_status(status):
            unavailable_count += 1
            infrastructure_count += 1
        elif status in {"success", "oscillation", "max_iter_no_convergence"}:
            if entry.get("convergence_outcome") == "fixed_point":
                non_divergent_count += 1
            else:
                divergent_count += 1
        else:
            unavailable_count += 1
    measured_count = divergent_count + non_divergent_count
    payload = {"divergent_count": divergent_count, "non_divergent_count": non_divergent_count, "measured_count": measured_count, "unavailable_count": unavailable_count, "infrastructure_count": infrastructure_count, "denominator": measured_count}
    if measured_count == 0:
        return {**payload, "availability": "unavailable", "reason": "no_measured_values"}
    return {**payload, "availability": "measured", "divergence_rate": divergent_count / measured_count}


def _collect_run_manifest_paths(*, output_root: Path, run_id: str, run_results: Sequence[RTTRunResult] | None) -> list[Path]:
    if run_results is not None:
        paths = [Path(result.run_manifest_path).resolve() for result in run_results]
    else:
        run_root = _resolve_run_id_within_output_root(output_root=output_root, run_id=run_id)
        paths = sorted(path.resolve() for path in run_root.glob("**/run.json"))
    for path in paths:
        try:
            path.relative_to(output_root)
        except ValueError as exc:
            raise ReportingError(f"Run manifest escapes output root: {path}") from exc
    return paths


def _resolve_run_id_within_output_root(*, output_root: Path, run_id: str) -> Path:
    if not isinstance(run_id, str) or not run_id.strip():
        raise ReportingError("`run_id` must be a non-empty string.")
    candidate = Path(run_id.strip())
    if candidate.is_absolute():
        raise ReportingError(f"`run_id` must not be an absolute path: {run_id!r}.")
    resolved = (output_root / candidate).resolve()
    try:
        resolved.relative_to(output_root)
    except ValueError as exc:
        raise ReportingError(f"`run_id` escapes output root: {run_id!r}.") from exc
    return resolved


def _resolve_path_within_output_root(*, output_root: Path, relative_path: str, field_name: str) -> Path:
    if not isinstance(relative_path, str) or not relative_path.strip():
        raise ReportingError(f"`{field_name}` must be a non-empty relative path.")
    candidate = Path(relative_path.strip())
    if candidate.is_absolute():
        raise ReportingError(f"`{field_name}` must not be absolute: {relative_path!r}.")
    resolved = (output_root / candidate).resolve()
    try:
        resolved.relative_to(output_root)
    except ValueError as exc:
        raise ReportingError(f"`{field_name}` escapes output root: {relative_path!r}.") from exc
    return resolved


def _load_json_file(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_optional_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else None


def _convergence_outcome(final_record: FailureRecord) -> str:
    details = final_record.details if isinstance(final_record.details, dict) else {}
    status = details.get("convergence_status")
    return status if isinstance(status, str) and status else "terminated_on_failure"


def _format_measurement(measurement: dict[str, Any]) -> str:
    if measurement.get("availability") == "measured":
        return str(measurement.get("value"))
    failure = measurement.get("failure")
    if isinstance(failure, dict):
        return f"unavailable ({failure.get('status', 'unknown')} at {failure.get('stage', 'unknown')})"
    return f"unavailable ({measurement.get('reason', 'unknown')})"


def _paper_semantic_status(entry: dict[str, Any]) -> str:
    distance_metrics = entry.get("distance_metrics")
    if isinstance(distance_metrics, dict):
        semantic_preservation = distance_metrics.get("semantic_preservation")
        if isinstance(semantic_preservation, dict):
            status = semantic_preservation.get("status")
            if isinstance(status, str) and status:
                return status
    semantic_summary = entry.get("semantic_summary")
    if isinstance(semantic_summary, dict):
        status = semantic_summary.get("overall")
        if isinstance(status, str) and status:
            return status
    return "unknown"


def _format_distance_metric(metric: Any) -> str:
    if not isinstance(metric, dict):
        return "unavailable (missing)"
    if metric.get("available") is True or metric.get("availability") == "measured":
        value = metric.get("value")
        if isinstance(value, float):
            return f"measured {value:.6f}"
        if value is not None:
            return f"measured {value}"
        status = metric.get("status")
        return str(status) if isinstance(status, str) and status else "available"
    reason = metric.get("reason")
    if isinstance(reason, str) and reason:
        return f"unavailable ({reason})"
    status = metric.get("status")
    return f"unavailable ({status})" if isinstance(status, str) and status else "unavailable"


def _format_aggregate_rate(measurement: dict[str, Any]) -> str:
    if measurement.get("availability") != "measured":
        return "unavailable"
    value = measurement.get("divergence_rate")
    return f"{float(value):.6f}" if isinstance(value, (int, float)) else "unavailable"


def _population_stddev(values: Sequence[float]) -> float:
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    return math.sqrt(sum((value - mean) ** 2 for value in values) / len(values))


def _is_infrastructure_measurement_failure(measurement: dict[str, Any]) -> bool:
    failure = measurement.get("failure")
    return isinstance(failure, dict) and _is_infrastructure_failure_status(str(failure.get("status", "")))


def _is_infrastructure_failure_status(status: str) -> bool:
    return status in {"api_error", "parse_error", "compile_error", "runtime_error", "timeout"}


def _relative_to(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _require_mapping(value: Any, *, field_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ReportingError(f"`{field_name}` must be a mapping.")
    return value


def _require_list(value: Any, *, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise ReportingError(f"`{field_name}` must be a list.")
    return value


def _require_text(value: Any, *, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReportingError(f"`{field_name}` must be a non-empty string.")
    return value.strip()


def _optional_text(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None
