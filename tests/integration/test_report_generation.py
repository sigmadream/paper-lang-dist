from __future__ import annotations

import json
from pathlib import Path

from rttdist.artifacts import (
    MockOpenAIChoice,
    MockOpenAIMessage,
    MockOpenAIRequest,
    MockOpenAIResponse,
    MockOpenAIUsage,
)
from rttdist.config import ExperimentConfig, OpenAIConfig, RuntimeConfig
from rttdist.corpus import FixturePair, ProblemCorpusEntry
from rttdist.exec.adapters import (
    ExecutionBatchResult,
    ExecutionStatus,
    FixtureRunResult,
)
from rttdist.openai_client import TranslationResult
from rttdist.pipeline import TranslationClientProtocol, run_pipeline_service
from rttdist.reporting import write_run_summary


def test_report_generation_writes_stable_summary_files_from_persisted_run_artifacts(
    tmp_path: Path,
) -> None:
    config = ExperimentConfig(
        problem_ids=("IPOP_REPORT",),
        target_languages=("python", "c"),
        openai=OpenAIConfig(model="gpt-4o-mini", temperature=0.0),
        runtime=RuntimeConfig(max_iterations=2, timeout_seconds=1),
        output_root=tmp_path / "artifacts",
        problem_root=tmp_path / "problem",
        corpus_root=tmp_path / "corpus" / "solutions",
    )
    config.output_root.mkdir(parents=True)
    problem = _build_problem_entry(tmp_path, problem_id="IPOP_REPORT")

    run_pipeline_service(
        config=config,
        run_id="report-run",
        corpus_entries=(problem,),
        translation_client_factory=SequencedFactory(
            clients=(FailingTranslationClient(), ConvergingTranslationClient())
        ),
        evaluate_source_fn=FakeEvaluator(),
    )

    artifacts = write_run_summary(output_root=config.output_root, run_id="report-run")

    success_manifest_path = (
        config.output_root / "report-run" / "IPOP_REPORT" / "c" / "run.json"
    )
    success_manifest = json.loads(success_manifest_path.read_text(encoding="utf-8"))
    seed_artifact_path = success_manifest["metadata"].get("seed_artifact_path")
    assert isinstance(seed_artifact_path, str)
    assert (config.output_root / seed_artifact_path).is_file()

    assert (
        artifacts.summary_json_path
        == config.output_root / "report-run" / "summary.json"
    )
    assert (
        artifacts.summary_markdown_path
        == config.output_root / "report-run" / "summary.md"
    )
    assert artifacts.summary_json_path.is_file()
    assert artifacts.summary_markdown_path.is_file()

    summary = json.loads(artifacts.summary_json_path.read_text(encoding="utf-8"))
    assert summary["schema_version"] == "report_summary.v1"
    assert summary["run_id"] == "report-run"
    assert summary["result_count"] == 2

    by_target_language = {
        entry["target_language"]: entry for entry in summary["results"]
    }
    success_entry = by_target_language["c"]
    failure_entry = by_target_language["python"]

    assert success_entry["final_status"] == "success"
    assert success_entry["iteration_count"] == 2
    assert success_entry["change_count_distance"] == {
        "availability": "measured",
        "value": 2,
        "unit": "cpp_to_target_to_cpp_cycles",
        "definition": "1 cycle = C++ -> target -> C++",
    }
    assert success_entry["convergence_outcome"] == "fixed_point"
    assert success_entry["residual_similarity"]["availability"] == "measured"
    assert success_entry["semantic_summary"]["overall"] == "pass"
    assert success_entry["ast_distance"]["availability"] == "measured"
    assert success_entry["complexity_deltas"]["target"]["availability"] == "measured"
    assert (
        success_entry["artifacts"]["run_manifest_path"]
        == "report-run/IPOP_REPORT/c/run.json"
    )

    assert failure_entry["final_status"] == "api_error"
    assert failure_entry["change_count_distance"] == {
        "availability": "measured",
        "value": 0,
        "unit": "cpp_to_target_to_cpp_cycles",
        "definition": "1 cycle = C++ -> target -> C++",
    }
    assert failure_entry["convergence_outcome"] == "terminated_on_failure"
    assert failure_entry["semantic_summary"]["overall"] == "fail"
    assert failure_entry["residual_similarity"] == {
        "availability": "unavailable",
        "reason": "residual_similarity_not_recorded",
        "failure": {
            "status": "api_error",
            "stage": "cpp_to_target_translation",
            "iteration_index": 1,
        },
    }
    assert failure_entry["ast_distance"]["availability"] == "unavailable"
    assert failure_entry["complexity_deltas"]["target"]["availability"] == "unavailable"
    assert (
        failure_entry["complexity_deltas"]["roundtrip_cpp"]["availability"]
        == "unavailable"
    )

    markdown = artifacts.summary_markdown_path.read_text(encoding="utf-8")
    assert "# Run Summary: report-run" in markdown
    assert "| IPOP_REPORT | c | success | 2 | 2 | fixed_point |" in markdown
    assert (
        "| IPOP_REPORT | python | api_error | 1 | 0 | terminated_on_failure |"
        in markdown
    )
    assert "Change-count distance (1 cycle = C++ -> target -> C++): 2" in markdown
    assert (
        "Residual similarity to seed C++: unavailable (api_error at cpp_to_target_translation)"
        in markdown
    )

    problem.seed_path.unlink()

    regenerated = write_run_summary(output_root=config.output_root, run_id="report-run")
    regenerated_summary = json.loads(
        regenerated.summary_json_path.read_text(encoding="utf-8")
    )
    regenerated_by_target_language = {
        entry["target_language"]: entry for entry in regenerated_summary["results"]
    }
    assert (
        regenerated_by_target_language["c"]["ast_distance"]["availability"]
        == "measured"
    )


class SequencedFactory:
    def __init__(self, *, clients: tuple[TranslationClientProtocol, ...]) -> None:
        self._clients = list(clients)

    def __call__(self) -> TranslationClientProtocol:
        if not self._clients:
            raise AssertionError("No translation client prepared for factory call.")
        return self._clients.pop(0)


class FailingTranslationClient:
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
    ) -> TranslationResult:
        del problem_id
        del target_language
        del problem_statement
        del sample_input
        del sample_output
        del source_code
        del iteration_index
        raise RuntimeError("mock translation failure")

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
    ) -> TranslationResult:
        del problem_id
        del source_language
        del problem_statement
        del sample_input
        del sample_output
        del source_code
        del iteration_index
        raise AssertionError("Should not translate back to C++ after a failure.")


class ConvergingTranslationClient:
    def __init__(self) -> None:
        self._roundtrip_sources = [
            "int solve(int x){ if (x > 0) { return x; } return 0; }",
            "int solve(int x){ if (x > 0) { return x; } return 0; }",
        ]

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
    ) -> TranslationResult:
        del problem_statement
        del sample_input
        del sample_output
        return _translation_result(
            direction="seed_to_target",
            problem_id=problem_id,
            source_language="cpp",
            target_language=target_language,
            iteration_index=iteration_index,
            source_code=source_code,
            extracted_source=(
                "int solve(int x) {\n"
                "    if (x > 0) {\n"
                "        return x;\n"
                "    }\n"
                "    return 0;\n"
                "}\n"
            ),
        )

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
    ) -> TranslationResult:
        del problem_statement
        del sample_input
        del sample_output
        if not self._roundtrip_sources:
            raise AssertionError("No mocked roundtrip source available.")
        return _translation_result(
            direction="target_to_roundtrip_cpp",
            problem_id=problem_id,
            source_language=source_language,
            target_language="cpp",
            iteration_index=iteration_index,
            source_code=source_code,
            extracted_source=self._roundtrip_sources.pop(0),
        )


class FakeEvaluator:
    def __call__(
        self,
        *,
        language: str,
        source_path: Path,
        problem: ProblemCorpusEntry,
        workspace_root: Path,
        timeout_seconds: int,
    ) -> ExecutionBatchResult:
        del source_path
        del timeout_seconds
        compile_log_path = workspace_root / "compile" / f"{language}.log"
        compile_log_path.parent.mkdir(parents=True, exist_ok=True)
        compile_log_path.write_text(f"compiled {language}\n", encoding="utf-8")

        stdout_log_path = workspace_root / "fixtures" / language / "stdout.log"
        stderr_log_path = workspace_root / "fixtures" / language / "stderr.log"
        stdout_log_path.parent.mkdir(parents=True, exist_ok=True)
        stdout_log_path.write_text("ok\n", encoding="utf-8")
        stderr_log_path.write_text("", encoding="utf-8")

        fixture = FixtureRunResult(
            fixture_stem=problem.fixture_pairs[0].input_path.stem,
            input_path=problem.fixture_pairs[0].input_path,
            output_path=problem.fixture_pairs[0].output_path,
            status=ExecutionStatus.SUCCESS,
            stdout="ok\n",
            stderr="",
            exit_code=0,
            duration_seconds=0.001,
            stdout_log_path=stdout_log_path,
            stderr_log_path=stderr_log_path,
            message="ok",
        )
        return ExecutionBatchResult(
            language=language,
            problem_id=problem.problem_id,
            status=ExecutionStatus.SUCCESS,
            work_directory=workspace_root / "exec" / problem.problem_id / language,
            compile_log_path=compile_log_path,
            compile_result=None,
            fixture_results=(fixture,),
            message="All fixture pairs passed.",
        )


def _translation_result(
    *,
    direction: str,
    problem_id: str,
    source_language: str,
    target_language: str,
    iteration_index: int,
    source_code: str,
    extracted_source: str,
) -> TranslationResult:
    request = MockOpenAIRequest(
        model="gpt-4o-mini",
        temperature=0.0,
        messages=(
            MockOpenAIMessage(role="system", content=direction),
            MockOpenAIMessage(role="user", content=source_code),
        ),
        metadata={
            "problem_id": problem_id,
            "source_language": source_language,
            "target_language": target_language,
            "iteration_index": iteration_index,
        },
    )
    response = MockOpenAIResponse(
        response_id=f"resp-{direction}-{iteration_index}",
        model="gpt-4o-mini",
        choices=(
            MockOpenAIChoice(
                index=0,
                message=MockOpenAIMessage(role="assistant", content=extracted_source),
                finish_reason="stop",
            ),
        ),
        usage=MockOpenAIUsage(prompt_tokens=7, completion_tokens=3, total_tokens=10),
    )
    return TranslationResult(
        request=request,
        response=response,
        extracted_source=extracted_source,
    )


def _build_problem_entry(tmp_path: Path, *, problem_id: str) -> ProblemCorpusEntry:
    fixture_directory = tmp_path / "problem" / problem_id
    fixture_directory.mkdir(parents=True, exist_ok=True)

    input_path = fixture_directory / "1.inp"
    output_path = fixture_directory / "1.out"
    input_path.write_text("1\n", encoding="utf-8")
    output_path.write_text("1\n", encoding="utf-8")

    statement_path = tmp_path / "problem" / f"{problem_id}.md"
    statement_path.parent.mkdir(parents=True, exist_ok=True)
    statement_path.write_text("statement\n", encoding="utf-8")

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

    return ProblemCorpusEntry(
        problem_id=problem_id,
        statement_path=statement_path,
        fixture_directory=fixture_directory,
        fixture_pairs=(FixturePair(input_path=input_path, output_path=output_path),),
        seed_path=seed_path,
    )
