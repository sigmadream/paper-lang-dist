from __future__ import annotations

import json
from pathlib import Path
from typing import Any

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
from rttdist.lmstudio_client import (
    LMStudioResponseParseError,
    LMStudioTranslationClient,
    TranslationResult,
)
from rttdist.pipeline import run_rtt_loop


class FakeTranslationClient:
    def __init__(
        self,
        *,
        target_sources: list[str],
        roundtrip_sources: list[str],
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


def test_pipeline_converges_and_writes_complete_iteration_artifacts(
    tmp_path: Path,
) -> None:
    run_id = "smoke"
    config = _build_config(tmp_path, max_iterations=5)
    problem = _build_problem_entry(tmp_path, problem_id="IPOP_CONVERGE")

    translator = FakeTranslationClient(
        target_sources=[
            "print(666)",
            "print(666)",
        ],
        roundtrip_sources=[
            "#include <iostream>\nint main(){ std::cout << 666 << '\\n'; }",
            "#include <iostream>\nint main(){ std::cout << 666 << '\\n'; }",
        ],
    )
    evaluator = FakeEvaluator()

    result = run_rtt_loop(
        config=config,
        run_id=run_id,
        problem=problem,
        target_language="python",
        translation_client=translator,
        evaluate_source_fn=evaluator,
    )

    assert result.iteration_count == 2
    assert result.final_record.status.value == "success"
    assert result.final_record.stage == "convergence"
    assert result.final_record.details["convergence_status"] == "fixed_point"
    assert result.final_record.details["convergence"] == {
        "seed_state": "fixed_point",
        "target_state": "fixed_point",
        "overall": "fixed_point",
    }

    manifest = _load_json(result.run_manifest_path)
    assert manifest["metadata"]["config_hash"]
    assert manifest["final"]["status"] == "success"
    assert manifest["final"]["details"]["convergence_status"] == "fixed_point"
    assert manifest["final"]["details"]["convergence"]["overall"] == "fixed_point"
    assert len(manifest["status_transitions"]) == 2

    iter2_paths = build_iteration_artifact_paths(
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language="python",
        seed_language=config.seed_language,
        iteration_index=2,
    )
    iter2_metrics = _load_json(config.output_root / iter2_paths.metrics_path)
    assert iter2_metrics["convergence"] == {
        "seed_state": "fixed_point",
        "target_state": "fixed_point",
        "overall": "fixed_point",
    }

    for iteration_index in (1, 2):
        paths = build_iteration_artifact_paths(
            run_id=run_id,
            problem_id=problem.problem_id,
            target_language="python",
            seed_language=config.seed_language,
            iteration_index=iteration_index,
        )
        for relative_path in (
            paths.iteration_metadata_path,
            paths.llm_request_path,
            paths.llm_response_path,
            paths.input_seed_source_path,
            paths.translated_source_path,
            paths.roundtrip_source_path,
            paths.compile_log_path,
            paths.execution_result_path,
            paths.metrics_path,
        ):
            assert (config.output_root / relative_path).is_file()

        execution_payload = _load_json(config.output_root / paths.execution_result_path)
        assert execution_payload["target"]["status"] == "success"
        assert execution_payload["roundtrip_cpp"]["status"] == "success"


def test_pipeline_persists_iteration_input_cpp_history(
    tmp_path: Path,
) -> None:
    run_id = "input-history"
    config = _build_config(tmp_path, max_iterations=3)
    problem = _build_problem_entry(tmp_path, problem_id="IPOP_INPUT_HISTORY")
    seed_source = problem.seed_path.read_text(encoding="utf-8").rstrip()

    first_roundtrip = "int main(){return 1;}"
    second_roundtrip = "int main(){return 1;}"
    translator = FakeTranslationClient(
        target_sources=["print(1)", "print(1)"],
        roundtrip_sources=[first_roundtrip, second_roundtrip],
    )
    evaluator = FakeEvaluator()

    run_rtt_loop(
        config=config,
        run_id=run_id,
        problem=problem,
        target_language="python",
        translation_client=translator,
        evaluate_source_fn=evaluator,
    )

    iter1_paths = build_iteration_artifact_paths(
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language="python",
        seed_language=config.seed_language,
        iteration_index=1,
    )
    iter2_paths = build_iteration_artifact_paths(
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language="python",
        seed_language=config.seed_language,
        iteration_index=2,
    )

    iter1_input = (config.output_root / iter1_paths.input_seed_source_path).read_text(
        encoding="utf-8"
    )
    iter2_input = (config.output_root / iter2_paths.input_seed_source_path).read_text(
        encoding="utf-8"
    )

    assert iter1_input == f"{seed_source}\n"
    assert iter2_input == f"{first_roundtrip}\n"


def test_pipeline_dual_state_history_requires_both_histories_to_fix_before_stopping(
    tmp_path: Path,
) -> None:
    run_id = "dual-state-history"
    config = _build_config(tmp_path, max_iterations=3)
    problem = _build_problem_entry(tmp_path, problem_id="IPOP_DUAL_STATE")

    translator = FakeTranslationClient(
        target_sources=["print(1)", "print(2)", "print(2)"],
        roundtrip_sources=[
            "int main(){return 1;}",
            "int main(){return 1;}",
            "int main(){return 1;}",
        ],
    )
    evaluator = FakeEvaluator()

    result = run_rtt_loop(
        config=config,
        run_id=run_id,
        problem=problem,
        target_language="python",
        translation_client=translator,
        evaluate_source_fn=evaluator,
    )

    assert result.iteration_count == 3
    assert result.final_record.status.value == "success"
    assert result.final_record.details["convergence"] == {
        "seed_state": "fixed_point",
        "target_state": "fixed_point",
        "overall": "fixed_point",
    }

    iter2_paths = build_iteration_artifact_paths(
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language="python",
        seed_language=config.seed_language,
        iteration_index=2,
    )
    iter2_metrics = _load_json(config.output_root / iter2_paths.metrics_path)
    assert iter2_metrics["convergence"] == {
        "seed_state": "fixed_point",
        "target_state": "continue",
        "overall": "continue",
    }


def test_pipeline_stops_at_max_iteration_and_preserves_prior_artifacts(
    tmp_path: Path,
) -> None:
    run_id = "maxiter"
    config = _build_config(tmp_path, max_iterations=3)
    problem = _build_problem_entry(tmp_path, problem_id="IPOP_MAX")

    translator = FakeTranslationClient(
        target_sources=["print(1)", "print(2)", "print(3)"],
        roundtrip_sources=[
            "int main(){return 1;}",
            "int main(){return 2;}",
            "int main(){return 3;}",
        ],
    )
    evaluator = FakeEvaluator()

    result = run_rtt_loop(
        config=config,
        run_id=run_id,
        problem=problem,
        target_language="python",
        translation_client=translator,
        evaluate_source_fn=evaluator,
    )

    assert result.iteration_count == 3
    assert result.final_record.status.value == "max_iter_no_convergence"
    assert result.final_record.stage == "convergence"
    assert result.final_record.details["convergence"]["overall"] == "continue"

    manifest = _load_json(result.run_manifest_path)
    assert manifest["final"]["status"] == "max_iter_no_convergence"
    assert manifest["final"]["iteration_index"] == 3
    assert manifest["final"]["details"]["convergence"]["overall"] == "continue"

    iter1_paths = build_iteration_artifact_paths(
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language="python",
        seed_language=config.seed_language,
        iteration_index=1,
    )
    iter3_paths = build_iteration_artifact_paths(
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language="python",
        seed_language=config.seed_language,
        iteration_index=3,
    )
    assert (config.output_root / iter1_paths.execution_result_path).is_file()
    assert (config.output_root / iter3_paths.execution_result_path).is_file()

    first_iteration = _load_json(
        config.output_root / iter1_paths.iteration_metadata_path
    )
    third_iteration = _load_json(
        config.output_root / iter3_paths.iteration_metadata_path
    )
    assert first_iteration["result"]["status"] == "success"
    assert third_iteration["result"]["status"] == "max_iter_no_convergence"


def test_pipeline_classifies_runtime_execution_failure_distinct_from_wrong_answer(
    tmp_path: Path,
) -> None:
    config = _build_config(tmp_path, max_iterations=2)
    problem = _build_problem_entry(tmp_path, problem_id="IPOP_RUNTIME")

    translator = FakeTranslationClient(
        target_sources=["print(666)"],
        roundtrip_sources=["int main(){return 0;}"],
    )
    evaluator = RuntimeFailureEvaluator()

    result = run_rtt_loop(
        config=config,
        run_id="runtime-failure",
        problem=problem,
        target_language="python",
        translation_client=translator,
        evaluate_source_fn=evaluator,
    )

    assert result.final_record.status.value == "runtime_error"
    assert result.final_record.stage == "target_execution"


def test_pipeline_classifies_translation_parse_failures_as_parse_error(
    tmp_path: Path,
) -> None:
    config = _build_config(tmp_path, max_iterations=2)
    problem = _build_problem_entry(tmp_path, problem_id="IPOP_PARSE")

    result = run_rtt_loop(
        config=config,
        run_id="parse-failure",
        problem=problem,
        target_language="python",
        translation_client=ParseFailingTranslationClient(),
        evaluate_source_fn=FakeEvaluator(),
    )

    assert result.final_record.status.value == "parse_error"
    assert result.final_record.stage == "cpp_to_target_translation"


def test_pipeline_persists_raw_translation_payloads_on_parse_error(
    tmp_path: Path,
) -> None:
    config = _build_config(tmp_path, max_iterations=2)
    problem = _build_problem_entry(tmp_path, problem_id="IPOP_PARSE_PAYLOADS")
    transport = ParseErrorTransport(
        responses=[
            {
                "id": "resp-parse-001",
                "model": "gpt-5.4",
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": "No source code is provided in this answer.",
                        },
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 5,
                    "total_tokens": 15,
                },
            }
        ]
    )
    translator = LMStudioTranslationClient(
        model="gpt-5.4", transport=transport
    )

    result = run_rtt_loop(
        config=config,
        run_id="parse-payloads",
        problem=problem,
        target_language="python",
        translation_client=translator,
        evaluate_source_fn=FakeEvaluator(),
    )

    assert result.final_record.status.value == "parse_error"

    paths = build_iteration_artifact_paths(
        run_id="parse-payloads",
        problem_id=problem.problem_id,
        target_language="python",
        seed_language=config.seed_language,
        iteration_index=1,
    )
    request_payload = _load_json(config.output_root / paths.llm_request_path)
    response_payload = _load_json(config.output_root / paths.llm_response_path)

    assert request_payload["cpp_to_target"]["metadata"]["iteration_index"] == 1
    assert response_payload["cpp_to_target"]["choices"][0]["message"][
        "content"
    ].startswith("No source code")


def test_pipeline_persists_stable_iteration_execution_evidence_paths(
    tmp_path: Path,
) -> None:
    run_id = "stable-evidence"
    config = _build_config(tmp_path, max_iterations=2)
    problem = _build_problem_entry(tmp_path, problem_id="IPOP_STABLE_EVIDENCE")

    translator = FakeTranslationClient(
        target_sources=["print(666)", "print(666)"],
        roundtrip_sources=["int main(){return 0;}", "int main(){return 0;}"],
    )
    evaluator = OverwritingLogEvaluator()

    run_rtt_loop(
        config=config,
        run_id=run_id,
        problem=problem,
        target_language="python",
        translation_client=translator,
        evaluate_source_fn=evaluator,
    )

    iter1_paths = build_iteration_artifact_paths(
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language="python",
        seed_language=config.seed_language,
        iteration_index=1,
    )
    iter2_paths = build_iteration_artifact_paths(
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language="python",
        seed_language=config.seed_language,
        iteration_index=2,
    )

    iter1_exec = _load_json(config.output_root / iter1_paths.execution_result_path)
    iter2_exec = _load_json(config.output_root / iter2_paths.execution_result_path)

    iter1_compile_rel = iter1_exec["target"]["compile_log_path"]
    iter2_compile_rel = iter2_exec["target"]["compile_log_path"]
    assert iter1_compile_rel != iter2_compile_rel
    assert "iter-001/evidence/target/compile.log" in iter1_compile_rel
    assert "iter-002/evidence/target/compile.log" in iter2_compile_rel

    iter1_compile_log = (config.output_root / iter1_compile_rel).read_text(
        encoding="utf-8"
    )
    iter2_compile_log = (config.output_root / iter2_compile_rel).read_text(
        encoding="utf-8"
    )
    assert "compile-call-1" in iter1_compile_log
    assert "compile-call-3" in iter2_compile_log


class FakeEvaluator:
    def __init__(self) -> None:
        self.calls: list[tuple[str, int]] = []

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
        call_index = len(self.calls) + 1
        self.calls.append((language, call_index))

        compile_log_path = (
            workspace_root / "fake-compile" / f"{language}-{call_index}.log"
        )
        compile_log_path.parent.mkdir(parents=True, exist_ok=True)
        compile_log_path.write_text(f"compile log for {language}\n", encoding="utf-8")

        stdout_log_path = (
            workspace_root / "fake-exec" / f"{language}-{call_index}.stdout"
        )
        stderr_log_path = (
            workspace_root / "fake-exec" / f"{language}-{call_index}.stderr"
        )
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


class RuntimeFailureEvaluator:
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

        compile_log_path = workspace_root / "runtime" / "compile.log"
        compile_log_path.parent.mkdir(parents=True, exist_ok=True)
        compile_log_path.write_text("compile ok\n", encoding="utf-8")

        stdout_log_path = workspace_root / "runtime" / "stdout.log"
        stderr_log_path = workspace_root / "runtime" / "stderr.log"
        stdout_log_path.write_text("", encoding="utf-8")
        stderr_log_path.write_text("runtime failure\n", encoding="utf-8")

        fixture = FixtureRunResult(
            fixture_stem=problem.fixture_pairs[0].input_path.stem,
            input_path=problem.fixture_pairs[0].input_path,
            output_path=problem.fixture_pairs[0].output_path,
            status=ExecutionStatus.RUNTIME_ERROR,
            stdout="",
            stderr="runtime failure\n",
            exit_code=1,
            duration_seconds=0.001,
            stdout_log_path=stdout_log_path,
            stderr_log_path=stderr_log_path,
            message="runtime failure",
        )

        return ExecutionBatchResult(
            language=language,
            problem_id=problem.problem_id,
            status=ExecutionStatus.RUNTIME_ERROR,
            work_directory=workspace_root / "exec" / problem.problem_id / language,
            compile_log_path=compile_log_path,
            compile_result=None,
            fixture_results=(fixture,),
            message="At least one fixture failed at runtime.",
        )


class ParseFailingTranslationClient:
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
        raise LMStudioResponseParseError("missing choices")

    def translate_cpp_to_target(self, **kwargs: Any) -> TranslationResult:
        del kwargs
        raise LMStudioResponseParseError("missing choices")

    def translate_target_to_cpp(self, **kwargs: Any) -> TranslationResult:
        del kwargs
        raise AssertionError("Should not execute roundtrip translation.")


class OverwritingLogEvaluator:
    def __init__(self) -> None:
        self._call_count = 0

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
        self._call_count += 1
        call_count = self._call_count

        compile_log_path = workspace_root / "shared" / "compile.log"
        compile_log_path.parent.mkdir(parents=True, exist_ok=True)
        compile_log_path.write_text(f"compile-call-{call_count}\n", encoding="utf-8")

        stdout_log_path = workspace_root / "shared" / "stdout.log"
        stderr_log_path = workspace_root / "shared" / "stderr.log"
        stdout_log_path.write_text(f"stdout-call-{call_count}\n", encoding="utf-8")
        stderr_log_path.write_text(f"stderr-call-{call_count}\n", encoding="utf-8")

        fixture = FixtureRunResult(
            fixture_stem=problem.fixture_pairs[0].input_path.stem,
            input_path=problem.fixture_pairs[0].input_path,
            output_path=problem.fixture_pairs[0].output_path,
            status=ExecutionStatus.SUCCESS,
            stdout=f"stdout-call-{call_count}\n",
            stderr=f"stderr-call-{call_count}\n",
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


class ParseErrorTransport:
    def __init__(self, responses: list[dict[str, object]]) -> None:
        self._responses = responses

    def create_chat_completion(self, payload: dict[str, object]) -> dict[str, object]:
        del payload
        if not self._responses:
            raise AssertionError("No mocked parse-error response available.")
        response = self._responses.pop(0)
        if not isinstance(response, dict):
            raise AssertionError("Mocked parse-error response must be a mapping.")
        return response


def _build_config(tmp_path: Path, *, max_iterations: int) -> ExperimentConfig:
    output_root = tmp_path / "artifacts"
    output_root.mkdir(parents=True)
    return ExperimentConfig(
        problem_ids=("IPOP_TEST",),
        seed_language="cpp",
        target_languages=("python",),
        lmstudio=LMStudioConfig(
            model="gpt-5.4", temperature=0.0, host="http://localhost:1234/v1"
        ),
        runtime=RuntimeConfig(max_iterations=max_iterations, timeout_seconds=1),
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
    output_path.write_text("666\n", encoding="utf-8")

    statement_path = tmp_path / "problem" / f"{problem_id}.md"
    statement_path.parent.mkdir(parents=True, exist_ok=True)
    statement_path.write_text("dummy statement\n", encoding="utf-8")

    seed_path = tmp_path / "corpus" / "solutions" / problem_id / "reference.cpp"
    seed_path.parent.mkdir(parents=True, exist_ok=True)
    seed_path.write_text(
        "#include <iostream>\nint main(){ std::cout << 666 << '\\n'; }\n",
        encoding="utf-8",
    )

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
    request = MockLLMRequest(
        model="gpt-5.4",
        temperature=0.0,
        messages=(
            MockLLMMessage(role="system", content=f"direction={direction}"),
            MockLLMMessage(role="user", content=source_code),
        ),
        metadata={
            "direction": direction,
            "problem_id": problem_id,
            "source_language": source_language,
            "target_language": target_language,
            "iteration_index": iteration_index,
        },
    )
    response = MockLLMResponse(
        response_id=f"mock-{direction}-{iteration_index}",
        model="gpt-5.4",
        choices=(
            MockLLMChoice(
                index=0,
                message=MockLLMMessage(role="assistant", content=extracted_source),
                finish_reason="stop",
            ),
        ),
        usage=MockLLMUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
    )
    return TranslationResult(
        request=request, response=response, extracted_source=extracted_source
    )


def _load_json(
    path: Path,
) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
