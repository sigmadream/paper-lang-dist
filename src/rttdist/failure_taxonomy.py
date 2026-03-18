from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FailureTaxonomyError(ValueError):
    pass


class FailureStatus(str, Enum):
    SUCCESS = "success"
    API_ERROR = "api_error"
    PARSE_ERROR = "parse_error"
    COMPILE_ERROR = "compile_error"
    RUNTIME_ERROR = "runtime_error"
    WRONG_ANSWER = "wrong_answer"
    TIMEOUT = "timeout"
    OSCILLATION = "oscillation"
    MAX_ITER_NO_CONVERGENCE = "max_iter_no_convergence"


def parse_failure_status(value: str) -> FailureStatus:
    try:
        return FailureStatus(value)
    except ValueError as exc:
        supported = ", ".join(status.value for status in FailureStatus)
        raise FailureTaxonomyError(
            f"Unsupported failure status `{value}`. Supported statuses: {supported}."
        ) from exc


@dataclass(frozen=True)
class FailureRecord:
    status: FailureStatus
    stage: str
    iteration_index: int
    message: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "stage": self.stage,
            "iteration_index": self.iteration_index,
            "message": self.message,
            "details": deepcopy(self.details),
        }


def failure_record_from_dict(raw_data: dict[str, Any]) -> FailureRecord:
    if not isinstance(raw_data, dict):
        raise FailureTaxonomyError("Failure record must be a mapping.")

    stage = raw_data.get("stage")
    if not isinstance(stage, str) or not stage.strip():
        raise FailureTaxonomyError("`stage` must be a non-empty string.")

    iteration_index = raw_data.get("iteration_index")
    if not isinstance(iteration_index, int) or isinstance(iteration_index, bool):
        raise FailureTaxonomyError("`iteration_index` must be an integer >= 1.")
    if iteration_index < 1:
        raise FailureTaxonomyError(
            f"`iteration_index` must be >= 1, got {iteration_index}."
        )

    message = raw_data.get("message")
    if not isinstance(message, str) or not message.strip():
        raise FailureTaxonomyError("`message` must be a non-empty string.")

    details = raw_data.get("details", {})
    if not isinstance(details, dict):
        raise FailureTaxonomyError("`details` must be a mapping when provided.")

    status_value = raw_data.get("status")
    if not isinstance(status_value, str):
        raise FailureTaxonomyError("`status` must be a string.")

    return FailureRecord(
        status=parse_failure_status(status_value),
        stage=stage.strip(),
        iteration_index=iteration_index,
        message=message.strip(),
        details=deepcopy(details),
    )
