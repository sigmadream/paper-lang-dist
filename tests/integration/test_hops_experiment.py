import json
from pathlib import Path
import socket

import pytest

from rttdist import hops_experiment as hops
from rttdist.experiment_io import read_json, write_json


class MockProvider:
    def __init__(self, outputs=None, actual_model="test"):
        self.outputs = iter(outputs or [f"code-{n}" for n in range(1, 13)])
        self.calls = []
        self.actual_model = actual_model

    def complete(self, payload, folder):
        self.calls.append(payload)
        return {
            "text": next(self.outputs),
            "finish_reason": "stop",
            "actual_model": self.actual_model,
            "model_evidence": "exact",
            "usage": {"input_tokens": 10, "output_tokens": 5},
            "cost_usd": None,
            "request_id": str(payload["logical_request"]),
            "requested_generation": {"seed": 20261117},
            "sent_generation": {"seed": 20261117},
            "effective_generation": None,
        }


@pytest.fixture
def setup(tmp_path, monkeypatch):
    monkeypatch.setattr(
        socket,
        "create_connection",
        lambda *a, **k: pytest.fail("실제 네트워크 호출 금지"),
    )
    cfg = hops.load_hops_config(
        Path(__file__).resolve().parents[2] / "configs/v1.6/experiment.yaml"
    )
    cfg.update(corpus_root=str(tmp_path / "corpus"), output_root=str(tmp_path / "out"))
    cfg["llm"].update(model="test", allowed_response_models=[])
    problem = Path(cfg["corpus_root"]) / "IPOP_11729"
    problem.mkdir(parents=True)
    (problem / "reference.cpp").write_text("origin", encoding="utf-8")
    (problem / "statement.md").write_text("공개 명세", encoding="utf-8")
    examples = problem / "prompt_examples"
    examples.mkdir()
    for n in range(3):
        (examples / f"{n}.inp").write_text(f"public-{n}", encoding="utf-8")
        (examples / f"{n}.out").write_text("example", encoding="utf-8")
    private = problem / "evaluation"
    private.mkdir()
    (private / "secret.inp").write_text("PRIVATE-INPUT", encoding="utf-8")
    (private / "secret.out").write_text("PRIVATE-ANSWER", encoding="utf-8")
    monkeypatch.setattr(
        hops, "evaluate", lambda *a: {"status": "success"}, raising=False
    )
    monkeypatch.setattr(
        hops,
        "measure",
        lambda *a, **k: {"status": "measured", "value": 0.95},
        raising=False,
    )
    job = {
        "campaign_id": "test-campaign",
        "phase": "pilot",
        "problem_id": "IPOP_11729",
        "route": "cpp-via-python",
        "seed_language": "cpp",
        "target_language": "python",
        "repeat": 1,
    }
    return cfg, job, tmp_path / "observation"


def test_normalized_response_two_hop_success_and_confirmation(setup):
    cfg, job, folder = setup
    assert hasattr(hops, "run_hops_observation"), "v1.6 실행기가 필요합니다."
    provider = MockProvider()
    record = hops.run_hops_observation(cfg, job, provider, folder)
    assert record["outcomes"]["0.85"]["reached_step"] == 2
    assert record["translation_steps"] == 4
    assert record["confirmation_status"] == "passed"
    assert record["complete_by_threshold"] == {"0.80": True, "0.85": True, "0.90": True}
    assert record["steps"][0]["effective_generation"] is None
    assert record["steps"][1]["sym_origin"] == 0.95
    assert read_json(folder / "observation.json") == record
    assert hops.audit_observation(record, {"config": cfg})["passed"]
    prompt = json.dumps(provider.calls, ensure_ascii=False)
    assert "PRIVATE-INPUT" not in prompt and "PRIVATE-ANSWER" not in prompt
    assert "public-0" in prompt and "public-1" in prompt and "public-2" not in prompt
    assert all(
        p["logical_request"]["phase"] == "pilot"
        and p["logical_request"]["campaign"] == "test-campaign"
        for p in provider.calls
    )


def test_tenth_reach_and_confirmation_only_twelfth_score(setup, monkeypatch):
    cfg, job, folder = setup
    scores = iter([0.1, 0.1, 0.1, 0.1, 0.86, 0.95])
    monkeypatch.setattr(
        hops,
        "measure",
        lambda a, b, p, **k: {
            "status": "measured",
            "value": next(scores) if p.name.startswith("sym_adj") else 0.4,
        },
        raising=False,
    )
    assert hasattr(hops, "run_hops_observation"), "v1.6 실행기가 필요합니다."
    record = hops.run_hops_observation(cfg, job, MockProvider(), folder)
    assert record["translation_steps"] == 12
    assert record["outcomes"]["0.85"]["reached_step"] == 10
    assert record["outcomes"]["0.90"]["category"] == "hop_limit"
    assert record["steps"][-1]["kind"] == "confirmation"


def test_local_similarity_retry_and_unresolved_invalid(setup, monkeypatch):
    cfg, job, folder = setup
    calls = []

    def unavailable(a, b, p, **kwargs):
        calls.append(p)
        return {"status": "unavailable", "value": None}

    monkeypatch.setattr(hops, "measure", unavailable, raising=False)
    assert hasattr(hops, "run_hops_observation"), "v1.6 실행기가 필요합니다."
    provider = MockProvider()
    record = hops.run_hops_observation(cfg, job, provider, folder)
    assert record["outcomes"]["0.85"]["category"] == "invalid"
    assert len(provider.calls) == 2
    assert sum(p.name.startswith("sym_adj") for p in calls) == 2
    assert len({str(p) for p in calls}) == len(calls)


def test_unresolved_origin_similarity_also_blocks_unreached_outcomes(
    setup, monkeypatch
):
    cfg, job, folder = setup
    monkeypatch.setattr(
        hops,
        "measure",
        lambda a, b, path, **k: {
            "status": (
                "unavailable" if path.name.startswith("sym_origin") else "measured"
            ),
            "value": None if path.name.startswith("sym_origin") else 0.95,
        },
    )
    record = hops.run_hops_observation(cfg, job, MockProvider(), folder)
    assert record["outcomes"]["0.85"]["category"] == "invalid"
    assert record["translation_steps"] == 2


@pytest.mark.parametrize("model", ["other-test", None])
def test_direct_model_mismatch_or_missing_is_invalid(setup, model):
    cfg, job, folder = setup
    assert hasattr(hops, "run_hops_observation"), "v1.6 실행기가 필요합니다."
    record = hops.run_hops_observation(
        cfg, job, MockProvider(actual_model=model), folder
    )
    assert record["outcomes"]["0.85"]["category"] == "invalid"
    assert record["terminal_status"] == "infrastructure_error"


def test_later_failure_preserves_primary_success(setup, monkeypatch):
    cfg, job, folder = setup
    monkeypatch.setattr(
        hops,
        "measure",
        lambda *a, **k: {"status": "measured", "value": 0.86},
        raising=False,
    )
    monkeypatch.setattr(
        hops,
        "evaluate",
        lambda source, *a: {"status": "wrong_answer" if source == "bad" else "success"},
        raising=False,
    )
    assert hasattr(hops, "run_hops_observation"), "v1.6 실행기가 필요합니다."
    record = hops.run_hops_observation(
        cfg, job, MockProvider(["B", "A1", "bad"]), folder
    )
    assert record["outcomes"]["0.85"]["success"]
    assert record["outcomes"]["0.90"]["category"] == "functional_failure"
    assert record["confirmation_status"] == "failed"


def test_wall_clock_is_infrastructure_stop(setup, monkeypatch):
    cfg, job, folder = setup
    assert hasattr(hops, "run_hops_observation"), "v1.6 실행기가 필요합니다."
    ticks = iter([0, 901])
    monkeypatch.setattr(hops.time, "monotonic", lambda: next(ticks))
    provider = MockProvider()
    record = hops.run_hops_observation(cfg, job, provider, folder)
    assert not provider.calls
    assert record["reason"] == "observation_wall_clock"
    assert record["outcomes"]["0.85"]["category"] == "invalid"


def test_fixed_schedule_partition_has_no_duplicate_or_missing_slots():
    cfg = hops.load_hops_config(
        Path(__file__).resolve().parents[2] / "configs/v1.6/experiment.yaml"
    )
    assert hasattr(hops, "build_hops_schedule"), "고정 작업 순서가 필요합니다."
    main = hops.build_hops_schedule(cfg, "main")
    pilot = hops.build_hops_schedule(cfg, "pilot")
    shards = [hops.build_hops_schedule(cfg, "main", f"{i}/3") for i in (1, 2, 3)]
    key = lambda j: (j["problem_id"], j["route"], j["repeat"])
    assert len(main) == len(set(map(key, main))) == 300
    assert len(pilot) == 12
    assert set(map(key, main)) == {key(j) for shard in shards for j in shard}
    assert sum(map(len, shards)) == 300
    assert main == hops.build_hops_schedule(cfg, "main")
    assert all(j["phase"] == "pilot" for j in pilot)


def test_payload_uses_real_protocol_contract(setup):
    from rttdist.provider_protocols import build_request

    cfg, job, folder = setup

    class ContractProvider(MockProvider):
        def complete(self, payload, folder):
            body = build_request(
                "chat_completions",
                payload,
                {"supported_options": list(cfg["llm"]["generation"])},
            )
            assert "logical_request" not in body
            return super().complete(payload, folder)

    hops.run_hops_observation(cfg, job, ContractProvider(), folder)


def test_real_reporter_reads_hop_outcomes(setup):
    cfg, job, unused_folder = setup
    root = hops.campaign_root(cfg) / "main"
    job = {**job, "phase": "main"}
    folder = root / job["problem_id"] / job["route"] / "attempt-01"
    record = hops.run_hops_observation(cfg, job, MockProvider(), folder)
    write_json(root / "contract.json", read_json(folder / "contract.json"))
    summary = hops.report_hops_campaign(cfg, "main")
    assert summary["routes"][job["route"]]["H"] == 2
    assert summary["routes"][job["route"]]["D"] == 2
    assert not summary["complete_by_threshold"]["0.85"]


def test_real_copilot_config_sends_empty_generation_without_common_defaults(setup):
    cfg, job, folder = setup
    root = Path(__file__).resolve().parents[2]
    cfg["llm"] = hops.load_hops_config(
        root / "configs/v1.6/experiment.yaml",
        root / "configs/v1.6/providers/copilot.yaml",
    )["llm"]
    cfg["llm"]["model"] = "selected-model"

    class SdkMock(MockProvider):
        def complete(self, payload, folder):
            assert payload["generation"] == {}
            result = super().complete(payload, folder)
            result.update(
                actual_model=None,
                model_evidence={"status": "missing", "valid": False},
                requested_generation={},
                sent_generation={},
                effective_generation=None,
            )
            return result

    record = hops.run_hops_observation(cfg, job, SdkMock(), folder)
    assert record["comparison_class"] == "sdk_exploratory"
    assert record["steps"][0]["requested_generation"] == {}
    assert record["steps"][0]["sent_generation"] == {}
    assert record["steps"][0]["effective_generation"] is None
