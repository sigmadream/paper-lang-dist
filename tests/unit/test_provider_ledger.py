import io
import json

import pytest

from rttdist.providers import create_provider, CostCapReached, ProviderError


def config(**overrides):
    result = {
        "provider": "compatible",
        "protocol": "chat_completions",
        "base_url": "https://example.test/v1",
        "model": "test",
        "generation": {"max_tokens": 20},
        "generation_profile": {"supported_options": ["max_tokens"]},
        "retries": 2,
        "request_timeout": 1,
        "max_calls": 10,
    }
    result.update(overrides)
    return result


def test_missing_usage_stays_null_but_counts_against_shared_call_cap(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(
        "rttdist.providers.request.urlopen",
        lambda *a, **k: io.BytesIO(b'{"model":"test","choices":[]}'),
    )
    ledger = tmp_path / "ledger.jsonl"
    first = create_provider(config(max_calls=1), ledger)
    result = first.complete({"model": "test", "messages": []}, tmp_path / "one")
    assert result["cost_usd"] is None and result["cost_source"] is None
    second = create_provider(config(max_calls=1), ledger)
    with pytest.raises(CostCapReached):
        second.complete({"model": "test", "messages": []}, tmp_path / "two")
    assert len(ledger.read_text().splitlines()) == 1


def test_pending_shard_reservation_prevents_overspending(tmp_path):
    cfg = config(cost_cap_usd=0.15, max_request_cost_usd=0.1)
    first = create_provider(cfg, tmp_path / "ledger.jsonl")
    second = create_provider(cfg, tmp_path / "ledger.jsonl")
    first.reserve_request_budget("one", 0.1)
    with pytest.raises(CostCapReached):
        second.reserve_request_budget("two", 0.1)


def test_dollar_cap_requires_price_bound_and_negative_limits_rejected():
    with pytest.raises(ValueError, match="estimat|pricing|maximum"):
        create_provider(config(cost_cap_usd=1))
    with pytest.raises(ValueError):
        create_provider(config(max_calls=-1))
    with pytest.raises(ValueError, match="cap|상한"):
        create_provider(config(max_calls=None))


def test_reported_cost_and_estimated_cost_are_distinguished(tmp_path, monkeypatch):
    bodies = iter(
        [
            {
                "model": "test",
                "choices": [],
                "usage": {"prompt_tokens": 1000, "completion_tokens": 10, "cost": 0.2},
            },
            {
                "model": "test",
                "choices": [],
                "usage": {"prompt_tokens": 1000, "completion_tokens": 10},
            },
        ]
    )
    monkeypatch.setattr(
        "rttdist.providers.request.urlopen",
        lambda *a, **k: io.BytesIO(json.dumps(next(bodies)).encode()),
    )
    provider = create_provider(
        config(pricing={"input_per_million": 1, "output_per_million": 2}),
        tmp_path / "ledger.jsonl",
    )
    first = provider.complete({"messages": []}, tmp_path / "one")
    second = provider.complete({"messages": []}, tmp_path / "two")
    assert first["cost_usd"] == 0.2 and first["cost_source"] == "reported"
    assert (
        second["cost_usd"] == pytest.approx(0.00102)
        and second["cost_source"] == "estimated"
    )


def test_logical_key_deduplicates_other_shard_folder_and_rejects_changed_request(
    tmp_path, monkeypatch
):
    calls = []

    def send(*args, **kwargs):
        calls.append(1)
        return io.BytesIO(b'{"model":"test","choices":[]}')

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    payload = {
        "messages": [],
        "logical_request": {
            "campaign": "c",
            "phase": "main",
            "problem": "p",
            "route": "python",
            "repeat": 1,
            "step": 2,
        },
    }
    ledger = tmp_path / "ledger.jsonl"
    create_provider(config(), ledger).complete(payload, tmp_path / "a")
    create_provider(config(), ledger).complete(payload, tmp_path / "b")
    assert len(calls) == 1
    payload["messages"] = [{"role": "user", "content": "different"}]
    with pytest.raises(ValueError, match="changed"):
        create_provider(config(), ledger).complete(payload, tmp_path / "c")


def test_concurrent_shards_reserve_only_one_last_budget_slot(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    import threading

    barrier = threading.Barrier(2)

    def reserve(name):
        provider = create_provider(config(max_calls=1), tmp_path / "ledger.jsonl")
        barrier.wait()
        try:
            provider.reserve_request_budget(name, None)
            return "reserved"
        except CostCapReached:
            return "capped"

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(reserve, ["one", "two"]))
    assert sorted(outcomes) == ["capped", "reserved"]


def test_distinct_processes_share_the_same_budget_reservation(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    import subprocess
    import sys

    script = """
import json
import sys
from rttdist.providers import create_provider, CostCapReached
provider = create_provider(json.loads(sys.argv[1]), sys.argv[2])
try:
    provider.reserve_request_budget(sys.argv[3], None)
    print('reserved')
except CostCapReached:
    print('capped')
"""

    def reserve(name):
        proc = subprocess.run(
            [
                sys.executable,
                "-c",
                script,
                json.dumps(config(max_calls=1)),
                str(tmp_path / "ledger.jsonl"),
                name,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert proc.returncode == 0, proc.stderr
        return proc.stdout.strip()

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(reserve, ["one", "two"]))
    assert sorted(outcomes) == ["capped", "reserved"]


def test_unknown_usage_with_dollar_cap_keeps_conservative_reservation(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(
        "rttdist.providers.request.urlopen",
        lambda *a, **k: io.BytesIO(b'{"model":"test","choices":[]}'),
    )
    cfg = config(cost_cap_usd=0.15, max_request_cost_usd=0.1)
    ledger = tmp_path / "ledger.jsonl"
    create_provider(cfg, ledger).complete({"messages": []}, tmp_path / "one")
    with pytest.raises(CostCapReached):
        create_provider(cfg, ledger).complete({"messages": []}, tmp_path / "two")


def test_missing_completion_usage_is_not_priced_as_zero():
    from rttdist.providers import usage_cost

    assert (
        usage_cost(
            {"prompt_tokens": 100}, {"input_per_million": 1, "output_per_million": 2}
        )
        is None
    )


def test_transport_cap_is_shared_between_distinct_shards(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "rttdist.providers.request.urlopen",
        lambda *a, **k: io.BytesIO(b'{"model":"test","choices":[]}'),
    )
    ledger = tmp_path / "ledger.jsonl"
    cfg = config(max_transport_attempts=1)
    create_provider(cfg, ledger).complete({"messages": []}, tmp_path / "one")
    with pytest.raises(CostCapReached, match="Transport"):
        create_provider(cfg, ledger).complete({"messages": []}, tmp_path / "two")


def test_estimated_dollar_bound_rejects_oversized_prompt_before_network(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(
        "rttdist.providers.request.urlopen",
        lambda *a, **k: pytest.fail("oversized prompt must not be sent"),
    )
    cfg = config(
        cost_cap_usd=1,
        pricing={"input_per_million": 1, "output_per_million": 2},
        max_input_tokens=10,
    )
    with pytest.raises(ValueError, match="input|입력"):
        create_provider(cfg, tmp_path / "ledger.jsonl").complete(
            {"messages": [{"role": "user", "content": "x" * 100}]}, tmp_path / "call"
        )
