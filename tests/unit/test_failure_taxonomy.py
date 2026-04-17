from __future__ import annotations

import json
from pathlib import Path

import pytest

from rttdist.failure_taxonomy import (
    FailureRecord,
    FailureStatus,
    FailureTaxonomyError,
    failure_record_from_dict,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
FAILURE_FIXTURE_PATH = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "contracts"
    / "failure_taxonomy"
    / "all_statuses.json"
)


def test_failure_taxonomy_matches_golden_fixture() -> None:
    actual = [record.to_dict() for record in _build_failure_records()]

    assert actual == _load_json(FAILURE_FIXTURE_PATH)


def test_failure_taxonomy_round_trips_from_fixture_json() -> None:
    expected = _load_json(FAILURE_FIXTURE_PATH)
    actual = [failure_record_from_dict(item).to_dict() for item in expected]

    assert actual == expected


def test_failure_taxonomy_rejects_unknown_status() -> None:
    with pytest.raises(FailureTaxonomyError) as excinfo:
        failure_record_from_dict(
            {
                "status": "unexpected_failure_status",
                "stage": "translation",
                "iteration_index": 1,
                "message": "Mock response failed.",
                "details": {},
            }
        )

    assert "Unsupported failure status" in str(excinfo.value)


def _build_failure_records() -> list[FailureRecord]:
    return [
        FailureRecord(
            status=FailureStatus.SUCCESS,
            stage="completed",
            iteration_index=1,
            message="Round-trip translation satisfied the curated sample contract.",
            details={
                "sample_output_file": "tests/fixtures/curated_problem/IPOP_1436/1.out",
            },
        ),
        FailureRecord(
            status=FailureStatus.API_ERROR,
            stage="translation",
            iteration_index=2,
            message="LLM API request failed due to a transport outage.",
            details={
                "error_type": "LMStudioClientError",
                "error": "connection reset",
            },
        ),
        FailureRecord(
            status=FailureStatus.PARSE_ERROR,
            stage="translation",
            iteration_index=2,
            message="LLM response parsing failed for fenced code extraction.",
            details={
                "error_type": "LMStudioResponseParseError",
                "error": "missing choices",
            },
        ),
        FailureRecord(
            status=FailureStatus.COMPILE_ERROR,
            stage="compile",
            iteration_index=2,
            message="Translated source failed to compile for the target language.",
            details={
                "compiler": "javac",
                "log_path": "smoke/IPOP_1436/java/iterations/iter-002/compile.log",
            },
        ),
        FailureRecord(
            status=FailureStatus.RUNTIME_ERROR,
            stage="execution",
            iteration_index=3,
            message="Program exited with a runtime error while running fixtures.",
            details={
                "exit_code": 1,
                "stderr": "segmentation fault",
            },
        ),
        FailureRecord(
            status=FailureStatus.WRONG_ANSWER,
            stage="execution",
            iteration_index=3,
            message="Program output did not match the curated sample output.",
            details={
                "expected_output_path": "tests/fixtures/curated_problem/IPOP_1436/1.out",
                "actual_output": "667",
            },
        ),
        FailureRecord(
            status=FailureStatus.TIMEOUT,
            stage="execution",
            iteration_index=4,
            message="Program exceeded the configured execution timeout.",
            details={
                "timeout_seconds": 30,
            },
        ),
        FailureRecord(
            status=FailureStatus.OSCILLATION,
            stage="convergence",
            iteration_index=6,
            message="Normalized round-trip hashes repeated with period 2.",
            details={
                "hash_cycle": ["hash-a", "hash-b", "hash-a"],
            },
        ),
        FailureRecord(
            status=FailureStatus.MAX_ITER_NO_CONVERGENCE,
            stage="convergence",
            iteration_index=20,
            message="Iteration cap was reached before convergence.",
            details={
                "max_iterations": 20,
            },
        ),
    ]


def _load_json(path: Path) -> list[dict[str, object]]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)
