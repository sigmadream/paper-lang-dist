from copy import deepcopy
from pathlib import Path

import pytest

from rttdist.ast_similarity import _calculate, ast_similarity
from rttdist.experiment_v1 import apply_iteration, convergence, initial_metrics, sf_success
from rttdist.reporting_v1 import aggregate, interval
from rttdist.similarity import token_deltas


def iteration(t, ci=None, status="success", same=True):
    return {"iteration_index": t, "confirmation_index": ci, "status": status,
            "hash_unchanged": same if ci else None, "roundtrip_hash": "a" if status in ("success", "confirmation_failed") else None,
            "all_steps_passed": status in ("success", "confirmation_failed"),
            "steps": [{"step_index": 1, "target_language": "c", "status": "success", "execution": {}},
                      {"step_index": 2, "target_language": "cpp", "status": "wrong_answer" if status == "wrong_answer" else "success", "execution": {}}]}


@pytest.mark.parametrize("failure", ["wrong_answer", "parse_error", "confirmation_failed"])
def test_success_prefix_survives_later_failure(failure):
    m = initial_metrics()
    assert apply_iteration(m, iteration(10), ["a", "a"], 5) is None
    assert m["stabilization"]["tau_candidate"] == 10
    assert apply_iteration(m, iteration(11, 1), ["a"]*3, 5) is None
    assert apply_iteration(m, iteration(12, 2), ["a"]*4, 5) is None
    assert apply_iteration(m, iteration(13, 3, failure, False), ["a"]*4+["b"], 5) == failure
    assert [sf_success(m, c) for c in range(6)] == [True, True, True, False, False, False]


def test_no_candidate_is_not_success_even_if_all_steps_pass():
    m = initial_metrics()
    assert apply_iteration(m, iteration(1), ["a", "b"], 5) is None
    assert m["route_preservation"]["candidate_phase_all_passed"] is None
    assert not sf_success(m, 0)


def test_confirmation_at_search_limit_and_all_five():
    m = initial_metrics()
    apply_iteration(m, iteration(10), ["a", "a"], 5)
    for ci in range(1, 6):
        status = apply_iteration(m, iteration(10+ci, ci), ["a"]*(ci+2), 5)
        assert status == ("success" if ci == 5 else None)
    assert sf_success(m, 5)
    assert m["stabilization"]["confirmation_cycles_run"] == 5


@pytest.mark.parametrize("period", [2, 3, 4])
def test_oscillation_minimum_history(period):
    history = list("abcd"[:period])*2
    assert convergence(history[:-1]) == "continue"
    assert convergence(history) == "oscillation"


def test_ast_contract():
    assert _calculate("int f(int a){return a+1;}", "int g(int b){return b+1;}", 5000)["value"] == 1
    for b in ["int f(int a){return a-1;}", "int f(int a){return a+2;}"]:
        assert _calculate("int f(int a){return a+1;}", b, 5000)["value"] < 1
    assert _calculate("int main( {", "int main(){}", 5000)["reason"] == "parse_invalid"
    assert ast_similarity("int main(){}", "int main(){}", node_limit=1)["reason"] == "tree_too_large"
    assert ast_similarity("int main(){}", "int main(){}", timeout=.0001)["reason"] == "ast_timeout"


def test_tokens_direction_and_reference():
    a = "int main(){int a=1; int b=2; return a+b;}"
    b = "int main(){int b=2; int a=1; return a+b;}"
    values = token_deltas(a, b)
    assert values["token_multiset_dice"]["value"] == 0
    assert values["token_sequence_ratio"]["value"] > 0
    assert all(v["value"] == 0 for v in token_deltas(a, a).values())
    assert token_deltas(a, b) != token_deltas(b, b)
    repeated = "int main(){" + "a++;"*220 + "}"
    assert token_deltas(repeated, repeated)["token_sequence_ratio"]["value"] == 0


def test_cluster_bootstrap_repeats_do_not_increase_problem_count():
    rows = []
    for run in ("r1", "r2", "r3"):
        for p, success in (("p1", True), ("p2", False)):
            m = initial_metrics()
            m["delta_0"] = {name: {"status": "unavailable", "reason": "ast_timeout", "value": None} for name in ("ast_tsed", "token_sequence_ratio", "token_multiset_dice")}
            rows.append({"run_id": run, "problem_id": p, "route": "cpp-to-c", "status": "success" if success else "wrong_answer",
                         "category": "success" if success else "functionality_error", "success": {str(c): success for c in range(6)}, "tau": 1 if success else None, "distance_metrics": m})
    meta = {"problem_ids": ["p1", "p2"], "target_languages": ["c"], "runtime": {"confirmation_cycles": 5},
            "experiment_version": "test", "condition_hash": "a", "validation_snapshot": {"problems": {}}}
    metas = [{**meta, "run_id": run} for run in ("r1", "r2", "r3")]
    pooled, _ = aggregate(rows, metas)
    single, _ = aggregate(rows[:2], metas[:1])
    a, b = pooled["cpp-to-c"], single["cpp-to-c"]
    assert a["problem_count"] == b["problem_count"] == 2
    assert a["evaluable_count"] == 6
    assert a["by_confirmation"]["5"]["p_sf_ci95"] == b["by_confirmation"]["5"]["p_sf_ci95"]
    assert a["conditional"]["5"]["delta_0"]["ast_tsed"]["measurement_rate"] == 0
    assert interval([None]*2000) == (None, "unavailable")
    assert interval([0]*2000) == ([0, 0], "degenerate")


def test_run_route_resume_preserves_completed_step_and_confirmation(tmp_path, monkeypatch):
    from dataclasses import replace
    from tests.integration.test_rtt_pipeline import _config, _problem, SuccessEvaluator
    from rttdist.experiment_v1 import run_route
    from rttdist.experiment_io import read_json, timestamp
    import rttdist.experiment_v1 as runner
    config = _config(tmp_path)
    config = replace(config, lmstudio=replace(config.lmstudio, max_tokens=100))
    problem = _problem(tmp_path)
    seed = problem.seed_path.read_text(encoding="utf-8")
    problem.fixture_pairs[0].input_path.write_text("0\n", encoding="utf-8")
    problem.fixture_pairs[0].output_path.write_text("0\n", encoding="utf-8")
    calls = []
    def transport(payload, host, folder):
        calls.append(str(folder))
        if len(calls) == 4:
            raise RuntimeError("temporary network interruption")
        return {"choices": [{"message": {"content": "```\n" + seed + "\n```"}, "finish_reason": "stop"}]}
    monkeypatch.setattr(runner, "request_translation", transport)
    monkeypatch.setattr(runner, "evaluate_source", SuccessEvaluator())
    meta = {"condition_hash": "fixed", "validation_hash": "validated", "decoding": {},
            "started_at": timestamp(), "recovery": {"max_resumes_per_route": 2, "max_wall_hours": 24}}
    first = run_route(config, problem, "python", "r1", meta)
    assert first["status"] == "api_error"
    assert first["distance_metrics"]["stabilization"]["tau_candidate"] == 1
    resumed = run_route(config, problem, "python", "r1", meta, resume=True)
    assert resumed["status"] == "success"
    assert len(resumed["iterations"]) == 6
    assert len(calls) == 13  # twelve successful calls, one failed; no duplicate completed step
    assert resumed["distance_metrics"]["stabilization"]["confirmations_held"] == 5
    root = config.output_root / "r1" / problem.problem_id / "cpp-to-python"
    assert read_json(root / "attempts.json")["selected_attempt_id"] == "attempt-001"
    with pytest.raises(ValueError, match="condition"):
        run_route(config, problem, "python", "r1", {**meta, "condition_hash": "changed"}, resume=True)
    before = len(calls)
    run_route(config, problem, "python", "r1", meta, resume=True)
    assert len(calls) == before


def test_intermediate_failure_is_terminal_and_selected(tmp_path, monkeypatch):
    from dataclasses import replace
    from tests.integration.test_rtt_pipeline import _config, _problem, StatusByLanguageEvaluator
    from rttdist.exec.adapters import ExecutionStatus
    from rttdist.experiment_v1 import run_route
    from rttdist.experiment_io import read_json, timestamp
    import rttdist.experiment_v1 as runner
    config = _config(tmp_path)
    config = replace(config, lmstudio=replace(config.lmstudio, max_tokens=100))
    problem = _problem(tmp_path)
    calls = []
    problem.fixture_pairs[0].input_path.write_text("0\n", encoding="utf-8")
    problem.fixture_pairs[0].output_path.write_text("0\n", encoding="utf-8")
    def transport(*args):
        calls.append(1)
        return {"choices": [{"message": {"content": "```python\nprint(1)\n```"}}]}
    monkeypatch.setattr(runner, "request_translation", transport)
    monkeypatch.setattr(runner, "evaluate_source", StatusByLanguageEvaluator({"python": ExecutionStatus.WRONG_ANSWER}))
    meta = {"condition_hash": "fixed", "validation_hash": "validated", "decoding": {},
            "started_at": timestamp(), "recovery": {"max_resumes_per_route": 2, "max_wall_hours": 24}}
    result = run_route(config, problem, "python", "r1", meta)
    assert result["status"] == "wrong_answer"
    assert len(calls) == 1
    assert not sf_success(result["distance_metrics"], 0)
    root = config.output_root / "r1" / problem.problem_id / "cpp-to-python"
    assert read_json(root / "attempts.json")["selected_attempt_id"] == "attempt-001"


def test_corpus_gate_rejects_stale_seed_and_fixture(tmp_path, monkeypatch):
    from tests.integration.test_rtt_pipeline import _config, _problem
    from rttdist.experiment_io import corpus_hashes, digest, write_json, validation_gate
    import rttdist.experiment_io as io
    config, problem = _config(tmp_path), _problem(tmp_path)
    env = {"environment": "fixed"}
    monkeypatch.setattr(io, "environment", lambda: env)
    monkeypatch.setattr(io, "validate_corpus", lambda c: (problem,))
    def save(status="success"):
        saved = {"environment": env, "timeout_seconds": config.runtime.timeout_seconds,
                 "content_hashes": corpus_hashes((problem,)), "problems": {problem.problem_id: {"status": status}}}
        saved["validation_hash"] = digest(saved)
        write_json(config.output_root / "corpus_validation.json", saved)
    save()
    assert validation_gate(config)[0] == (problem,)
    problem.seed_path.write_text("int main(){return 2;}", encoding="utf-8")
    with pytest.raises(ValueError, match="Corpus changed"):
        validation_gate(config)
    save()
    problem.fixture_pairs[0].input_path.write_text("new input", encoding="utf-8")
    with pytest.raises(ValueError, match="Corpus changed"):
        validation_gate(config)
    save("wrong_answer")
    with pytest.raises(ValueError, match="seed failures"):
        validation_gate(config)


def test_pooled_report_rejects_mixed_conditions_and_pilot(tmp_path):
    from rttdist.experiment_io import write_json
    from rttdist.reporting_v1 import load_selected
    write_json(tmp_path / "r1/run_metadata.json", {"condition_hash": "a", "phase": "main"})
    write_json(tmp_path / "r2/run_metadata.json", {"condition_hash": "b", "phase": "main"})
    with pytest.raises(ValueError, match="Mixed conditions"):
        load_selected(tmp_path, ["r1", "r2"])
    write_json(tmp_path / "r2/run_metadata.json", {"condition_hash": "a", "phase": "pilot"})
    with pytest.raises(ValueError, match="Pilot"):
        load_selected(tmp_path, ["r1", "r2"])
    with pytest.raises(ValueError, match="Duplicate run"):
        load_selected(tmp_path, ["r1", "r1"])


def test_request_retries_preserve_wire_payload_and_attempts(tmp_path, monkeypatch):
    import io
    import json
    from urllib.error import HTTPError
    import rttdist.experiment_v1 as runner
    calls = []
    class Response:
        status = 200
        def __enter__(self): return self
        def __exit__(self, *args): return False
        def read(self): return json.dumps({"choices": [{"message": {"content": "x"}, "finish_reason": "length"}]}).encode()
    def urlopen(req, timeout):
        calls.append(json.loads(req.data))
        if len(calls) <= 3:
            raise HTTPError(req.full_url, 503, "busy", {}, io.BytesIO(b"busy"))
        return Response()
    monkeypatch.setattr(runner.request, "urlopen", urlopen)
    monkeypatch.setattr(runner.time, "sleep", lambda seconds: None)
    payload = {"model": "test", "messages": [], "max_tokens": 4096, "temperature": 0}
    result = runner.request_translation(payload, "http://localhost:1234/v1", tmp_path)
    assert result["choices"][0]["finish_reason"] == "length"
    assert calls == [payload]*4
    assert len(list(tmp_path.glob("api-attempt-*.json"))) == 4
    assert runner.request_translation(payload, "http://localhost:1234/v1", tmp_path) == result
    assert len(calls) == 4


def test_nontransient_http_error_is_not_retried(tmp_path, monkeypatch):
    import io
    from urllib.error import HTTPError
    import rttdist.experiment_v1 as runner
    def urlopen(req, timeout):
        raise HTTPError(req.full_url, 400, "bad request", {}, io.BytesIO(b"invalid"))
    monkeypatch.setattr(runner.request, "urlopen", urlopen)
    with pytest.raises(RuntimeError, match="400"):
        runner.request_translation({"model": "test"}, "http://localhost:1234/v1", tmp_path)
    assert len(list(tmp_path.glob("api-attempt-*.json"))) == 1


def test_new_attempt_keeps_interrupted_artifacts_and_selects_once(tmp_path, monkeypatch):
    from dataclasses import replace
    from tests.integration.test_rtt_pipeline import _config, _problem, SuccessEvaluator
    from rttdist.experiment_v1 import run_route
    from rttdist.experiment_io import read_json, timestamp
    import rttdist.experiment_v1 as runner
    config, problem = _config(tmp_path), _problem(tmp_path)
    config = replace(config, lmstudio=replace(config.lmstudio, max_tokens=100))
    problem.fixture_pairs[0].input_path.write_text("0\n", encoding="utf-8")
    problem.fixture_pairs[0].output_path.write_text("0\n", encoding="utf-8")
    calls = []
    seed = problem.seed_path.read_text(encoding="utf-8")
    def transport(*args):
        calls.append(1)
        if len(calls) == 1:
            raise RuntimeError("interrupted")
        return {"choices": [{"message": {"content": "```\n"+seed+"\n```"}}]}
    monkeypatch.setattr(runner, "request_translation", transport)
    monkeypatch.setattr(runner, "evaluate_source", SuccessEvaluator())
    meta = {"condition_hash": "fixed", "validation_hash": "validated", "decoding": {},
            "started_at": timestamp(), "recovery": {"max_resumes_per_route": 2, "max_wall_hours": 24}}
    run_route(config, problem, "python", "r1", meta)
    root = config.output_root / "r1" / problem.problem_id / "cpp-to-python"
    old = (root / "attempt-001/run.json").read_bytes()
    run_route(config, problem, "python", "r1", meta, resume=True, new_attempt=True)
    assert (root / "attempt-001/run.json").read_bytes() == old
    index = read_json(root / "attempts.json")
    assert index["selected_attempt_id"] == "attempt-002"
    assert index["attempts"][0]["status"] == "api_error"
    before = len(calls)
    run_route(config, problem, "python", "r1", meta, resume=True, new_attempt=True)
    assert len(calls) == before
