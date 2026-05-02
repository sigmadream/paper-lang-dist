import json
from pathlib import Path

from rttdist.artifacts import LLMChoice, LLMMessage, LLMRequest, LLMResponse, LLMUsage, build_iteration_artifact_paths
from rttdist.config import ExperimentConfig, LMStudioConfig, RuntimeConfig
from rttdist.corpus import FixturePair, ProblemCorpusEntry
from rttdist.exec.adapters import ExecutionBatchResult, ExecutionStatus, ProcessResult
from rttdist.lmstudio_client import LMStudioClientError
from rttdist.lmstudio_client import TranslationResult
from rttdist.pipeline import run_rtt_loop


class RouteClient:
    def __init__(self, sources: list[str | Exception]) -> None:
        self.sources = list(sources)
        self.calls: list[tuple[str, str]] = []

    def translate(self, **kwargs) -> TranslationResult:
        self.calls.append((kwargs["source_language"], kwargs["target_language"]))
        source = self.sources.pop(0)
        if isinstance(source, Exception):
            raise source
        request = LLMRequest(model="test", temperature=0.0, messages=(LLMMessage(role="user", content="x"),), metadata={"source_language": kwargs["source_language"], "target_language": kwargs["target_language"], "iteration_index": kwargs["iteration_index"]})
        response = LLMResponse(response_id="r", model="test", choices=(LLMChoice(index=0, message=LLMMessage(role="assistant", content=source), finish_reason="stop"),), usage=LLMUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0))
        return TranslationResult(request=request, response=response, extracted_source=source)


class SuccessEvaluator:
    def __call__(self, *, language: str, source_path: Path, problem: ProblemCorpusEntry, workspace_root: Path, timeout_seconds: int) -> ExecutionBatchResult:
        work = workspace_root / "eval" / language
        work.mkdir(parents=True, exist_ok=True)
        log = work / "compile.log"
        log.write_text("ok\n", encoding="utf-8")
        return ExecutionBatchResult(language=language, problem_id=problem.problem_id, status=ExecutionStatus.SUCCESS, work_directory=work, compile_log_path=log, compile_result=None, fixture_results=tuple(), message="ok")


class StatusByLanguageEvaluator:
    def __init__(self, statuses: dict[str, ExecutionStatus]) -> None:
        self.statuses = dict(statuses)

    def __call__(self, *, language: str, source_path: Path, problem: ProblemCorpusEntry, workspace_root: Path, timeout_seconds: int) -> ExecutionBatchResult:
        del source_path
        del timeout_seconds
        work = workspace_root / "eval" / language
        work.mkdir(parents=True, exist_ok=True)
        log = work / "compile.log"
        log.write_text("ok\n", encoding="utf-8")
        status = self.statuses.get(language, ExecutionStatus.SUCCESS)
        return ExecutionBatchResult(
            language=language,
            problem_id=problem.problem_id,
            status=status,
            work_directory=work,
            compile_log_path=log,
            compile_result=ProcessResult(
                command=("compile", language),
                stdout="",
                stderr="",
                exit_code=0,
                timed_out=False,
                duration_seconds=0.01,
            ),
            fixture_results=tuple(),
            message=status.value,
        )


def test_rtt_loop_runs_one_independent_target_route(tmp_path: Path) -> None:
    config = _config(tmp_path)
    problem = _problem(tmp_path)
    client = RouteClient([
        "print(0)",
        "int main(){return 0;}",
    ])
    result = run_rtt_loop(config=config, run_id="r", problem=problem, target_language="python", translation_client=client, evaluate_source_fn=SuccessEvaluator())
    assert result.final_record.status.value == "success"
    assert client.calls == [("cpp", "python"), ("python", "cpp")]
    paths = build_iteration_artifact_paths(run_id="r", problem_id=problem.problem_id, target_language="python", seed_language="cpp", iteration_index=1)
    assert (config.output_root / paths.roundtrip_source_path).is_file()

    metrics = json.loads((config.output_root / paths.metrics_path).read_text(encoding="utf-8"))
    assert metrics["translation_count_per_cycle"] == 2
    assert metrics["attempted_translation_count"] == 2
    assert metrics["completed_translation_count"] == 2
    assert metrics["failed_translation_count"] == 0
    assert metrics["translation_count"] == {
        "per_cycle": 2,
        "attempted": 2,
        "completed": 2,
        "failed": 0,
        "unit": "translations",
        "definition": "number of source->target conversions in one complete RTT language route",
    }
    assert [
        (step["source_language"], step["target_language"], step["status"])
        for step in metrics["translation_steps"]
    ] == [
        ("cpp", "python", "completed"),
        ("python", "cpp", "completed"),
    ]
    distance_metrics = metrics["distance_metrics"]
    assert distance_metrics["schema_version"] == 1
    assert metrics["rtt_distance"]["availability"] == "measured"
    assert distance_metrics["change_count"]["canonical_source"] == "rtt_distance"
    assert distance_metrics["change_count"]["value"] == metrics["rtt_distance"]["value"]
    assert distance_metrics["residual_similarity"]["status"] == "measured"
    assert 0.0 <= distance_metrics["residual_similarity"]["value"] <= 1.0
    assert distance_metrics["semantic_preservation"]["canonical_source"] == "evaluation_checks"
    assert distance_metrics["semantic_preservation"]["status"] == "pass"
    assert set(distance_metrics["complexity_delta"]["metrics"]) == {
        "loc",
        "token_count",
        "cyclomatic",
        "function_count",
        "max_nesting",
    }
    conversion_log = config.output_root / metrics["conversion_log_path"]
    assert conversion_log.is_file()
    log_text = conversion_log.read_text(encoding="utf-8")
    assert "translation_count_per_cycle=2" in log_text
    assert "step 2/2 COMPLETE python->cpp" in log_text


def test_rtt_loop_records_compile_and_functionality_checks(tmp_path: Path) -> None:
    config = _config(tmp_path)
    problem = _problem(tmp_path)
    client = RouteClient(["print(0)", "int main(){return 0;}"])

    run_rtt_loop(
        config=config,
        run_id="checks",
        problem=problem,
        target_language="python",
        translation_client=client,
        evaluate_source_fn=StatusByLanguageEvaluator({}),
    )

    paths = build_iteration_artifact_paths(
        run_id="checks",
        problem_id=problem.problem_id,
        target_language="python",
        seed_language="cpp",
        iteration_index=1,
    )
    metrics = json.loads((config.output_root / paths.metrics_path).read_text(encoding="utf-8"))
    assert [
        (step["compile_status"], step["compile_passed"], step["functionality_status"], step["functionality_passed"])
        for step in metrics["translation_steps"]
    ] == [
        ("passed", True, "passed", True),
        ("passed", True, "passed", True),
    ]
    assert metrics["evaluation_checks"]["compile"]["passed"] == 2
    assert metrics["evaluation_checks"]["functionality"]["passed"] == 2

    execution = json.loads((config.output_root / paths.execution_result_path).read_text(encoding="utf-8"))
    assert execution["steps"][0]["compile_check"]["status"] == "passed"
    assert execution["steps"][0]["functionality_check"]["status"] == "passed"


def test_non_final_functionality_failure_continues_and_still_allows_fixed_point(
    tmp_path: Path,
) -> None:
    config = _config(tmp_path)
    problem = _problem(tmp_path)
    client = RouteClient(["print(123)", "int main(){return 0;}"])

    result = run_rtt_loop(
        config=config,
        run_id="intermediate-functionality-failure",
        problem=problem,
        target_language="python",
        translation_client=client,
        evaluate_source_fn=StatusByLanguageEvaluator({"python": ExecutionStatus.WRONG_ANSWER}),
    )

    assert result.final_record.status.value == "success"
    assert result.final_record.details["convergence_status"] == "fixed_point"
    assert client.calls == [("cpp", "python"), ("python", "cpp")]

    paths = build_iteration_artifact_paths(
        run_id="intermediate-functionality-failure",
        problem_id=problem.problem_id,
        target_language="python",
        seed_language="cpp",
        iteration_index=1,
    )
    metrics = json.loads((config.output_root / paths.metrics_path).read_text(encoding="utf-8"))
    assert [
        (step["status"], step["compile_passed"], step["functionality_passed"])
        for step in metrics["translation_steps"]
    ] == [
        ("completed_with_functionality_failure", True, False),
        ("completed", True, True),
    ]
    assert metrics["evaluation_checks"]["functionality"]["failed"] == 1
    assert metrics["evaluation_checks"]["functionality"]["passed"] == 1
    semantic = metrics["distance_metrics"]["semantic_preservation"]
    assert semantic["status"] == "degraded"
    assert semantic["overall_passed"] is False
    assert semantic["route_had_degradation"] is True
    assert semantic["final_roundtrip_passed"] is True
    assert semantic["reason"] == "route_degraded"
    log_text = (config.output_root / metrics["conversion_log_path"]).read_text(encoding="utf-8")
    assert "FUNCTIONALITY_FAILED_CONTINUING cpp->python: wrong_answer" in log_text


def test_translation_failure_before_evaluation_marks_distance_metrics_unavailable(
    tmp_path: Path,
) -> None:
    config = _config(tmp_path)
    problem = _problem(tmp_path)
    client = RouteClient([LMStudioClientError("service unavailable")])

    result = run_rtt_loop(
        config=config,
        run_id="translation-failure",
        problem=problem,
        target_language="python",
        translation_client=client,
        evaluate_source_fn=SuccessEvaluator(),
    )

    assert result.final_record.status.value == "api_error"
    paths = build_iteration_artifact_paths(
        run_id="translation-failure",
        problem_id=problem.problem_id,
        target_language="python",
        seed_language="cpp",
        iteration_index=1,
    )
    metrics = json.loads((config.output_root / paths.metrics_path).read_text(encoding="utf-8"))
    assert metrics["rtt_distance"]["availability"] == "unavailable"
    assert metrics["rtt_distance"]["reason"] == "no_completed_route"
    assert metrics["rtt_distance"]["failure"]["status"] == "api_error"
    assert metrics["rtt_distance"]["failure"]["status"] != "translation_failed"
    change_count = metrics["distance_metrics"]["change_count"]
    assert change_count["available"] is False
    assert change_count["status"] == "unavailable"
    assert change_count["reason"] == "no_completed_route"
    semantic = metrics["distance_metrics"]["semantic_preservation"]
    assert semantic["available"] is False
    assert semantic["status"] == "not_evaluated"
    assert semantic["reason"] == "no_evaluation_results"


def test_partial_evaluated_route_then_incomplete_final_seed_step(
    tmp_path: Path,
) -> None:
    config = _config(tmp_path)
    problem = _problem(tmp_path)
    client = RouteClient(["print(0)", LMStudioClientError("second translation failed")])

    result = run_rtt_loop(
        config=config,
        run_id="partial-route-incomplete",
        problem=problem,
        target_language="python",
        translation_client=client,
        evaluate_source_fn=StatusByLanguageEvaluator({}),
    )

    assert result.final_record.status.value == "api_error"
    paths = build_iteration_artifact_paths(
        run_id="partial-route-incomplete",
        problem_id=problem.problem_id,
        target_language="python",
        seed_language="cpp",
        iteration_index=1,
    )
    metrics = json.loads((config.output_root / paths.metrics_path).read_text(encoding="utf-8"))
    assert metrics["rtt_distance"]["availability"] == "unavailable"
    assert metrics["rtt_distance"]["reason"] == "no_completed_route"
    assert metrics["distance_metrics"]["change_count"]["available"] is False
    semantic = metrics["distance_metrics"]["semantic_preservation"]
    assert semantic["status"] == "fail"
    assert semantic["reason"] == "route_incomplete"


def _config(tmp_path: Path) -> ExperimentConfig:
    return ExperimentConfig(problem_ids=("IPOP",), seed_language="cpp", target_languages=("c", "java", "python"), lmstudio=LMStudioConfig(model="local", temperature=0.0, host="http://localhost:1234/v1"), runtime=RuntimeConfig(max_iterations=2, timeout_seconds=1), output_root=tmp_path / "artifacts", problem_root=tmp_path / "problem", corpus_root=tmp_path / "corpus")


def _problem(tmp_path: Path) -> ProblemCorpusEntry:
    root = tmp_path / "problem" / "IPOP"
    fix = root / "fixtures"
    fix.mkdir(parents=True)
    (root / "statement.md").write_text("print zero", encoding="utf-8")
    (root / "reference.cpp").write_text("int main(){return 0;}", encoding="utf-8")
    inp = fix / "1.inp"; out = fix / "1.out"
    inp.write_text("", encoding="utf-8"); out.write_text("", encoding="utf-8")
    return ProblemCorpusEntry("IPOP", root / "statement.md", fix, (FixturePair(inp, out),), root / "reference.cpp")
