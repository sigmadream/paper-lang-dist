from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from rttdist.artifacts import (
    IterationArtifactPaths,
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
from rttdist.lmstudio_client import LMStudioResponseParseError, TranslationResult
from rttdist.pipeline import run_rtt_loop
from rttdist.run_state import ResumeValidationError


def test_manifest_v2_resume_recovers_missing_manifest_and_continues_next_iteration(
    tmp_path: Path,
) -> None:
    run_id = "resume-recovery"
    config = _build_config(tmp_path=tmp_path, max_iterations=3, timeout_seconds=1)
    problem = _build_problem_entry(tmp_path=tmp_path, problem_id="IPOP_RESUME")

    iteration_paths = build_iteration_artifact_paths(
        run_id=run_id,
        problem_id=problem.problem_id,
        target_language="python",
        seed_language=config.seed_language,
        iteration_index=1,
    )
    prior_target = "print(666)\n"
    prior_roundtrip = "int main(){return 0;}\n"
    _write_partial_iteration(
        output_root=config.output_root,
        paths=iteration_paths,
        input_cpp_source="int main(){return 0;}\n",
        target_source=prior_target,
        roundtrip_source=prior_roundtrip,
    )
    target_path = config.output_root / iteration_paths.translated_source_path
    before_hash = hashlib.sha256(target_path.read_bytes()).hexdigest()

    translator = TrackingTranslationClient(
        target_sources=["print(666)"],
        roundtrip_sources=["int main(){return 0;}"],
    )
    evaluator = AlwaysSuccessEvaluator()

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
    assert result.final_record.details["convergence_status"] == "fixed_point"
    assert translator.cpp_to_target_calls == [2]
    assert translator.target_to_cpp_calls == [2]

    after_hash = hashlib.sha256(target_path.read_bytes()).hexdigest()
    assert after_hash == before_hash

    manifest = json.loads(result.run_manifest_path.read_text(encoding="utf-8"))
    assert manifest["metadata"]["checksums"]["config_hash"]
    assert manifest["metadata"]["checksums"]["seed_source_hash"]
    assert manifest["metadata"]["checksums"]["prompt_template_hash"]
    assert manifest["schema_version"] == "run_manifest.v2"
    assert (
        manifest["metadata"]["run_directory"]
        == f"{run_id}/{problem.problem_id}/cpp-to-python"
    )
    assert manifest["metadata"]["run_metadata_path"].endswith("cpp-to-python/run.json")
    assert len(manifest["iterations"]) == 2
    assert manifest["iterations"][0]["iteration_index"] == 1
    assert manifest["iterations"][1]["iteration_index"] == 2
    assert manifest["iterations"][1]["result"]["details"]["convergence"] == {
        "seed_state": "fixed_point",
        "target_state": "fixed_point",
        "overall": "fixed_point",
    }


def test_resume_rejects_config_hash_mismatch_without_overwriting_artifacts(
    tmp_path: Path,
) -> None:
    run_id = "resume-config-mismatch"
    config_a = _build_config(tmp_path=tmp_path, max_iterations=3, timeout_seconds=1)
    problem = _build_problem_entry(tmp_path=tmp_path, problem_id="IPOP_RESUME_MISMATCH")

    first_run = run_rtt_loop(
        config=config_a,
        run_id=run_id,
        problem=problem,
        target_language="python",
        translation_client=TrackingTranslationClient(
            target_sources=["print(1)", "print(1)"],
            roundtrip_sources=["int main(){return 0;}", "int main(){return 0;}"],
        ),
        evaluate_source_fn=AlwaysSuccessEvaluator(),
    )
    manifest_before = first_run.run_manifest_path.read_text(encoding="utf-8")

    config_b = _build_config(tmp_path=tmp_path, max_iterations=3, timeout_seconds=2)

    with pytest.raises(ResumeValidationError, match="config hash mismatch"):
        run_rtt_loop(
            config=config_b,
            run_id=run_id,
            problem=problem,
            target_language="python",
            translation_client=TrackingTranslationClient(
                target_sources=["print(2)"],
                roundtrip_sources=["int main(){return 2;}"],
            ),
            evaluate_source_fn=AlwaysSuccessEvaluator(),
        )

    manifest_after = first_run.run_manifest_path.read_text(encoding="utf-8")
    assert manifest_after == manifest_before


def test_manifest_v2_seed_snapshot_path_uses_seed_language_extension(
    tmp_path: Path,
) -> None:
    config = _build_config(tmp_path=tmp_path, max_iterations=1, timeout_seconds=1)
    config = ExperimentConfig(
        problem_ids=config.problem_ids,
        seed_language="python",
        target_languages=config.target_languages,
        lmstudio=config.lmstudio,
        runtime=config.runtime,
        output_root=config.output_root,
        problem_root=config.problem_root,
        corpus_root=config.corpus_root,
        provider=config.provider,
    )
    problem = _build_problem_entry(tmp_path=tmp_path, problem_id="IPOP_SEED_PATH")
    problem.seed_path.unlink()
    seed_path = problem.seed_path.with_name("reference.py")
    seed_path.write_text("print(0)\n", encoding="utf-8")
    problem = ProblemCorpusEntry(
        problem_id=problem.problem_id,
        statement_path=problem.statement_path,
        fixture_directory=problem.fixture_directory,
        fixture_pairs=problem.fixture_pairs,
        seed_path=seed_path,
    )

    result = run_rtt_loop(
        config=config,
        run_id="manifest-v2-seed-ext",
        problem=problem,
        target_language="cpp",
        translation_client=TrackingTranslationClient(
            target_sources=["int main(){return 0;}"],
            roundtrip_sources=["int main(){return 0;}"],
        ),
        evaluate_source_fn=AlwaysSuccessEvaluator(),
    )

    manifest = json.loads(result.run_manifest_path.read_text(encoding="utf-8"))
    assert manifest["metadata"]["seed_language"] == "python"
    assert manifest["metadata"]["seed_artifact_path"].endswith("/seed/reference.py")


def test_resume_rejects_seed_source_hash_mismatch(tmp_path: Path) -> None:
    run_id = "resume-seed-mismatch"
    config = _build_config(tmp_path=tmp_path, max_iterations=3, timeout_seconds=1)
    problem = _build_problem_entry(tmp_path=tmp_path, problem_id="IPOP_SEED_MISMATCH")

    first_run = run_rtt_loop(
        config=config,
        run_id=run_id,
        problem=problem,
        target_language="python",
        translation_client=TrackingTranslationClient(
            target_sources=["print(1)", "print(1)"],
            roundtrip_sources=["int main(){return 0;}", "int main(){return 0;}"],
        ),
        evaluate_source_fn=AlwaysSuccessEvaluator(),
    )
    manifest_before = first_run.run_manifest_path.read_text(encoding="utf-8")

    problem.seed_path.write_text("int main(){return 42;}\n", encoding="utf-8")

    with pytest.raises(ResumeValidationError, match="seed source hash mismatch"):
        run_rtt_loop(
            config=config,
            run_id=run_id,
            problem=problem,
            target_language="python",
            translation_client=TrackingTranslationClient(
                target_sources=["print(2)"],
                roundtrip_sources=["int main(){return 2;}"],
            ),
            evaluate_source_fn=AlwaysSuccessEvaluator(),
        )

    assert first_run.run_manifest_path.read_text(encoding="utf-8") == manifest_before


def test_resume_rejects_manifest_artifact_path_outside_output_root(
    tmp_path: Path,
) -> None:
    run_id = "resume-malicious-artifact-path"
    config = _build_config(tmp_path=tmp_path, max_iterations=3, timeout_seconds=1)
    problem = _build_problem_entry(tmp_path=tmp_path, problem_id="IPOP_RESUME_PATH")

    first_run = run_rtt_loop(
        config=config,
        run_id=run_id,
        problem=problem,
        target_language="python",
        translation_client=TrackingTranslationClient(
            target_sources=["print(1)", "print(1)"],
            roundtrip_sources=["int main(){return 0;}", "int main(){return 0;}"],
        ),
        evaluate_source_fn=AlwaysSuccessEvaluator(),
    )
    manifest = json.loads(first_run.run_manifest_path.read_text(encoding="utf-8"))
    manifest["iterations"][0]["artifact_paths"]["roundtrip_source_path"] = (
        "../../../../etc/passwd"
    )
    first_run.run_manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    with pytest.raises(ResumeValidationError, match="escapes output root"):
        run_rtt_loop(
            config=config,
            run_id=run_id,
            problem=problem,
            target_language="python",
            translation_client=BlockedTranslationClient(),
            evaluate_source_fn=AlwaysSuccessEvaluator(),
        )


def test_resume_ordered_pair_or_embedding_metadata_rejects_identity_mismatch(
    tmp_path: Path,
) -> None:
    run_id = "resume-ordered-pair-identity"
    config = _build_config(tmp_path=tmp_path, max_iterations=2, timeout_seconds=1)
    problem = _build_problem_entry(tmp_path=tmp_path, problem_id="IPOP_ORDERED_PAIR")

    first_run = run_rtt_loop(
        config=config,
        run_id=run_id,
        problem=problem,
        target_language="python",
        translation_client=TrackingTranslationClient(
            target_sources=["print(1)", "print(1)"],
            roundtrip_sources=["int main(){return 0;}", "int main(){return 0;}"],
        ),
        evaluate_source_fn=AlwaysSuccessEvaluator(),
    )

    manifest = json.loads(first_run.run_manifest_path.read_text(encoding="utf-8"))
    manifest["metadata"]["run_directory"] = (
        f"{run_id}/{problem.problem_id}/python-to-cpp"
    )
    first_run.run_manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    with pytest.raises(ResumeValidationError, match="run_directory mismatch"):
        run_rtt_loop(
            config=config,
            run_id=run_id,
            problem=problem,
            target_language="python",
            translation_client=BlockedTranslationClient(),
            evaluate_source_fn=AlwaysSuccessEvaluator(),
        )


def test_resume_rejects_manifest_seed_language_identity_mismatch(
    tmp_path: Path,
) -> None:
    run_id = "resume-seed-language-identity"
    config = _build_config(tmp_path=tmp_path, max_iterations=2, timeout_seconds=1)
    problem = _build_problem_entry(tmp_path=tmp_path, problem_id="IPOP_SEED_LANGUAGE")

    first_run = run_rtt_loop(
        config=config,
        run_id=run_id,
        problem=problem,
        target_language="python",
        translation_client=TrackingTranslationClient(
            target_sources=["print(1)", "print(1)"],
            roundtrip_sources=["int main(){return 0;}", "int main(){return 0;}"],
        ),
        evaluate_source_fn=AlwaysSuccessEvaluator(),
    )

    manifest = json.loads(first_run.run_manifest_path.read_text(encoding="utf-8"))
    manifest["metadata"]["seed_language"] = "python"
    first_run.run_manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    with pytest.raises(ResumeValidationError, match="seed_language mismatch"):
        run_rtt_loop(
            config=config,
            run_id=run_id,
            problem=problem,
            target_language="python",
            translation_client=BlockedTranslationClient(),
            evaluate_source_fn=AlwaysSuccessEvaluator(),
        )


@pytest.mark.parametrize(
    "failure_status", ["api_error", "parse_error", "runtime_error"]
)
def test_resume_treats_terminal_failures_as_final(
    tmp_path: Path,
    failure_status: str,
) -> None:
    run_id = f"resume-terminal-{failure_status}"
    config = _build_config(tmp_path=tmp_path, max_iterations=3, timeout_seconds=1)
    problem = _build_problem_entry(tmp_path=tmp_path, problem_id="IPOP_RESUME_TERMINAL")

    if failure_status == "api_error":
        translation_client = ApiFailingTranslationClient()
        evaluator = AlwaysSuccessEvaluator()
    elif failure_status == "parse_error":
        translation_client = ParseFailingTranslationClient()
        evaluator = AlwaysSuccessEvaluator()
    else:
        translation_client = TrackingTranslationClient(
            target_sources=["print(1)"],
            roundtrip_sources=["int main(){return 0;}"],
        )
        evaluator = RuntimeErrorEvaluator()

    first_run = run_rtt_loop(
        config=config,
        run_id=run_id,
        problem=problem,
        target_language="python",
        translation_client=translation_client,
        evaluate_source_fn=evaluator,
    )
    assert first_run.final_record.status.value == failure_status
    assert first_run.iteration_count == 1

    blocked_client = BlockedTranslationClient()
    resumed = run_rtt_loop(
        config=config,
        run_id=run_id,
        problem=problem,
        target_language="python",
        translation_client=blocked_client,
        evaluate_source_fn=AlwaysSuccessEvaluator(),
    )

    assert blocked_client.cpp_to_target_calls == 0
    assert blocked_client.target_to_cpp_calls == 0
    assert resumed.final_record.status.value == failure_status
    assert resumed.iteration_count == 1
    manifest = json.loads(resumed.run_manifest_path.read_text(encoding="utf-8"))
    assert len(manifest["iterations"]) == 1
    assert manifest["final"]["status"] == failure_status


class TrackingTranslationClient:
    def __init__(
        self, *, target_sources: list[str], roundtrip_sources: list[str]
    ) -> None:
        self._target_sources = list(target_sources)
        self._roundtrip_sources = list(roundtrip_sources)
        self.cpp_to_target_calls: list[int] = []
        self.target_to_cpp_calls: list[int] = []

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
        self.cpp_to_target_calls.append(iteration_index)
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
        self.target_to_cpp_calls.append(iteration_index)
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


class ApiFailingTranslationClient:
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
        raise RuntimeError("simulated api failure")

    def translate_cpp_to_target(self, **kwargs: object) -> TranslationResult:
        del kwargs
        raise RuntimeError("simulated api failure")

    def translate_target_to_cpp(self, **kwargs: object) -> TranslationResult:
        del kwargs
        raise AssertionError("Roundtrip translation must not be called.")


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
        raise LMStudioResponseParseError("simulated parse failure")

    def translate_cpp_to_target(self, **kwargs: object) -> TranslationResult:
        del kwargs
        raise LMStudioResponseParseError("simulated parse failure")

    def translate_target_to_cpp(self, **kwargs: object) -> TranslationResult:
        del kwargs
        raise AssertionError("Roundtrip translation must not be called.")


class BlockedTranslationClient:
    def __init__(self) -> None:
        self.cpp_to_target_calls = 0
        self.target_to_cpp_calls = 0

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
        if direction == "seed_to_target":
            self.cpp_to_target_calls += 1
        else:
            self.target_to_cpp_calls += 1
        raise AssertionError("Resume should not invoke translation for terminal runs.")

    def translate_cpp_to_target(self, **kwargs: object) -> TranslationResult:
        del kwargs
        self.cpp_to_target_calls += 1
        raise AssertionError("Resume should not invoke translation for terminal runs.")

    def translate_target_to_cpp(self, **kwargs: object) -> TranslationResult:
        del kwargs
        self.target_to_cpp_calls += 1
        raise AssertionError("Resume should not invoke translation for terminal runs.")


class AlwaysSuccessEvaluator:
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


class RuntimeErrorEvaluator:
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
        compile_log_path.write_text("compile ok\n", encoding="utf-8")

        stdout_log_path = workspace_root / "fixtures" / language / "stdout.log"
        stderr_log_path = workspace_root / "fixtures" / language / "stderr.log"
        stdout_log_path.parent.mkdir(parents=True, exist_ok=True)
        stdout_log_path.write_text("", encoding="utf-8")
        stderr_log_path.write_text("runtime error\n", encoding="utf-8")

        fixture = FixtureRunResult(
            fixture_stem=problem.fixture_pairs[0].input_path.stem,
            input_path=problem.fixture_pairs[0].input_path,
            output_path=problem.fixture_pairs[0].output_path,
            status=ExecutionStatus.RUNTIME_ERROR,
            stdout="",
            stderr="runtime error\n",
            exit_code=1,
            duration_seconds=0.001,
            stdout_log_path=stdout_log_path,
            stderr_log_path=stderr_log_path,
            message="runtime error",
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


def _build_config(
    *, tmp_path: Path, max_iterations: int, timeout_seconds: int
) -> ExperimentConfig:
    output_root = tmp_path / "artifacts"
    output_root.mkdir(parents=True, exist_ok=True)
    return ExperimentConfig(
        problem_ids=("IPOP_TEST",),
        seed_language="cpp",
        target_languages=("python",),
        lmstudio=LMStudioConfig(model="gpt-5.4", temperature=0.0, host="http://localhost:1234/v1"),
        runtime=RuntimeConfig(
            max_iterations=max_iterations,
            timeout_seconds=timeout_seconds,
        ),
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
        request=request,
        response=response,
        extracted_source=extracted_source,
    )


def _write_partial_iteration(
    *,
    output_root: Path,
    paths: IterationArtifactPaths,
    input_cpp_source: str,
    target_source: str,
    roundtrip_source: str,
) -> None:
    output_root.joinpath(paths.iteration_directory).mkdir(parents=True, exist_ok=True)
    _write_json(
        output_root / paths.llm_request_path,
        {"cpp_to_target": {}, "target_to_cpp": {}},
    )
    _write_json(
        output_root / paths.llm_response_path,
        {"cpp_to_target": {}, "target_to_cpp": {}},
    )
    (output_root / paths.input_seed_source_path).write_text(
        input_cpp_source, encoding="utf-8"
    )
    (output_root / paths.translated_source_path).write_text(
        target_source, encoding="utf-8"
    )
    (output_root / paths.roundtrip_source_path).write_text(
        roundtrip_source, encoding="utf-8"
    )
    (output_root / paths.compile_log_path).write_text("ok\n", encoding="utf-8")
    _write_json(
        output_root / paths.execution_result_path,
        {
            "target": {"status": "success", "fixture_results": [], "message": "ok"},
            "roundtrip_cpp": {
                "status": "success",
                "fixture_results": [],
                "message": "ok",
            },
        },
    )
    _write_json(
        output_root / paths.metrics_path,
        {"residual_similarity": 0.9, "convergence_status": "continue"},
    )
    _write_json(
        output_root / paths.iteration_metadata_path,
        {
            "iteration_index": 1,
            "started_at": "2026-03-18T00:00:00Z",
            "ended_at": "2026-03-18T00:00:01Z",
            "result": {
                "status": "success",
                "stage": "iteration",
                "iteration_index": 1,
                "message": "Iteration completed; continuing toward convergence.",
                "details": {"convergence_status": "continue"},
            },
            "artifact_paths": {
                "iteration_directory": paths.iteration_directory,
                "iteration_metadata_path": paths.iteration_metadata_path,
                "llm_request_path": paths.llm_request_path,
                "llm_response_path": paths.llm_response_path,
                "input_seed_source_path": paths.input_seed_source_path,
                "translated_source_path": paths.translated_source_path,
                "roundtrip_source_path": paths.roundtrip_source_path,
                "compile_log_path": paths.compile_log_path,
                "execution_result_path": paths.execution_result_path,
                "metrics_path": paths.metrics_path,
            },
        },
    )


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
