from copy import deepcopy

import pytest

from rttdist import hops_experiment as hops
from rttdist.experiment_io import read_json
from tests.integration.test_hops_experiment import MockProvider, setup


@pytest.mark.parametrize("stage", ["response", "evaluation", "sym_adj", "sym_origin"])
@pytest.mark.parametrize("late_step", [2, 4, 10, 12])
def test_late_result_is_not_accepted_and_cached_replay_cannot_bypass_limit(
    setup, monkeypatch, stage, late_step
):
    cfg, job, folder = setup
    clock = {"now": 0}
    monkeypatch.setattr(hops.time, "monotonic", lambda: clock["now"])
    reason = "confirmation_wall_clock" if late_step == 12 else "observation_wall_clock"

    def expire():
        clock["now"] = 301 if late_step == 12 else 901

    class TimedProvider(MockProvider):
        def complete(self, payload, destination):
            response = super().complete(payload, destination)
            response["cost_usd"] = 0.25
            if len(self.calls) == late_step and stage == "response":
                expire()
            return response

    def evaluate(source, *args):
        if source == f"code-{late_step}" and stage == "evaluation":
            expire()
        return {"status": "success"}

    def measure(a, b, destination, **kwargs):
        number = int(destination.parent.name.split("-")[1])
        if number == late_step and destination.name == stage:
            expire()
        score = 0.1
        if number == late_step:
            score = 0.95
        elif (late_step == 4 and number == 2) or (late_step == 12 and number == 10):
            score = 0.86
        return {"status": "measured", "value": score}

    monkeypatch.setattr(hops, "evaluate", evaluate)
    monkeypatch.setattr(hops, "measure", measure)
    provider = TimedProvider()
    record = hops.run_hops_observation(cfg, job, provider, folder)
    assert record["reason"] == reason
    assert record["terminal_status"] == "infrastructure_error"
    assert record["translation_steps"] == late_step
    assert record["cost_usd"] == late_step * 0.25
    if late_step in (4, 12):
        assert record["outcomes"]["0.85"]["reached_step"] == (
            2 if late_step == 4 else 10
        )
        assert record["confirmation_status"] == "unavailable"
    else:
        assert record["outcomes"]["0.85"]["category"] == "invalid"
    assert record["outcomes"]["0.90"]["category"] == (
        "hop_limit" if late_step == 12 else "invalid"
    )
    late_folder = folder / f"step-{late_step:02}"
    assert read_json(late_folder / "provider_result.json")["cost_usd"] == 0.25
    assert read_json(late_folder / "processed.json")["deadline_reason"] == reason
    frozen_outcomes = deepcopy(record["outcomes"])
    (folder / "observation.json").unlink()
    clock["now"] = 0
    monkeypatch.setattr(
        hops, "evaluate", lambda *a: pytest.fail("평가 캐시를 재생해야 합니다.")
    )
    monkeypatch.setattr(
        hops, "measure", lambda *a, **k: pytest.fail("유사도 캐시를 재생해야 합니다.")
    )
    resumed = hops.run_hops_observation(cfg, job, provider, folder)
    assert resumed["outcomes"] == frozen_outcomes
    assert resumed["reason"] == reason
    assert resumed["cost_usd"] == record["cost_usd"]
    assert len(provider.calls) == late_step


def test_confirmation_budget_includes_pause_after_tenth_processed_result(
    setup, monkeypatch
):
    cfg, job, folder = setup
    clock = {"now": 0}
    monkeypatch.setattr(hops.time, "monotonic", lambda: clock["now"])
    monkeypatch.setattr(
        hops,
        "measure",
        lambda a, b, destination, **k: {
            "status": "measured",
            "value": 0.86 if destination.parent.name == "step-10" else 0.1,
        },
    )
    provider = MockProvider()
    original_write = hops.write_json

    def crash(path, value):
        if path.name == "step.json" and path.parent.name == "step-10":
            raise KeyboardInterrupt("10홉 결과 저장 후 충돌")
        return original_write(path, value)

    monkeypatch.setattr(hops, "write_json", crash)
    with pytest.raises(KeyboardInterrupt):
        hops.run_hops_observation(cfg, job, provider, folder)
    clock["now"] = 301
    monkeypatch.setattr(hops, "write_json", original_write)
    record = hops.run_hops_observation(cfg, job, provider, folder)
    assert record["reason"] == "confirmation_wall_clock"
    assert record["confirmation_status"] == "unavailable"
    assert record["outcomes"]["0.85"]["reached_step"] == 10
    assert record["outcomes"]["0.90"]["category"] == "hop_limit"
    assert len(provider.calls) == 10


def test_response_cost_is_retained_after_crash_before_processed_timing(
    setup, monkeypatch
):
    cfg, job, folder = setup
    clock = {"now": 0}
    monkeypatch.setattr(hops.time, "monotonic", lambda: clock["now"])

    def crash(source, *args):
        if source == "code-2":
            clock["now"] = 901
            raise KeyboardInterrupt("평가 중 충돌")
        return {"status": "success"}

    monkeypatch.setattr(hops, "evaluate", crash)

    class ChargedProvider(MockProvider):
        def complete(self, payload, destination):
            return {**super().complete(payload, destination), "cost_usd": 0.25}

    provider = ChargedProvider()
    with pytest.raises(KeyboardInterrupt):
        hops.run_hops_observation(cfg, job, provider, folder)
    assert not (folder / "step-02/processed.json").exists()
    monkeypatch.setattr(
        hops,
        "evaluate",
        lambda *a: pytest.fail("시간 초과 응답은 재평가하지 않습니다."),
    )
    record = hops.run_hops_observation(cfg, job, provider, folder)
    assert record["reason"] == "observation_wall_clock"
    assert record["outcomes"]["0.85"]["category"] == "invalid"
    assert record["cost_usd"] == 0.5
    assert len(provider.calls) == 2


def test_clock_regression_cannot_reset_budget_for_saved_response(setup, monkeypatch):
    cfg, job, folder = setup
    clock = {"now": 100}
    monkeypatch.setattr(hops.time, "monotonic", lambda: clock["now"])

    def crash(*args):
        clock["now"] = 1001
        raise KeyboardInterrupt("평가 중 충돌")

    monkeypatch.setattr(hops, "evaluate", crash)
    provider = MockProvider()
    with pytest.raises(KeyboardInterrupt):
        hops.run_hops_observation(cfg, job, provider, folder)
    clock["now"] = 0
    monkeypatch.setattr(
        hops,
        "evaluate",
        lambda *a: pytest.fail("신뢰할 수 없는 시계에서 재평가하지 않습니다."),
    )
    record = hops.run_hops_observation(cfg, job, provider, folder)
    assert record["reason"] == "observation_clock_unavailable"
    assert record["outcomes"]["0.85"]["category"] == "invalid"
    assert len(provider.calls) == 1
    (folder / "observation.json").unlink()
    (folder / "step-01/processed.json").unlink()
    restarted = hops.run_hops_observation(cfg, job, provider, folder)
    assert restarted["reason"] == "observation_clock_unavailable"
    assert len(provider.calls) == 1


def test_deadline_crossed_while_saving_processed_result_blocks_new_reach(
    setup, monkeypatch
):
    cfg, job, folder = setup
    clock = {"now": 0}
    monkeypatch.setattr(hops.time, "monotonic", lambda: clock["now"])
    real_write = hops.write_json

    def delayed_write(path, value):
        result = real_write(path, value)
        if path.name == "processed.json" and path.parent.name == "step-02":
            clock["now"] = 901
        return result

    monkeypatch.setattr(hops, "write_json", delayed_write)
    provider = MockProvider()
    record = hops.run_hops_observation(cfg, job, provider, folder)
    assert record["outcomes"]["0.85"]["category"] == "invalid"
    assert record["reason"] == "observation_wall_clock"
    (folder / "observation.json").unlink()
    clock["now"] = 0
    resumed = hops.run_hops_observation(cfg, job, provider, folder)
    assert resumed["outcomes"] == record["outcomes"]
    assert resumed["reason"] == record["reason"]
    assert len(provider.calls) == 2
