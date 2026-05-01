from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import TYPE_CHECKING, Any, Sequence

from rttdist.artifacts import ArtifactContractError, resolve_contract_path
from rttdist.config import SUPPORTED_TARGET_LANGUAGES
from rttdist.failure_taxonomy import FailureRecord, failure_record_from_dict
from rttdist.metrics import MetricExtractionError, compute_metric_deltas
from rttdist.moss import MossSimilarityMatch

if TYPE_CHECKING:
    from rttdist.pipeline import RTTRunResult


class ReportingError(RuntimeError):
    pass


MossSimilarityFn = Callable[[str, str, str], MossSimilarityMatch]


def _resolve_run_id_within_output_root(*, output_root: Path, run_id: str) -> Path:
    if not isinstance(run_id, str) or not run_id.strip():
        raise ReportingError("`run_id` must be a non-empty string.")

    normalized_run_id = run_id.strip()
    candidate_path = Path(normalized_run_id)

    if candidate_path.is_absolute():
        raise ReportingError(f"`run_id` must not be an absolute path: {run_id!r}.")

    resolved = (output_root / candidate_path).resolve()
    try:
        resolved.relative_to(output_root)
    except ValueError as exc:
        raise ReportingError(f"`run_id` escapes output root: {run_id!r}.") from exc

    return resolved


@dataclass(frozen=True)
class RunSummaryArtifacts:
    summary_json_path: Path
    summary_markdown_path: Path


def generate_run_summary(
    *,
    output_root: Path,
    run_id: str,
    run_results: Sequence[RTTRunResult] | None = None,
    moss_similarity_fn: MossSimilarityFn | None = None,
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
    manifest_paths = _collect_run_manifest_paths(
        output_root=normalized_output_root,
        run_id=normalized_run_id,
        run_results=run_results,
    )
    entries = [
        _build_summary_entry(
            output_root=normalized_output_root,
            manifest_path=path,
            moss_similarity_fn=moss_similarity_fn,
        )
        for path in manifest_paths
    ]
    entries.sort(
        key=lambda item: (
            item["problem_id"],
            item["seed_language"],
            item["target_language"],
        )
    )
    ordered_pair_aggregates = _build_ordered_pair_aggregates(entries)

    return {
        "schema_version": "report_summary.v2",
        "run_id": normalized_run_id,
        "result_count": len(entries),
        "results": entries,
        "ordered_pair_aggregates": ordered_pair_aggregates,
    }


def write_run_summary(
    *,
    output_root: Path,
    run_id: str,
    run_results: Sequence[RTTRunResult] | None = None,
    moss_similarity_fn: MossSimilarityFn | None = None,
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
        moss_similarity_fn=moss_similarity_fn,
    )
    summary_json_path = run_root / "summary.json"
    summary_markdown_path = run_root / "summary.md"
    summary_json_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    summary_markdown_path.write_text(
        render_run_summary_markdown(summary),
        encoding="utf-8",
    )
    return RunSummaryArtifacts(
        summary_json_path=summary_json_path,
        summary_markdown_path=summary_markdown_path,
    )


def render_run_summary_markdown(summary: dict[str, Any]) -> str:
    run_id = str(summary["run_id"])
    results = list(_require_list(summary.get("results"), field_name="results"))
    aggregate_mappings = summary.get("ordered_pair_aggregates")
    if isinstance(aggregate_mappings, dict):
        ordered_pair_aggregates = [
            _require_mapping(item, field_name="ordered_pair_aggregates")
            for _, item in sorted(aggregate_mappings.items())
        ]
    else:
        ordered_pair_aggregates = list(_build_ordered_pair_aggregates(results).values())
    include_moss = any("moss_similarity" in entry for entry in results)

    lines = [
        f"# Run Summary: {run_id}",
        "",
    ]
    if include_moss:
        lines.extend(
            [
                "| Problem | Ordered pair | Final status | Iterations | Change-count distance | Convergence | Residual similarity | MOSS similarity | Semantic |",
                "| --- | --- | --- | ---: | ---: | --- | --- | --- |",
            ]
        )
    else:
        lines.extend(
            [
                "| Problem | Ordered pair | Final status | Iterations | Change-count distance | Convergence | Residual similarity | Semantic |",
                "| --- | --- | --- | ---: | ---: | --- | --- | --- |",
            ]
        )
    for entry in results:
        row_values = {
            "problem": entry["problem_id"],
            "ordered_pair": _ordered_pair_key_from_entry(entry),
            "status": entry["final_status"],
            "iterations": entry["iteration_count"],
            "change_distance": _format_change_count_distance(
                entry["change_count_distance"]
            ),
            "convergence": entry["convergence_outcome"],
            "residual": _format_measurement(entry["residual_similarity"]),
            "semantic": entry["semantic_summary"]["overall"],
        }
        if include_moss:
            row_values["moss"] = _format_moss_measurement(entry.get("moss_similarity"))
            lines.append(
                "| {problem} | {ordered_pair} | {status} | {iterations} | {change_distance} | {convergence} | {residual} | {moss} | {semantic} |".format(
                    **row_values
                )
            )
        else:
            lines.append(
                "| {problem} | {ordered_pair} | {status} | {iterations} | {change_distance} | {convergence} | {residual} | {semantic} |".format(
                    **row_values
                )
            )

    lines.extend(
        [
            "",
            "## Ordered-pair aggregates",
            "",
            "| Ordered pair | Results | Divergence rate | Measured divergence count | Unavailable divergence count | Infrastructure divergence count |",
            "| --- | ---: | --- | ---: | ---: | ---: |",
        ]
    )
    for aggregate in ordered_pair_aggregates:
        divergence = _require_mapping(
            aggregate.get("divergence"), field_name="ordered_pair_aggregate.divergence"
        )
        lines.append(
            "| {ordered_pair} | {result_count} | {rate} | {measured} | {unavailable} | {infrastructure} |".format(
                ordered_pair=_require_text(
                    aggregate.get("ordered_pair_key"),
                    field_name="ordered_pair_aggregate.ordered_pair_key",
                ),
                result_count=aggregate.get("result_count", 0),
                rate=_format_aggregate_rate(divergence),
                measured=divergence.get("measured_count", 0),
                unavailable=divergence.get("unavailable_count", 0),
                infrastructure=divergence.get("infrastructure_count", 0),
            )
        )

    for aggregate in ordered_pair_aggregates:
        ordered_pair_key = _require_text(
            aggregate.get("ordered_pair_key"),
            field_name="ordered_pair_aggregate.ordered_pair_key",
        )
        change_count_distance = _require_mapping(
            aggregate.get("change_count_distance"),
            field_name="ordered_pair_aggregate.change_count_distance",
        )
        residual_similarity = _require_mapping(
            aggregate.get("residual_similarity"),
            field_name="ordered_pair_aggregate.residual_similarity",
        )
        final_similarity_score = _require_mapping(
            aggregate.get("final_similarity_score"),
            field_name="ordered_pair_aggregate.final_similarity_score",
        )
        divergence = _require_mapping(
            aggregate.get("divergence"), field_name="ordered_pair_aggregate.divergence"
        )
        lines.extend(
            [
                "",
                f"### Ordered pair: {ordered_pair_key}",
                "",
                (
                    "- Change-count distance aggregate: "
                    f"{_format_numeric_aggregate(change_count_distance)}"
                ),
                (
                    "- Residual similarity aggregate: "
                    f"{_format_numeric_aggregate(residual_similarity)}"
                ),
                (
                    "- Final similarity score aggregate: "
                    f"{_format_numeric_aggregate(final_similarity_score)}"
                ),
                (f"- Divergence aggregate: {_format_divergence_aggregate(divergence)}"),
            ]
        )

    for entry in results:
        section_lines = [
            "",
            f"## {entry['problem_id']} / {_ordered_pair_key_from_entry(entry)}",
            "",
            f"- Ordered pair: {_ordered_pair_key_from_entry(entry)}",
            f"- Final status: {entry['final_status']}",
            f"- Iteration count: {entry['iteration_count']}",
            (
                "- Change-count distance (1 cycle = C++ -> target -> C++): "
                f"{_format_change_count_distance(entry['change_count_distance'])}"
            ),
            f"- Convergence outcome: {entry['convergence_outcome']}",
            (
                "- Residual similarity to seed C++: "
                f"{_format_measurement(entry['residual_similarity'])}"
            ),
        ]
        if "moss_similarity" in entry:
            section_lines.append(
                "- MOSS similarity to seed C++: "
                f"{_format_moss_measurement(entry['moss_similarity'])}"
            )
        section_lines.extend(
            [
                (
                    "- Semantic summary: "
                    f"{entry['semantic_summary']['overall']} "
                    f"(target={entry['semantic_summary']['target']['status']}, "
                    f"roundtrip_cpp={entry['semantic_summary']['roundtrip_cpp']['status']})"
                ),
                (
                    "- Target complexity deltas: "
                    f"{_format_complexity_measurement(entry['complexity_deltas']['target'])}"
                ),
                (
                    "- Roundtrip C++ complexity deltas: "
                    f"{_format_complexity_measurement(entry['complexity_deltas']['roundtrip_cpp'])}"
                ),
            ]
        )
        lines.extend(section_lines)

    lines.append("")
    return "\n".join(lines)


def _build_final_similarity_summary(
    *,
    output_root: Path,
    metadata: dict[str, Any],
    manifest_path: Path,
    failure_record: FailureRecord,
) -> dict[str, Any]:
    configured_relative_path = _optional_text(
        metadata.get("final_similarity_artifact_path")
    )
    if configured_relative_path is not None:
        similarity_path = _resolve_path_within_output_root(
            output_root=output_root,
            relative_path=configured_relative_path,
            field_name="metadata.final_similarity_artifact_path",
        )
    else:
        similarity_path = manifest_path.parent / "final-similarity.json"

    payload = _load_optional_json(similarity_path)
    if payload is None:
        return _unavailable_measurement(
            reason="missing_final_similarity_artifact",
            failure_record=failure_record,
        )

    availability = payload.get("availability")
    if availability == "measured":
        score = payload.get("score")
        if isinstance(score, (int, float)):
            return _measured_measurement(
                {
                    "score": float(score),
                    "provider": payload.get("provider"),
                    "configured_model": payload.get("configured_model"),
                    "observed_model": payload.get("observed_model"),
                    "dimensions": payload.get("dimensions"),
                    "usage": payload.get("usage"),
                    "request_ids": payload.get("request_ids"),
                    "source_hashes": payload.get("source_hashes"),
                    "revision_evidence": payload.get("revision_evidence"),
                }
            )
        return _unavailable_measurement(
            reason="invalid_final_similarity_artifact",
            failure_record=failure_record,
        )

    reason = payload.get("reason")
    if isinstance(reason, str) and reason.strip():
        return _unavailable_measurement(
            reason=reason.strip(),
            failure_record=failure_record,
            details=_require_mapping(payload, field_name="final_similarity_artifact"),
        )

    return _unavailable_measurement(
        reason="invalid_final_similarity_artifact",
        failure_record=failure_record,
    )


def _build_summary_entry(
    *,
    output_root: Path,
    manifest_path: Path,
    moss_similarity_fn: MossSimilarityFn | None,
) -> dict[str, Any]:
    manifest = _require_mapping(
        _load_json_file(manifest_path),
        field_name=f"manifest:{manifest_path.as_posix()}",
    )
    metadata = _require_mapping(manifest.get("metadata"), field_name="metadata")
    problem = _require_mapping(metadata.get("problem"), field_name="metadata.problem")
    iterations = _require_list(manifest.get("iterations"), field_name="iterations")
    if not iterations:
        raise ReportingError(
            f"Run manifest has no iterations: {manifest_path.as_posix()}"
        )

    final_record = failure_record_from_dict(
        _require_mapping(manifest.get("final"), field_name="final")
    )
    final_iteration = _require_mapping(iterations[-1], field_name="iterations[-1]")
    artifact_paths = _require_mapping(
        final_iteration.get("artifact_paths"),
        field_name="iterations[-1].artifact_paths",
    )

    problem_id = _require_text(problem.get("problem_id"), field_name="problem_id")
    seed_language = _optional_text(metadata.get("seed_language")) or "cpp"
    target_language = _require_text(
        metadata.get("target_language"), field_name="target_language"
    )
    execution_payload = _load_optional_json(
        _resolve_path_within_output_root(
            output_root=output_root,
            relative_path=_require_text(
                artifact_paths.get("execution_result_path"),
                field_name="execution_result_path",
            ),
            field_name="execution_result_path",
        )
    )
    metrics_payload = _load_optional_json(
        _resolve_path_within_output_root(
            output_root=output_root,
            relative_path=_require_text(
                artifact_paths.get("metrics_path"),
                field_name="metrics_path",
            ),
            field_name="metrics_path",
        )
    )

    translated_source = _read_source_if_present(
        _resolve_path_within_output_root(
            output_root=output_root,
            relative_path=_require_text(
                artifact_paths.get("translated_source_path"),
                field_name="translated_source_path",
            ),
            field_name="translated_source_path",
        )
    )
    roundtrip_source = _read_source_if_present(
        _resolve_path_within_output_root(
            output_root=output_root,
            relative_path=_require_text(
                artifact_paths.get("roundtrip_source_path"),
                field_name="roundtrip_source_path",
            ),
            field_name="roundtrip_source_path",
        )
    )
    seed_source = _load_seed_source(
        output_root=output_root,
        metadata=metadata,
        problem=problem,
    )

    previous_target_source = _load_previous_source(
        output_root=output_root,
        iterations=iterations,
        artifact_key="translated_source_path",
    )
    previous_roundtrip_source = _load_previous_source(
        output_root=output_root,
        iterations=iterations,
        artifact_key="roundtrip_source_path",
    )

    semantic_summary = _build_semantic_summary(execution_payload)
    completed_cycle_count = _count_completed_rtt_cycles(
        output_root=output_root,
        iterations=iterations,
    )
    final_similarity = _build_final_similarity_summary(
        output_root=output_root,
        metadata=metadata,
        manifest_path=manifest_path,
        failure_record=final_record,
    )

    entry = {
        "problem_id": problem_id,
        "seed_language": seed_language,
        "target_language": target_language,
        "ordered_pair_key": _ordered_pair_key(
            seed_language=seed_language,
            target_language=target_language,
        ),
        "final_status": final_record.status.value,
        "iteration_count": len(iterations),
        "change_count_distance": _build_change_count_distance_summary(
            completed_cycle_count=completed_cycle_count
        ),
        "final_iteration_index": final_record.iteration_index,
        "convergence_outcome": _convergence_outcome(final_record),
        "residual_similarity": _build_residual_similarity_summary(
            seed_language=seed_language,
            metrics_payload=metrics_payload,
            failure_record=final_record,
        ),
        "final_similarity": final_similarity,
        "semantic_summary": semantic_summary,
        "complexity_deltas": {
            "target": _build_complexity_delta_summary(
                current_language=target_language,
                current_source=translated_source,
                seed_cpp_source=seed_source,
                previous_source=previous_target_source,
                previous_language=target_language,
                missing_reason="missing_target_source",
                failure_record=final_record,
            ),
            "roundtrip_cpp": _build_complexity_delta_summary(
                current_language="cpp",
                current_source=roundtrip_source,
                seed_cpp_source=seed_source,
                previous_source=previous_roundtrip_source,
                previous_language="cpp",
                missing_reason="missing_roundtrip_cpp_source",
                failure_record=final_record,
            ),
        },
        "artifacts": {
            "run_manifest_path": _relative_to(output_root, manifest_path),
            "final_iteration_directory": _require_text(
                artifact_paths.get("iteration_directory"),
                field_name="iteration_directory",
            ),
            "final_execution_path": _require_text(
                artifact_paths.get("execution_result_path"),
                field_name="execution_result_path",
            ),
            "final_metrics_path": _require_text(
                artifact_paths.get("metrics_path"),
                field_name="metrics_path",
            ),
            "final_similarity_path": _optional_text(
                metadata.get("final_similarity_artifact_path")
            ),
        },
    }
    if moss_similarity_fn is not None:
        entry["moss_similarity"] = _build_moss_similarity_summary(
            seed_cpp_source=seed_source,
            roundtrip_cpp_source=roundtrip_source,
            failure_record=final_record,
            problem_id=problem_id,
            target_language=target_language,
            moss_similarity_fn=moss_similarity_fn,
        )
    return entry


def _ordered_pair_key(*, seed_language: str, target_language: str) -> str:
    return f"{seed_language}->{target_language}"


def _ordered_pair_key_from_entry(entry: dict[str, Any]) -> str:
    existing = _optional_text(entry.get("ordered_pair_key"))
    if existing is not None:
        return existing
    seed_language = _optional_text(entry.get("seed_language")) or "cpp"
    target_language = _require_text(
        entry.get("target_language"), field_name="target_language"
    )
    return _ordered_pair_key(
        seed_language=seed_language, target_language=target_language
    )


def _build_ordered_pair_aggregates(
    entries: Sequence[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    grouped_entries: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        ordered_pair_key = _ordered_pair_key_from_entry(entry)
        grouped_entries.setdefault(ordered_pair_key, []).append(entry)

    aggregates: dict[str, dict[str, Any]] = {}
    for ordered_pair_key in sorted(grouped_entries):
        grouped = grouped_entries[ordered_pair_key]
        seed_language, target_language = ordered_pair_key.split("->", maxsplit=1)
        aggregates[ordered_pair_key] = {
            "ordered_pair_key": ordered_pair_key,
            "seed_language": seed_language,
            "target_language": target_language,
            "result_count": len(grouped),
            "change_count_distance": _build_numeric_aggregate(
                grouped,
                measurement_getter=lambda item: item.get("change_count_distance"),
                value_getter=lambda value: (
                    float(value) if isinstance(value, (int, float)) else None
                ),
            ),
            "residual_similarity": _build_numeric_aggregate(
                grouped,
                measurement_getter=lambda item: item.get("residual_similarity"),
                value_getter=lambda value: (
                    float(value) if isinstance(value, (int, float)) else None
                ),
            ),
            "final_similarity_score": _build_numeric_aggregate(
                grouped,
                measurement_getter=lambda item: item.get("final_similarity"),
                value_getter=_extract_final_similarity_score,
            ),
            "divergence": _build_divergence_aggregate(grouped),
        }
    return aggregates


def _build_numeric_aggregate(
    entries: Sequence[dict[str, Any]],
    *,
    measurement_getter: Callable[[dict[str, Any]], Any],
    value_getter: Callable[[Any], float | None],
) -> dict[str, Any]:
    values: list[float] = []
    unavailable_count = 0
    infrastructure_count = 0
    for entry in entries:
        measurement = measurement_getter(entry)
        measurement_mapping = (
            _require_mapping(measurement, field_name="measurement")
            if isinstance(measurement, dict)
            else None
        )
        if measurement_mapping is None:
            unavailable_count += 1
            continue
        if measurement_mapping.get("availability") != "measured":
            unavailable_count += 1
            if _is_infrastructure_measurement_failure(measurement_mapping):
                infrastructure_count += 1
            continue

        value = value_getter(measurement_mapping.get("value"))
        if value is None:
            unavailable_count += 1
            if _is_infrastructure_measurement_failure(measurement_mapping):
                infrastructure_count += 1
            continue
        values.append(value)

    measured_count = len(values)
    payload: dict[str, Any] = {
        "measured_count": measured_count,
        "unavailable_count": unavailable_count,
        "infrastructure_count": infrastructure_count,
        "denominator": measured_count,
    }
    if measured_count == 0:
        payload.update(
            {
                "availability": "unavailable",
                "reason": "no_measured_values",
            }
        )
        return payload

    payload.update(
        {
            "availability": "measured",
            "mean": sum(values) / measured_count,
            "stddev": _population_stddev(values),
        }
    )
    return payload


def _extract_final_similarity_score(value: Any) -> float | None:
    if not isinstance(value, dict):
        return None
    score = value.get("score")
    if isinstance(score, (int, float)):
        return float(score)
    return None


def _build_divergence_aggregate(entries: Sequence[dict[str, Any]]) -> dict[str, Any]:
    divergent_count = 0
    non_divergent_count = 0
    unavailable_count = 0
    infrastructure_count = 0

    for entry in entries:
        final_status = _optional_text(entry.get("final_status")) or ""
        if _is_infrastructure_failure_status(final_status):
            unavailable_count += 1
            infrastructure_count += 1
            continue

        if final_status in {"success", "oscillation", "max_iter_no_convergence"}:
            if entry.get("convergence_outcome") == "fixed_point":
                non_divergent_count += 1
            else:
                divergent_count += 1
            continue

        unavailable_count += 1

    measured_count = divergent_count + non_divergent_count
    payload: dict[str, Any] = {
        "divergent_count": divergent_count,
        "non_divergent_count": non_divergent_count,
        "measured_count": measured_count,
        "unavailable_count": unavailable_count,
        "infrastructure_count": infrastructure_count,
        "denominator": measured_count,
    }
    if measured_count == 0:
        payload.update(
            {
                "availability": "unavailable",
                "reason": "no_measured_values",
            }
        )
        return payload

    payload.update(
        {
            "availability": "measured",
            "divergence_rate": divergent_count / measured_count,
        }
    )
    return payload


def _is_infrastructure_measurement_failure(measurement: dict[str, Any]) -> bool:
    failure = measurement.get("failure")
    if not isinstance(failure, dict):
        return False
    status = _optional_text(failure.get("status"))
    return _is_infrastructure_failure_status(status)


def _is_infrastructure_failure_status(status: str | None) -> bool:
    return status == "api_error"


def _population_stddev(values: Sequence[float]) -> float:
    if len(values) <= 1:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return math.sqrt(variance)


def _build_moss_similarity_summary(
    *,
    seed_cpp_source: str | None,
    roundtrip_cpp_source: str | None,
    failure_record: FailureRecord,
    problem_id: str,
    target_language: str,
    moss_similarity_fn: MossSimilarityFn,
) -> dict[str, Any]:
    if seed_cpp_source is None:
        return _unavailable_measurement(
            reason="missing_seed_cpp_source",
            failure_record=failure_record,
        )
    if roundtrip_cpp_source is None:
        return _unavailable_measurement(
            reason="missing_roundtrip_cpp_source",
            failure_record=failure_record,
        )

    try:
        match = moss_similarity_fn(
            seed_cpp_source,
            roundtrip_cpp_source,
            f"rttdist:{problem_id}/{target_language}",
        )
    except Exception as exc:
        return _unavailable_measurement(
            reason="moss_execution_failed",
            details={"message": str(exc)},
        )

    return _measured_measurement(
        {
            "seed_percentage": match.seed_percentage,
            "roundtrip_percentage": match.roundtrip_percentage,
            "report_url": match.report_url,
            "match_url": match.match_url,
        }
    )


def _collect_run_manifest_paths(
    *,
    output_root: Path,
    run_id: str,
    run_results: Sequence[RTTRunResult] | None,
) -> tuple[Path, ...]:
    if run_results is not None:
        unique_paths: set[Path] = set()
        for item in run_results:
            candidate_manifest_path = Path(item.run_manifest_path).resolve()
            try:
                relative_manifest_path = candidate_manifest_path.relative_to(
                    output_root
                )
            except ValueError as exc:
                raise ReportingError(
                    "Unsafe report path rejected for `run_manifest_path`: "
                    f"{candidate_manifest_path.as_posix()!r}."
                ) from exc
            unique_paths.add(
                _resolve_path_within_output_root(
                    output_root=output_root,
                    relative_path=relative_manifest_path.as_posix(),
                    field_name="run_manifest_path",
                )
            )
        manifest_paths = tuple(sorted(unique_paths))
    else:
        manifest_paths = _discover_manifest_paths_for_run_id(
            output_root=output_root,
            run_id=run_id,
        )

    if not manifest_paths:
        raise ReportingError(
            f"No persisted run manifests found for run `{run_id}` under {output_root}."
        )
    return manifest_paths


def _discover_manifest_paths_for_run_id(
    *, output_root: Path, run_id: str
) -> tuple[Path, ...]:
    run_root = _resolve_path_within_output_root(
        output_root=output_root,
        relative_path=run_id,
        field_name="run_id",
    )
    v2_manifest_paths = _discover_v2_manifest_paths(run_root)
    legacy_manifest_paths = _discover_legacy_v1_manifest_paths(run_root)

    combined: set[Path] = set()
    for path in v2_manifest_paths + legacy_manifest_paths:
        combined.add(
            _resolve_path_within_output_root(
                output_root=output_root,
                relative_path=path.relative_to(output_root).as_posix(),
                field_name="run_manifest_path",
            )
        )
    return tuple(sorted(combined))


def _discover_v2_manifest_paths(run_root: Path) -> list[Path]:
    return sorted(run_root.glob("*/*-to-*/run.json"))


def _discover_legacy_v1_manifest_paths(run_root: Path) -> list[Path]:
    legacy_paths: list[Path] = []
    for path in sorted(run_root.glob("*/*/run.json")):
        if path.parent.name not in SUPPORTED_TARGET_LANGUAGES:
            continue
        legacy_paths.append(path)
    return legacy_paths


def _build_residual_similarity_summary(
    *,
    seed_language: str,
    metrics_payload: dict[str, Any] | None,
    failure_record: FailureRecord,
) -> dict[str, Any]:
    if seed_language != "cpp":
        return _unavailable_measurement(
            reason="seed_language_not_cpp",
            failure_record=failure_record,
        )

    if metrics_payload is None:
        return _unavailable_measurement(
            reason="missing_metrics_artifact",
            failure_record=failure_record,
        )

    residual_similarity = metrics_payload.get("residual_similarity")
    if isinstance(residual_similarity, (int, float)):
        return _measured_measurement(float(residual_similarity))

    return _unavailable_measurement(
        reason="residual_similarity_not_recorded",
        failure_record=failure_record,
    )


def _build_change_count_distance_summary(
    *, completed_cycle_count: int
) -> dict[str, Any]:
    return {
        "availability": "measured",
        "value": int(completed_cycle_count),
        "unit": "cpp_to_target_to_cpp_cycles",
        "definition": "1 cycle = C++ -> target -> C++",
    }


def _count_completed_rtt_cycles(*, output_root: Path, iterations: list[Any]) -> int:
    completed = 0
    for index, iteration in enumerate(iterations):
        iteration_mapping = _require_mapping(
            iteration, field_name=f"iterations[{index}]"
        )
        artifact_paths = _require_mapping(
            iteration_mapping.get("artifact_paths"),
            field_name=f"iterations[{index}].artifact_paths",
        )
        roundtrip_source = _read_source_if_present(
            _resolve_path_within_output_root(
                output_root=output_root,
                relative_path=_require_text(
                    artifact_paths.get("roundtrip_source_path"),
                    field_name="roundtrip_source_path",
                ),
                field_name="roundtrip_source_path",
            )
        )
        if roundtrip_source is not None:
            completed += 1
    return completed


def _build_complexity_delta_summary(
    *,
    current_language: str,
    current_source: str | None,
    seed_cpp_source: str | None,
    previous_source: str | None,
    previous_language: str,
    missing_reason: str,
    failure_record: FailureRecord,
) -> dict[str, Any]:
    if current_source is None:
        return _unavailable_measurement(
            reason=missing_reason,
            failure_record=failure_record,
        )
    if seed_cpp_source is None:
        return _unavailable_measurement(reason="missing_seed_cpp_source")

    try:
        metric_deltas = compute_metric_deltas(
            current_language=current_language,
            current_source=current_source,
            seed_cpp_source=seed_cpp_source,
            previous_source=previous_source,
            previous_language=previous_language
            if previous_source is not None
            else None,
        )
    except MetricExtractionError as exc:
        return _unavailable_measurement(
            reason="metric_extraction_error",
            details={"message": str(exc)},
        )
    return _measured_measurement(metric_deltas.to_dict())


def _build_semantic_summary(
    execution_payload: dict[str, Any] | None,
) -> dict[str, Any]:
    if execution_payload is None:
        target = _not_evaluated_stage_summary(reason="missing_execution_artifact")
        roundtrip_cpp = _not_evaluated_stage_summary(
            reason="missing_execution_artifact"
        )
    else:
        target = _semantic_stage_summary(execution_payload.get("target"))
        roundtrip_cpp = _semantic_stage_summary(execution_payload.get("roundtrip_cpp"))

    overall = "pass" if target["passed"] and roundtrip_cpp["passed"] else "fail"
    return {
        "overall": overall,
        "target": target,
        "roundtrip_cpp": roundtrip_cpp,
    }


def _semantic_stage_summary(stage_payload: Any) -> dict[str, Any]:
    if not isinstance(stage_payload, dict):
        return _not_evaluated_stage_summary(reason="stage_not_executed")

    status = stage_payload.get("status")
    normalized_status = status if isinstance(status, str) and status else "unknown"
    fixture_results = stage_payload.get("fixture_results")
    if not isinstance(fixture_results, list):
        fixture_results = []

    fixture_pass_count = sum(
        1
        for item in fixture_results
        if isinstance(item, dict) and item.get("status") == "success"
    )
    fixture_fail_count = len(fixture_results) - fixture_pass_count

    return {
        "available": True,
        "status": normalized_status,
        "passed": normalized_status == "success",
        "fixture_pass_count": fixture_pass_count,
        "fixture_fail_count": fixture_fail_count,
        "message": stage_payload.get("message"),
    }


def _not_evaluated_stage_summary(*, reason: str) -> dict[str, Any]:
    return {
        "available": False,
        "status": "not_evaluated",
        "passed": False,
        "fixture_pass_count": 0,
        "fixture_fail_count": 0,
        "message": reason,
    }


def _convergence_outcome(failure_record: FailureRecord) -> str:
    convergence_status = failure_record.details.get("convergence_status")
    if convergence_status == "fixed_point":
        return "fixed_point"
    if (
        convergence_status == "oscillation"
        or failure_record.status.value == "oscillation"
    ):
        return "oscillation"
    if failure_record.status.value == "max_iter_no_convergence":
        return "max_iter_no_convergence"
    return "terminated_on_failure"


def _load_previous_source(
    *,
    output_root: Path,
    iterations: list[Any],
    artifact_key: str,
) -> str | None:
    if len(iterations) < 2:
        return None

    previous_iteration = _require_mapping(iterations[-2], field_name="iterations[-2]")
    artifact_paths = _require_mapping(
        previous_iteration.get("artifact_paths"),
        field_name="iterations[-2].artifact_paths",
    )
    return _read_source_if_present(
        _resolve_path_within_output_root(
            output_root=output_root,
            relative_path=_require_text(
                artifact_paths.get(artifact_key), field_name=artifact_key
            ),
            field_name=artifact_key,
        )
    )


def _load_seed_source(
    *,
    output_root: Path,
    metadata: dict[str, Any],
    problem: dict[str, Any],
) -> str | None:
    seed_artifact_path = metadata.get("seed_artifact_path")
    if isinstance(seed_artifact_path, str) and seed_artifact_path.strip():
        return _read_source_if_present(
            _resolve_path_within_output_root(
                output_root=output_root,
                relative_path=seed_artifact_path.strip(),
                field_name="metadata.seed_artifact_path",
            )
        )

    legacy_seed_source_path = problem.get("seed_source_path")
    if isinstance(legacy_seed_source_path, str) and legacy_seed_source_path.strip():
        return _read_source_if_present(
            _resolve_path_within_output_root(
                output_root=output_root,
                relative_path=legacy_seed_source_path.strip(),
                field_name="metadata.problem.seed_source_path",
            )
        )

    return None


def _resolve_path_within_output_root(
    *, output_root: Path, relative_path: str, field_name: str
) -> Path:
    try:
        return resolve_contract_path(output_root, relative_path)
    except ArtifactContractError as exc:
        raise ReportingError(
            f"Unsafe report path rejected for `{field_name}`: {relative_path!r}."
        ) from exc


def _missing_metric_input_reason(
    *,
    seed_cpp_source: str | None,
    target_source: str | None,
    roundtrip_cpp_source: str | None,
) -> str | None:
    if seed_cpp_source is None:
        return "missing_seed_cpp_source"
    if target_source is None:
        return "missing_target_source"
    if roundtrip_cpp_source is None:
        return "missing_roundtrip_cpp_source"
    return None


def _measured_measurement(value: Any) -> dict[str, Any]:
    return {
        "availability": "measured",
        "value": value,
    }


def _unavailable_measurement(
    *,
    reason: str,
    failure_record: FailureRecord | None = None,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "availability": "unavailable",
        "reason": reason,
    }
    if failure_record is not None:
        payload["failure"] = {
            "status": failure_record.status.value,
            "stage": failure_record.stage,
            "iteration_index": failure_record.iteration_index,
        }
    if details is not None:
        payload["details"] = details
    return payload


def _format_measurement(measurement: dict[str, Any]) -> str:
    if measurement.get("availability") == "measured":
        value = measurement.get("value")
        if isinstance(value, float):
            return f"{value:.6f}"
        return str(value)

    failure = measurement.get("failure")
    if isinstance(failure, dict):
        failure_status = failure.get("status", "unknown")
        failure_stage = failure.get("stage", "unknown")
        return f"unavailable ({failure_status} at {failure_stage})"
    return f"unavailable ({measurement.get('reason', 'unknown')})"


def _format_change_count_distance(measurement: dict[str, Any]) -> str:
    if measurement.get("availability") != "measured":
        return _format_measurement(measurement)
    return str(measurement.get("value"))


def _format_moss_measurement(measurement: dict[str, Any] | None) -> str:
    if measurement is None:
        return "not_requested"
    if measurement.get("availability") != "measured":
        return _format_measurement(measurement)

    value = _require_mapping(
        measurement.get("value"), field_name="moss_similarity.value"
    )
    return "seed={seed}%, roundtrip={roundtrip}%".format(
        seed=value.get("seed_percentage"),
        roundtrip=value.get("roundtrip_percentage"),
    )


def _format_complexity_measurement(measurement: dict[str, Any]) -> str:
    if measurement.get("availability") != "measured":
        return _format_measurement(measurement)

    value = _require_mapping(
        measurement.get("value"), field_name="complexity_measurement.value"
    )
    delta_vs_seed_cpp = _require_mapping(
        value.get("delta_vs_seed_cpp"), field_name="delta_vs_seed_cpp"
    )
    delta_vs_previous = value.get("delta_vs_previous")
    formatted = f"vs_seed_cpp[{_format_metric_delta(delta_vs_seed_cpp)}]"
    if isinstance(delta_vs_previous, dict):
        formatted = (
            f"{formatted}; vs_previous[{_format_metric_delta(delta_vs_previous)}]"
        )
    return formatted


def _format_metric_delta(delta: dict[str, Any]) -> str:
    return ", ".join(f"{name}={delta[name]}" for name in sorted(delta))


def _format_numeric_aggregate(aggregate: dict[str, Any]) -> str:
    measured_count = aggregate.get("measured_count", 0)
    unavailable_count = aggregate.get("unavailable_count", 0)
    infrastructure_count = aggregate.get("infrastructure_count", 0)
    if aggregate.get("availability") != "measured":
        return (
            "unavailable "
            f"(measured={measured_count}, unavailable={unavailable_count}, "
            f"infrastructure={infrastructure_count})"
        )
    mean = aggregate.get("mean")
    stddev = aggregate.get("stddev")
    return (
        f"mean={mean:.6f}, stddev={stddev:.6f}, measured={measured_count}, "
        f"unavailable={unavailable_count}, infrastructure={infrastructure_count}"
    )


def _format_aggregate_rate(aggregate: dict[str, Any]) -> str:
    if aggregate.get("availability") != "measured":
        return "unavailable"
    value = aggregate.get("divergence_rate")
    if isinstance(value, float):
        return f"{value:.6f}"
    return str(value)


def _format_divergence_aggregate(aggregate: dict[str, Any]) -> str:
    measured_count = aggregate.get("measured_count", 0)
    unavailable_count = aggregate.get("unavailable_count", 0)
    infrastructure_count = aggregate.get("infrastructure_count", 0)
    if aggregate.get("availability") != "measured":
        return (
            "unavailable "
            f"(measured={measured_count}, unavailable={unavailable_count}, "
            f"infrastructure={infrastructure_count})"
        )
    divergence_rate = aggregate.get("divergence_rate")
    return (
        f"rate={divergence_rate:.6f}, divergent={aggregate.get('divergent_count', 0)}, "
        f"non_divergent={aggregate.get('non_divergent_count', 0)}, measured={measured_count}, "
        f"unavailable={unavailable_count}, infrastructure={infrastructure_count}"
    )


def _relative_to(output_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(output_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _load_json_file(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_optional_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    raw_payload = _load_json_file(path)
    if not isinstance(raw_payload, dict):
        raise ReportingError(f"Expected JSON object at {path.as_posix()}.")
    return raw_payload


def _read_source_if_present(path: Path) -> str | None:
    if not path.is_file():
        return None
    source = path.read_text(encoding="utf-8").rstrip()
    if not source.strip():
        return None
    return source


def _require_mapping(value: Any, *, field_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ReportingError(f"Expected `{field_name}` to be a mapping.")
    return value


def _require_list(value: Any, *, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise ReportingError(f"Expected `{field_name}` to be a list.")
    return value


def _require_text(value: Any, *, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReportingError(f"Expected `{field_name}` to be a non-empty string.")
    return value.strip()


def _optional_text(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    return stripped if stripped else None
