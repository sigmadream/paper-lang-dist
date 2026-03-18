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


def test_summary_fields_include_status_iterations_semantics_ast_and_complexity(
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

    assert summary["schema_version"] == "report_summary.v1"
    assert summary["result_count"] == 1
    entry = summary["results"][0]
    assert entry["problem_id"] == "IPOP_SUMMARY"
    assert entry["target_language"] == "python"
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

    artifacts = write_run_summary(output_root=output_root, run_id=run_id)
    assert (
        json.loads(artifacts.summary_json_path.read_text(encoding="utf-8")) == summary
    )

    markdown = artifacts.summary_markdown_path.read_text(encoding="utf-8")
    assert "# Run Summary: summary-fields" in markdown
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
        "| IPOP_MOSS | python | success | 1 | 1 | fixed_point | 1.000000 | seed=91%, roundtrip=88% | pass |"
        in markdown
    )


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
) -> None:
    metadata = build_run_metadata(
        run_id=run_id,
        problem=problem,
        target_language=target_language,
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
) -> dict[str, Any]:
    paths = build_iteration_artifact_paths(
        run_id=run_id,
        problem_id=problem_id,
        target_language=target_language,
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
