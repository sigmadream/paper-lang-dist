import pytest

from rttdist import hops_experiment as hops
from rttdist.experiment_io import read_json, write_json
from tests.integration.test_hops_experiment import MockProvider, setup


def test_cached_observation_never_calls_provider_again(setup):
    cfg, job, folder = setup
    assert hasattr(hops, "run_hops_observation"), "재개 기능이 필요합니다."
    provider = MockProvider()
    first = hops.run_hops_observation(cfg, job, provider, folder)
    second = hops.run_hops_observation(cfg, job, provider, folder)
    assert first == second
    assert len(provider.calls) == 4


def test_response_reused_after_evaluation_crash(setup, monkeypatch):
    cfg, job, folder = setup
    assert hasattr(hops, "run_hops_observation"), "재개 기능이 필요합니다."
    provider = MockProvider()
    real_evaluate = hops.evaluate

    def crash(*args):
        raise KeyboardInterrupt("응답 저장 후 프로세스 충돌")

    monkeypatch.setattr(hops, "evaluate", crash)
    with pytest.raises(KeyboardInterrupt):
        hops.run_hops_observation(cfg, job, provider, folder)
    assert (folder / "step-01/provider_result.json").is_file()
    monkeypatch.setattr(hops, "evaluate", real_evaluate)
    record = hops.run_hops_observation(cfg, job, provider, folder)
    assert record["translation_steps"] == 4
    assert len(provider.calls) == 4


def test_replay_step_cache_and_contract_change_refused(setup, monkeypatch):
    cfg, job, folder = setup
    assert hasattr(hops, "run_hops_observation"), "재개 기능이 필요합니다."
    provider = MockProvider()
    hops.run_hops_observation(cfg, job, provider, folder)
    (folder / "observation.json").unlink()
    monkeypatch.setattr(
        hops,
        "evaluate",
        lambda *a: pytest.fail("저장된 평가는 다시 실행하지 않습니다."),
    )
    monkeypatch.setattr(
        hops, "measure", lambda *a, **k: pytest.fail("저장된 유사도는 재사용합니다.")
    )
    hops.run_hops_observation(cfg, job, provider, folder)
    assert len(provider.calls) == 4
    cfg["llm"]["generation"]["temperature"] = 0.1
    with pytest.raises(ValueError, match="계약"):
        hops.run_hops_observation(cfg, job, provider, folder)


def test_pilot_response_never_reused_for_main(setup):
    cfg, job, folder = setup
    assert hasattr(hops, "run_hops_observation"), "단계 격리가 필요합니다."
    provider = MockProvider()
    pilot = hops.run_hops_observation(cfg, job, provider, folder / "pilot")
    job = {**job, "phase": "main"}
    main = hops.run_hops_observation(cfg, job, provider, folder / "main")
    assert len(provider.calls) == 8
    assert pilot["steps"][0]["call_id"] != main["steps"][0]["call_id"]


def test_ambiguous_request_cannot_be_replayed_without_response(setup):
    cfg, job, folder = setup
    assert hasattr(
        hops, "run_hops_observation"
    ), "불명확한 전송 복구 차단이 필요합니다."

    class InterruptedProvider(MockProvider):
        def complete(self, payload, folder):
            raise KeyboardInterrupt("응답 수신 여부 불명")

    with pytest.raises(KeyboardInterrupt):
        hops.run_hops_observation(cfg, job, InterruptedProvider(), folder)
    provider = MockProvider()
    record = hops.run_hops_observation(cfg, job, provider, folder)
    assert not provider.calls
    assert record["reason"] == "request_outcome_unknown"


def test_resume_restores_reached_outcomes_before_applying_elapsed_budget(setup):
    cfg, job, folder = setup
    provider = MockProvider()
    original = hops.run_hops_observation(cfg, job, provider, folder)
    (folder / "observation.json").unlink()
    write_json(folder / "timing.json", {"elapsed_seconds": 901})
    restored = hops.run_hops_observation(cfg, job, provider, folder)
    assert restored["outcomes"] == original["outcomes"]
    assert restored["confirmation_status"] == "passed"
    assert len(provider.calls) == 4
