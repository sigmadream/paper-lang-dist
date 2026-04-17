from __future__ import annotations

from pathlib import Path

import pytest

import rttdist.pipeline as pipeline_module
from rttdist.artifacts import (
    MockOpenAIChoice,
    MockOpenAIMessage,
    MockOpenAIRequest,
    MockOpenAIResponse,
    MockOpenAIUsage,
)
from rttdist.config import ExperimentConfig, OllamaConfig, OpenAIConfig, RuntimeConfig
from rttdist.corpus import FixturePair, ProblemCorpusEntry
from rttdist.exec.adapters import (
    ExecutionBatchResult,
    ExecutionStatus,
    FixtureRunResult,
)
from rttdist.openai_client import TranslationResult
from rttdist.pipeline import run_rtt_loop


def test_idempotent_rerun_skips_existing_artifacts_when_checksums_match(
    tmp_path: Path,
) -> None:
    config = _build_config(tmp_path)
    problem = _build_problem_entry(tmp_path, problem_id="IPOP_IDEMPOTENT")
    run_id = "idempotent"

    first_translator = TrackingTranslationClient(
        target_sources=["print(1)", "print(1)"],
        roundtrip_sources=["int main(){return 0;}", "int main(){return 0;}"],
    )
    evaluator = CountingSuccessEvaluator()

    first_result = run_rtt_loop(
        config=config,
        run_id=run_id,
        problem=problem,
        target_language="python",
        translation_client=first_translator,
        evaluate_source_fn=evaluator,
    )
    assert first_result.iteration_count == 2
    assert first_result.final_record.details["convergence_status"] == "fixed_point"
    assert first_result.final_record.details["convergence"]["overall"] == "fixed_point"

    manifest_before = first_result.run_manifest_path.read_text(encoding="utf-8")

    second_result = run_rtt_loop(
        config=config,
        run_id=run_id,
        problem=problem,
        target_language="python",
        translation_client=NoopTranslationClient(),
        evaluate_source_fn=FailIfCalledEvaluator(),
    )

    assert second_result.iteration_count == 2
    assert second_result.final_record.status.value == "success"
    assert second_result.final_record.details["convergence_status"] == "fixed_point"
    assert second_result.final_record.details["convergence"]["overall"] == "fixed_point"
    assert (
        second_result.run_manifest_path.read_text(encoding="utf-8") == manifest_before
    )


def test_idempotent_rerun_without_translation_work_does_not_construct_openai_client(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = _build_config(tmp_path)
    problem = _build_problem_entry(tmp_path, problem_id="IPOP_IDEMPOTENT_LAZY")
    run_id = "idempotent-lazy"

    first_result = run_rtt_loop(
        config=config,
        run_id=run_id,
        problem=problem,
        target_language="python",
        translation_client=TrackingTranslationClient(
            target_sources=["print(1)", "print(1)"],
            roundtrip_sources=["int main(){return 0;}", "int main(){return 0;}"],
        ),
        evaluate_source_fn=CountingSuccessEvaluator(),
    )
    assert first_result.final_record.status.value == "success"

    class ForbiddenOpenAIClient:
        def __init__(self, **kwargs: object) -> None:
            del kwargs
            raise AssertionError("Completed rerun must not construct OpenAI client.")

    monkeypatch.setattr(
        pipeline_module,
        "OpenAITranslationClient",
        ForbiddenOpenAIClient,
    )

    second_result = run_rtt_loop(
        config=config,
        run_id=run_id,
        problem=problem,
        target_language="python",
        translation_client=None,
        evaluate_source_fn=FailIfCalledEvaluator(),
    )

    assert second_result.iteration_count == 2
    assert second_result.final_record.status.value == "success"


def test_run_uses_ollama_client_when_provider_is_ollama(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = _build_config(tmp_path)
    config = ExperimentConfig(
        problem_ids=config.problem_ids,
        seed_language=config.seed_language,
        target_languages=config.target_languages,
        openai=config.openai,
        runtime=config.runtime,
        output_root=config.output_root,
        problem_root=config.problem_root,
        corpus_root=config.corpus_root,
        provider="ollama",
        ollama=OllamaConfig(
            model="qwen2.5-coder:7b",
            temperature=0.0,
            host="http://localhost:11434",
        ),
    )
    problem = _build_problem_entry(tmp_path, problem_id="IPOP_OLLAMA_SELECTION")
    created: list[dict[str, object]] = []

    class FakeOllamaClient(TrackingTranslationClient):
        def __init__(self, **kwargs: object) -> None:
            created.append(dict(kwargs))
            super().__init__(
                target_sources=["print(1)", "print(1)"],
                roundtrip_sources=["int main(){return 0;}", "int main(){return 0;}"],
            )

    monkeypatch.setattr(pipeline_module, "OllamaTranslationClient", FakeOllamaClient)

    result = run_rtt_loop(
        config=config,
        run_id="ollama-selection",
        problem=problem,
        target_language="python",
        translation_client=None,
        evaluate_source_fn=CountingSuccessEvaluator(),
    )

    assert result.final_record.status.value == "success"
    assert created == [
        {
            "model": "qwen2.5-coder:7b",
            "temperature": 0.0,
            "host": "http://localhost:11434",
        }
    ]


class TrackingTranslationClient:
    def __init__(
        self, *, target_sources: list[str], roundtrip_sources: list[str]
    ) -> None:
        self._target_sources = list(target_sources)
        self._roundtrip_sources = list(roundtrip_sources)

    def translate(
        self,
        *,
        problem_id: str,
        source_language: str,
        target_language: str,
        problem_statement: str,
        sample_input: str,
        sample_output: str,
        source_code: str,
        iteration_index: int,
        direction: str,
    ) -> TranslationResult:
        if direction == "seed_to_target":
            return self.translate_cpp_to_target(
                problem_id=problem_id,
                target_language=target_language,
                problem_statement=problem_statement,
                sample_input=sample_input,
                sample_output=sample_output,
                source_code=source_code,
                iteration_index=iteration_index,
            )
        if direction == "target_to_roundtrip_cpp":
            return self.translate_target_to_cpp(
                problem_id=problem_id,
                source_language=source_language,
                problem_statement=problem_statement,
                sample_input=sample_input,
                sample_output=sample_output,
                source_code=source_code,
                iteration_index=iteration_index,
            )
        raise AssertionError(f"Unexpected translation direction: {direction!r}")

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
        if not self._target_sources:
            raise AssertionError("No mocked target translation source available.")
        source = self._target_sources.pop(0)
        return _translation_result(
            direction="seed_to_target",
            problem_id=problem_id,
            source_language="cpp",
            target_language=target_language,
            iteration_index=iteration_index,
            source_code=source_code,
            extracted_source=source,
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
            raise AssertionError("No mocked roundtrip translation source available.")
        source = self._roundtrip_sources.pop(0)
        return _translation_result(
            direction="target_to_roundtrip_cpp",
            problem_id=problem_id,
            source_language=source_language,
            target_language="cpp",
            iteration_index=iteration_index,
            source_code=source_code,
            extracted_source=source,
        )


class NoopTranslationClient:
    def translate(
        self,
        *,
        problem_id: str,
        source_language: str,
        target_language: str,
        problem_statement: str,
        sample_input: str,
        sample_output: str,
        source_code: str,
        iteration_index: int,
        direction: str,
    ) -> TranslationResult:
        del problem_id
        del source_language
        del target_language
        del problem_statement
        del sample_input
        del sample_output
        del source_code
        del iteration_index
        del direction
        raise AssertionError("Idempotent rerun must not call translation.")

    def translate_cpp_to_target(self, **kwargs: object) -> TranslationResult:
        del kwargs
        raise AssertionError("Idempotent rerun must not call translation.")

    def translate_target_to_cpp(self, **kwargs: object) -> TranslationResult:
        del kwargs
        raise AssertionError("Idempotent rerun must not call translation.")


class CountingSuccessEvaluator:
    def __init__(self) -> None:
        self.call_count = 0

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
        self.call_count += 1

        compile_log_path = workspace_root / "compile" / f"{language}.log"
        compile_log_path.parent.mkdir(parents=True, exist_ok=True)
        compile_log_path.write_text("ok\n", encoding="utf-8")

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


class FailIfCalledEvaluator:
    def __call__(self, **kwargs: object) -> ExecutionBatchResult:
        del kwargs
        raise AssertionError("Idempotent rerun must not call evaluator.")


def _build_config(tmp_path: Path) -> ExperimentConfig:
    output_root = tmp_path / "artifacts"
    output_root.mkdir(parents=True, exist_ok=True)
    return ExperimentConfig(
        problem_ids=("IPOP_TEST",),
        seed_language="cpp",
        target_languages=("python",),
        openai=OpenAIConfig(model="gpt-5.4", temperature=0.0),
        runtime=RuntimeConfig(max_iterations=3, timeout_seconds=1),
        output_root=output_root,
        problem_root=tmp_path / "problem",
        corpus_root=tmp_path / "corpus" / "solutions",
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
    seed_path.write_text("int main(){return 0;}\n", encoding="utf-8")

    return ProblemCorpusEntry(
        problem_id=problem_id,
        statement_path=statement_path,
        fixture_directory=fixture_directory,
        fixture_pairs=(FixturePair(input_path=input_path, output_path=output_path),),
        seed_path=seed_path,
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
        model="gpt-5.4",
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
        response_id=f"resp-{iteration_index}",
        model="gpt-5.4",
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
