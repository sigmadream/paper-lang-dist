from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

from rttdist.artifacts import ArtifactContractError, resolve_contract_path
from rttdist.config import ExperimentConfig
from rttdist.failure_taxonomy import (
    FailureRecord,
    FailureStatus,
    failure_record_from_dict,
)


class RunStateError(RuntimeError):
    pass


class ResumeValidationError(RunStateError):
    pass


RUN_MANIFEST_SCHEMA_VERSION_V1 = "run_manifest.v1"
RUN_MANIFEST_SCHEMA_VERSION_V2 = "run_manifest.v2"
ITERATION_INPUT_ARTIFACT_KEY_V1 = "input_cpp_source_path"
ITERATION_INPUT_ARTIFACT_KEY_V2 = "input_seed_source_path"


@dataclass(frozen=True)
class RunResumePlan:
    manifest: dict[str, Any]
    start_iteration: int
    current_seed_source: str
    seed_source_history: tuple[str, ...]
    target_source_history: tuple[str, ...]
    previous_status: str
    final_record: FailureRecord | None


def compute_config_hash(config: ExperimentConfig) -> str:
    payload = {
        "provider": config.provider,
        "problem_ids": list(config.problem_ids),
        "seed_language": config.seed_language,
        "target_languages": list(config.target_languages),
        "openai": {
            "model": config.openai.model,
            "temperature": config.openai.temperature,
        },
        "ollama": {
            "model": config.ollama.model,
            "temperature": config.ollama.temperature,
            "host": config.ollama.host,
        },
        "runtime": {
            "max_iterations": config.runtime.max_iterations,
            "timeout_seconds": config.runtime.timeout_seconds,
        },
        "output_root": config.output_root.as_posix(),
        "problem_root": config.problem_root.as_posix(),
        "corpus_root": config.corpus_root.as_posix(),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_manifest_checksums(
    *,
    config: ExperimentConfig,
    prompt_template_version: str,
    seed_source: str,
) -> dict[str, str]:
    normalized_prompt_version = prompt_template_version.strip()
    if not normalized_prompt_version:
        raise RunStateError("Prompt template version must be a non-empty string.")
    return {
        "config_hash": compute_config_hash(config),
        "prompt_template_version": normalized_prompt_version,
        "prompt_template_hash": _sha256_text(normalized_prompt_version),
        "seed_source_hash": _sha256_text(seed_source),
    }


def plan_run_resume(
    *,
    run_manifest_path: Path,
    run_directory: Path,
    output_root: Path,
    metadata: dict[str, Any],
    checksums: dict[str, str],
    seed_cpp_source: str,
    created_at: str,
) -> RunResumePlan:
    existing_manifest = _load_existing_manifest(run_manifest_path)
    if existing_manifest is None:
        existing_manifest = _recover_manifest_from_iteration_artifacts(
            run_directory=run_directory,
            output_root=output_root,
            metadata=metadata,
            checksums=checksums,
            created_at=created_at,
        )

    if existing_manifest is None:
        manifest = _build_new_manifest(
            metadata=metadata,
            checksums=checksums,
            created_at=created_at,
        )
        return RunResumePlan(
            manifest=manifest,
            start_iteration=1,
            current_seed_source=seed_cpp_source,
            seed_source_history=(),
            target_source_history=(),
            previous_status="running",
            final_record=None,
        )

    _validate_manifest_schema_compatibility(existing_manifest)
    _validate_metadata_compatibility(existing_manifest, metadata)
    _validate_resume_checksums(existing_manifest, checksums)

    normalized_manifest = _normalize_manifest(
        existing_manifest,
        metadata,
        checksums,
        created_at=created_at,
    )
    recovered_iterations = _filter_contiguous_complete_iterations(
        manifest=normalized_manifest,
        output_root=output_root,
    )

    normalized_manifest["iterations"] = recovered_iterations
    normalized_manifest["status_transitions"] = _rebuild_status_transitions(
        recovered_iterations,
        problem_id=_as_text(
            _as_mapping(metadata.get("problem"), field_name="problem").get(
                "problem_id"
            ),
            field_name="problem.problem_id",
        ),
        seed_language=_as_text(
            metadata.get("seed_language"), field_name="seed_language"
        ),
        target_language=_as_text(
            metadata.get("target_language"), field_name="target_language"
        ),
    )
    normalized_manifest["metadata"]["updated_at"] = created_at

    if not recovered_iterations:
        normalized_manifest["final"] = None
        return RunResumePlan(
            manifest=normalized_manifest,
            start_iteration=1,
            current_seed_source=seed_cpp_source,
            seed_source_history=(),
            target_source_history=(),
            previous_status="running",
            final_record=None,
        )

    seed_source_history = _read_source_history(
        iterations=recovered_iterations,
        output_root=output_root,
        artifact_key="roundtrip_source_path",
    )
    target_source_history = _read_source_history(
        iterations=recovered_iterations,
        output_root=output_root,
        artifact_key="translated_source_path",
    )
    current_seed_source = (
        seed_source_history[-1] if seed_source_history else seed_cpp_source
    )
    previous_status = _latest_status(recovered_iterations)
    last_record = _iteration_failure_record(recovered_iterations[-1])

    if _is_terminal_record(last_record):
        normalized_manifest["final"] = last_record.to_dict()
        return RunResumePlan(
            manifest=normalized_manifest,
            start_iteration=len(recovered_iterations) + 1,
            current_seed_source=current_seed_source,
            seed_source_history=tuple(seed_source_history),
            target_source_history=tuple(target_source_history),
            previous_status=previous_status,
            final_record=last_record,
        )

    normalized_manifest["final"] = None
    return RunResumePlan(
        manifest=normalized_manifest,
        start_iteration=len(recovered_iterations) + 1,
        current_seed_source=current_seed_source,
        seed_source_history=tuple(seed_source_history),
        target_source_history=tuple(target_source_history),
        previous_status=previous_status,
        final_record=None,
    )


def _build_new_manifest(
    *,
    metadata: dict[str, Any],
    checksums: dict[str, str],
    created_at: str,
) -> dict[str, Any]:
    return {
        "schema_version": RUN_MANIFEST_SCHEMA_VERSION_V2,
        "metadata": {
            **metadata,
            "config_hash": checksums["config_hash"],
            "checksums": dict(checksums),
            "created_at": created_at,
            "updated_at": None,
            "ended_at": None,
        },
        "status_transitions": [],
        "iterations": [],
        "final": None,
    }


def _load_existing_manifest(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RunStateError(f"Invalid run manifest payload at {path.as_posix()}.")
    return payload


def _recover_manifest_from_iteration_artifacts(
    *,
    run_directory: Path,
    output_root: Path,
    metadata: dict[str, Any],
    checksums: dict[str, str],
    created_at: str,
) -> dict[str, Any] | None:
    iterations_root = run_directory / "iterations"
    if not iterations_root.is_dir():
        return None

    recovered: list[dict[str, Any]] = []
    for iteration_file in sorted(iterations_root.glob("iter-*/iteration.json")):
        payload = json.loads(iteration_file.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            continue
        recovered.append(payload)

    if not recovered:
        return None

    schema_version = _infer_recovered_manifest_schema_version(recovered)

    return {
        "schema_version": schema_version,
        "metadata": {
            **metadata,
            "config_hash": checksums["config_hash"],
            "checksums": dict(checksums),
            "created_at": created_at,
            "updated_at": created_at,
            "ended_at": None,
            "recovered_from_iterations": True,
        },
        "status_transitions": _rebuild_status_transitions(
            recovered,
            problem_id=_as_text(
                _as_mapping(metadata.get("problem"), field_name="problem").get(
                    "problem_id"
                ),
                field_name="problem.problem_id",
            ),
            seed_language=_as_text(
                metadata.get("seed_language"), field_name="seed_language"
            ),
            target_language=_as_text(
                metadata.get("target_language"), field_name="target_language"
            ),
        ),
        "iterations": recovered,
        "final": None,
    }


def _validate_metadata_compatibility(
    manifest: dict[str, Any], metadata: dict[str, Any]
) -> None:
    manifest_metadata = _as_mapping(manifest.get("metadata"), field_name="metadata")
    existing_run_id = _as_text(
        manifest_metadata.get("run_id"), field_name="metadata.run_id"
    )
    existing_target = _as_text(
        manifest_metadata.get("target_language"), field_name="metadata.target_language"
    )
    existing_problem = _as_mapping(
        manifest_metadata.get("problem"), field_name="metadata.problem"
    )
    existing_problem_id = _as_text(
        existing_problem.get("problem_id"), field_name="metadata.problem.problem_id"
    )
    existing_seed_language = _as_text(
        manifest_metadata.get("seed_language"), field_name="metadata.seed_language"
    )
    existing_run_directory = _as_text(
        manifest_metadata.get("run_directory"), field_name="metadata.run_directory"
    )
    existing_run_metadata_path = _as_text(
        manifest_metadata.get("run_metadata_path"),
        field_name="metadata.run_metadata_path",
    )

    expected_problem = _as_mapping(metadata.get("problem"), field_name="problem")
    expected_problem_id = _as_text(
        expected_problem.get("problem_id"), field_name="problem.problem_id"
    )
    expected_run_id = _as_text(metadata.get("run_id"), field_name="run_id")
    expected_target = _as_text(
        metadata.get("target_language"), field_name="target_language"
    )
    expected_seed_language = _as_text(
        metadata.get("seed_language"), field_name="seed_language"
    )
    expected_run_directory = _as_text(
        metadata.get("run_directory"), field_name="run_directory"
    )
    expected_run_metadata_path = _as_text(
        metadata.get("run_metadata_path"), field_name="run_metadata_path"
    )

    if existing_run_id != expected_run_id:
        raise ResumeValidationError(
            "Unsafe resume rejected: run_id mismatch in existing manifest."
        )
    if existing_problem_id != expected_problem_id:
        raise ResumeValidationError(
            "Unsafe resume rejected: problem_id mismatch in existing manifest."
        )
    if existing_seed_language != expected_seed_language:
        raise ResumeValidationError(
            "Unsafe resume rejected: seed_language mismatch in existing manifest."
        )
    if existing_target != expected_target:
        raise ResumeValidationError(
            "Unsafe resume rejected: target_language mismatch in existing manifest."
        )
    if existing_run_directory != expected_run_directory:
        raise ResumeValidationError(
            "Unsafe resume rejected: run_directory mismatch in existing manifest."
        )
    if existing_run_metadata_path != expected_run_metadata_path:
        raise ResumeValidationError(
            "Unsafe resume rejected: run_metadata_path mismatch in existing manifest."
        )


def _validate_manifest_schema_compatibility(manifest: dict[str, Any]) -> None:
    schema_version = _as_optional_text(manifest.get("schema_version"))
    if schema_version is None:
        return
    if schema_version in {
        RUN_MANIFEST_SCHEMA_VERSION_V1,
        RUN_MANIFEST_SCHEMA_VERSION_V2,
    }:
        return
    raise ResumeValidationError(
        "Unsafe resume rejected: unsupported run manifest schema version."
    )


def _validate_resume_checksums(
    manifest: dict[str, Any], expected: dict[str, str]
) -> None:
    metadata = _as_mapping(manifest.get("metadata"), field_name="metadata")
    raw_checksums = metadata.get("checksums")
    if not isinstance(raw_checksums, dict):
        raise ResumeValidationError(
            "Unsafe resume rejected: existing manifest is missing checksum metadata."
        )
    checksums = raw_checksums

    config_hash = _as_text(
        checksums.get("config_hash"), field_name="checksums.config_hash"
    )
    prompt_template_hash = _as_text(
        checksums.get("prompt_template_hash"),
        field_name="checksums.prompt_template_hash",
    )
    seed_source_hash = _as_text(
        checksums.get("seed_source_hash"), field_name="checksums.seed_source_hash"
    )

    if config_hash != expected["config_hash"]:
        raise ResumeValidationError(
            "Unsafe resume rejected: config hash mismatch for existing run artifacts."
        )
    if prompt_template_hash != expected["prompt_template_hash"]:
        raise ResumeValidationError(
            "Unsafe resume rejected: prompt template checksum mismatch."
        )
    if seed_source_hash != expected["seed_source_hash"]:
        raise ResumeValidationError(
            "Unsafe resume rejected: seed source hash mismatch for existing run artifacts."
        )


def _normalize_manifest(
    manifest: dict[str, Any],
    metadata: dict[str, Any],
    checksums: dict[str, str],
    *,
    created_at: str,
) -> dict[str, Any]:
    existing_schema_version = _as_optional_text(manifest.get("schema_version"))
    normalized_schema_version = (
        RUN_MANIFEST_SCHEMA_VERSION_V1
        if existing_schema_version == RUN_MANIFEST_SCHEMA_VERSION_V1
        else RUN_MANIFEST_SCHEMA_VERSION_V2
    )

    normalized_metadata = {
        **metadata,
        "config_hash": checksums["config_hash"],
        "checksums": dict(checksums),
        "created_at": _as_optional_text(
            _as_mapping(manifest.get("metadata"), field_name="metadata").get(
                "created_at"
            )
        ),
        "updated_at": _as_optional_text(
            _as_mapping(manifest.get("metadata"), field_name="metadata").get(
                "updated_at"
            )
        ),
        "ended_at": _as_optional_text(
            _as_mapping(manifest.get("metadata"), field_name="metadata").get("ended_at")
        ),
    }
    if not normalized_metadata["created_at"]:
        normalized_metadata["created_at"] = created_at

    return {
        "schema_version": normalized_schema_version,
        "metadata": normalized_metadata,
        "status_transitions": _as_list(
            manifest.get("status_transitions"), field_name="status_transitions"
        ),
        "iterations": _as_list(manifest.get("iterations"), field_name="iterations"),
        "final": manifest.get("final"),
    }


def _filter_contiguous_complete_iterations(
    *,
    manifest: dict[str, Any],
    output_root: Path,
) -> list[dict[str, Any]]:
    iterations = _as_list(manifest.get("iterations"), field_name="iterations")
    recovered: list[dict[str, Any]] = []
    expected_index = 1

    schema_version = _as_optional_text(manifest.get("schema_version"))
    normalized_schema_version = (
        RUN_MANIFEST_SCHEMA_VERSION_V1
        if schema_version == RUN_MANIFEST_SCHEMA_VERSION_V1
        else RUN_MANIFEST_SCHEMA_VERSION_V2
    )

    for item in iterations:
        mapping = _as_mapping(item, field_name=f"iterations[{expected_index - 1}]")
        index = mapping.get("iteration_index")
        if not isinstance(index, int) or index != expected_index:
            break
        if not _is_iteration_artifact_complete(
            mapping,
            output_root,
            schema_version=normalized_schema_version,
        ):
            break
        recovered.append(mapping)
        expected_index += 1

    return recovered


def _is_iteration_artifact_complete(
    iteration: dict[str, Any], output_root: Path, *, schema_version: str
) -> bool:
    artifact_paths = _as_mapping(
        iteration.get("artifact_paths"), field_name="artifact_paths"
    )
    required_keys = (
        "iteration_metadata_path",
        "openai_request_path",
        "openai_response_path",
        "translated_source_path",
        "roundtrip_source_path",
        "compile_log_path",
        "execution_result_path",
        "metrics_path",
    )
    for key in required_keys:
        relative_path = artifact_paths.get(key)
        if not isinstance(relative_path, str) or not relative_path.strip():
            return False
        resolved_path = _resolve_artifact_path_within_output_root(
            output_root=output_root,
            relative_path=relative_path,
            field_name=f"artifact_paths.{key}",
        )
        if not resolved_path.is_file():
            return False
    if schema_version == RUN_MANIFEST_SCHEMA_VERSION_V1:
        input_artifact_key = ITERATION_INPUT_ARTIFACT_KEY_V1
    else:
        input_artifact_key = ITERATION_INPUT_ARTIFACT_KEY_V2

    input_seed_source_path = artifact_paths.get(input_artifact_key)
    if input_seed_source_path is not None:
        if (
            not isinstance(input_seed_source_path, str)
            or not input_seed_source_path.strip()
        ):
            return False
        resolved_input_path = _resolve_artifact_path_within_output_root(
            output_root=output_root,
            relative_path=input_seed_source_path,
            field_name=f"artifact_paths.{input_artifact_key}",
        )
        if not resolved_input_path.is_file():
            return False
    elif schema_version == RUN_MANIFEST_SCHEMA_VERSION_V2:
        return False
    return True


def _infer_recovered_manifest_schema_version(
    recovered_iterations: list[dict[str, Any]],
) -> str:
    for item in recovered_iterations:
        artifact_paths = item.get("artifact_paths")
        if not isinstance(artifact_paths, dict):
            continue
        if ITERATION_INPUT_ARTIFACT_KEY_V2 in artifact_paths:
            return RUN_MANIFEST_SCHEMA_VERSION_V2
        if ITERATION_INPUT_ARTIFACT_KEY_V1 in artifact_paths:
            return RUN_MANIFEST_SCHEMA_VERSION_V1
    return RUN_MANIFEST_SCHEMA_VERSION_V2


def _read_source_history(
    *, iterations: list[dict[str, Any]], output_root: Path, artifact_key: str
) -> list[str]:
    history: list[str] = []
    for item in iterations:
        artifact_paths = _as_mapping(
            item.get("artifact_paths"), field_name="artifact_paths"
        )
        source_relative = _as_text(
            artifact_paths.get(artifact_key),
            field_name=f"artifact_paths.{artifact_key}",
        )
        source_path = _resolve_artifact_path_within_output_root(
            output_root=output_root,
            relative_path=source_relative,
            field_name=f"artifact_paths.{artifact_key}",
        )
        history.append(source_path.read_text(encoding="utf-8").rstrip())
    return history


def _resolve_artifact_path_within_output_root(
    *, output_root: Path, relative_path: str, field_name: str
) -> Path:
    try:
        return resolve_contract_path(output_root, relative_path)
    except ArtifactContractError as exc:
        raise ResumeValidationError(
            "Unsafe resume rejected: "
            f"`{field_name}` escapes output root ({relative_path!r})."
        ) from exc


def _latest_status(iterations: list[dict[str, Any]]) -> str:
    if not iterations:
        return "running"
    return _iteration_failure_record(iterations[-1]).status.value


def _iteration_failure_record(iteration: dict[str, Any]) -> FailureRecord:
    result = _as_mapping(iteration.get("result"), field_name="iteration.result")
    return failure_record_from_dict(result)


def _rebuild_status_transitions(
    iterations: list[dict[str, Any]],
    *,
    problem_id: str,
    seed_language: str,
    target_language: str,
) -> list[dict[str, Any]]:
    transitions: list[dict[str, Any]] = []
    previous_status = "running"
    for item in iterations:
        record = _iteration_failure_record(item)
        transitions.append(
            {
                "timestamp": item.get("ended_at") or item.get("started_at"),
                "problem_id": problem_id,
                "seed_language": seed_language,
                "target_language": target_language,
                "iteration_index": record.iteration_index,
                "from_status": previous_status,
                "to_status": record.status.value,
            }
        )
        previous_status = record.status.value
    return transitions


def _is_terminal_record(record: FailureRecord) -> bool:
    if record.status in {
        FailureStatus.API_ERROR,
        FailureStatus.PARSE_ERROR,
        FailureStatus.COMPILE_ERROR,
        FailureStatus.RUNTIME_ERROR,
        FailureStatus.WRONG_ANSWER,
        FailureStatus.TIMEOUT,
        FailureStatus.OSCILLATION,
        FailureStatus.MAX_ITER_NO_CONVERGENCE,
    }:
        return True
    return (
        record.status == FailureStatus.SUCCESS
        and _extract_overall_convergence_status(record.details) == "fixed_point"
    )


def _extract_overall_convergence_status(details: dict[str, Any]) -> str | None:
    convergence = details.get("convergence")
    if isinstance(convergence, dict):
        overall = convergence.get("overall")
        if isinstance(overall, str) and overall.strip():
            return overall.strip()
    value = details.get("convergence_status")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _as_mapping(value: Any, *, field_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RunStateError(f"Expected `{field_name}` to be a mapping.")
    return value


def _as_list(value: Any, *, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise RunStateError(f"Expected `{field_name}` to be a list.")
    return value


def _as_text(value: Any, *, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RunStateError(f"Expected `{field_name}` to be a non-empty string.")
    return value.strip()


def _as_optional_text(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    return stripped if stripped else None
