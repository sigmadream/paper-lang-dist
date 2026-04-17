from __future__ import annotations

from collections.abc import Sequence
from contextlib import contextmanager
from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import TYPE_CHECKING, Any, cast

from rttdist.artifacts import (
    CuratedProblemReference,
    build_iteration_artifact_paths,
    build_run_metadata,
)
from rttdist.failure_taxonomy import FailureRecord, FailureStatus
from rttdist.moss import MossSimilarityMatch
from rttdist.reporting import ReportingError, generate_run_summary, write_run_summary

if TYPE_CHECKING:
    from rttdist.pipeline import RTTRunResult


@dataclass(frozen=True)
class _RunResultStub:
    run_manifest_path: Path


def test_schema_version_summary_fields_include_status_iterations_semantics_ast_and_complexity(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "artifacts"
    output_root.mkdir(parents=True)
    problem = _create_problem_reference(tmp_path, problem_id="IPOP_SUMMARY")
    run_id = "summary-fields"

    iter1_result = FailureRecord(
        status=FailureStatus.SUCCESS,
        stage="iteration",
        iteration_index=1,
        message="Iteration completed; continuing.",
        details={"convergence_status": "continue"},
    )
    iter2_result = FailureRecord(
        status=FailureStatus.SUCCESS,
        stage="convergence",
        iteration_index=2,
        message="Fixed point reached.",
        details={"convergence_status": "fixed_point"},
    )

    iteration_payloads = [
        _write_iteration_artifacts(
            output_root=output_root,
            run_id=run_id,
            problem_id=problem.problem_id,
            target_language="python",
            iteration_index=1,
            result=iter1_result,
            target_source=(
                "def solve(x):\n    if x > 0:\n        return x\n    return 0\n"
            ),
            roundtrip_source=(
                "int solve(int x){\n"
                "    if (x > 0) {\n"
                "        return x;\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            execution_payload={
                "target": _execution_stage_payload(status="success"),
                "roundtrip_cpp": _execution_stage_payload(status="success"),
            },
            metrics_payload={
                "residual_similarity": 0.8,
                "convergence_status": "continue",
            },
        ),
        _write_iteration_artifacts(
            output_root=output_root,
            run_id=run_id,
            problem_id=problem.problem_id,
            target_language="python",
            iteration_index=2,
            result=iter2_result,
            target_source=(
                "def helper(x):\n"
                "    return x\n\n"
                "def solve(x):\n"
                "    if x > 0:\n"
                "        return helper(x)\n"
                "    return 0\n"
            ),
            roundtrip_source=(
                "int solve(int x){\n"
                "    if (x > 0) {\n"
                "        return x;\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
            execution_payload={
                "target": _execution_stage_payload(status="success"),
                "roundtrip_cpp": _execution_stage_payload(status="success"),
            },
            metrics_payload={
                "residual_similarity": 1.0,
                "convergence_status": "fixed_point",
            },
        ),
    ]
    _write_run_manifest(
        output_root=output_root,
        run_id=run_id,
        problem=problem,
        target_language="python",
        final_result=iter2_result,
        iteration_payloads=iteration_payloads,
    )

    summary = generate_run_summary(output_root=output_root, run_id=run_id)

    assert summary["schema_version"] == "report_summary.v2"
    assert summary["result_count"] == 1
    entry = summary["results"][0]
    assert entry["problem_id"] == "IPOP_SUMMARY"
    assert entry["seed_language"] == "cpp"
    assert entry["target_language"] == "python"
    assert entry["ordered_pair_key"] == "cpp->python"
    assert entry["final_status"] == "success"
    assert entry["iteration_count"] == 2
    assert entry["change_count_distance"] == {
        "availability": "measured",
        "value": 2,
        "unit": "cpp_to_target_to_cpp_cycles",
        "definition": "1 cycle = C++ -> target -> C++",
    }
    assert entry["convergence_outcome"] == "fixed_point"
    assert entry["residual_similarity"] == {
        "availability": "measured",
        "value": 1.0,
    }
    assert entry["semantic_summary"]["overall"] == "pass"
    assert entry["semantic_summary"]["target"]["status"] == "success"
    assert entry["ast_distance"]["availability"] == "measured"
    assert entry["ast_distance"]["value"]["distance_to_seed_cpp"] is not None
    assert entry["complexity_deltas"]["target"]["availability"] == "measured"
    assert (
        entry["complexity_deltas"]["target"]["value"]["delta_vs_previous"] is not None
    )
    assert entry["complexity_deltas"]["roundtrip_cpp"]["value"][
        "delta_vs_seed_cpp"
    ] == {
        "loc": 0,
        "token_count": 0,
        "cyclomatic_complexity": 0,
        "function_count": 0,
        "max_nesting_depth": 0,
    }
    assert summary["ordered_pair_aggregates"]["cpp->python"] == {
        "ordered_pair_key": "cpp->python",
        "seed_language": "cpp",
        "target_language": "python",
        "result_count": 1,
        "change_count_distance": {
            "availability": "measured",
            "mean": 2.0,
            "stddev": 0.0,
            "measured_count": 1,
            "unavailable_count": 0,
            "infrastructure_count": 0,
            "denominator": 1,
        },
        "residual_similarity": {
            "availability": "measured",
            "mean": 1.0,
            "stddev": 0.0,
            "measured_count": 1,
            "unavailable_count": 0,
            "infrastructure_count": 0,
            "denominator": 1,
        },
        "final_similarity_score": {
            "availability": "unavailable",
            "reason": "no_measured_values",
            "measured_count": 0,
            "unavailable_count": 1,
            "infrastructure_count": 0,
            "denominator": 0,
        },
        "divergence": {
            "availability": "measured",
            "divergence_rate": 0.0,
            "divergent_count": 0,
            "non_divergent_count": 1,
            "measured_count": 1,
            "unavailable_count": 0,
            "infrastructure_count": 0,
            "denominator": 1,
        },
    }

    artifacts = write_run_summary(output_root=output_root, run_id=run_id)
    assert (
        json.loads(artifacts.summary_json_path.read_text(encoding="utf-8")) == summary
    )

    markdown = artifacts.summary_markdown_path.read_text(encoding="utf-8")
    assert "# Run Summary: summary-fields" in markdown
    assert "## Ordered-pair aggregates" in markdown
    assert "### Ordered pair: cpp->python" in markdown
    assert "Change-count distance (1 cycle = C++ -> target -> C++): 2" in markdown
    assert "Residual similarity to seed C++: 1.000000" in markdown
    assert "Semantic summary: pass" in markdown
    assert "AST distance:" in markdown
    assert "Target complexity deltas:" in markdown


def test_failed_metric_inputs_are_rendered_explicitly_in_summary_outputs(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "artifacts"
    output_root.mkdir(parents=True)
    problem = _create_problem_reference(tmp_path, problem_id="IPOP_FAILURE")
    run_id = "summary-failure"

    failure_result = FailureRecord(
        status=FailureStatus.API_ERROR,
        stage="cpp_to_target_translation",
        iteration_index=1,
        message="Translation step failed.",
        details={"error_type": "RuntimeError", "error": "mock translation failure"},
    )
    iteration_payload = _write_iteration_artifacts(
        output_root=output_root,
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language="python",
        iteration_index=1,
        result=failure_result,
        target_source="",
        roundtrip_source="",
        execution_payload={"target": None, "roundtrip_cpp": None},
        metrics_payload={"residual_similarity": None, "convergence_status": "continue"},
    )
    _write_run_manifest(
        output_root=output_root,
        run_id=run_id,
        problem=problem,
        target_language="python",
        final_result=failure_result,
        iteration_payloads=[iteration_payload],
    )

    summary = generate_run_summary(output_root=output_root, run_id=run_id)
    entry = summary["results"][0]

    assert entry["final_status"] == "api_error"
    assert entry["convergence_outcome"] == "terminated_on_failure"
    assert entry["change_count_distance"] == {
        "availability": "measured",
        "value": 0,
        "unit": "cpp_to_target_to_cpp_cycles",
        "definition": "1 cycle = C++ -> target -> C++",
    }
    assert entry["semantic_summary"]["overall"] == "fail"
    assert entry["semantic_summary"]["target"] == {
        "available": False,
        "status": "not_evaluated",
        "passed": False,
        "fixture_pass_count": 0,
        "fixture_fail_count": 0,
        "message": "stage_not_executed",
    }
    assert entry["residual_similarity"] == {
        "availability": "unavailable",
        "reason": "residual_similarity_not_recorded",
        "failure": {
            "status": "api_error",
            "stage": "cpp_to_target_translation",
            "iteration_index": 1,
        },
    }
    assert entry["ast_distance"] == {
        "availability": "unavailable",
        "reason": "missing_target_source",
        "failure": {
            "status": "api_error",
            "stage": "cpp_to_target_translation",
            "iteration_index": 1,
        },
    }
    assert entry["complexity_deltas"]["target"] == {
        "availability": "unavailable",
        "reason": "missing_target_source",
        "failure": {
            "status": "api_error",
            "stage": "cpp_to_target_translation",
            "iteration_index": 1,
        },
    }
    assert entry["complexity_deltas"]["roundtrip_cpp"] == {
        "availability": "unavailable",
        "reason": "missing_roundtrip_cpp_source",
        "failure": {
            "status": "api_error",
            "stage": "cpp_to_target_translation",
            "iteration_index": 1,
        },
    }

    artifacts = write_run_summary(output_root=output_root, run_id=run_id)
    markdown = artifacts.summary_markdown_path.read_text(encoding="utf-8")
    assert "Change-count distance (1 cycle = C++ -> target -> C++): 0" in markdown
    assert (
        "Residual similarity to seed C++: unavailable (api_error at cpp_to_target_translation)"
        in markdown
    )
    assert (
        "AST distance: unavailable (api_error at cpp_to_target_translation)" in markdown
    )
    assert (
        "Roundtrip C++ complexity deltas: unavailable (api_error at cpp_to_target_translation)"
        in markdown
    )


def test_summary_can_include_opt_in_moss_similarity(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "artifacts"
    output_root.mkdir(parents=True)
    problem = _create_problem_reference(tmp_path, problem_id="IPOP_MOSS")
    run_id = "summary-moss"

    result = FailureRecord(
        status=FailureStatus.SUCCESS,
        stage="convergence",
        iteration_index=1,
        message="Fixed point reached.",
        details={"convergence_status": "fixed_point"},
    )
    iteration_payload = _write_iteration_artifacts(
        output_root=output_root,
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language="python",
        iteration_index=1,
        result=result,
        target_source="print(1)",
        roundtrip_source="int solve(int x){ return x; }",
        execution_payload={
            "target": _execution_stage_payload(status="success"),
            "roundtrip_cpp": _execution_stage_payload(status="success"),
        },
        metrics_payload={
            "residual_similarity": 1.0,
            "convergence_status": "fixed_point",
        },
    )
    _write_run_manifest(
        output_root=output_root,
        run_id=run_id,
        problem=problem,
        target_language="python",
        final_result=result,
        iteration_payloads=[iteration_payload],
    )

    def _fake_moss(
        seed_cpp_source: str,
        roundtrip_cpp_source: str,
        label: str,
    ) -> MossSimilarityMatch:
        assert "return x;" in seed_cpp_source
        assert "return x;" in roundtrip_cpp_source
        assert label == "rttdist:IPOP_MOSS/python"
        return MossSimilarityMatch(
            report_url="http://moss.stanford.edu/results/1/2",
            match_url="http://moss.stanford.edu/results/1/2/match0.html",
            seed_percentage=91,
            roundtrip_percentage=88,
        )

    summary = generate_run_summary(
        output_root=output_root,
        run_id=run_id,
        moss_similarity_fn=_fake_moss,
    )

    entry = summary["results"][0]
    assert entry["moss_similarity"] == {
        "availability": "measured",
        "value": {
            "seed_percentage": 91,
            "roundtrip_percentage": 88,
            "report_url": "http://moss.stanford.edu/results/1/2",
            "match_url": "http://moss.stanford.edu/results/1/2/match0.html",
        },
    }

    artifacts = write_run_summary(
        output_root=output_root,
        run_id=run_id,
        moss_similarity_fn=_fake_moss,
    )
    markdown = artifacts.summary_markdown_path.read_text(encoding="utf-8")
    assert "MOSS similarity to seed C++: seed=91%, roundtrip=88%" in markdown
    assert (
        "| IPOP_MOSS | cpp->python | success | 1 | 1 | fixed_point | 1.000000 | seed=91%, roundtrip=88% | pass |"
        in markdown
    )


def test_ordered_pair_aggregates_keep_reverse_directions_and_divergence_denominator_rules(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "artifacts"
    output_root.mkdir(parents=True)
    problem = _create_problem_reference(tmp_path, problem_id="IPOP_ORDERED_PAIR")
    run_id = "summary-ordered-pair"

    fixed_point_success = FailureRecord(
        status=FailureStatus.SUCCESS,
        stage="convergence",
        iteration_index=1,
        message="Fixed point reached.",
        details={"convergence_status": "fixed_point"},
    )
    max_iter_result = FailureRecord(
        status=FailureStatus.MAX_ITER_NO_CONVERGENCE,
        stage="convergence",
        iteration_index=1,
        message="Iteration cap reached.",
        details={"convergence_status": "continue"},
    )
    infrastructure_failure = FailureRecord(
        status=FailureStatus.API_ERROR,
        stage="cpp_to_target_translation",
        iteration_index=1,
        message="Provider unavailable.",
        details={"error": "upstream failure"},
    )

    cpp_python_success = _write_iteration_artifacts(
        output_root=output_root,
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language="python",
        iteration_index=1,
        result=fixed_point_success,
        target_source="print(1)",
        roundtrip_source="int solve(int x){ return x; }",
        execution_payload={
            "target": _execution_stage_payload(status="success"),
            "roundtrip_cpp": _execution_stage_payload(status="success"),
        },
        metrics_payload={
            "residual_similarity": 1.0,
            "convergence_status": "fixed_point",
        },
    )
    _write_run_manifest(
        output_root=output_root,
        run_id=run_id,
        problem=problem,
        target_language="python",
        final_result=fixed_point_success,
        iteration_payloads=[cpp_python_success],
        seed_language="cpp",
    )

    cpp_python_max_iter = _write_iteration_artifacts(
        output_root=output_root,
        run_id=run_id,
        problem_id=f"{problem.problem_id}_MAX_ITER",
        target_language="python",
        iteration_index=1,
        result=max_iter_result,
        target_source="print(2)",
        roundtrip_source="int solve(int x){ return x + 1; }",
        execution_payload={
            "target": _execution_stage_payload(status="success"),
            "roundtrip_cpp": _execution_stage_payload(status="success"),
        },
        metrics_payload={"residual_similarity": 0.4, "convergence_status": "continue"},
    )
    _write_run_manifest(
        output_root=output_root,
        run_id=run_id,
        problem=_create_problem_reference(
            tmp_path, problem_id="IPOP_ORDERED_PAIR_MAX_ITER"
        ),
        target_language="python",
        final_result=max_iter_result,
        iteration_payloads=[cpp_python_max_iter],
        seed_language="cpp",
    )

    cpp_python_api_error = _write_iteration_artifacts(
        output_root=output_root,
        run_id=run_id,
        problem_id=f"{problem.problem_id}_INFRA",
        target_language="python",
        iteration_index=1,
        result=infrastructure_failure,
        target_source="",
        roundtrip_source="",
        execution_payload={"target": None, "roundtrip_cpp": None},
        metrics_payload={"residual_similarity": None, "convergence_status": "continue"},
    )
    _write_run_manifest(
        output_root=output_root,
        run_id=run_id,
        problem=_create_problem_reference(
            tmp_path, problem_id="IPOP_ORDERED_PAIR_INFRA"
        ),
        target_language="python",
        final_result=infrastructure_failure,
        iteration_payloads=[cpp_python_api_error],
        seed_language="cpp",
    )

    python_cpp_success = _write_iteration_artifacts(
        output_root=output_root,
        run_id=run_id,
        problem_id=f"{problem.problem_id}_REVERSE",
        target_language="cpp",
        iteration_index=1,
        result=fixed_point_success,
        target_source="int solve(int x){ return x; }",
        roundtrip_source="int solve(int x){ return x; }",
        execution_payload={
            "target": _execution_stage_payload(status="success"),
            "roundtrip_cpp": _execution_stage_payload(status="success"),
        },
        metrics_payload={
            "residual_similarity": 1.0,
            "convergence_status": "fixed_point",
        },
        seed_language="python",
    )
    _write_run_manifest(
        output_root=output_root,
        run_id=run_id,
        problem=_create_problem_reference(
            tmp_path, problem_id="IPOP_ORDERED_PAIR_REVERSE"
        ),
        target_language="cpp",
        final_result=fixed_point_success,
        iteration_payloads=[python_cpp_success],
        seed_language="python",
    )

    summary = generate_run_summary(output_root=output_root, run_id=run_id)
    aggregates = summary["ordered_pair_aggregates"]

    assert sorted(aggregates) == ["cpp->python", "python->cpp"]

    cpp_python = aggregates["cpp->python"]
    assert cpp_python["result_count"] == 3
    assert cpp_python["change_count_distance"]["mean"] == 2.0 / 3.0
    assert cpp_python["change_count_distance"]["measured_count"] == 3
    assert cpp_python["residual_similarity"]["measured_count"] == 2
    assert cpp_python["residual_similarity"]["unavailable_count"] == 1
    assert cpp_python["residual_similarity"]["infrastructure_count"] == 1
    assert cpp_python["divergence"] == {
        "availability": "measured",
        "divergence_rate": 0.5,
        "divergent_count": 1,
        "non_divergent_count": 1,
        "measured_count": 2,
        "unavailable_count": 1,
        "infrastructure_count": 1,
        "denominator": 2,
    }

    python_cpp = aggregates["python->cpp"]
    assert python_cpp["result_count"] == 1
    assert python_cpp["residual_similarity"] == {
        "availability": "unavailable",
        "reason": "no_measured_values",
        "measured_count": 0,
        "unavailable_count": 1,
        "infrastructure_count": 0,
        "denominator": 0,
    }
    assert python_cpp["divergence"]["divergence_rate"] == 0.0

    artifacts = write_run_summary(output_root=output_root, run_id=run_id)
    markdown = artifacts.summary_markdown_path.read_text(encoding="utf-8")
    assert "| IPOP_ORDERED_PAIR | cpp->python | success |" in markdown
    assert "| IPOP_ORDERED_PAIR_REVERSE | python->cpp | success |" in markdown
    assert "| cpp->python | 3 | 0.500000 | 2 | 1 | 1 |" in markdown
    assert "| python->cpp | 1 | 0.000000 | 1 | 0 | 0 |" in markdown


def test_summary_surfaces_moss_failures_without_breaking_report(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "artifacts"
    output_root.mkdir(parents=True)
    problem = _create_problem_reference(tmp_path, problem_id="IPOP_MOSS_FAIL")
    run_id = "summary-moss-fail"

    result = FailureRecord(
        status=FailureStatus.SUCCESS,
        stage="convergence",
        iteration_index=1,
        message="Fixed point reached.",
        details={"convergence_status": "fixed_point"},
    )
    iteration_payload = _write_iteration_artifacts(
        output_root=output_root,
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language="python",
        iteration_index=1,
        result=result,
        target_source="print(1)",
        roundtrip_source="int solve(int x){ return x; }",
        execution_payload={
            "target": _execution_stage_payload(status="success"),
            "roundtrip_cpp": _execution_stage_payload(status="success"),
        },
        metrics_payload={
            "residual_similarity": 1.0,
            "convergence_status": "fixed_point",
        },
    )
    _write_run_manifest(
        output_root=output_root,
        run_id=run_id,
        problem=problem,
        target_language="python",
        final_result=result,
        iteration_payloads=[iteration_payload],
    )

    def _broken_moss(
        seed_cpp_source: str,
        roundtrip_cpp_source: str,
        label: str,
    ) -> MossSimilarityMatch:
        del seed_cpp_source
        del roundtrip_cpp_source
        del label
        raise RuntimeError("mock moss failure")

    summary = generate_run_summary(
        output_root=output_root,
        run_id=run_id,
        moss_similarity_fn=_broken_moss,
    )

    assert summary["results"][0]["moss_similarity"] == {
        "availability": "unavailable",
        "reason": "moss_execution_failed",
        "details": {"message": "mock moss failure"},
    }


def test_residual_similarity_is_unavailable_with_seed_language_not_cpp(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "artifacts"
    output_root.mkdir(parents=True)
    problem = _create_problem_reference(tmp_path, problem_id="IPOP_NON_CPP_SEED")
    run_id = "summary-non-cpp-seed"

    result = FailureRecord(
        status=FailureStatus.SUCCESS,
        stage="convergence",
        iteration_index=1,
        message="Fixed point reached.",
        details={"convergence_status": "fixed_point"},
    )
    iteration_payload = _write_iteration_artifacts(
        output_root=output_root,
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language="python",
        iteration_index=1,
        result=result,
        target_source="print(1)",
        roundtrip_source="int solve(int x){ return x; }",
        execution_payload={
            "target": _execution_stage_payload(status="success"),
            "roundtrip_cpp": _execution_stage_payload(status="success"),
        },
        metrics_payload={
            "residual_similarity": 1.0,
            "convergence_status": "fixed_point",
        },
    )
    _write_run_manifest(
        output_root=output_root,
        run_id=run_id,
        problem=problem,
        target_language="python",
        final_result=result,
        iteration_payloads=[iteration_payload],
        seed_language="python",
    )

    summary = generate_run_summary(output_root=output_root, run_id=run_id)

    assert summary["results"][0]["residual_similarity"] == {
        "availability": "unavailable",
        "reason": "seed_language_not_cpp",
        "failure": {
            "status": "success",
            "stage": "convergence",
            "iteration_index": 1,
        },
    }


def test_summary_records_zero_similarity_when_moss_reports_no_matches(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "artifacts"
    output_root.mkdir(parents=True)
    problem = _create_problem_reference(tmp_path, problem_id="IPOP_MOSS_ZERO")
    run_id = "summary-moss-zero"

    result = FailureRecord(
        status=FailureStatus.SUCCESS,
        stage="convergence",
        iteration_index=1,
        message="Fixed point reached.",
        details={"convergence_status": "fixed_point"},
    )
    iteration_payload = _write_iteration_artifacts(
        output_root=output_root,
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language="python",
        iteration_index=1,
        result=result,
        target_source="print(1)",
        roundtrip_source="int solve(int x){ return x; }",
        execution_payload={
            "target": _execution_stage_payload(status="success"),
            "roundtrip_cpp": _execution_stage_payload(status="success"),
        },
        metrics_payload={
            "residual_similarity": 1.0,
            "convergence_status": "fixed_point",
        },
    )
    _write_run_manifest(
        output_root=output_root,
        run_id=run_id,
        problem=problem,
        target_language="python",
        final_result=result,
        iteration_payloads=[iteration_payload],
    )

    def _zero_moss(
        seed_cpp_source: str,
        roundtrip_cpp_source: str,
        label: str,
    ) -> MossSimilarityMatch:
        del seed_cpp_source
        del roundtrip_cpp_source
        del label
        return MossSimilarityMatch(
            report_url="http://moss.stanford.edu/results/1/2",
            match_url=None,
            seed_percentage=0,
            roundtrip_percentage=0,
        )

    summary = generate_run_summary(
        output_root=output_root,
        run_id=run_id,
        moss_similarity_fn=_zero_moss,
    )

    assert summary["results"][0]["moss_similarity"] == {
        "availability": "measured",
        "value": {
            "seed_percentage": 0,
            "roundtrip_percentage": 0,
            "report_url": "http://moss.stanford.edu/results/1/2",
            "match_url": None,
        },
    }

    artifacts = write_run_summary(
        output_root=output_root,
        run_id=run_id,
        moss_similarity_fn=_zero_moss,
    )
    markdown = artifacts.summary_markdown_path.read_text(encoding="utf-8")
    assert "MOSS similarity to seed C++: seed=0%, roundtrip=0%" in markdown


def test_report_rejects_malicious_manifest_artifact_path(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "artifacts"
    output_root.mkdir(parents=True)
    problem = _create_problem_reference(tmp_path, problem_id="IPOP_REPORT_PATH_ESCAPE")
    run_id = "summary-path-escape"

    result = FailureRecord(
        status=FailureStatus.SUCCESS,
        stage="convergence",
        iteration_index=1,
        message="Fixed point reached.",
        details={"convergence_status": "fixed_point"},
    )
    iteration_payload = _write_iteration_artifacts(
        output_root=output_root,
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language="python",
        iteration_index=1,
        result=result,
        target_source="print(1)",
        roundtrip_source="int main(){return 0;}",
        execution_payload={
            "target": _execution_stage_payload(status="success"),
            "roundtrip_cpp": _execution_stage_payload(status="success"),
        },
        metrics_payload={
            "residual_similarity": 1.0,
            "convergence_status": "fixed_point",
        },
    )
    artifact_paths = iteration_payload["artifact_paths"]
    if not isinstance(artifact_paths, dict):
        raise AssertionError("artifact_paths payload should be a mapping.")
    artifact_paths["execution_result_path"] = "../../../../etc/passwd"
    _write_run_manifest(
        output_root=output_root,
        run_id=run_id,
        problem=problem,
        target_language="python",
        final_result=result,
        iteration_payloads=[iteration_payload],
    )

    with _assert_raises(ReportingError, match="Unsafe report path rejected"):
        generate_run_summary(output_root=output_root, run_id=run_id)


def test_legacy_seed_fallback_rejects_absolute_host_path(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "artifacts"
    output_root.mkdir(parents=True)
    problem = _create_problem_reference(tmp_path, problem_id="IPOP_LEGACY_SEED")
    run_id = "summary-legacy-seed-escape"

    result = FailureRecord(
        status=FailureStatus.SUCCESS,
        stage="convergence",
        iteration_index=1,
        message="Fixed point reached.",
        details={"convergence_status": "fixed_point"},
    )
    iteration_payload = _write_iteration_artifacts(
        output_root=output_root,
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language="python",
        iteration_index=1,
        result=result,
        target_source="print(1)",
        roundtrip_source="int main(){return 0;}",
        execution_payload={
            "target": _execution_stage_payload(status="success"),
            "roundtrip_cpp": _execution_stage_payload(status="success"),
        },
        metrics_payload={
            "residual_similarity": 1.0,
            "convergence_status": "fixed_point",
        },
    )
    _write_run_manifest(
        output_root=output_root,
        run_id=run_id,
        problem=problem,
        target_language="python",
        final_result=result,
        iteration_payloads=[iteration_payload],
    )

    metadata = build_run_metadata(
        run_id=run_id,
        problem=problem,
        target_language="python",
        seed_language="cpp",
        max_iterations=20,
    )
    manifest_path = output_root / metadata.run_metadata_path
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_metadata = manifest.get("metadata")
    if not isinstance(manifest_metadata, dict):
        raise AssertionError("metadata payload should be a mapping.")
    manifest_metadata.pop("seed_artifact_path", None)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    with _assert_raises(ReportingError, match="metadata.problem.seed_source_path"):
        generate_run_summary(output_root=output_root, run_id=run_id)


def test_report_rejects_run_results_manifest_path_outside_output_root(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "artifacts"
    output_root.mkdir(parents=True)
    outside_manifest = tmp_path / "outside" / "run.json"
    outside_manifest.parent.mkdir(parents=True, exist_ok=True)
    outside_manifest.write_text("{}", encoding="utf-8")

    with _assert_raises(ReportingError, match="run_manifest_path"):
        generate_run_summary(
            output_root=output_root,
            run_id="ignored-by-run-results",
            run_results=cast(
                Sequence["RTTRunResult"],
                [_RunResultStub(run_manifest_path=outside_manifest)],
            ),
        )


def test_write_run_summary_rejects_path_traversal_run_id(tmp_path: Path) -> None:
    output_root = tmp_path / "artifacts"
    output_root.mkdir(parents=True)

    with _assert_raises(ReportingError, match="escapes output root"):
        write_run_summary(output_root=output_root, run_id="../etc/passwd")


def test_generate_run_summary_rejects_path_traversal_run_id(tmp_path: Path) -> None:
    output_root = tmp_path / "artifacts"
    output_root.mkdir(parents=True)

    with _assert_raises(ReportingError, match="escapes output root"):
        generate_run_summary(output_root=output_root, run_id="../etc/passwd")


def test_write_run_summary_rejects_absolute_run_id(tmp_path: Path) -> None:
    output_root = tmp_path / "artifacts"
    output_root.mkdir(parents=True)

    with _assert_raises(ReportingError, match="must not be an absolute path"):
        write_run_summary(output_root=output_root, run_id="/tmp/malicious")


def test_write_run_summary_rejects_empty_run_id(tmp_path: Path) -> None:
    output_root = tmp_path / "artifacts"
    output_root.mkdir(parents=True)

    with _assert_raises(ReportingError, match="must be a non-empty string"):
        write_run_summary(output_root=output_root, run_id="   ")


@contextmanager
def _assert_raises(expected_exception: type[BaseException], *, match: str):
    try:
        yield
    except expected_exception as exc:
        if re.search(match, str(exc)) is None:
            raise AssertionError(
                f"Expected {expected_exception.__name__} message to match {match!r}, got {exc!r}."
            ) from exc
        return
    raise AssertionError(
        f"Expected {expected_exception.__name__} to be raised with match {match!r}."
    )


def _create_problem_reference(
    tmp_path: Path, *, problem_id: str
) -> CuratedProblemReference:
    problem_root = tmp_path / "problem" / problem_id
    problem_root.mkdir(parents=True, exist_ok=True)

    statement_path = tmp_path / "problem" / f"{problem_id}.md"
    statement_path.write_text("statement\n", encoding="utf-8")
    input_path = problem_root / "1.inp"
    output_path = problem_root / "1.out"
    input_path.write_text("1\n", encoding="utf-8")
    output_path.write_text("1\n", encoding="utf-8")

    seed_path = tmp_path / "corpus" / "solutions" / problem_id / "reference.cpp"
    seed_path.parent.mkdir(parents=True, exist_ok=True)
    seed_path.write_text(
        "int solve(int x){\n"
        "    if (x > 0) {\n"
        "        return x;\n"
        "    }\n"
        "    return 0;\n"
        "}\n",
        encoding="utf-8",
    )

    return CuratedProblemReference(
        problem_id=problem_id,
        statement_path=statement_path.as_posix(),
        fixture_input_path=input_path.as_posix(),
        fixture_output_path=output_path.as_posix(),
        seed_source_path=seed_path.as_posix(),
    )


def _write_run_manifest(
    *,
    output_root: Path,
    run_id: str,
    problem: CuratedProblemReference,
    target_language: str,
    final_result: FailureRecord,
    iteration_payloads: list[dict[str, Any]],
    seed_language: str = "cpp",
) -> None:
    metadata = build_run_metadata(
        run_id=run_id,
        problem=problem,
        target_language=target_language,
        seed_language=seed_language,
        max_iterations=20,
    )
    seed_artifact_path = Path(metadata.run_directory) / "seed" / "reference.cpp"
    source = Path(problem.seed_source_path).read_text(encoding="utf-8").rstrip()
    persisted_seed = output_root / seed_artifact_path
    persisted_seed.parent.mkdir(parents=True, exist_ok=True)
    persisted_seed.write_text(f"{source}\n", encoding="utf-8")

    manifest_path = output_root / metadata.run_metadata_path
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(
            {
                "metadata": {
                    **metadata.to_dict(),
                    "config_hash": "cfg-hash",
                    "seed_artifact_path": seed_artifact_path.as_posix(),
                    "created_at": "2026-03-18T00:00:00Z",
                    "updated_at": "2026-03-18T00:00:00Z",
                    "ended_at": "2026-03-18T00:00:01Z",
                },
                "status_transitions": [],
                "iterations": iteration_payloads,
                "final": final_result.to_dict(),
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )


def _write_iteration_artifacts(
    *,
    output_root: Path,
    run_id: str,
    problem_id: str,
    target_language: str,
    iteration_index: int,
    result: FailureRecord,
    target_source: str,
    roundtrip_source: str,
    execution_payload: dict[str, object],
    metrics_payload: dict[str, object],
    seed_language: str = "cpp",
) -> dict[str, Any]:
    paths = build_iteration_artifact_paths(
        run_id=run_id,
        problem_id=problem_id,
        target_language=target_language,
        seed_language=seed_language,
        iteration_index=iteration_index,
    )
    for relative_path, content in (
        (paths.translated_source_path, f"{target_source}\n"),
        (paths.roundtrip_source_path, f"{roundtrip_source}\n"),
        (paths.openai_request_path, json.dumps({"request": iteration_index}, indent=2)),
        (
            paths.openai_response_path,
            json.dumps({"response": iteration_index}, indent=2),
        ),
        (paths.compile_log_path, "compile log\n"),
        (
            paths.execution_result_path,
            json.dumps(execution_payload, indent=2, sort_keys=True),
        ),
        (paths.metrics_path, json.dumps(metrics_payload, indent=2, sort_keys=True)),
    ):
        path = output_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    iteration_payload: dict[str, Any] = {
        "iteration_index": iteration_index,
        "started_at": "2026-03-18T00:00:00Z",
        "ended_at": "2026-03-18T00:00:01Z",
        "result": result.to_dict(),
        "artifact_paths": paths.to_dict(),
    }
    iteration_metadata_path = output_root / paths.iteration_metadata_path
    iteration_metadata_path.write_text(
        json.dumps(iteration_payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return iteration_payload


def _execution_stage_payload(*, status: str) -> dict[str, object]:
    payload: dict[str, object] = {
        "status": status,
        "message": "ok" if status == "success" else "failed",
        "fixture_results": [
            {
                "fixture_stem": "1",
                "status": status,
            }
        ],
    }
    return payload
