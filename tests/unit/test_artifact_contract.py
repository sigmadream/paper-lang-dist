from __future__ import annotations

import json
from pathlib import Path

from rttdist.artifacts import (
    CuratedProblemReference,
    IterationArtifactRecord,
    MockOpenAIChoice,
    MockOpenAIMessage,
    MockOpenAIRequest,
    MockOpenAIResponse,
    MockOpenAIUsage,
    RunArtifactRecord,
    build_iteration_artifact_paths,
    build_run_metadata,
)
from rttdist.failure_taxonomy import FailureRecord, FailureStatus


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "contracts" / "artifacts"
CURATED_PROBLEM_ROOT = (
    REPO_ROOT / "tests" / "fixtures" / "curated_problem" / "IPOP_1436"
)


def test_run_artifact_contract_matches_golden_success_fixture() -> None:
    problem = _build_curated_problem_reference()
    metadata = build_run_metadata(
        run_id="smoke",
        problem=problem,
        target_language="python",
        max_iterations=20,
    )
    iteration_paths = build_iteration_artifact_paths(
        run_id="smoke",
        problem_id=problem.problem_id,
        target_language="python",
        iteration_index=1,
    )
    iteration = IterationArtifactRecord(
        iteration_index=1,
        result=FailureRecord(
            status=FailureStatus.SUCCESS,
            stage="completed",
            iteration_index=1,
            message="Round-trip translation satisfied the curated sample contract.",
            details={
                "fixture_input_path": problem.fixture_input_path,
                "fixture_output_path": problem.fixture_output_path,
            },
        ),
        artifact_paths=iteration_paths,
        openai_request=_build_openai_request(
            problem=problem, target_language="python", iteration_index=1
        ),
        openai_response=MockOpenAIResponse(
            response_id="mock-response-001",
            model="gpt-4o-mini",
            choices=(
                MockOpenAIChoice(
                    index=0,
                    message=MockOpenAIMessage(
                        role="assistant",
                        content="```python\nprint(666)\n```",
                    ),
                    finish_reason="stop",
                ),
            ),
            usage=MockOpenAIUsage(
                prompt_tokens=123,
                completion_tokens=21,
                total_tokens=144,
            ),
        ),
    )

    actual = RunArtifactRecord(metadata=metadata, iterations=(iteration,)).to_dict()

    assert actual == _load_json(CONTRACT_FIXTURE_ROOT / "success_run_contract.json")


def test_iteration_artifact_contract_matches_golden_compile_failure_fixture() -> None:
    problem = _build_curated_problem_reference()
    iteration_paths = build_iteration_artifact_paths(
        run_id="smoke",
        problem_id=problem.problem_id,
        target_language="java",
        iteration_index=2,
    )

    actual = IterationArtifactRecord(
        iteration_index=2,
        result=FailureRecord(
            status=FailureStatus.COMPILE_ERROR,
            stage="compile",
            iteration_index=2,
            message="Translated Java source did not compile against the curated fixture harness.",
            details={
                "compiler": "javac",
                "log_path": iteration_paths.compile_log_path,
            },
        ),
        artifact_paths=iteration_paths,
        openai_request=_build_openai_request(
            problem=problem, target_language="java", iteration_index=2
        ),
        openai_response=MockOpenAIResponse(
            response_id="mock-response-002",
            model="gpt-4o-mini",
            choices=(
                MockOpenAIChoice(
                    index=0,
                    message=MockOpenAIMessage(
                        role="assistant",
                        content=(
                            "```java\n"
                            "public class Main {\n"
                            "    public static void main(String[] args) {\n"
                            '        System.out.println("666")\n'
                            "    }\n"
                            "}\n"
                            "```"
                        ),
                    ),
                    finish_reason="stop",
                ),
            ),
            usage=MockOpenAIUsage(
                prompt_tokens=131,
                completion_tokens=38,
                total_tokens=169,
            ),
        ),
    ).to_dict()

    assert actual == _load_json(
        CONTRACT_FIXTURE_ROOT / "compile_failure_iteration_contract.json"
    )


def _build_curated_problem_reference() -> CuratedProblemReference:
    base_path = Path("tests") / "fixtures" / "curated_problem" / "IPOP_1436"
    return CuratedProblemReference(
        problem_id="IPOP_1436",
        statement_path=(base_path / "statement.md").as_posix(),
        fixture_input_path=(base_path / "1.inp").as_posix(),
        fixture_output_path=(base_path / "1.out").as_posix(),
        seed_source_path=(base_path / "reference.cpp").as_posix(),
    )


def _build_openai_request(
    *,
    problem: CuratedProblemReference,
    target_language: str,
    iteration_index: int,
) -> MockOpenAIRequest:
    target_name = target_language.capitalize()
    return MockOpenAIRequest(
        model="gpt-4o-mini",
        temperature=0.0,
        messages=(
            MockOpenAIMessage(
                role="system",
                content=(
                    "Translate the provided C++ solution into "
                    f"{target_name} while preserving the curated sample I/O behavior."
                ),
            ),
            MockOpenAIMessage(
                role="user",
                content=_build_user_prompt(problem),
            ),
        ),
        metadata={
            "problem_id": problem.problem_id,
            "seed_language": "cpp",
            "target_language": target_language,
            "iteration_index": iteration_index,
            "fixture_input_path": problem.fixture_input_path,
            "fixture_output_path": problem.fixture_output_path,
        },
    )


def _build_user_prompt(problem: CuratedProblemReference) -> str:
    statement = (REPO_ROOT / problem.statement_path).read_text(encoding="utf-8").strip()
    sample_input = (
        (REPO_ROOT / problem.fixture_input_path).read_text(encoding="utf-8").strip()
    )
    sample_output = (
        (REPO_ROOT / problem.fixture_output_path).read_text(encoding="utf-8").strip()
    )
    seed_source = (
        (REPO_ROOT / problem.seed_source_path).read_text(encoding="utf-8").rstrip()
    )

    return (
        f"Problem: {problem.problem_id}\n"
        f"Statement:\n{statement}\n"
        f"Sample input:\n{sample_input}\n"
        f"Expected output:\n{sample_output}\n"
        "Reference C++:\n"
        f"```cpp\n{seed_source}\n```"
    )


def _load_json(path: Path) -> dict[str, object]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


import pytest

from rttdist.artifacts import (
    ArtifactContractError,
    build_iteration_artifact_paths,
    build_run_directory,
    build_run_metadata,
)


class TestPathTraversalRejection:
    def test_run_id_rejects_forward_slash_separator(self) -> None:
        problem = _build_curated_problem_reference()
        with pytest.raises(ArtifactContractError, match=r"path separators"):
            build_run_metadata(
                run_id="run/segment",
                problem=problem,
                target_language="python",
                max_iterations=1,
            )

    def test_run_id_rejects_windows_backslash_separator(self) -> None:
        problem = _build_curated_problem_reference()
        with pytest.raises(ArtifactContractError, match=r"path separators"):
            build_run_metadata(
                run_id=r"run\\segment",
                problem=problem,
                target_language="python",
                max_iterations=1,
            )

    def test_run_id_rejects_parent_directory(self) -> None:
        problem = _build_curated_problem_reference()
        with pytest.raises(ArtifactContractError, match=r"path traversal"):
            build_run_metadata(
                run_id="../etc/passwd",
                problem=problem,
                target_language="python",
                max_iterations=1,
            )

    def test_run_id_rejects_double_dot(self) -> None:
        problem = _build_curated_problem_reference()
        with pytest.raises(ArtifactContractError, match=r"path traversal"):
            build_run_metadata(
                run_id="foo/bar/../../etc",
                problem=problem,
                target_language="python",
                max_iterations=1,
            )

    def test_run_id_rejects_absolute_path(self) -> None:
        problem = _build_curated_problem_reference()
        with pytest.raises(ArtifactContractError, match=r"absolute path"):
            build_run_metadata(
                run_id="/etc/passwd",
                problem=problem,
                target_language="python",
                max_iterations=1,
            )

    def test_problem_id_rejects_parent_directory(self) -> None:
        with pytest.raises(ArtifactContractError, match=r"path traversal"):
            build_run_directory("run1", "../../../etc", "python")

    def test_problem_id_rejects_absolute_path(self) -> None:
        with pytest.raises(ArtifactContractError, match=r"absolute path"):
            build_run_directory("run1", "/etc/passwd", "python")

    def test_iteration_artifact_paths_rejects_path_traversal_run_id(self) -> None:
        with pytest.raises(ArtifactContractError, match=r"path traversal"):
            build_iteration_artifact_paths(
                run_id="../foo",
                problem_id="IPOP_1436",
                target_language="python",
                iteration_index=1,
            )

    def test_iteration_artifact_paths_rejects_path_traversal_problem_id(self) -> None:
        with pytest.raises(ArtifactContractError, match=r"path traversal"):
            build_iteration_artifact_paths(
                run_id="run1",
                problem_id="../../etc",
                target_language="python",
                iteration_index=1,
            )
