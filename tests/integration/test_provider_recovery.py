import io
import json
from urllib.error import HTTPError

import pytest

from rttdist.providers import create_provider, ProviderError
from tests.unit.test_provider_ledger import config


def test_timeout_is_unknown_and_restart_does_not_regenerate(tmp_path, monkeypatch):
    calls = []

    def send(*a, **k):
        calls.append(1)
        raise TimeoutError("do-not-store-secret")

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    for _ in range(2):
        with pytest.raises(ProviderError, match="unknown"):
            create_provider(config(), tmp_path / "ledger.jsonl").complete(
                {"messages": []}, tmp_path / "call"
            )
    assert len(calls) == 1
    assert "do-not-store-secret" not in "".join(
        p.read_text() for p in tmp_path.rglob("*.json")
    )


def test_retry_after_and_max_two_retries_preserve_same_opencode_session(
    tmp_path, monkeypatch
):
    calls, delays = [], []

    def send(req, timeout):
        calls.append(req)
        if len(calls) < 3:
            raise HTTPError(req.full_url, 429, "withheld", {"Retry-After": "3"}, None)
        return io.BytesIO(b'{"model":"test","choices":[]}')

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    monkeypatch.setattr("rttdist.providers.time.sleep", delays.append)
    cfg = config(
        provider="opencode_go", base_url="https://opencode.ai/inference/go/openai/v1"
    )
    create_provider(cfg, tmp_path / "ledger.jsonl").complete(
        {"messages": []}, tmp_path / "call"
    )
    assert delays == [3, 3] and len(calls) == 3
    assert len({req.get_header("X-opencode-session") for req in calls}) == 1
    assert calls[0].get_header("X-opencode-session")
    assert (
        len(json.loads((tmp_path / "call" / "transport_attempts.json").read_text()))
        == 3
    )


def test_raw_receipt_survives_normalization_crash_and_ledger_crash(
    tmp_path, monkeypatch
):
    calls = []

    def send(*a, **k):
        calls.append(1)
        return io.BytesIO(
            b'{"model":"test","choices":[],"usage":{"prompt_tokens":10,"completion_tokens":2}}'
        )

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    provider = create_provider(
        config(pricing={"input_per_million": 1, "output_per_million": 2}),
        tmp_path / "ledger.jsonl",
    )
    original = provider.finalize_request
    monkeypatch.setattr(
        provider,
        "finalize_request",
        lambda *a: (_ for _ in ()).throw(RuntimeError("simulated crash")),
    )
    with pytest.raises(RuntimeError):
        provider.complete({"messages": []}, tmp_path / "call")
    monkeypatch.setattr(provider, "finalize_request", original)
    first = provider.complete({"messages": []}, tmp_path / "call")
    second = create_provider(
        config(pricing={"input_per_million": 1, "output_per_million": 2}),
        tmp_path / "ledger.jsonl",
    ).complete({"messages": []}, tmp_path / "call")
    assert first == second and len(calls) == 1
    assert len((tmp_path / "ledger.jsonl").read_text().splitlines()) == 1


def test_secret_echo_is_masked_in_raw_response_and_model_mismatch_not_retried(
    tmp_path, monkeypatch
):
    secret = "sentinel-private-key"
    monkeypatch.setenv("V16_TEST_KEY", secret)
    monkeypatch.setattr(
        "rttdist.providers.request.urlopen",
        lambda *a, **k: io.BytesIO(
            json.dumps(
                {"model": "other", "choices": [{"message": {"content": secret}}]}
            ).encode()
        ),
    )
    provider = create_provider(
        config(auth={"type": "bearer", "api_key_env": "V16_TEST_KEY"}),
        tmp_path / "ledger.jsonl",
    )
    for _ in range(2):
        with pytest.raises(ProviderError, match="model"):
            provider.complete({"messages": []}, tmp_path / "call")
    assert all(secret not in p.read_text() for p in tmp_path.rglob("*") if p.is_file())


def test_crash_during_normalization_reuses_raw_receipt(tmp_path, monkeypatch):
    from rttdist import provider_protocols

    calls = []

    def send(*a, **k):
        calls.append(1)
        return io.BytesIO(b'{"model":"test","choices":[]}')

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    original = provider_protocols.normalize_response
    monkeypatch.setattr(
        provider_protocols,
        "normalize_response",
        lambda *a: (_ for _ in ()).throw(RuntimeError("crash")),
    )
    provider = create_provider(config(), tmp_path / "ledger.jsonl")
    with pytest.raises(RuntimeError):
        provider.complete({"messages": []}, tmp_path / "call")
    monkeypatch.setattr(provider_protocols, "normalize_response", original)
    assert (
        provider.complete({"messages": []}, tmp_path / "call")["actual_model"] == "test"
    )
    assert len(calls) == 1


def test_malformed_protocol_is_preserved_and_never_regenerated(tmp_path, monkeypatch):
    calls = []

    def send(*a, **k):
        calls.append(1)
        return io.BytesIO(b"not-json")

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    for _ in range(2):
        with pytest.raises(ProviderError, match="Malformed"):
            create_provider(config(), tmp_path / "ledger.jsonl").complete(
                {"messages": []}, tmp_path / "call"
            )
    assert (
        len(calls) == 1
        and (tmp_path / "call" / "response_body.txt").read_text() == "not-json"
    )


def test_retry_budget_is_not_reset_on_restart(tmp_path, monkeypatch):
    calls = []

    def send(req, timeout):
        calls.append(1)
        raise HTTPError(req.full_url, 429, "withheld", {}, None)

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    monkeypatch.setattr("rttdist.providers.time.sleep", lambda delay: None)
    for _ in range(2):
        with pytest.raises(ProviderError):
            create_provider(config(), tmp_path / "ledger.jsonl").complete(
                {"messages": []}, tmp_path / "call"
            )
    assert len(calls) == 3


def test_retry_attempt_reservation_cannot_exceed_shared_dollar_cap(
    tmp_path, monkeypatch
):
    calls = []

    def send(req, timeout):
        calls.append(1)
        raise HTTPError(req.full_url, 503, "withheld", {}, None)

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    monkeypatch.setattr("rttdist.providers.time.sleep", lambda delay: None)
    cfg = config(cost_cap_usd=0.15, max_request_cost_usd=0.1)
    with pytest.raises(ProviderError):
        create_provider(cfg, tmp_path / "ledger.jsonl").complete(
            {"messages": []}, tmp_path / "call"
        )
    assert len(calls) == 1
