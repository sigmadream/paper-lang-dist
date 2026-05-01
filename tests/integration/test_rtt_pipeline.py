import json
from pathlib import Path

from rttdist.artifacts import LLMChoice, LLMMessage, LLMRequest, LLMResponse, LLMUsage, build_iteration_artifact_paths
from rttdist.config import ExperimentConfig, LMStudioConfig, RuntimeConfig
from rttdist.corpus import FixturePair, ProblemCorpusEntry
from rttdist.exec.adapters import ExecutionBatchResult, ExecutionStatus
from rttdist.lmstudio_client import TranslationResult
from rttdist.pipeline import run_rtt_loop


class RouteClient:
    def __init__(self, sources: list[str]) -> None:
        self.sources = list(sources)
        self.calls: list[tuple[str, str]] = []

    def translate(self, **kwargs) -> TranslationResult:
        self.calls.append((kwargs["source_language"], kwargs["target_language"]))
        source = self.sources.pop(0)
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
    conversion_log = config.output_root / metrics["conversion_log_path"]
    assert conversion_log.is_file()
    log_text = conversion_log.read_text(encoding="utf-8")
    assert "translation_count_per_cycle=2" in log_text
    assert "step 2/2 COMPLETE python->cpp" in log_text


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
