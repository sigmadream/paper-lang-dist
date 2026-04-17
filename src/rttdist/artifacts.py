from __future__ import annotations

import os
import ntpath
import posixpath
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rttdist.config import SUPPORTED_EXPERIMENT_LANGUAGES, SUPPORTED_TARGET_LANGUAGES
from rttdist.failure_taxonomy import FailureRecord

SOURCE_FILE_EXTENSIONS = {
    "cpp": ".cpp",
    "c": ".c",
    "java": ".java",
    "python": ".py",
}


class ArtifactContractError(ValueError):
    pass


@dataclass(frozen=True)
class CuratedProblemReference:
    problem_id: str
    statement_path: str
    fixture_input_path: str
    fixture_output_path: str
    seed_source_path: str

    def to_dict(self) -> dict[str, str]:
        return {
            "problem_id": self.problem_id,
            "statement_path": self.statement_path,
            "fixture_input_path": self.fixture_input_path,
            "fixture_output_path": self.fixture_output_path,
            "seed_source_path": self.seed_source_path,
        }


@dataclass(frozen=True)
class MockOpenAIMessage:
    role: str
    content: str

    def to_dict(self) -> dict[str, str]:
        return {
            "role": self.role,
            "content": self.content,
        }


@dataclass(frozen=True)
class MockOpenAIRequest:
    model: str
    temperature: float
    messages: tuple[MockOpenAIMessage, ...]
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "temperature": self.temperature,
            "messages": [message.to_dict() for message in self.messages],
            "metadata": {
                str(key): _stringify_metadata_value(value)
                for key, value in deepcopy(self.metadata).items()
            },
        }


def _stringify_metadata_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


@dataclass(frozen=True)
class MockOpenAIChoice:
    index: int
    message: MockOpenAIMessage
    finish_reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "message": self.message.to_dict(),
            "finish_reason": self.finish_reason,
        }


@dataclass(frozen=True)
class MockOpenAIUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    def to_dict(self) -> dict[str, int]:
        return {
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
        }


@dataclass(frozen=True)
class MockOpenAIResponse:
    response_id: str
    model: str
    choices: tuple[MockOpenAIChoice, ...]
    usage: MockOpenAIUsage

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.response_id,
            "model": self.model,
            "choices": [choice.to_dict() for choice in self.choices],
            "usage": self.usage.to_dict(),
        }


@dataclass(frozen=True)
class IterationArtifactPaths:
    iteration_directory: str
    iteration_metadata_path: str
    openai_request_path: str
    openai_response_path: str
    input_seed_source_path: str
    translated_source_path: str
    roundtrip_source_path: str
    compile_log_path: str
    execution_result_path: str
    metrics_path: str

    def to_dict(self) -> dict[str, str]:
        return {
            "iteration_directory": self.iteration_directory,
            "iteration_metadata_path": self.iteration_metadata_path,
            "openai_request_path": self.openai_request_path,
            "openai_response_path": self.openai_response_path,
            "input_seed_source_path": self.input_seed_source_path,
            "translated_source_path": self.translated_source_path,
            "roundtrip_source_path": self.roundtrip_source_path,
            "compile_log_path": self.compile_log_path,
            "execution_result_path": self.execution_result_path,
            "metrics_path": self.metrics_path,
        }


@dataclass(frozen=True)
class RunMetadata:
    run_id: str
    problem: CuratedProblemReference
    seed_language: str
    target_language: str
    max_iterations: int
    run_directory: str
    run_metadata_path: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "problem": self.problem.to_dict(),
            "seed_language": self.seed_language,
            "target_language": self.target_language,
            "max_iterations": self.max_iterations,
            "run_directory": self.run_directory,
            "run_metadata_path": self.run_metadata_path,
        }


@dataclass(frozen=True)
class IterationArtifactRecord:
    iteration_index: int
    result: FailureRecord
    artifact_paths: IterationArtifactPaths
    openai_request: MockOpenAIRequest
    openai_response: MockOpenAIResponse

    def to_dict(self) -> dict[str, Any]:
        return {
            "iteration_index": self.iteration_index,
            "result": self.result.to_dict(),
            "artifact_paths": self.artifact_paths.to_dict(),
            "openai_request": self.openai_request.to_dict(),
            "openai_response": self.openai_response.to_dict(),
        }


@dataclass(frozen=True)
class RunArtifactRecord:
    metadata: RunMetadata
    iterations: tuple[IterationArtifactRecord, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "metadata": self.metadata.to_dict(),
            "iterations": [iteration.to_dict() for iteration in self.iterations],
        }


def build_run_metadata(
    run_id: str,
    problem: CuratedProblemReference,
    target_language: str,
    seed_language: str,
    max_iterations: int,
) -> RunMetadata:
    if not isinstance(max_iterations, int) or isinstance(max_iterations, bool):
        raise ArtifactContractError("`max_iterations` must be an integer >= 1.")
    if max_iterations < 1:
        raise ArtifactContractError(
            f"`max_iterations` must be >= 1, got {max_iterations}."
        )

    normalized_seed_language = _normalize_language(
        seed_language,
        field_name="seed_language",
        supported=SUPPORTED_EXPERIMENT_LANGUAGES,
    )
    run_directory = build_run_directory(
        run_id,
        problem.problem_id,
        target_language,
        normalized_seed_language,
    )

    return RunMetadata(
        run_id=_normalize_text(run_id, field_name="run_id"),
        problem=problem,
        seed_language=normalized_seed_language,
        target_language=target_language,
        max_iterations=max_iterations,
        run_directory=_to_contract_path(run_directory),
        run_metadata_path=_to_contract_path(run_directory / "run.json"),
    )


def build_run_directory(
    run_id: str,
    problem_id: str,
    target_language: str,
    seed_language: str,
) -> Path:
    _validate_target_language(target_language)
    normalized_seed_language = _normalize_language(
        seed_language,
        field_name="seed_language",
        supported=SUPPORTED_EXPERIMENT_LANGUAGES,
    )
    normalized_target_language = _normalize_language(
        target_language,
        field_name="target_language",
        supported=SUPPORTED_TARGET_LANGUAGES,
    )
    normalized_run_id = _normalize_text(run_id, field_name="run_id")
    normalized_problem_id = _normalize_text(problem_id, field_name="problem_id")
    return (
        Path(normalized_run_id)
        / normalized_problem_id
        / f"{normalized_seed_language}-to-{normalized_target_language}"
    )


def build_legacy_run_directory(
    run_id: str, problem_id: str, target_language: str
) -> Path:
    _validate_target_language(target_language)
    normalized_run_id = _normalize_text(run_id, field_name="run_id")
    normalized_problem_id = _normalize_text(problem_id, field_name="problem_id")
    normalized_target_language = _normalize_language(
        target_language,
        field_name="target_language",
        supported=SUPPORTED_TARGET_LANGUAGES,
    )
    return Path(normalized_run_id) / normalized_problem_id / normalized_target_language


def build_iteration_artifact_paths(
    run_id: str,
    problem_id: str,
    target_language: str,
    seed_language: str,
    iteration_index: int,
) -> IterationArtifactPaths:
    if not isinstance(iteration_index, int) or isinstance(iteration_index, bool):
        raise ArtifactContractError("`iteration_index` must be an integer >= 1.")
    if iteration_index < 1:
        raise ArtifactContractError(
            f"`iteration_index` must be >= 1, got {iteration_index}."
        )

    run_directory = build_run_directory(
        run_id,
        problem_id,
        target_language,
        seed_language,
    )
    iteration_directory = run_directory / "iterations" / f"iter-{iteration_index:03d}"
    seed_source_extension = source_file_extension(seed_language)
    source_extension = source_file_extension(target_language)

    return IterationArtifactPaths(
        iteration_directory=_to_contract_path(iteration_directory),
        iteration_metadata_path=_to_contract_path(
            iteration_directory / "iteration.json"
        ),
        openai_request_path=_to_contract_path(
            iteration_directory / "openai-request.json"
        ),
        openai_response_path=_to_contract_path(
            iteration_directory / "openai-response.json"
        ),
        input_seed_source_path=_to_contract_path(
            iteration_directory / f"input{seed_source_extension}"
        ),
        translated_source_path=_to_contract_path(
            iteration_directory / f"translated{source_extension}"
        ),
        roundtrip_source_path=_to_contract_path(iteration_directory / "roundtrip.cpp"),
        compile_log_path=_to_contract_path(iteration_directory / "compile.log"),
        execution_result_path=_to_contract_path(iteration_directory / "execution.json"),
        metrics_path=_to_contract_path(iteration_directory / "metrics.json"),
    )


def resolve_contract_path(output_root: Path, relative_contract_path: str) -> Path:
    if (
        not isinstance(relative_contract_path, str)
        or not relative_contract_path.strip()
    ):
        raise ArtifactContractError(
            "`relative_contract_path` must be a non-empty string."
        )

    normalized_output_root = Path(output_root).resolve()
    raw_path = relative_contract_path.strip()
    candidate_path = Path(raw_path)
    if candidate_path.is_absolute():
        raise ArtifactContractError(
            "`relative_contract_path` must not be absolute: "
            f"{relative_contract_path!r}."
        )

    resolved = (normalized_output_root / candidate_path).resolve()
    try:
        resolved.relative_to(normalized_output_root)
    except ValueError as exc:
        raise ArtifactContractError(
            f"`relative_contract_path` escapes output root: {relative_contract_path!r}."
        ) from exc
    return resolved


def source_file_extension(language: str) -> str:
    normalized_language = language.strip().lower() if isinstance(language, str) else ""
    try:
        return SOURCE_FILE_EXTENSIONS[normalized_language]
    except KeyError as exc:
        supported = ", ".join(sorted(SUPPORTED_TARGET_LANGUAGES))
        raise ArtifactContractError(
            f"Unsupported language `{language}`. Supported languages: {supported}."
        ) from exc


def _normalize_language(
    value: str,
    *,
    field_name: str,
    supported: frozenset[str],
) -> str:
    normalized = value.strip().lower() if isinstance(value, str) else ""
    if normalized not in supported:
        supported_values = ", ".join(sorted(supported))
        raise ArtifactContractError(
            f"Unsupported {field_name} `{value}`. Supported values: {supported_values}."
        )
    return normalized


def _normalize_text(value: str, *, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ArtifactContractError(f"`{field_name}` must be a non-empty string.")
    _validate_no_path_traversal(value, field_name)
    return value.strip()


def _validate_no_path_traversal(value: str, field_name: str) -> None:
    normalized = value.strip()
    if (
        os.path.isabs(normalized)
        or posixpath.isabs(normalized)
        or ntpath.isabs(normalized)
    ):
        raise ArtifactContractError(
            f"`{field_name}` must not be an absolute path: {value!r}."
        )
    if "/" in normalized or "\\" in normalized:
        raise ArtifactContractError(
            f"`{field_name}` must not contain path separators "
            f"or path traversal components: {value!r}."
        )
    if normalized in (".", ".."):
        raise ArtifactContractError(
            f"`{field_name}` must not contain path traversal components: {value!r}."
        )


def _validate_target_language(target_language: str) -> None:
    if target_language not in SUPPORTED_TARGET_LANGUAGES:
        supported = ", ".join(sorted(SUPPORTED_TARGET_LANGUAGES))
        raise ArtifactContractError(
            "Unsupported target language "
            f"`{target_language}`. Supported target languages: {supported}."
        )


def _to_contract_path(path: Path) -> str:
    return path.as_posix()
