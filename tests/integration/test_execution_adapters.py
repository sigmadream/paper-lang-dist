from __future__ import annotations

from pathlib import Path

from rttdist.corpus import FixturePair, ProblemCorpusEntry
from rttdist.exec import ExecutionStatus, evaluate_source, get_execution_adapter


def test_adapter_factory_supports_all_required_languages() -> None:
    assert get_execution_adapter("c").language == "c"
    assert get_execution_adapter("cpp").language == "cpp"
    assert get_execution_adapter("java").language == "java"
    assert get_execution_adapter("python").language == "python"


def test_python_adapter_classifies_wrong_answer(tmp_path: Path) -> None:
    source_path = tmp_path / "wrong.py"
    source_path.write_text("print(123)\n", encoding="utf-8")
    problem = _build_problem_entry(tmp_path, expected_output="666\n")

    result = evaluate_source(
        language="python",
        source_path=source_path,
        problem=problem,
        workspace_root=tmp_path / "workspace",
        timeout_seconds=2,
    )

    assert result.status == ExecutionStatus.WRONG_ANSWER
    assert len(result.fixture_results) == 1
    assert result.fixture_results[0].status == ExecutionStatus.WRONG_ANSWER


def test_python_adapter_classifies_runtime_error_and_captures_stderr(
    tmp_path: Path,
) -> None:
    source_path = tmp_path / "runtime_error.py"
    source_path.write_text("raise RuntimeError('boom')\n", encoding="utf-8")
    problem = _build_problem_entry(tmp_path, expected_output="666\n")

    result = evaluate_source(
        language="python",
        source_path=source_path,
        problem=problem,
        workspace_root=tmp_path / "workspace",
        timeout_seconds=2,
    )

    assert result.status == ExecutionStatus.RUNTIME_ERROR
    assert len(result.fixture_results) == 1
    fixture = result.fixture_results[0]
    assert fixture.status == ExecutionStatus.RUNTIME_ERROR
    assert fixture.exit_code is not None and fixture.exit_code != 0
    assert "RuntimeError" in fixture.stderr


def test_timeout_case_returns_timeout_without_hanging(tmp_path: Path) -> None:
    source_path = tmp_path / "timeout.py"
    source_path.write_text("while True:\n    pass\n", encoding="utf-8")
    problem = _build_problem_entry(tmp_path, expected_output="666\n")

    result = evaluate_source(
        language="python",
        source_path=source_path,
        problem=problem,
        workspace_root=tmp_path / "workspace",
        timeout_seconds=1,
    )

    assert result.status == ExecutionStatus.TIMEOUT
    assert len(result.fixture_results) == 1
    fixture = result.fixture_results[0]
    assert fixture.status == ExecutionStatus.TIMEOUT
    assert fixture.exit_code is None


def _build_problem_entry(tmp_path: Path, *, expected_output: str) -> ProblemCorpusEntry:
    fixture_directory = tmp_path / "problem" / "IPOP_TEST"
    fixture_directory.mkdir(parents=True)

    input_path = fixture_directory / "1.inp"
    output_path = fixture_directory / "1.out"
    input_path.write_text("1\n", encoding="utf-8")
    output_path.write_text(expected_output, encoding="utf-8")

    statement_path = tmp_path / "problem" / "IPOP_TEST.md"
    statement_path.write_text("dummy statement\n", encoding="utf-8")

    seed_path = tmp_path / "corpus" / "solutions" / "IPOP_TEST" / "reference.cpp"
    seed_path.parent.mkdir(parents=True)
    seed_path.write_text("int main(){return 0;}\n", encoding="utf-8")

    return ProblemCorpusEntry(
        problem_id="IPOP_TEST",
        statement_path=statement_path,
        fixture_directory=fixture_directory,
        fixture_pairs=(FixturePair(input_path=input_path, output_path=output_path),),
        seed_path=seed_path,
    )
