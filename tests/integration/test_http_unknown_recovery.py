import io
import json
from pathlib import Path
import socket
import subprocess
import sys
from urllib.error import HTTPError, URLError

import pytest

from rttdist import hops_experiment as hops
from rttdist.experiment_io import digest, read_json, write_json
from rttdist.providers import (
    CostCapReached,
    ProviderError,
    UnknownRequestState,
    create_provider,
)
from tests.integration.test_hops_experiment import setup
from tests.unit.test_provider_ledger import config

AMBIGUOUS_HTTP = [
    408,
    500,
    501,
    502,
    503,
    504,
    505,
    507,
    508,
    511,
    520,
    521,
    522,
    523,
    524,
    525,
    526,
    530,
    599,
]
SUCCESS = {
    "model": "test",
    "choices": [{"message": {"content": "source"}, "finish_reason": "stop"}],
    "usage": {"prompt_tokens": 10, "completion_tokens": 2, "cost": 0.02},
}


def payload(step=1):
    return {
        "messages": [],
        "logical_request": {
            "campaign": "new-mock-campaign",
            "phase": "main",
            "problem": "p",
            "route": "cpp-via-python",
            "repeat": 1,
            "step": step,
        },
    }


@pytest.mark.parametrize("http_status", AMBIGUOUS_HTTP)
def test_ambiguous_http_is_one_unknown_attempt_and_keeps_reservation(
    tmp_path, monkeypatch, http_status
):
    calls, delays = [], []
    secret = "fake-private-http-key"
    monkeypatch.setenv("HTTP_UNKNOWN_FAKE_KEY", secret)

    def send(req, timeout):
        calls.append(req)
        raise HTTPError(
            req.full_url,
            http_status,
            "private-error-" + secret,
            {"Retry-After": "0", "x-private": secret},
            io.BytesIO(secret.encode()),
        )

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    monkeypatch.setattr("rttdist.providers.time.sleep", delays.append)
    cfg = config(
        cost_cap_usd=0.15,
        max_request_cost_usd=0.1,
        auth={"type": "bearer", "api_key_env": "HTTP_UNKNOWN_FAKE_KEY"},
    )
    ledger = tmp_path / "ledger.jsonl"
    for destination in ("first", "resumed", "again"):
        with pytest.raises(UnknownRequestState) as captured:
            create_provider(cfg, ledger).complete(payload(), tmp_path / destination)
        assert secret not in str(captured.value)
    assert len(calls) == 1 and delays == []
    state = read_json(ledger.with_suffix(".jsonl.state.json"))
    request = state["requests"][digest(payload()["logical_request"])]
    assert request["status"] == "unknown" and request["reserved_usd"] == 0.1
    assert request["cost_usd"] is None
    assert len(state["attempts"]) == 1
    assert state["attempts"][0]["status"] == "unknown"
    assert state["attempts"][0]["http_status"] == http_status
    with pytest.raises(CostCapReached):
        create_provider(cfg, ledger).reserve_request_budget("another", 0.1)
    assert not (tmp_path / "first/response_body.txt").exists()
    for path in tmp_path.rglob("*"):
        if path.is_file():
            assert secret.encode() not in path.read_bytes()
            assert b"private-error-" not in path.read_bytes()


@pytest.mark.parametrize("http_status", [524, 504])
def test_unknown_http_stays_blocked_in_new_process(tmp_path, monkeypatch, http_status):
    calls = []

    def send(req, timeout):
        calls.append(1)
        raise HTTPError(req.full_url, http_status, "withheld", {}, None)

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    monkeypatch.setattr("rttdist.providers.time.sleep", lambda *a: None)
    cfg = config(cost_cap_usd=0.15, max_request_cost_usd=0.1)
    ledger = tmp_path / "ledger.jsonl"
    with pytest.raises(UnknownRequestState):
        create_provider(cfg, ledger).complete(payload(), tmp_path / "first")
    write_json(tmp_path / "input.json", {"config": cfg, "payload": payload()})
    script = """
import json
import sys
from pathlib import Path
from rttdist import providers
from rttdist.experiment_io import read_json
root = Path(sys.argv[1])
def blocked(*args, **kwargs):
    (root / 'unexpected-call').write_text('called')
    raise AssertionError('실제 전송을 차단했습니다.')
providers.request.urlopen = blocked
data = read_json(root / 'input.json')
try:
    providers.create_provider(data['config'], root / 'ledger.jsonl').complete(data['payload'], root / 'child')
except providers.UnknownRequestState:
    print(json.dumps({'unknown': True}))
else:
    raise AssertionError('불명 상태가 보존되어야 합니다.')
"""
    for _ in range(2):
        result = subprocess.run(
            [sys.executable, "-c", script, str(tmp_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
        )
        assert result.returncode == 0, result.stderr
        assert json.loads(result.stdout) == {"unknown": True}
    assert len(calls) == 1 and not (tmp_path / "unexpected-call").exists()
    request = next(
        iter(read_json(ledger.with_suffix(".jsonl.state.json"))["requests"].values())
    )
    assert request["status"] == "unknown" and request["reserved_usd"] == 0.1


def test_completed_response_replay_preserves_cost_after_other_http_is_unknown(
    tmp_path, monkeypatch
):
    calls = []

    def send(req, timeout):
        calls.append(1)
        if len(calls) == 1:
            return io.BytesIO(json.dumps(SUCCESS).encode())
        raise HTTPError(req.full_url, 524, "withheld", {}, None)

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    monkeypatch.setattr("rttdist.providers.time.sleep", lambda *a: None)
    cfg = config(cost_cap_usd=1, max_request_cost_usd=0.1)
    ledger = tmp_path / "ledger.jsonl"
    first = create_provider(cfg, ledger).complete(payload(), tmp_path / "done")
    completed_ledger = ledger.read_bytes()
    raw_response = (tmp_path / "done/response_body.txt").read_bytes()
    with pytest.raises(UnknownRequestState):
        create_provider(cfg, ledger).complete(payload(2), tmp_path / "unknown")
    replay = create_provider(cfg, ledger).complete(payload(), tmp_path / "replay")
    assert replay == first and replay["cost_usd"] == 0.02
    assert ledger.read_bytes() == completed_ledger
    assert (tmp_path / "done/response_body.txt").read_bytes() == raw_response
    assert len(calls) == 2


@pytest.mark.parametrize("failure", ["429", "dns", "refused"])
def test_proven_pre_execution_failures_keep_bounded_retries_and_response_replay(
    tmp_path, monkeypatch, failure
):
    calls, delays = [], []

    def send(req, timeout):
        calls.append(1)
        if len(calls) < 3:
            if failure == "429":
                raise HTTPError(
                    req.full_url, 429, "withheld", {"Retry-After": "3"}, None
                )
            raise URLError(
                socket.gaierror("fake DNS failure")
                if failure == "dns"
                else ConnectionRefusedError("fake refusal")
            )
        return io.BytesIO(json.dumps(SUCCESS).encode())

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    monkeypatch.setattr("rttdist.providers.time.sleep", delays.append)
    ledger = tmp_path / "ledger.jsonl"
    first = create_provider(config(), ledger).complete(payload(), tmp_path / "call")
    replay = create_provider(config(), ledger).complete(payload(), tmp_path / "replay")
    assert replay == first and len(calls) == 3
    assert delays == ([3, 3] if failure == "429" else [1, 2])


@pytest.mark.parametrize("http_status", [500, 503, 504, 520, 524])
def test_legacy_provider_preserves_unknown_without_regeneration(
    tmp_path, monkeypatch, http_status
):
    calls = []

    def send(req, timeout):
        calls.append(1)
        raise HTTPError(
            req.full_url, http_status, "private-error", {}, io.BytesIO(b"private-body")
        )

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    monkeypatch.setattr("rttdist.providers.time.sleep", lambda *a: None)
    cfg = {
        "provider": "openai_compatible",
        "endpoint": "https://example.test/v1",
        "model": "test",
        "generation": {},
        "request_timeout": 1,
        "retries": 2,
    }
    for _ in range(2):
        with pytest.raises(UnknownRequestState):
            create_provider(cfg).complete({}, tmp_path)
    assert len(calls) == 1
    assert all(
        b"private-body" not in path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    )


def test_core_records_typed_unknown_state_as_request_outcome_unknown(setup):
    cfg, job, folder = setup

    class UnknownProvider:
        def complete(self, *args):
            raise UnknownRequestState("HTTP 524; request state unknown")

    record = hops.run_hops_observation(cfg, job, UnknownProvider(), folder)
    assert record["reason"] == "request_outcome_unknown"
    assert record["outcomes"]["0.85"]["category"] == "invalid"
    assert record["translation_steps"] == 0


def test_http_524_reaches_core_without_duplicate_transport(setup, monkeypatch):
    cfg, job, folder = setup
    cfg["llm"] = config()
    calls = []

    def send(req, timeout):
        calls.append(1)
        raise HTTPError(req.full_url, 524, "withheld", {}, None)

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    monkeypatch.setattr("rttdist.providers.time.sleep", lambda *a: None)
    provider = create_provider(cfg["llm"], folder / "ledger.jsonl")
    record = hops.run_hops_observation(cfg, job, provider, folder)
    assert record["reason"] == "request_outcome_unknown"
    assert record["outcomes"]["0.85"]["category"] == "invalid"
    assert hops.run_hops_observation(cfg, job, provider, folder) == record
    assert len(calls) == 1
