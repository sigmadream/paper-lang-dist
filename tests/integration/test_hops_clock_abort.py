from copy import deepcopy

import pytest

from rttdist import hops_experiment as hops
from rttdist.experiment_io import read_json
from tests.integration.test_hops_experiment import MockProvider, setup


@pytest.mark.parametrize("committed_steps", [1, 2])
@pytest.mark.parametrize("next_cache", ["missing", "response", "processed"])
def test_clock_abort_survives_repeated_observation_save_crashes(
    setup, monkeypatch, committed_steps, next_cache
):
    cfg, job, folder = setup
    clock = {"now": 100}
    monkeypatch.setattr(hops.time, "monotonic", lambda: clock["now"])
    monkeypatch.setattr(
        hops,
        "measure",
        lambda *a, **k: {
            "status": "measured",
            "value": 0.95 if committed_steps == 1 else 0.86,
        },
    )

    class ChargedProvider(MockProvider):
        def complete(self, payload, destination):
            return {**super().complete(payload, destination), "cost_usd": 0.25}

    provider = ChargedProvider()
    real_write = hops.write_json
    crash_file = {
        "missing": "step.json",
        "response": "provider_result.json",
        "processed": "processed.json",
    }[next_cache]
    crash_step = committed_steps if next_cache == "missing" else committed_steps + 1

    def initial_crash(path, value):
        result = real_write(path, value)
        if path.name == crash_file and path.parent.name == f"step-{crash_step:02}":
            raise KeyboardInterrupt("기존 단계·응답 저장 후 충돌")
        return result

    monkeypatch.setattr(hops, "write_json", initial_crash)
    with pytest.raises(KeyboardInterrupt):
        hops.run_hops_observation(cfg, job, provider, folder)
    initial_calls = len(provider.calls)
    assert initial_calls == crash_step
    assert read_json(folder / "timing.json")["checkpoint_monotonic"] == 100
    assert not (folder / "observation.json").exists()
    responses = {p: p.read_bytes() for p in folder.glob("step-*/provider_result.json")}
    valid_decisions = {
        folder
        / f"step-{number:02}/decision.json": (
            folder / f"step-{number:02}/decision.json"
        ).read_bytes()
        for number in range(1, committed_steps + 1)
    }
    attempted_records = []

    def final_save_crash(path, value):
        if path.name == "observation.json":
            attempted_records.append(deepcopy(value))
            raise KeyboardInterrupt("시계 역행 중단 후 최종 관측 저장 직전 충돌")
        return real_write(path, value)

    monkeypatch.setattr(hops, "write_json", final_save_crash)
    for now in (0, 101):
        clock["now"] = now
        with pytest.raises(KeyboardInterrupt):
            hops.run_hops_observation(cfg, job, provider, folder)
        assert attempted_records[-1]["reason"] == "observation_clock_unavailable"
        assert len(provider.calls) == initial_calls
        assert not (folder / "observation.json").exists()

    monkeypatch.setattr(hops, "write_json", real_write)
    clock["now"] = 102
    record = hops.run_hops_observation(cfg, job, provider, folder)
    assert record["reason"] == "observation_clock_unavailable"
    assert record["terminal_status"] == "infrastructure_error"
    assert record["outcomes"] == attempted_records[0]["outcomes"]
    assert record["outcomes"]["0.85"]["category"] == (
        "success" if committed_steps == 2 else "invalid"
    )
    assert record["outcomes"]["0.90"]["category"] == "invalid"
    assert record["cost_usd"] == initial_calls * 0.25
    assert len(provider.calls) == initial_calls
    assert all(path.read_bytes() == raw for path, raw in responses.items())
    assert all(path.read_bytes() == raw for path, raw in valid_decisions.items())
    if next_cache == "missing":
        assert (
            read_json(folder / "clock_abort.json")["reason"]
            == "observation_clock_unavailable"
        )
    assert hops.run_hops_observation(cfg, job, provider, folder) == record
    assert len(provider.calls) == initial_calls
