from __future__ import annotations

from pathlib import Path

from rttdist.corpus import FixturePair, ProblemCorpusEntry
from rttdist.exec import ExecutionStatus, evaluate_source


def test_known_good_seed_runs_all_fixture_pairs(tmp_path: Path) -> None:
    source_path = tmp_path / "seed.py"
    source_path.write_text("print(666)\n", encoding="utf-8")

    problem = _build_problem_entry_with_two_pairs(tmp_path)
    workspace_root = tmp_path / "workspace"

    result = evaluate_source(
        language="python",
        source_path=source_path,
        problem=problem,
        workspace_root=workspace_root,
        timeout_seconds=2,
    )

    assert result.status == ExecutionStatus.SUCCESS
    assert len(result.fixture_results) == 2
    assert all(
        item.status == ExecutionStatus.SUCCESS for item in result.fixture_results
    )


def test_runner_uses_deterministic_partitioned_workspace_layout(tmp_path: Path) -> None:
    source_path = tmp_path / "seed.py"
    source_path.write_text("print(666)\n", encoding="utf-8")

    problem = _build_problem_entry_with_two_pairs(tmp_path)
    workspace_root = tmp_path / "workspace"

    result = evaluate_source(
        language="python",
        source_path=source_path,
        problem=problem,
        workspace_root=workspace_root,
        timeout_seconds=2,
    )

    expected_work_directory = (
        workspace_root.resolve() / "exec" / problem.problem_id / "python"
    )
    assert result.work_directory == expected_work_directory
    assert result.compile_log_path == expected_work_directory / "compile.log"
    assert result.compile_log_path.read_text(encoding="utf-8") == "compile skipped\n"

    fixture_one_stdout = expected_work_directory / "fixtures" / "1" / "stdout.log"
    fixture_two_stdout = expected_work_directory / "fixtures" / "2" / "stdout.log"
    assert fixture_one_stdout.read_text(encoding="utf-8").strip() == "666"
    assert fixture_two_stdout.read_text(encoding="utf-8").strip() == "666"


def _build_problem_entry_with_two_pairs(tmp_path: Path) -> ProblemCorpusEntry:
    fixture_directory = tmp_path / "problem" / "IPOP_BATCH"
    fixture_directory.mkdir(parents=True)

    input_one = fixture_directory / "1.inp"
    output_one = fixture_directory / "1.out"
    input_one.write_text("1\n", encoding="utf-8")
    output_one.write_text("666\n", encoding="utf-8")

    input_two = fixture_directory / "2.inp"
    output_two = fixture_directory / "2.out"
    input_two.write_text("2\n", encoding="utf-8")
    output_two.write_text("666\n", encoding="utf-8")

    statement_path = tmp_path / "problem" / "IPOP_BATCH.md"
    statement_path.write_text("dummy statement\n", encoding="utf-8")

    seed_path = tmp_path / "corpus" / "solutions" / "IPOP_BATCH" / "reference.cpp"
    seed_path.parent.mkdir(parents=True)
    seed_path.write_text("int main(){return 0;}\n", encoding="utf-8")

    return ProblemCorpusEntry(
        problem_id="IPOP_BATCH",
        statement_path=statement_path,
        fixture_directory=fixture_directory,
        fixture_pairs=(
            FixturePair(input_path=input_one, output_path=output_one),
            FixturePair(input_path=input_two, output_path=output_two),
        ),
        seed_path=seed_path,
    )
