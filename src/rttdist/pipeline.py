from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
from typing import Any, Callable, Protocol, Sequence, cast

from rttdist.artifacts import (
    CuratedProblemReference,
    build_legacy_run_directory,
    build_iteration_artifact_paths,
    build_run_directory,
    build_run_metadata,
    resolve_contract_path,
)
from rttdist.config import ExperimentConfig, reference_filename_for_language
from rttdist.corpus import ProblemCorpusEntry
from rttdist.exec import ExecutionBatchResult, ExecutionStatus, evaluate_source
from rttdist.failure_taxonomy import FailureRecord, FailureStatus
from rttdist.fixed_point import classify_cpp_history
from rttdist.lmstudio_client import (
    LMStudioClientError,
    LMStudioResponseParseError,
    LMStudioTranslationClient,
    SourceExtractionError,
    TranslationResult,
)
from rttdist.prompts import PROMPT_TEMPLATE_VERSION
from rttdist.run_state import build_manifest_checksums, plan_run_resume


class RTTLoopError(RuntimeError):
    pass


class TranslationClientProtocol(Protocol):
    def translate(
        self,
        *,
        problem_id: str,
        source_language: str,
        target_language: str,
        problem_statement: str,
        sample_input: str,
        sample_output: str,
        source_code: str,
        iteration_index: int,
        direction: str,
    ) -> TranslationResult: ...

    def translate_cpp_to_target(
        self,
        *,
        problem_id: str,
        target_language: str,
        problem_statement: str,
        sample_input: str,
        sample_output: str,
        source_code: str,
        iteration_index: int,
    ) -> TranslationResult: ...

    def translate_target_to_cpp(
        self,
        *,
        problem_id: str,
        source_language: str,
        problem_statement: str,
        sample_input: str,
        sample_output: str,
        source_code: str,
        iteration_index: int,
    ) -> TranslationResult: ...


class EvaluateSourceProtocol(Protocol):
    def __call__(
        self,
        *,
        language: str,
        source_path: Path,
        problem: ProblemCorpusEntry,
        workspace_root: Path,
        timeout_seconds: int,
    ) -> ExecutionBatchResult: ...


class TimestampProvider(Protocol):
    def __call__(self) -> datetime: ...


@dataclass(frozen=True)
class RTTRunResult:
    run_id: str
    problem_id: str
    target_language: str
    iteration_count: int
    final_record: FailureRecord
    run_manifest_path: Path
    run_directory: Path

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "problem_id": self.problem_id,
            "target_language": self.target_language,
            "iteration_count": self.iteration_count,
            "final_record": self.final_record.to_dict(),
            "run_manifest_path": self.run_manifest_path.as_posix(),
            "run_directory": self.run_directory.as_posix(),
        }


def run_rtt_loop(
    *,
    config: ExperimentConfig,
    run_id: str,
    problem: ProblemCorpusEntry,
    target_language: str,
    translation_client: TranslationClientProtocol | None = None,
    evaluate_source_fn: EvaluateSourceProtocol = evaluate_source,
    timestamp_provider: TimestampProvider | None = None,
    progress_logger: Callable[[str], None] | None = None,
) -> RTTRunResult:
    now = timestamp_provider or _utcnow
    configured_intermediates = config.target_languages
    if config.seed_language in configured_intermediates and target_language != config.seed_language:
        configured_intermediates = (target_language,)
    language_route = _build_language_route(
        seed_language=config.seed_language,
        intermediate_languages=configured_intermediates,
    )
    route_terminal_language = language_route[-2]
    route_key = "->".join(language_route)
    route_step_count = len(_build_route_steps(language_route))

    problem_reference = _build_curated_problem_reference(problem)
    metadata = build_run_metadata(
        run_id=run_id,
        problem=problem_reference,
        target_language=route_terminal_language,
        seed_language=config.seed_language,
        max_iterations=config.runtime.max_iterations,
    ).to_dict()
    metadata["language_route"] = list(language_route)
    metadata["route_key"] = route_key
    metadata["experiment_unit"] = "rtt_cycle"
    metadata["translation_count_per_cycle"] = route_step_count

    run_directory, run_manifest_path = _select_run_paths_for_resume(
        output_root=config.output_root,
        run_id=run_id,
        problem_id=problem.problem_id,
        seed_language=config.seed_language,
        target_language=route_terminal_language,
    )
    run_directory_relative = run_directory.relative_to(
        config.output_root.resolve()
    ).as_posix()
    run_manifest_relative = run_manifest_path.relative_to(
        config.output_root.resolve()
    ).as_posix()
    metadata["run_directory"] = run_directory_relative
    metadata["run_metadata_path"] = run_manifest_relative
    run_directory.mkdir(parents=True, exist_ok=True)
    metadata["seed_artifact_path"] = _seed_source_relative_path(
        output_root=config.output_root,
        run_directory=run_directory,
        seed_language=config.seed_language,
    )

    statement = problem.statement_path.read_text(encoding="utf-8").strip()
    sample_input = problem.fixture_pairs[0].input_path.read_text(encoding="utf-8").strip()
    sample_output = problem.fixture_pairs[0].output_path.read_text(encoding="utf-8").strip()
    seed_source = problem.seed_path.read_text(encoding="utf-8").rstrip()

    resume_plan = plan_run_resume(
        run_manifest_path=run_manifest_path,
        run_directory=run_directory,
        output_root=config.output_root,
        metadata=metadata,
        checksums=build_manifest_checksums(
            config=config,
            prompt_template_version=PROMPT_TEMPLATE_VERSION,
            seed_source=seed_source,
        ),
        seed_cpp_source=seed_source,
        created_at=_to_iso(now()),
    )
    manifest = resume_plan.manifest
    manifest_metadata = manifest.get("metadata")
    if not isinstance(manifest_metadata, dict):
        raise RTTLoopError("Run manifest metadata is missing or invalid.")
    manifest_metadata["language_route"] = list(language_route)
    manifest_metadata["route_key"] = route_key
    manifest_metadata["experiment_unit"] = "rtt_cycle"
    manifest_metadata["translation_count_per_cycle"] = route_step_count

    seed_artifact_path = _ensure_seed_source_artifact(
        output_root=config.output_root,
        run_directory=run_directory,
        seed_cpp_source=seed_source,
        seed_language=config.seed_language,
    )
    if manifest_metadata.get("seed_artifact_path") != seed_artifact_path:
        manifest_metadata["seed_artifact_path"] = seed_artifact_path

    current_seed_source = resume_plan.current_seed_source
    seed_source_history = [seed_source, *resume_plan.seed_source_history]
    previous_status = resume_plan.previous_status
    final_record: FailureRecord | None = resume_plan.final_record

    if final_record is not None:
        _write_json(run_manifest_path, manifest)
        return RTTRunResult(
            run_id=run_id,
            problem_id=problem.problem_id,
            target_language=route_terminal_language,
            iteration_count=len(manifest["iterations"]),
            final_record=final_record,
            run_manifest_path=run_manifest_path,
            run_directory=run_directory,
        )

    client = translation_client or _build_translation_client(config)
    _emit_progress(
        progress_logger,
        f"{problem.problem_id}: RTT route {route_key} ({route_step_count} translations per cycle)",
    )

    for iteration_index in range(
        resume_plan.start_iteration, config.runtime.max_iterations + 1
    ):
        iteration_input_seed_source = current_seed_source
        iteration_paths = build_iteration_artifact_paths(
            run_id=run_id,
            problem_id=problem.problem_id,
            target_language=route_terminal_language,
            seed_language=config.seed_language,
            iteration_index=iteration_index,
        )
        iteration_started_at = _to_iso(now())
        iteration_directory = resolve_contract_path(
            config.output_root, iteration_paths.iteration_directory
        )
        route_steps = _build_route_steps(language_route)
        translation_count_per_cycle = len(route_steps)
        attempted_translation_count = 0
        completed_translation_count = 0
        failed_translation_count = 0
        translation_steps: list[dict[str, Any]] = []
        conversion_log_relative_path = (
            Path(iteration_paths.iteration_directory) / "conversion.log"
        ).as_posix()
        conversion_log_lines = [
            f"problem_id={problem.problem_id}",
            f"iteration={iteration_index}",
            f"language_route={route_key}",
            f"translation_count_per_cycle={translation_count_per_cycle}",
        ]
        _emit_progress(
            progress_logger,
            f"{problem.problem_id}: iteration {iteration_index} starts; "
            f"expecting {translation_count_per_cycle} translations",
        )
        llm_request_payload: dict[str, Any] = {}
        llm_response_payload: dict[str, Any] = {}
        execution_payload: dict[str, Any] = {"steps": [], "target": None, "roundtrip_cpp": None}
        metric_payload: dict[str, Any] = {
            "rtt_distance": None,
            "convergence": {"seed_state": "continue", "overall": "continue"},
            "convergence_status": "continue",
            "language_route": list(language_route),
        }
        iteration_record: FailureRecord | None = None
        route_step_records: list[dict[str, Any]] = []
        produced_by_language: dict[str, str] = {}
        current_source = current_seed_source
        roundtrip_source = ""
        final_intermediate_source = ""

        for step_index, source_language, next_language in route_steps:
            step_key = _route_step_key(step_index, source_language, next_language)
            llm_request_payload[step_key] = None
            llm_response_payload[step_key] = None
            source_path = _route_step_source_path(
                output_root=config.output_root,
                iteration_directory=iteration_directory,
                iteration_paths=iteration_paths,
                step_index=step_index,
                language=next_language,
                is_final_seed_step=next_language == config.seed_language,
                is_terminal_intermediate=step_index == len(route_steps) - 1,
            )
            relative_source_path = source_path.relative_to(config.output_root.resolve()).as_posix()
            direction = _legacy_direction_for_step(
                step_index=step_index,
                step_count=len(route_steps),
                source_language=source_language,
                target_language=next_language,
                seed_language=config.seed_language,
            )
            step_metric = {
                "step_index": step_index,
                "source_language": source_language,
                "target_language": next_language,
                "direction": step_key,
                "status": "started",
                "source_path": relative_source_path,
            }
            translation_steps.append(step_metric)
            attempted_translation_count += 1
            _append_conversion_log(
                conversion_log_lines,
                f"step {step_index}/{translation_count_per_cycle} START {source_language}->{next_language}",
            )
            _emit_progress(
                progress_logger,
                f"{problem.problem_id}: iteration {iteration_index} "
                f"step {step_index}/{translation_count_per_cycle} "
                f"{source_language}->{next_language} translating",
            )
            try:
                translation = _translate_with_explicit_languages(
                    client,
                    problem_id=problem.problem_id,
                    source_language=source_language,
                    target_language=next_language,
                    problem_statement=statement,
                    sample_input=sample_input,
                    sample_output=sample_output,
                    source_code=current_source,
                    iteration_index=iteration_index,
                    direction=direction,
                )
                llm_request_payload[step_key] = translation.request.to_dict()
                llm_response_payload[step_key] = translation.response.to_dict()
                if step_index == 1:
                    llm_request_payload["cpp_to_target"] = translation.request.to_dict()
                    llm_response_payload["cpp_to_target"] = translation.response.to_dict()
                if next_language == config.seed_language:
                    llm_request_payload["target_to_cpp"] = translation.request.to_dict()
                    llm_response_payload["target_to_cpp"] = translation.response.to_dict()
                translated_source = translation.extracted_source.rstrip()
                _write_text(source_path, f"{translated_source}\n")
                completed_translation_count += 1
                step_metric["status"] = "translated"
                step_metric["output_chars"] = len(translated_source)
                _append_conversion_log(
                    conversion_log_lines,
                    f"step {step_index}/{translation_count_per_cycle} TRANSLATED "
                    f"{source_language}->{next_language} chars={len(translated_source)}",
                )
            except Exception as exc:
                _capture_translation_debug_payloads(
                    exc=exc,
                    request_slot=step_key,
                    response_slot=step_key,
                    request_payloads=llm_request_payload,
                    response_payloads=llm_response_payload,
                )
                iteration_record = _failure_from_translation_exception(
                    exc=exc,
                    iteration_index=iteration_index,
                    stage=f"{step_key}_translation",
                )
                failed_translation_count += 1
                step_metric["status"] = "translation_failed"
                step_metric["error"] = str(exc)
                _append_conversion_log(
                    conversion_log_lines,
                    f"step {step_index}/{translation_count_per_cycle} TRANSLATION_FAILED "
                    f"{source_language}->{next_language}: {exc}",
                )
                _emit_progress(
                    progress_logger,
                    f"{problem.problem_id}: iteration {iteration_index} "
                    f"step {step_index}/{translation_count_per_cycle} "
                    f"{source_language}->{next_language} translation failed",
                )
                translated_source = ""

            route_step_record = {
                "step_index": step_index,
                "source_language": source_language,
                "target_language": next_language,
                "direction": step_key,
                "source_path": relative_source_path,
                "request_key": step_key,
                "response_key": step_key,
                "execution_key": None,
            }
            route_step_records.append(route_step_record)

            if iteration_record is not None:
                break

            execution_key = "roundtrip_cpp" if next_language == config.seed_language else f"step_{step_index:03d}_{next_language}"
            route_step_record["execution_key"] = execution_key
            try:
                evaluation = evaluate_source_fn(
                    language=next_language,
                    source_path=source_path,
                    problem=problem,
                    workspace_root=run_directory,
                    timeout_seconds=config.runtime.timeout_seconds,
                )
                execution_result = _execution_batch_to_dict(
                    result=evaluation,
                    output_root=config.output_root,
                    iteration_paths=iteration_paths,
                    stage_name=execution_key,
                )
                execution_payload[execution_key] = execution_result
                execution_payload["steps"].append(execution_result)
            except Exception as exc:
                iteration_record = _failure_from_runtime_exception(
                    exc=exc,
                    iteration_index=iteration_index,
                    stage=f"{step_key}_execution",
                    message="RTT route step evaluation failed unexpectedly.",
                )
                step_metric["status"] = "evaluation_failed"
                step_metric["error"] = str(exc)
                _append_conversion_log(
                    conversion_log_lines,
                    f"step {step_index}/{translation_count_per_cycle} EVALUATION_FAILED "
                    f"{source_language}->{next_language}: {exc}",
                )
                break

            step_failure = _failure_from_execution_result(
                result=evaluation,
                iteration_index=iteration_index,
                stage=f"{step_key}_execution",
            )
            if step_failure is not None:
                iteration_record = step_failure
                step_metric["status"] = "evaluation_failed"
                step_metric["evaluation_status"] = evaluation.status.value
                _append_conversion_log(
                    conversion_log_lines,
                    f"step {step_index}/{translation_count_per_cycle} EVALUATION_FAILED "
                    f"{source_language}->{next_language}: {evaluation.status.value}",
                )
                break

            step_metric["status"] = "completed"
            step_metric["evaluation_status"] = evaluation.status.value
            _append_conversion_log(
                conversion_log_lines,
                f"step {step_index}/{translation_count_per_cycle} COMPLETE "
                f"{source_language}->{next_language}",
            )
            _emit_progress(
                progress_logger,
                f"{problem.problem_id}: iteration {iteration_index} "
                f"step {step_index}/{translation_count_per_cycle} "
                f"{source_language}->{next_language} complete",
            )

            current_source = translated_source
            produced_by_language[next_language] = translated_source
            if next_language == config.seed_language:
                roundtrip_source = translated_source
            else:
                final_intermediate_source = translated_source
                execution_payload["target"] = execution_payload[execution_key]

        if iteration_record is None:
            seed_source_history.append(roundtrip_source)
            convergence_status = classify_cpp_history(seed_source_history)
            completed_cycles = len(seed_source_history) - 1
            metric_payload = {
                "rtt_distance": {
                    "availability": "measured",
                    "value": completed_cycles,
                    "unit": "completed_full_routes",
                    "definition": "one route = " + route_key,
                },
                "convergence": {
                    "seed_state": convergence_status,
                    "overall": convergence_status,
                },
                "convergence_status": convergence_status,
                "language_route": list(language_route),
            }
            if convergence_status == "fixed_point":
                iteration_record = FailureRecord(
                    status=FailureStatus.SUCCESS,
                    stage="convergence",
                    iteration_index=iteration_index,
                    message="Fixed point reached after a complete RTT language route.",
                    details={
                        "convergence_status": "fixed_point",
                        "convergence": metric_payload["convergence"],
                        "language_route": list(language_route),
                    },
                )
            elif convergence_status == "oscillation":
                iteration_record = FailureRecord(
                    status=FailureStatus.OSCILLATION,
                    stage="convergence",
                    iteration_index=iteration_index,
                    message="Detected oscillation before RTT route fixed point convergence.",
                    details={
                        "convergence_status": "oscillation",
                        "convergence": metric_payload["convergence"],
                        "language_route": list(language_route),
                    },
                )
            else:
                iteration_record = FailureRecord(
                    status=FailureStatus.SUCCESS,
                    stage="iteration",
                    iteration_index=iteration_index,
                    message="Full RTT route completed; convergence still in progress.",
                    details={
                        "convergence_status": "continue",
                        "convergence": metric_payload["convergence"],
                        "language_route": list(language_route),
                    },
                )
                current_seed_source = roundtrip_source

        if iteration_record is None:
            raise RTTLoopError("Internal error: final record was not produced.")

        input_seed_source_path = resolve_contract_path(
            config.output_root, iteration_paths.input_seed_source_path
        )
        translated_source_path = resolve_contract_path(
            config.output_root, iteration_paths.translated_source_path
        )
        roundtrip_source_path = resolve_contract_path(
            config.output_root, iteration_paths.roundtrip_source_path
        )
        compile_log_path = resolve_contract_path(
            config.output_root, iteration_paths.compile_log_path
        )
        execution_result_path = resolve_contract_path(
            config.output_root, iteration_paths.execution_result_path
        )
        metrics_path = resolve_contract_path(config.output_root, iteration_paths.metrics_path)
        request_path = resolve_contract_path(config.output_root, iteration_paths.llm_request_path)
        response_path = resolve_contract_path(config.output_root, iteration_paths.llm_response_path)
        iteration_metadata_path = resolve_contract_path(
            config.output_root, iteration_paths.iteration_metadata_path
        )

        _write_text(input_seed_source_path, f"{iteration_input_seed_source}\n")
        _write_text(translated_source_path, f"{final_intermediate_source}\n")
        _write_text(roundtrip_source_path, f"{roundtrip_source}\n")
        _write_json(request_path, _fill_missing_payloads(llm_request_payload, "request unavailable"))
        _write_json(response_path, _fill_missing_payloads(llm_response_payload, "response unavailable"))
        metric_payload.update(
            _build_translation_count_metrics(
                translation_count_per_cycle=translation_count_per_cycle,
                attempted_translation_count=attempted_translation_count,
                completed_translation_count=completed_translation_count,
                failed_translation_count=failed_translation_count,
                translation_steps=translation_steps,
                conversion_log_path=conversion_log_relative_path,
            )
        )
        conversion_log_path = resolve_contract_path(
            config.output_root, conversion_log_relative_path
        )
        _append_conversion_log(
            conversion_log_lines,
            "summary "
            f"attempted={attempted_translation_count} "
            f"completed={completed_translation_count} "
            f"failed={failed_translation_count}",
        )
        _write_compile_log(
            output_root=config.output_root,
            compile_log_path=compile_log_path,
            execution_payload=execution_payload,
        )
        _write_json(execution_result_path, execution_payload)
        _write_json(metrics_path, metric_payload)
        _write_text(conversion_log_path, "\n".join(conversion_log_lines) + "\n")

        iteration_status = iteration_record.status
        if (
            iteration_index == config.runtime.max_iterations
            and iteration_record.status == FailureStatus.SUCCESS
            and _overall_convergence_status(iteration_record) == "continue"
        ):
            iteration_record = FailureRecord(
                status=FailureStatus.MAX_ITER_NO_CONVERGENCE,
                stage="convergence",
                iteration_index=iteration_index,
                message="Iteration cap reached before RTT route convergence.",
                details={
                    "max_iterations": config.runtime.max_iterations,
                    "convergence_status": "continue",
                    "convergence": metric_payload["convergence"],
                    "seed_history_length": len(seed_source_history),
                    "language_route": list(language_route),
                },
            )
            iteration_status = iteration_record.status

        iteration_payload = {
            "iteration_index": iteration_index,
            "started_at": iteration_started_at,
            "ended_at": _to_iso(now()),
            "result": iteration_record.to_dict(),
            "artifact_paths": iteration_paths.to_dict(),
            "route_steps": route_step_records,
            "translation_count_per_cycle": translation_count_per_cycle,
            "attempted_translation_count": attempted_translation_count,
            "completed_translation_count": completed_translation_count,
            "failed_translation_count": failed_translation_count,
            "conversion_log_path": conversion_log_relative_path,
        }
        _write_json(iteration_metadata_path, iteration_payload)

        manifest["iterations"].append(iteration_payload)
        manifest["status_transitions"].append(
            {
                "timestamp": _to_iso(now()),
                "problem_id": problem.problem_id,
                "seed_language": config.seed_language,
                "target_language": route_terminal_language,
                "route_key": route_key,
                "iteration_index": iteration_index,
                "from_status": previous_status,
                "to_status": iteration_status.value,
            }
        )
        previous_status = iteration_status.value
        manifest["metadata"]["updated_at"] = _to_iso(now())
        manifest["metadata"]["ended_at"] = None
        manifest["final"] = None
        _write_json(run_manifest_path, manifest)

        should_stop = iteration_status in {
            FailureStatus.API_ERROR,
            FailureStatus.PARSE_ERROR,
            FailureStatus.COMPILE_ERROR,
            FailureStatus.RUNTIME_ERROR,
            FailureStatus.WRONG_ANSWER,
            FailureStatus.TIMEOUT,
            FailureStatus.OSCILLATION,
            FailureStatus.MAX_ITER_NO_CONVERGENCE,
        } or (
            iteration_status == FailureStatus.SUCCESS
            and _overall_convergence_status(iteration_record) == "fixed_point"
        )
        final_record = iteration_record
        if should_stop:
            break

    if final_record is None:
        raise RTTLoopError("Internal error: loop completed without a final record.")

    manifest["final"] = final_record.to_dict()
    manifest["metadata"]["ended_at"] = _to_iso(now())
    manifest["metadata"]["updated_at"] = manifest["metadata"]["ended_at"]
    _write_json(run_manifest_path, manifest)

    return RTTRunResult(
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language=route_terminal_language,
        iteration_count=len(manifest["iterations"]),
        final_record=final_record,
        run_manifest_path=run_manifest_path,
        run_directory=run_directory,
    )


def run_pipeline_service(
    *,
    config: ExperimentConfig,
    run_id: str,
    corpus_entries: Sequence[ProblemCorpusEntry],
    translation_client_factory: Callable[[], TranslationClientProtocol] | None = None,
    evaluate_source_fn: EvaluateSourceProtocol = evaluate_source,
    timestamp_provider: TimestampProvider | None = None,
    progress_logger: Callable[[str], None] | None = None,
) -> tuple[RTTRunResult, ...]:
    results: list[RTTRunResult] = []
    route_terminal_language = config.target_languages[-1]
    for problem in corpus_entries:
        client = (
            translation_client_factory()
            if translation_client_factory is not None
            else None
        )
        results.append(
            run_rtt_loop(
                config=config,
                run_id=run_id,
                problem=problem,
                target_language=route_terminal_language,
                translation_client=client,
                evaluate_source_fn=evaluate_source_fn,
                timestamp_provider=timestamp_provider,
                progress_logger=progress_logger,
            )
        )
    return tuple(results)


def _build_translation_count_metrics(
    *,
    translation_count_per_cycle: int,
    attempted_translation_count: int,
    completed_translation_count: int,
    failed_translation_count: int,
    translation_steps: Sequence[dict[str, Any]],
    conversion_log_path: str,
) -> dict[str, Any]:
    return {
        "translation_count_per_cycle": translation_count_per_cycle,
        "attempted_translation_count": attempted_translation_count,
        "completed_translation_count": completed_translation_count,
        "failed_translation_count": failed_translation_count,
        "translation_count": {
            "per_cycle": translation_count_per_cycle,
            "attempted": attempted_translation_count,
            "completed": completed_translation_count,
            "failed": failed_translation_count,
            "unit": "translations",
            "definition": "number of source->target conversions in one complete RTT language route",
        },
        "translation_steps": [dict(step) for step in translation_steps],
        "conversion_log_path": conversion_log_path,
    }


def _append_conversion_log(lines: list[str], message: str) -> None:
    lines.append(message)


def _emit_progress(
    progress_logger: Callable[[str], None] | None, message: str
) -> None:
    if progress_logger is not None:
        progress_logger(message)


def _build_translation_client(config: ExperimentConfig) -> TranslationClientProtocol:
    if config.provider == "lmstudio":
        return LMStudioTranslationClient(
            model=config.lmstudio.model,
            temperature=config.lmstudio.temperature,
            host=config.lmstudio.host,
        )
    raise RTTLoopError(f"Unsupported translation provider: {config.provider}")


def _build_language_route(
    *, seed_language: str, intermediate_languages: Sequence[str]
) -> tuple[str, ...]:
    route = (seed_language, *tuple(intermediate_languages), seed_language)
    if len(route) < 3:
        raise RTTLoopError("RTT route requires at least one intermediate language.")
    for left, right in zip(route, route[1:]):
        if left == right:
            raise RTTLoopError(
                f"RTT route contains adjacent duplicate language: {left!r}."
            )
    return route


def _build_route_steps(language_route: Sequence[str]) -> list[tuple[int, str, str]]:
    return [
        (index, source_language, target_language)
        for index, (source_language, target_language) in enumerate(
            zip(language_route, language_route[1:]), start=1
        )
    ]


def _route_step_key(step_index: int, source_language: str, target_language: str) -> str:
    return f"step_{step_index:03d}_{source_language}_to_{target_language}"



def _legacy_direction_for_step(
    *,
    step_index: int,
    step_count: int,
    source_language: str,
    target_language: str,
    seed_language: str,
) -> str:
    if step_index == 1:
        return "seed_to_target"
    if step_index == step_count and target_language == seed_language:
        return "target_to_roundtrip_cpp"
    return _route_step_key(step_index, source_language, target_language)


def _route_step_source_path(
    *,
    output_root: Path,
    iteration_directory: Path,
    iteration_paths: Any,
    step_index: int,
    language: str,
    is_final_seed_step: bool,
    is_terminal_intermediate: bool,
) -> Path:
    if is_final_seed_step:
        return resolve_contract_path(output_root, iteration_paths.roundtrip_source_path)
    if is_terminal_intermediate:
        return resolve_contract_path(output_root, iteration_paths.translated_source_path)
    return iteration_directory / "steps" / f"step-{step_index:03d}{_source_extension(language)}"


def _source_extension(language: str) -> str:
    extension_by_language = {"cpp": ".cpp", "c": ".c", "java": ".java", "python": ".py"}
    try:
        return extension_by_language[language]
    except KeyError as exc:
        raise RTTLoopError(f"Unsupported route language: {language!r}.") from exc


def _fill_missing_payloads(payloads: dict[str, Any], message: str) -> dict[str, Any]:
    return {
        key: ({"error": message} if value is None else value)
        for key, value in payloads.items()
    }


def _build_curated_problem_reference(
    problem: ProblemCorpusEntry,
) -> CuratedProblemReference:
    sample_pair = problem.fixture_pairs[0]
    return CuratedProblemReference(
        problem_id=problem.problem_id,
        statement_path=problem.statement_path.as_posix(),
        fixture_input_path=sample_pair.input_path.as_posix(),
        fixture_output_path=sample_pair.output_path.as_posix(),
        seed_source_path=problem.seed_path.as_posix(),
    )


def _failure_from_execution_result(
    *,
    result: ExecutionBatchResult,
    iteration_index: int,
    stage: str,
) -> FailureRecord | None:
    if result.status == ExecutionStatus.SUCCESS:
        return None

    if result.status == ExecutionStatus.COMPILE_ERROR:
        status = FailureStatus.COMPILE_ERROR
    elif result.status == ExecutionStatus.RUNTIME_ERROR:
        status = FailureStatus.RUNTIME_ERROR
    elif result.status == ExecutionStatus.TIMEOUT:
        status = FailureStatus.TIMEOUT
    else:
        status = FailureStatus.WRONG_ANSWER

    return FailureRecord(
        status=status,
        stage=stage,
        iteration_index=iteration_index,
        message=result.message,
        details={
            "execution_status": result.status.value,
            "compile_log_path": result.compile_log_path.as_posix(),
            "work_directory": result.work_directory.as_posix(),
        },
    )


def _execution_batch_to_dict(
    *,
    result: ExecutionBatchResult,
    output_root: Path,
    iteration_paths: Any,
    stage_name: str,
) -> dict[str, Any]:
    evidence_root = Path(iteration_paths.iteration_directory) / "evidence" / stage_name
    compile_log_path = _snapshot_log_path(
        output_root=output_root,
        source_path=result.compile_log_path,
        destination_relative_path=evidence_root / "compile.log",
        fallback_text="compile log unavailable\n",
    )

    fixture_payloads: list[dict[str, Any]] = []
    for item in result.fixture_results:
        fixture_root = evidence_root / "fixtures" / item.fixture_stem
        stdout_log_path = _snapshot_text(
            output_root=output_root,
            destination_relative_path=fixture_root / "stdout.log",
            text=item.stdout,
        )
        stderr_log_path = _snapshot_text(
            output_root=output_root,
            destination_relative_path=fixture_root / "stderr.log",
            text=item.stderr,
        )
        fixture_payloads.append(
            {
                "fixture_stem": item.fixture_stem,
                "input_path": item.input_path.as_posix(),
                "output_path": item.output_path.as_posix(),
                "status": item.status.value,
                "stdout": item.stdout,
                "stderr": item.stderr,
                "exit_code": item.exit_code,
                "duration_seconds": item.duration_seconds,
                "stdout_log_path": stdout_log_path,
                "stderr_log_path": stderr_log_path,
                "message": item.message,
            }
        )

    return {
        "stage_name": stage_name,
        "language": result.language,
        "problem_id": result.problem_id,
        "status": result.status.value,
        "work_directory": result.work_directory.as_posix(),
        "compile_log_path": compile_log_path,
        "message": result.message,
        "compile_result": None
        if result.compile_result is None
        else {
            "command": list(result.compile_result.command),
            "stdout": result.compile_result.stdout,
            "stderr": result.compile_result.stderr,
            "exit_code": result.compile_result.exit_code,
            "timed_out": result.compile_result.timed_out,
            "duration_seconds": result.compile_result.duration_seconds,
        },
        "fixture_results": fixture_payloads,
    }


def _write_compile_log(
    *,
    output_root: Path,
    compile_log_path: Path,
    execution_payload: dict[str, Any],
) -> None:
    sections: list[str] = []
    for step in execution_payload.get("steps", []):
        if not isinstance(step, dict):
            continue
        stage = str(step.get("stage_name") or step.get("language") or "step")
        sections.append(f"[{stage}]\n{_extract_compile_log_text(step, output_root=output_root)}")
    if not sections:
        sections.append("[rtt]\ncompile log unavailable")
    _write_text(compile_log_path, "\n".join(sections) + "\n")


def _extract_compile_log_text(
    execution_payload: dict[str, Any] | None, *, output_root: Path
) -> str:
    if execution_payload is None:
        return "compile log unavailable"

    compile_log_path = execution_payload.get("compile_log_path")
    if not isinstance(compile_log_path, str) or not compile_log_path:
        return "compile log unavailable"

    path = Path(compile_log_path)
    if not path.is_absolute():
        path = resolve_contract_path(output_root, compile_log_path)
    if not path.is_file():
        return "compile log unavailable"
    return path.read_text(encoding="utf-8").rstrip()


def _failure_from_translation_exception(
    *,
    exc: Exception,
    iteration_index: int,
    stage: str,
) -> FailureRecord:
    if isinstance(
        exc,
        (
            LMStudioResponseParseError,
            SourceExtractionError,
        ),
    ):
        status = FailureStatus.PARSE_ERROR
        message = "Translation response parsing failed."
    elif isinstance(exc, LMStudioClientError):
        status = FailureStatus.API_ERROR
        message = "Translation API request failed."
    else:
        status = FailureStatus.API_ERROR
        message = "Translation step failed."

    return FailureRecord(
        status=status,
        stage=stage,
        iteration_index=iteration_index,
        message=message,
        details={
            "error_type": type(exc).__name__,
            "error": str(exc),
        },
    )


def _capture_translation_debug_payloads(
    *,
    exc: Exception,
    request_slot: str,
    response_slot: str,
    request_payloads: dict[str, Any],
    response_payloads: dict[str, Any],
) -> None:
    request_payload = getattr(exc, "request_payload", None)
    response_payload = getattr(exc, "response_payload", None)
    if isinstance(request_payload, dict):
        request_payloads[request_slot] = request_payload
    if isinstance(response_payload, dict):
        response_payloads[response_slot] = response_payload


def _failure_from_runtime_exception(
    *,
    exc: Exception,
    iteration_index: int,
    stage: str,
    message: str,
) -> FailureRecord:
    return FailureRecord(
        status=FailureStatus.RUNTIME_ERROR,
        stage=stage,
        iteration_index=iteration_index,
        message=message,
        details={
            "error_type": type(exc).__name__,
            "error": str(exc),
        },
    )


def _overall_convergence_status(record: FailureRecord) -> str | None:
    convergence = record.details.get("convergence")
    if isinstance(convergence, dict):
        overall = convergence.get("overall")
        if isinstance(overall, str) and overall.strip():
            return overall.strip()
    value = record.details.get("convergence_status")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _translate_with_explicit_languages(
    client: TranslationClientProtocol,
    *,
    problem_id: str,
    source_language: str,
    target_language: str,
    problem_statement: str,
    sample_input: str,
    sample_output: str,
    source_code: str,
    iteration_index: int,
    direction: str,
) -> TranslationResult:
    translate = getattr(client, "translate", None)
    if callable(translate):
        return cast(
            TranslationResult,
            translate(
                problem_id=problem_id,
                source_language=source_language,
                target_language=target_language,
                problem_statement=problem_statement,
                sample_input=sample_input,
                sample_output=sample_output,
                source_code=source_code,
                iteration_index=iteration_index,
                direction=direction,
            ),
        )

    if source_language == "cpp" and hasattr(client, "translate_cpp_to_target"):
        return client.translate_cpp_to_target(
            problem_id=problem_id,
            target_language=target_language,
            problem_statement=problem_statement,
            sample_input=sample_input,
            sample_output=sample_output,
            source_code=source_code,
            iteration_index=iteration_index,
        )
    if target_language == "cpp" and hasattr(client, "translate_target_to_cpp"):
        return client.translate_target_to_cpp(
            problem_id=problem_id,
            source_language=source_language,
            problem_statement=problem_statement,
            sample_input=sample_input,
            sample_output=sample_output,
            source_code=source_code,
            iteration_index=iteration_index,
        )

    raise RTTLoopError(
        "Translation client must support explicit source/target language translation."
    )


def _snapshot_log_path(
    *,
    output_root: Path,
    source_path: Path,
    destination_relative_path: Path,
    fallback_text: str,
) -> str:
    destination_path = resolve_contract_path(
        output_root, destination_relative_path.as_posix()
    )
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    if source_path.is_file():
        shutil.copyfile(source_path, destination_path)
    else:
        destination_path.write_text(fallback_text, encoding="utf-8")
    return destination_relative_path.as_posix()


def _snapshot_text(
    *,
    output_root: Path,
    destination_relative_path: Path,
    text: str,
) -> str:
    destination_path = resolve_contract_path(
        output_root, destination_relative_path.as_posix()
    )
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    destination_path.write_text(text, encoding="utf-8")
    return destination_relative_path.as_posix()


def _ensure_seed_source_artifact(
    *,
    output_root: Path,
    run_directory: Path,
    seed_cpp_source: str,
    seed_language: str,
) -> str:
    seed_relative_path = _seed_source_relative_path(
        output_root=output_root,
        run_directory=run_directory,
        seed_language=seed_language,
    )
    seed_path = resolve_contract_path(Path(output_root).resolve(), seed_relative_path)
    seed_path.parent.mkdir(parents=True, exist_ok=True)
    if not seed_path.is_file():
        _write_text(seed_path, f"{seed_cpp_source}\n")
    return seed_relative_path


def _seed_source_relative_path(
    *, output_root: Path, run_directory: Path, seed_language: str
) -> str:
    normalized_output_root = Path(output_root).resolve()
    normalized_run_directory = Path(run_directory).resolve()
    try:
        run_relative = normalized_run_directory.relative_to(normalized_output_root)
    except ValueError as exc:
        raise RTTLoopError(
            "Run directory must be contained under output root."
        ) from exc

    return (
        run_relative / "seed" / reference_filename_for_language(seed_language)
    ).as_posix()


def _select_run_paths_for_resume(
    *,
    output_root: Path,
    run_id: str,
    problem_id: str,
    seed_language: str,
    target_language: str,
) -> tuple[Path, Path]:
    normalized_output_root = Path(output_root).resolve()

    v2_relative_run_directory = build_run_directory(
        run_id,
        problem_id,
        target_language,
        seed_language,
    ).as_posix()
    v2_run_directory = resolve_contract_path(
        normalized_output_root, v2_relative_run_directory
    )
    v2_manifest_path = resolve_contract_path(
        normalized_output_root,
        (Path(v2_relative_run_directory) / "run.json").as_posix(),
    )

    legacy_relative_run_directory = build_legacy_run_directory(
        run_id,
        problem_id,
        target_language,
    ).as_posix()
    legacy_run_directory = resolve_contract_path(
        normalized_output_root,
        legacy_relative_run_directory,
    )
    legacy_manifest_path = resolve_contract_path(
        normalized_output_root,
        (Path(legacy_relative_run_directory) / "run.json").as_posix(),
    )

    if v2_manifest_path.is_file() or (v2_run_directory / "iterations").is_dir():
        return v2_run_directory, v2_manifest_path
    if legacy_manifest_path.is_file() or (legacy_run_directory / "iterations").is_dir():
        return legacy_run_directory, legacy_manifest_path
    return v2_run_directory, v2_manifest_path


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            default=_json_fallback,
        ),
        encoding="utf-8",
    )


def _json_fallback(value: object) -> object:
    if isinstance(value, (set, frozenset)):
        return sorted(str(item) for item in value)
    return str(value)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _to_iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
