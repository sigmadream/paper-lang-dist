from __future__ import annotations

import json
from pathlib import Path

from rttdist.artifacts import (
    MockLLMChoice,
    MockLLMMessage,
    MockLLMRequest,
    MockLLMResponse,
    MockLLMUsage,
    build_iteration_artifact_paths,
)
from rttdist.config import ExperimentConfig, LMStudioConfig, RuntimeConfig
from rttdist.corpus import FixturePair, ProblemCorpusEntry
from rttdist.exec.adapters import (
    ExecutionBatchResult,
    ExecutionStatus,
    FixtureRunResult,
)
from rttdist.lmstudio_client import TranslationResult
from rttdist.pipeline import TranslationClientProtocol, run_pipeline_service


def test_pipeline_service_continues_other_targets_after_failure(tmp_path: Path) -> None:
    config = ExperimentConfig(
        problem_ids=("IPOP_SERVICE",),
        seed_language="cpp",
        target_languages=("python", "c"),
        lmstudio=LMStudioConfig(model="gpt-5.4", temperature=0.0, host="http://localhost:1234/v1"),
        runtime=RuntimeConfig(max_iterations=2, timeout_seconds=1),
        output_root=tmp_path / "artifacts",
        problem_root=tmp_path / "problem",
        corpus_root=tmp_path / "corpus" / "solutions",
    )
    config.output_root.mkdir(parents=True)

    problem = _build_problem_entry(tmp_path, problem_id="IPOP_SERVICE")

    evaluator = FakeEvaluator()
    factory = SequencedFactory(
        clients=(
            FailingTranslationClient(),
            ConvergingTranslationClient(),
        )
    )

    results = run_pipeline_service(
        config=config,
        run_id="svc",
        corpus_entries=(problem,),
        translation_client_factory=factory,
        evaluate_source_fn=evaluator,
    )

    assert len(results) == 2
    assert {item.target_language for item in results} == {"python", "c"}
    assert factory.call_count == 2

    failed = next(item for item in results if item.target_language == "python")
    succeeded = next(item for item in results if item.target_language == "c")

    assert failed.final_record.status.value == "api_error"
    assert failed.final_record.stage == "cpp_to_target_translation"
    assert failed.iteration_count == 1

    failed_iter_paths = build_iteration_artifact_paths(
        run_id="svc",
        problem_id=problem.problem_id,
        target_language="python",
        seed_language=config.seed_language,
        iteration_index=1,
    )
    for relative_path in (
        failed_iter_paths.iteration_metadata_path,
        failed_iter_paths.llm_request_path,
        failed_iter_paths.llm_response_path,
        failed_iter_paths.input_seed_source_path,
        failed_iter_paths.translated_source_path,
        failed_iter_paths.roundtrip_source_path,
        failed_iter_paths.compile_log_path,
        failed_iter_paths.execution_result_path,
        failed_iter_paths.metrics_path,
    ):
        assert (config.output_root / relative_path).is_file()

    assert succeeded.final_record.status.value == "success"
    assert succeeded.final_record.details["convergence_status"] == "fixed_point"
    assert succeeded.iteration_count == 2

    succeeded_manifest = json.loads(
        succeeded.run_manifest_path.read_text(encoding="utf-8")
    )
    assert succeeded_manifest["final"]["status"] == "success"


class SequencedFactory:
    def __init__(self, *, clients: tuple[TranslationClientProtocol, ...]) -> None:
        self._clients = list(clients)
        self.call_count = 0

    def __call__(self) -> TranslationClientProtocol:
        self.call_count += 1
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
        raise AssertionError("Should not call target->cpp after cpp->target failure.")


class ConvergingTranslationClient:
    def __init__(self) -> None:
        self._roundtrip_sources = [
            "int main(){return 0;}",
            "int main(){return 0;}",
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
            extracted_source="print(666)",
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
        roundtrip_source = self._roundtrip_sources.pop(0)
        return _translation_result(
            direction="target_to_roundtrip_cpp",
            problem_id=problem_id,
            source_language=source_language,
            target_language="cpp",
            iteration_index=iteration_index,
            source_code=source_code,
            extracted_source=roundtrip_source,
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
    request = MockLLMRequest(
        model="gpt-5.4",
        temperature=0.0,
        messages=(
            MockLLMMessage(role="system", content=direction),
            MockLLMMessage(role="user", content=source_code),
        ),
        metadata={
            "problem_id": problem_id,
            "source_language": source_language,
            "target_language": target_language,
            "iteration_index": iteration_index,
        },
    )
    response = MockLLMResponse(
        response_id=f"resp-{iteration_index}",
        model="gpt-5.4",
        choices=(
            MockLLMChoice(
                index=0,
                message=MockLLMMessage(role="assistant", content=extracted_source),
                finish_reason="stop",
            ),
        ),
        usage=MockLLMUsage(prompt_tokens=7, completion_tokens=3, total_tokens=10),
    )
    return TranslationResult(
        request=request, response=response, extracted_source=extracted_source
    )


def _build_problem_entry(tmp_path: Path, *, problem_id: str) -> ProblemCorpusEntry:
    fixture_directory = tmp_path / "problem" / problem_id
    fixture_directory.mkdir(parents=True, exist_ok=True)

    input_path = fixture_directory / "1.inp"
    output_path = fixture_directory / "1.out"
    input_path.write_text("1\n", encoding="utf-8")
    output_path.write_text("666\n", encoding="utf-8")

    statement_path = tmp_path / "problem" / f"{problem_id}.md"
    statement_path.parent.mkdir(parents=True, exist_ok=True)
    statement_path.write_text("statement\n", encoding="utf-8")

    seed_path = tmp_path / "corpus" / "solutions" / problem_id / "reference.cpp"
    seed_path.parent.mkdir(parents=True, exist_ok=True)
    seed_path.write_text("int main(){return 0;}\n", encoding="utf-8")

    return ProblemCorpusEntry(
        problem_id=problem_id,
        statement_path=statement_path,
        fixture_directory=fixture_directory,
        fixture_pairs=(FixturePair(input_path=input_path, output_path=output_path),),
        seed_path=seed_path,
    )
