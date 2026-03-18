from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Sequence

from rttdist.artifacts import ArtifactContractError, resolve_contract_path
from rttdist.ast_metrics import compute_roundtrip_ast_distance_metrics
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
    entries.sort(key=lambda item: (item["problem_id"], item["target_language"]))

    return {
        "schema_version": "report_summary.v1",
        "run_id": normalized_run_id,
        "result_count": len(entries),
        "results": entries,
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
    include_moss = any("moss_similarity" in entry for entry in results)

    lines = [
        f"# Run Summary: {run_id}",
        "",
    ]
    if include_moss:
        lines.extend(
            [
                "| Problem | Language | Final status | Iterations | Change-count distance | Convergence | Residual similarity | MOSS similarity | Semantic | AST distance to seed |",
                "| --- | --- | --- | ---: | ---: | --- | --- | --- | --- | --- |",
            ]
        )
    else:
        lines.extend(
            [
                "| Problem | Language | Final status | Iterations | Change-count distance | Convergence | Residual similarity | Semantic | AST distance to seed |",
                "| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |",
            ]
        )
    for entry in results:
        row_values = {
            "problem": entry["problem_id"],
            "language": entry["target_language"],
            "status": entry["final_status"],
            "iterations": entry["iteration_count"],
            "change_distance": _format_change_count_distance(
                entry["change_count_distance"]
            ),
            "convergence": entry["convergence_outcome"],
            "residual": _format_measurement(entry["residual_similarity"]),
            "semantic": entry["semantic_summary"]["overall"],
            "ast": _format_ast_seed_distance(entry["ast_distance"]),
        }
        if include_moss:
            row_values["moss"] = _format_moss_measurement(entry.get("moss_similarity"))
            lines.append(
                "| {problem} | {language} | {status} | {iterations} | {change_distance} | {convergence} | {residual} | {moss} | {semantic} | {ast} |".format(
                    **row_values
                )
            )
        else:
            lines.append(
                "| {problem} | {language} | {status} | {iterations} | {change_distance} | {convergence} | {residual} | {semantic} | {ast} |".format(
                    **row_values
                )
            )

    for entry in results:
        section_lines = [
            "",
            f"## {entry['problem_id']} / {entry['target_language']}",
            "",
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
                f"- AST distance: {_format_ast_distance(entry['ast_distance'])}",
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

    entry = {
        "problem_id": problem_id,
        "target_language": target_language,
        "final_status": final_record.status.value,
        "iteration_count": len(iterations),
        "change_count_distance": _build_change_count_distance_summary(
            completed_cycle_count=completed_cycle_count
        ),
        "final_iteration_index": final_record.iteration_index,
        "convergence_outcome": _convergence_outcome(final_record),
        "residual_similarity": _build_residual_similarity_summary(
            metrics_payload=metrics_payload,
            failure_record=final_record,
        ),
        "semantic_summary": semantic_summary,
        "ast_distance": _build_ast_distance_summary(
            seed_cpp_source=seed_source,
            target_language=target_language,
            target_source=translated_source,
            roundtrip_cpp_source=roundtrip_source,
            failure_record=final_record,
        ),
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
        manifest_paths = tuple(
            sorted(
                _resolve_path_within_output_root(
                    output_root=output_root,
                    relative_path=path.relative_to(output_root).as_posix(),
                    field_name="run_manifest_path",
                )
                for path in (output_root / run_id).glob("*/*/run.json")
            )
        )

    if not manifest_paths:
        raise ReportingError(
            f"No persisted run manifests found for run `{run_id}` under {output_root}."
        )
    return manifest_paths


def _build_residual_similarity_summary(
    *,
    metrics_payload: dict[str, Any] | None,
    failure_record: FailureRecord,
) -> dict[str, Any]:
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


def _build_ast_distance_summary(
    *,
    seed_cpp_source: str | None,
    target_language: str,
    target_source: str | None,
    roundtrip_cpp_source: str | None,
    failure_record: FailureRecord,
) -> dict[str, Any]:
    missing_source_reason = _missing_metric_input_reason(
        seed_cpp_source=seed_cpp_source,
        target_source=target_source,
        roundtrip_cpp_source=roundtrip_cpp_source,
    )
    if missing_source_reason is not None:
        return _unavailable_measurement(
            reason=missing_source_reason,
            failure_record=failure_record,
        )

    if seed_cpp_source is None or target_source is None or roundtrip_cpp_source is None:
        raise ReportingError(
            "AST distance inputs unexpectedly missing after validation."
        )

    ast_distance = compute_roundtrip_ast_distance_metrics(
        seed_cpp_source=seed_cpp_source,
        target_language=target_language,
        target_source=target_source,
        roundtrip_cpp_source=roundtrip_cpp_source,
    )
    if ast_distance.status != "ok":
        return _unavailable_measurement(
            reason="ast_parser_failure",
            details=ast_distance.to_dict(),
        )
    return _measured_measurement(ast_distance.to_dict())


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


def _format_ast_seed_distance(measurement: dict[str, Any]) -> str:
    if measurement.get("availability") != "measured":
        return _format_measurement(measurement)
    value = _require_mapping(measurement.get("value"), field_name="ast_distance.value")
    return str(value.get("distance_to_seed_cpp"))


def _format_ast_distance(measurement: dict[str, Any]) -> str:
    if measurement.get("availability") != "measured":
        return _format_measurement(measurement)

    value = _require_mapping(measurement.get("value"), field_name="ast_distance.value")
    return "distance_to_seed_cpp={seed}, distance_to_roundtrip_cpp={roundtrip}".format(
        seed=value.get("distance_to_seed_cpp"),
        roundtrip=value.get("distance_to_roundtrip_cpp"),
    )


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
