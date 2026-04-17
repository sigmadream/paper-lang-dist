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
from rttdist.embedding import (
    EmbeddedSource,
    EmbeddingProvider,
    EmbeddingProviderError,
    cosine_similarity,
    hash_source_text,
)
from rttdist.exec import ExecutionBatchResult, ExecutionStatus, evaluate_source
from rttdist.failure_taxonomy import FailureRecord, FailureStatus
from rttdist.fixed_point import classify_dual_cpp_histories, compute_residual_similarity
from rttdist.ollama_client import (
    OllamaClientError,
    OllamaResponseParseError,
    OllamaTranslationClient,
    SourceExtractionError as OllamaSourceExtractionError,
)
from rttdist.openai_client import (
    OpenAIClientError,
    OpenAIFinalSimilarityProvider,
    OpenAIResponseParseError,
    OpenAITranslationClient,
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
    final_similarity_provider: EmbeddingProvider | None = None,
    evaluate_source_fn: EvaluateSourceProtocol = evaluate_source,
    timestamp_provider: TimestampProvider | None = None,
) -> RTTRunResult:
    now = timestamp_provider or _utcnow

    problem_reference = _build_curated_problem_reference(problem)
    metadata = build_run_metadata(
        run_id=run_id,
        problem=problem_reference,
        target_language=target_language,
        seed_language=config.seed_language,
        max_iterations=config.runtime.max_iterations,
    ).to_dict()
    run_directory, run_manifest_path = _select_run_paths_for_resume(
        output_root=config.output_root,
        run_id=run_id,
        problem_id=problem.problem_id,
        seed_language=config.seed_language,
        target_language=target_language,
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
    sample_input = (
        problem.fixture_pairs[0].input_path.read_text(encoding="utf-8").strip()
    )
    sample_output = (
        problem.fixture_pairs[0].output_path.read_text(encoding="utf-8").strip()
    )
    seed_cpp_source = problem.seed_path.read_text(encoding="utf-8").rstrip()

    resume_plan = plan_run_resume(
        run_manifest_path=run_manifest_path,
        run_directory=run_directory,
        output_root=config.output_root,
        metadata=metadata,
        checksums=build_manifest_checksums(
            config=config,
            prompt_template_version=PROMPT_TEMPLATE_VERSION,
            seed_source=seed_cpp_source,
        ),
        seed_cpp_source=seed_cpp_source,
        created_at=_to_iso(now()),
    )
    manifest = resume_plan.manifest
    manifest_metadata = manifest.get("metadata")
    if not isinstance(manifest_metadata, dict):
        raise RTTLoopError("Run manifest metadata is missing or invalid.")
    seed_artifact_path = _ensure_seed_source_artifact(
        output_root=config.output_root,
        run_directory=run_directory,
        seed_cpp_source=seed_cpp_source,
        seed_language=config.seed_language,
    )
    seed_artifact_path_changed = (
        manifest_metadata.get("seed_artifact_path") != seed_artifact_path
    )
    if seed_artifact_path_changed:
        manifest_metadata["seed_artifact_path"] = seed_artifact_path

    current_seed_source = resume_plan.current_seed_source
    seed_source_history = list(resume_plan.seed_source_history)
    target_source_history = list(resume_plan.target_source_history)
    previous_status = resume_plan.previous_status
    final_record: FailureRecord | None = resume_plan.final_record

    if final_record is not None:
        _persist_final_similarity_artifact(
            config=config,
            run_directory=run_directory,
            manifest=manifest,
            final_similarity_provider=final_similarity_provider
            or _build_final_similarity_provider(config),
            seed_cpp_source=seed_cpp_source,
            now=now,
        )
        if seed_artifact_path_changed:
            _write_json(run_manifest_path, manifest)
        return RTTRunResult(
            run_id=run_id,
            problem_id=problem.problem_id,
            target_language=target_language,
            iteration_count=len(manifest["iterations"]),
            final_record=final_record,
            run_manifest_path=run_manifest_path,
            run_directory=run_directory,
        )

    client = translation_client or _build_translation_client(config)

    for iteration_index in range(
        resume_plan.start_iteration, config.runtime.max_iterations + 1
    ):
        iteration_input_seed_source = current_seed_source
        iteration_paths = build_iteration_artifact_paths(
            run_id=run_id,
            problem_id=problem.problem_id,
            target_language=target_language,
            seed_language=config.seed_language,
            iteration_index=iteration_index,
        )
        iteration_started_at = _to_iso(now())

        openai_request_payload: dict[str, Any] = {
            "cpp_to_target": None,
            "target_to_cpp": None,
        }
        openai_response_payload: dict[str, Any] = {
            "cpp_to_target": None,
            "target_to_cpp": None,
        }
        execution_payload: dict[str, Any] = {
            "target": None,
            "roundtrip_cpp": None,
        }
        metric_payload: dict[str, Any] = {
            "residual_similarity": None,
            "convergence": {
                "seed_state": "continue",
                "target_state": "continue",
                "overall": "continue",
            },
            "convergence_status": "continue",
        }
        iteration_record: FailureRecord | None = None

        target_source = ""
        roundtrip_cpp_source = ""
        target_evaluation: ExecutionBatchResult | None = None
        roundtrip_evaluation: ExecutionBatchResult | None = None

        try:
            cpp_to_target = _translate_with_explicit_languages(
                client,
                problem_id=problem.problem_id,
                source_language=config.seed_language,
                target_language=target_language,
                problem_statement=statement,
                sample_input=sample_input,
                sample_output=sample_output,
                source_code=current_seed_source,
                iteration_index=iteration_index,
                direction="seed_to_target",
            )
            openai_request_payload["cpp_to_target"] = cpp_to_target.request.to_dict()
            openai_response_payload["cpp_to_target"] = cpp_to_target.response.to_dict()
            target_source = cpp_to_target.extracted_source.rstrip()
        except Exception as exc:
            _capture_translation_debug_payloads(
                exc=exc,
                request_slot="cpp_to_target",
                response_slot="cpp_to_target",
                request_payloads=openai_request_payload,
                response_payloads=openai_response_payload,
            )
            iteration_record = _failure_from_translation_exception(
                exc=exc,
                iteration_index=iteration_index,
                stage="cpp_to_target_translation",
            )

        if iteration_record is None:
            target_source_path = resolve_contract_path(
                config.output_root, iteration_paths.translated_source_path
            )
            _write_text(target_source_path, f"{target_source}\n")

            try:
                target_evaluation = evaluate_source_fn(
                    language=target_language,
                    source_path=target_source_path,
                    problem=problem,
                    workspace_root=run_directory,
                    timeout_seconds=config.runtime.timeout_seconds,
                )
                execution_payload["target"] = _execution_batch_to_dict(
                    result=target_evaluation,
                    output_root=config.output_root,
                    iteration_paths=iteration_paths,
                    stage_name="target",
                )
            except Exception as exc:
                iteration_record = _failure_from_runtime_exception(
                    exc=exc,
                    iteration_index=iteration_index,
                    stage="target_execution",
                    message="Target program evaluation failed unexpectedly.",
                )

        if iteration_record is None:
            if target_evaluation is None:
                raise RTTLoopError("Internal error: target evaluation missing.")
            target_failure = _failure_from_execution_result(
                result=target_evaluation,
                iteration_index=iteration_index,
                stage="target_execution",
            )
            if target_failure is not None:
                iteration_record = target_failure

        if iteration_record is None:
            try:
                target_to_cpp = _translate_with_explicit_languages(
                    client,
                    problem_id=problem.problem_id,
                    source_language=target_language,
                    target_language=config.seed_language,
                    problem_statement=statement,
                    sample_input=sample_input,
                    sample_output=sample_output,
                    source_code=target_source,
                    iteration_index=iteration_index,
                    direction="target_to_roundtrip_cpp",
                )
                openai_request_payload["target_to_cpp"] = (
                    target_to_cpp.request.to_dict()
                )
                openai_response_payload["target_to_cpp"] = (
                    target_to_cpp.response.to_dict()
                )
                roundtrip_cpp_source = target_to_cpp.extracted_source.rstrip()
            except Exception as exc:
                _capture_translation_debug_payloads(
                    exc=exc,
                    request_slot="target_to_cpp",
                    response_slot="target_to_cpp",
                    request_payloads=openai_request_payload,
                    response_payloads=openai_response_payload,
                )
                iteration_record = _failure_from_translation_exception(
                    exc=exc,
                    iteration_index=iteration_index,
                    stage="target_to_cpp_translation",
                )

        if iteration_record is None:
            roundtrip_source_path = resolve_contract_path(
                config.output_root, iteration_paths.roundtrip_source_path
            )
            _write_text(roundtrip_source_path, f"{roundtrip_cpp_source}\n")

            try:
                roundtrip_evaluation = evaluate_source_fn(
                    language=config.seed_language,
                    source_path=roundtrip_source_path,
                    problem=problem,
                    workspace_root=run_directory,
                    timeout_seconds=config.runtime.timeout_seconds,
                )
                execution_payload["roundtrip_cpp"] = _execution_batch_to_dict(
                    result=roundtrip_evaluation,
                    output_root=config.output_root,
                    iteration_paths=iteration_paths,
                    stage_name="roundtrip_cpp",
                )
            except Exception as exc:
                iteration_record = _failure_from_runtime_exception(
                    exc=exc,
                    iteration_index=iteration_index,
                    stage="roundtrip_execution",
                    message="Roundtrip C++ evaluation failed unexpectedly.",
                )

        if iteration_record is None:
            if roundtrip_evaluation is None:
                raise RTTLoopError("Internal error: roundtrip evaluation missing.")
            roundtrip_failure = _failure_from_execution_result(
                result=roundtrip_evaluation,
                iteration_index=iteration_index,
                stage="roundtrip_execution",
            )
            if roundtrip_failure is not None:
                iteration_record = roundtrip_failure
            else:
                target_source_history.append(target_source)
                seed_source_history.append(roundtrip_cpp_source)
                residual_similarity = compute_residual_similarity(
                    seed_cpp_source=seed_cpp_source,
                    candidate_cpp_source=roundtrip_cpp_source,
                )
                convergence = classify_dual_cpp_histories(
                    seed_source_history=seed_source_history,
                    target_source_history=target_source_history,
                )
                metric_payload = {
                    "residual_similarity": residual_similarity,
                    "convergence": {
                        "seed_state": convergence.seed_state,
                        "target_state": convergence.target_state,
                        "overall": convergence.overall,
                    },
                    "convergence_status": convergence.overall,
                }

                if convergence.overall == "fixed_point":
                    iteration_record = FailureRecord(
                        status=FailureStatus.SUCCESS,
                        stage="convergence",
                        iteration_index=iteration_index,
                        message="Fixed point reached for both seed and target histories.",
                        details={
                            "convergence_status": "fixed_point",
                            "convergence": metric_payload["convergence"],
                        },
                    )
                elif convergence.overall == "oscillation":
                    iteration_record = FailureRecord(
                        status=FailureStatus.OSCILLATION,
                        stage="convergence",
                        iteration_index=iteration_index,
                        message="Detected oscillation before dual-state fixed point convergence.",
                        details={
                            "convergence_status": "oscillation",
                            "convergence": metric_payload["convergence"],
                        },
                    )
                else:
                    iteration_record = FailureRecord(
                        status=FailureStatus.SUCCESS,
                        stage="iteration",
                        iteration_index=iteration_index,
                        message="Iteration completed; dual-state convergence still in progress.",
                        details={
                            "convergence_status": "continue",
                            "convergence": metric_payload["convergence"],
                        },
                    )
                    current_seed_source = roundtrip_cpp_source

        if iteration_record is None:
            raise RTTLoopError("Internal error: final record was not produced.")
        assert iteration_record is not None

        if openai_request_payload["cpp_to_target"] is None:
            openai_request_payload["cpp_to_target"] = {
                "error": "request unavailable due to upstream failure"
            }
        if openai_response_payload["cpp_to_target"] is None:
            openai_response_payload["cpp_to_target"] = {
                "error": "response unavailable due to upstream failure"
            }
        if openai_request_payload["target_to_cpp"] is None:
            openai_request_payload["target_to_cpp"] = {
                "error": "request unavailable due to early termination"
            }
        if openai_response_payload["target_to_cpp"] is None:
            openai_response_payload["target_to_cpp"] = {
                "error": "response unavailable due to early termination"
            }

        target_source_path = resolve_contract_path(
            config.output_root, iteration_paths.translated_source_path
        )
        roundtrip_source_path = resolve_contract_path(
            config.output_root, iteration_paths.roundtrip_source_path
        )
        input_seed_source_path = resolve_contract_path(
            config.output_root, iteration_paths.input_seed_source_path
        )
        compile_log_path = resolve_contract_path(
            config.output_root, iteration_paths.compile_log_path
        )
        execution_result_path = resolve_contract_path(
            config.output_root, iteration_paths.execution_result_path
        )
        metrics_path = resolve_contract_path(
            config.output_root, iteration_paths.metrics_path
        )
        request_path = resolve_contract_path(
            config.output_root, iteration_paths.openai_request_path
        )
        response_path = resolve_contract_path(
            config.output_root, iteration_paths.openai_response_path
        )
        iteration_metadata_path = resolve_contract_path(
            config.output_root, iteration_paths.iteration_metadata_path
        )

        _write_text(input_seed_source_path, f"{iteration_input_seed_source}\n")
        _write_text(target_source_path, f"{target_source}\n")
        _write_text(roundtrip_source_path, f"{roundtrip_cpp_source}\n")
        _write_json(request_path, openai_request_payload)
        _write_json(response_path, openai_response_payload)
        _write_compile_log(
            output_root=config.output_root,
            compile_log_path=compile_log_path,
            target_execution=execution_payload.get("target"),
            roundtrip_execution=execution_payload.get("roundtrip_cpp"),
        )
        _write_json(execution_result_path, execution_payload)
        _write_json(metrics_path, metric_payload)

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
                message="Iteration cap reached before convergence.",
                details={
                    "max_iterations": config.runtime.max_iterations,
                    "last_residual_similarity": metric_payload["residual_similarity"],
                    "convergence_status": "continue",
                    "convergence": metric_payload["convergence"],
                    "seed_history_length": len(seed_source_history),
                    "target_history_length": len(target_source_history),
                },
            )
            iteration_status = iteration_record.status

        iteration_payload = {
            "iteration_index": iteration_index,
            "started_at": iteration_started_at,
            "ended_at": _to_iso(now()),
            "result": iteration_record.to_dict(),
            "artifact_paths": iteration_paths.to_dict(),
        }
        _write_json(iteration_metadata_path, iteration_payload)

        manifest["iterations"].append(iteration_payload)
        manifest["status_transitions"].append(
            {
                "timestamp": _to_iso(now()),
                "problem_id": problem.problem_id,
                "seed_language": config.seed_language,
                "target_language": target_language,
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
        if should_stop:
            final_record = iteration_record
            break

        final_record = iteration_record

    if final_record is None:
        raise RTTLoopError("Internal error: loop completed without a final record.")

    manifest["final"] = final_record.to_dict()
    manifest["metadata"]["ended_at"] = _to_iso(now())
    manifest["metadata"]["updated_at"] = manifest["metadata"]["ended_at"]
    _persist_final_similarity_artifact(
        config=config,
        run_directory=run_directory,
        manifest=manifest,
        final_similarity_provider=final_similarity_provider
        or _build_final_similarity_provider(config),
        seed_cpp_source=seed_cpp_source,
        now=now,
    )
    _write_json(run_manifest_path, manifest)

    return RTTRunResult(
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language=target_language,
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
    final_similarity_provider_factory: Callable[[], EmbeddingProvider | None]
    | None = None,
    evaluate_source_fn: EvaluateSourceProtocol = evaluate_source,
    timestamp_provider: TimestampProvider | None = None,
) -> tuple[RTTRunResult, ...]:
    results: list[RTTRunResult] = []
    for problem in corpus_entries:
        for target_language in config.target_languages:
            client = (
                translation_client_factory()
                if translation_client_factory is not None
                else None
            )
            final_similarity_provider = (
                final_similarity_provider_factory()
                if final_similarity_provider_factory is not None
                else None
            )
            results.append(
                run_rtt_loop(
                    config=config,
                    run_id=run_id,
                    problem=problem,
                    target_language=target_language,
                    translation_client=client,
                    final_similarity_provider=final_similarity_provider,
                    evaluate_source_fn=evaluate_source_fn,
                    timestamp_provider=timestamp_provider,
                )
            )
    return tuple(results)


def _build_translation_client(config: ExperimentConfig) -> TranslationClientProtocol:
    if config.provider == "openai":
        return OpenAITranslationClient(
            model=config.openai.model,
            temperature=config.openai.temperature,
        )
    if config.provider == "ollama":
        return OllamaTranslationClient(
            model=config.ollama.model,
            temperature=config.ollama.temperature,
            host=config.ollama.host,
        )
    raise RTTLoopError(f"Unsupported translation provider: {config.provider}")


def _build_final_similarity_provider(
    config: ExperimentConfig,
) -> EmbeddingProvider | None:
    if config.provider == "openai":
        return OpenAIFinalSimilarityProvider()
    return None


def _persist_final_similarity_artifact(
    *,
    config: ExperimentConfig,
    run_directory: Path,
    manifest: dict[str, Any],
    final_similarity_provider: EmbeddingProvider | None,
    seed_cpp_source: str,
    now: TimestampProvider,
) -> None:
    metadata = manifest.get("metadata")
    if not isinstance(metadata, dict):
        raise RTTLoopError("Run manifest metadata is missing or invalid.")

    default_relative_path = (
        run_directory.relative_to(config.output_root.resolve())
        / "final-similarity.json"
    ).as_posix()
    relative_path = metadata.get("final_similarity_artifact_path")
    if not isinstance(relative_path, str) or not relative_path.strip():
        relative_path = default_relative_path
        metadata["final_similarity_artifact_path"] = relative_path
    artifact_path = resolve_contract_path(config.output_root, relative_path)

    final_source, final_source_path = _load_final_roundtrip_source_for_similarity(
        output_root=config.output_root,
        manifest=manifest,
    )

    source_hashes = {
        "seed_source_sha256": hash_source_text(seed_cpp_source),
        "final_source_sha256": None
        if final_source is None
        else hash_source_text(final_source),
    }

    existing_artifact = _load_json_if_exists(artifact_path)
    if isinstance(existing_artifact, dict):
        if existing_artifact.get("source_hashes") == source_hashes:
            return

    if final_source is None:
        payload = _build_unavailable_final_similarity_payload(
            reason="missing_final_seed_language_source",
            source_hashes=source_hashes,
            seed_artifact_path=metadata.get("seed_artifact_path"),
            final_roundtrip_source_path=final_source_path,
            provider=final_similarity_provider,
            now=now,
        )
        _write_json(artifact_path, payload)
        return

    if final_similarity_provider is None:
        payload = _build_unavailable_final_similarity_payload(
            reason="embedding_provider_not_configured",
            source_hashes=source_hashes,
            seed_artifact_path=metadata.get("seed_artifact_path"),
            final_roundtrip_source_path=final_source_path,
            provider=None,
            now=now,
        )
        _write_json(artifact_path, payload)
        return

    try:
        seed_embedding = final_similarity_provider.embed_source(
            source_text=seed_cpp_source
        )
        final_embedding = final_similarity_provider.embed_source(
            source_text=final_source
        )
        if seed_embedding.provider != final_embedding.provider:
            raise EmbeddingProviderError(
                "Final similarity requires one embedding provider for both sources."
            )
        if seed_embedding.configured_model != final_embedding.configured_model:
            raise EmbeddingProviderError(
                "Final similarity requires one configured embedding model."
            )
        if seed_embedding.dimensions != final_embedding.dimensions:
            raise EmbeddingProviderError(
                "Final similarity requires equal embedding dimensions."
            )

        score = cosine_similarity(seed_embedding.vector, final_embedding.vector)
        payload = _build_measured_final_similarity_payload(
            score=score,
            source_hashes=source_hashes,
            seed_embedding=seed_embedding,
            final_embedding=final_embedding,
            seed_artifact_path=metadata.get("seed_artifact_path"),
            final_roundtrip_source_path=final_source_path,
            now=now,
        )
    except Exception as exc:
        payload = _build_unavailable_final_similarity_payload(
            reason="embedding_measurement_failed",
            source_hashes=source_hashes,
            seed_artifact_path=metadata.get("seed_artifact_path"),
            final_roundtrip_source_path=final_source_path,
            provider=final_similarity_provider,
            now=now,
            details={
                "error_type": type(exc).__name__,
                "error": str(exc),
            },
        )
    _write_json(artifact_path, payload)


def _build_measured_final_similarity_payload(
    *,
    score: float,
    source_hashes: dict[str, Any],
    seed_embedding: EmbeddedSource,
    final_embedding: EmbeddedSource,
    seed_artifact_path: Any,
    final_roundtrip_source_path: str | None,
    now: TimestampProvider,
) -> dict[str, Any]:
    seed_usage = (
        None if seed_embedding.usage is None else seed_embedding.usage.to_dict()
    )
    final_usage = (
        None if final_embedding.usage is None else final_embedding.usage.to_dict()
    )
    combined_usage: dict[str, int] = {}
    prompt_total = _sum_optional_ints(
        None if seed_usage is None else seed_usage.get("prompt_tokens"),
        None if final_usage is None else final_usage.get("prompt_tokens"),
    )
    total_tokens = _sum_optional_ints(
        None if seed_usage is None else seed_usage.get("total_tokens"),
        None if final_usage is None else final_usage.get("total_tokens"),
    )
    if prompt_total is not None:
        combined_usage["prompt_tokens"] = prompt_total
    if total_tokens is not None:
        combined_usage["total_tokens"] = total_tokens

    observed_model: str | None = None
    if seed_embedding.observed_model == final_embedding.observed_model:
        observed_model = seed_embedding.observed_model

    return {
        "schema_version": "final_similarity.v1",
        "computed_at": _to_iso(now()),
        "availability": "measured",
        "score": float(score),
        "provider": seed_embedding.provider,
        "configured_model": seed_embedding.configured_model,
        "observed_model": observed_model,
        "dimensions": seed_embedding.dimensions,
        "usage": {
            "seed": seed_usage,
            "final": final_usage,
            "combined": combined_usage,
        },
        "request_ids": {
            "seed": seed_embedding.request_id,
            "final": final_embedding.request_id,
        },
        "source_hashes": source_hashes,
        "source_artifacts": {
            "seed_artifact_path": seed_artifact_path,
            "final_roundtrip_source_path": final_roundtrip_source_path,
        },
        "revision_evidence": {
            "configured_model": seed_embedding.configured_model,
            "observed_models": {
                "seed": seed_embedding.observed_model,
                "final": final_embedding.observed_model,
            },
            "request_ids": {
                "seed": seed_embedding.request_id,
                "final": final_embedding.request_id,
            },
        },
    }


def _build_unavailable_final_similarity_payload(
    *,
    reason: str,
    source_hashes: dict[str, Any],
    seed_artifact_path: Any,
    final_roundtrip_source_path: str | None,
    provider: EmbeddingProvider | None,
    now: TimestampProvider,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema_version": "final_similarity.v1",
        "computed_at": _to_iso(now()),
        "availability": "unavailable",
        "reason": reason,
        "score": None,
        "provider": None if provider is None else provider.provider_name,
        "configured_model": None if provider is None else provider.configured_model,
        "observed_model": None,
        "dimensions": None,
        "usage": {
            "seed": None,
            "final": None,
            "combined": {},
        },
        "request_ids": {
            "seed": None,
            "final": None,
        },
        "source_hashes": source_hashes,
        "source_artifacts": {
            "seed_artifact_path": seed_artifact_path,
            "final_roundtrip_source_path": final_roundtrip_source_path,
        },
        "revision_evidence": {
            "configured_model": None if provider is None else provider.configured_model,
            "observed_models": {
                "seed": None,
                "final": None,
            },
            "request_ids": {
                "seed": None,
                "final": None,
            },
        },
    }
    if details is not None:
        payload["details"] = details
    return payload


def _load_final_roundtrip_source_for_similarity(
    *, output_root: Path, manifest: dict[str, Any]
) -> tuple[str | None, str | None]:
    iterations = manifest.get("iterations")
    if not isinstance(iterations, list) or not iterations:
        return None, None

    last_iteration = iterations[-1]
    if not isinstance(last_iteration, dict):
        return None, None
    artifact_paths = last_iteration.get("artifact_paths")
    if not isinstance(artifact_paths, dict):
        return None, None

    roundtrip_path = artifact_paths.get("roundtrip_source_path")
    if not isinstance(roundtrip_path, str) or not roundtrip_path.strip():
        return None, None
    path = resolve_contract_path(output_root, roundtrip_path)
    if not path.is_file():
        return None, roundtrip_path
    source = path.read_text(encoding="utf-8").rstrip()
    if not source.strip():
        return None, roundtrip_path
    return source, roundtrip_path


def _load_json_if_exists(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return None
    return payload


def _sum_optional_ints(left: Any, right: Any) -> int | None:
    values: list[int] = []
    for item in (left, right):
        if isinstance(item, int) and not isinstance(item, bool):
            values.append(item)
    if not values:
        return None
    return sum(values)


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
    target_execution: dict[str, Any] | None,
    roundtrip_execution: dict[str, Any] | None,
) -> None:
    target_log = _extract_compile_log_text(target_execution, output_root=output_root)
    roundtrip_log = _extract_compile_log_text(
        roundtrip_execution, output_root=output_root
    )

    log_text = f"[target]\n{target_log}\n[roundtrip_cpp]\n{roundtrip_log}\n"
    _write_text(compile_log_path, log_text)


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
            OpenAIResponseParseError,
            SourceExtractionError,
            OllamaResponseParseError,
            OllamaSourceExtractionError,
        ),
    ):
        status = FailureStatus.PARSE_ERROR
        message = "Translation response parsing failed."
    elif isinstance(exc, (OpenAIClientError, OllamaClientError)):
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
