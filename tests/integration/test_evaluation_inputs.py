import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from rttdist.config import ConfigValidationError, load_experiment_config
from rttdist.corpus import CorpusValidationError, validate_corpus
from rttdist.experiment_io import corpus_hashes, timestamp
from rttdist.pipeline import run_rtt_loop
from rttdist.run_state import ResumeValidationError
from tests.integration.test_rtt_pipeline import RouteClient, SuccessEvaluator, _config


REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(params=["IPOP_TEST", "LC_TEST"])
def separated_corpus(tmp_path, request):
    config = _config(tmp_path)
    problem_id = request.param
    root = config.problem_root
    directory = root / "dataset" / problem_id
    if problem_id.startswith("IPOP_"):
        statement = root / f"{problem_id}.md"
        examples = root / problem_id
        evaluation = directory
        seed = config.corpus_root / problem_id / "reference.cpp"
    else:
        statement = directory / "statement.md"
        examples = directory / "prompt_examples"
        evaluation = directory / "evaluation"
        seed = directory / "reference.cpp"
    for path, content in (
        (statement, "PUBLIC_STATEMENT"),
        (examples / "sample.inp", "PUBLIC_INPUT"),
        (examples / "sample.out", "PUBLIC_OUTPUT"),
        (evaluation / "case01.inp", "HELD_OUT_INPUT"),
        (evaluation / "case01.out", "HELD_OUT_OUTPUT"),
        (seed, "int main(){return 0;}"),
        (directory / "README.md", "PRIVATE_DIAGNOSTICS"),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    manifest = root / "dataset" / "manifest.json"
    manifest.write_text("{}", encoding="utf-8")
    index = root / "dataset-index.json"
    index.write_text(json.dumps({"schema_version": 1, "datasets": [{
        "manifest": "dataset/manifest.json",
        "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
        "problems": [{"id": problem_id, "directory": f"dataset/{problem_id}"}],
    }]}), encoding="utf-8")
    config = replace(config, problem_ids=(problem_id,), dataset_index=index,
                     runtime=replace(config.runtime, confirmation_cycles=0),
                     lmstudio=replace(config.lmstudio, max_tokens=100))
    return config, validate_corpus(config)[0]


def test_prepared_dataset_loads_all_400_evaluation_cases():
    config = load_experiment_config(REPO_ROOT / "lmstudio_v2.yaml")
    assert config.dataset_index == REPO_ROOT / "problem/dataset-index.json"
    entries = validate_corpus(config)
    assert len(entries) == 40
    assert sum(len(entry.fixture_pairs) for entry in entries) == 400
    for entry in entries:
        assert entry.prompt_examples
        assert entry.prompt_sample.input_path not in {p.input_path for p in entry.fixture_pairs}
        assert entry.statement_path.name != "README.md"


@pytest.mark.parametrize("runner", ["pipeline", "versioned"])
def test_both_runners_keep_evaluation_out_of_prompts(separated_corpus, monkeypatch, runner):
    config, problem = separated_corpus
    seed = problem.seed_path.read_text(encoding="utf-8")
    prompts, evaluations = [], []

    def evaluate(**kwargs):
        evaluated = kwargs["problem"]
        assert len(evaluated.fixture_pairs) == 1
        assert evaluated.fixture_pairs[0].input_path.read_text(encoding="utf-8") == "HELD_OUT_INPUT"
        assert evaluated.fixture_pairs[0].output_path.read_text(encoding="utf-8") == "HELD_OUT_OUTPUT"
        evaluations.append(kwargs["language"])
        return SuccessEvaluator()(**kwargs)

    if runner == "pipeline":
        class Client(RouteClient):
            def translate(self, **kwargs):
                prompts.append(json.dumps(kwargs))
                return super().translate(**kwargs)
        result = run_rtt_loop(config=config, run_id="split", problem=problem,
                              target_language="python", translation_client=Client([seed, seed]),
                              evaluate_source_fn=evaluate)
        assert result.final_record.status.value == "success"
    else:
        import rttdist.experiment_v1 as versioned

        def transport(payload, host, folder):
            prompts.append(json.dumps(payload))
            return {"choices": [{"message": {"content": f"```\n{seed}\n```"}, "finish_reason": "stop"}]}

        monkeypatch.setattr(versioned, "request_translation", transport)
        monkeypatch.setattr(versioned, "evaluate_source", evaluate)
        metadata = {"condition_hash": "fixed", "validation_hash": "validated", "decoding": {},
                    "started_at": timestamp(), "recovery": {"max_resumes_per_route": 2, "max_wall_hours": 24}}
        result = versioned.run_route(config, problem, "python", "split", metadata)
        assert result["status"] == "success"
    assert evaluations == ["python", "cpp"]
    assert len(prompts) == 2
    for prompt in prompts:
        assert "PUBLIC_INPUT" in prompt and "PUBLIC_OUTPUT" in prompt and "PUBLIC_STATEMENT" in prompt
        assert "HELD_OUT" not in prompt and "PRIVATE_DIAGNOSTICS" not in prompt


def test_missing_evaluation_never_falls_back_to_prompt_examples(separated_corpus):
    config, problem = separated_corpus
    problem.fixture_pairs[0].input_path.unlink()
    with pytest.raises(CorpusValidationError, match="Missing fixture pair"):
        validate_corpus(config)


def test_missing_prompt_never_falls_back_to_evaluation(separated_corpus):
    config, problem = separated_corpus
    problem.prompt_sample.input_path.unlink()
    with pytest.raises(CorpusValidationError, match="Missing fixture pair"):
        validate_corpus(config)


def test_rejects_overlapping_inputs(separated_corpus):
    config, problem = separated_corpus
    problem.fixture_pairs[0].input_path.write_text(" PUBLIC_INPUT\n", encoding="utf-8")
    with pytest.raises(CorpusValidationError, match="overlaps prompt"):
        validate_corpus(config)


def test_rejects_unindexed_problem(separated_corpus):
    config, _ = separated_corpus
    with pytest.raises(CorpusValidationError, match="missing from dataset index"):
        validate_corpus(replace(config, problem_ids=("IPOP_MISSING",)))


@pytest.mark.parametrize("source", ["prompt", "evaluation"])
def test_resume_and_provenance_detect_input_changes(separated_corpus, source):
    config, problem = separated_corpus
    seed = problem.seed_path.read_text(encoding="utf-8")
    before = corpus_hashes((problem,))
    arguments = dict(config=config, run_id="resume", problem=problem, target_language="python",
                     evaluate_source_fn=SuccessEvaluator())
    run_rtt_loop(**arguments, translation_client=RouteClient([seed, seed]))
    pair = problem.prompt_sample if source == "prompt" else problem.fixture_pairs[0]
    pair.output_path.write_text("CHANGED", encoding="utf-8")
    assert before != corpus_hashes((problem,))
    with pytest.raises(ResumeValidationError, match="corpus hash mismatch"):
        run_rtt_loop(**arguments, translation_client=RouteClient([]))


@pytest.mark.parametrize("value", [None, "", 123])
def test_invalid_dataset_index_config_is_rejected(tmp_path, value):
    import yaml
    raw = yaml.safe_load((REPO_ROOT / "lmstudio_v2.yaml").read_text(encoding="utf-8"))
    raw["dataset_index"] = value
    path = tmp_path / "invalid.yaml"
    path.write_text(yaml.safe_dump(raw), encoding="utf-8")
    with pytest.raises(ConfigValidationError, match="dataset_index"):
        load_experiment_config(path)
