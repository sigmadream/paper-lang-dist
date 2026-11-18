import io
import os

import pytest


def config():
    return {
        "provider": "compatible",
        "protocol": "chat_completions",
        "base_url": "https://example.test/v1",
        "model": "test",
        "generation_profile": {"supported_options": ["max_tokens"]},
        "generation": {"max_tokens": 16},
        "max_calls": 3600,
        "max_transport_attempts": 10800,
        "cost_cap_usd": 50,
        "max_request_cost_usd": 0.25,
        "retries": 2,
        "auth": {"type": "bearer", "api_key_env": "CMD_API_KEY"},
    }


def test_isolated_provider_replays_same_request_without_leaving_auth_environment(
    tmp_path, monkeypatch
):
    from scripts.run_commandcode_v16 import IsolatedProvider, phase_settings
    from rttdist.providers import create_provider

    calls = []

    def send(req, timeout):
        assert os.environ["CMD_API_KEY"] == "memory-only-test"
        calls.append(1)
        return io.BytesIO(
            b'{"model":"test","choices":[{"message":{"content":"x"},"finish_reason":"stop"}]}'
        )

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    provider = IsolatedProvider(
        create_provider(phase_settings(config(), "pilot"), tmp_path / "ledger.jsonl"),
        "memory-only-test",
    )
    first = provider.complete({"messages": []}, tmp_path / "call")
    second = provider.complete({"messages": []}, tmp_path / "call")
    assert first == second and len(calls) == 1
    assert "CMD_API_KEY" not in os.environ
    assert all(
        "memory-only-test" not in p.read_text() for p in tmp_path.rglob("*.json")
    )


def test_auth_environment_is_removed_on_provider_error():
    from scripts.run_commandcode_v16 import IsolatedProvider

    class Broken:
        def complete(self, payload, folder):
            assert os.environ["CMD_API_KEY"] == "memory-only-test"
            raise RuntimeError("simulated failure")

    with pytest.raises(RuntimeError):
        IsolatedProvider(Broken(), "memory-only-test").complete({}, ".")
    assert "CMD_API_KEY" not in os.environ


def test_phase_budgets_are_separate_and_retries_preserve_design():
    from scripts.run_commandcode_v16 import phase_settings

    pilot = phase_settings(config(), "pilot")
    main = phase_settings(config(), "main")
    preflight = phase_settings(config(), "preflight")
    assert (
        pilot["max_calls"],
        pilot["max_transport_attempts"],
        pilot["cost_cap_usd"],
    ) == (144, 432, 50)
    assert (
        main["max_calls"],
        main["max_transport_attempts"],
        main["cost_cap_usd"],
    ) == (3600, 10800, 50)
    assert (
        preflight["max_calls"],
        preflight["max_transport_attempts"],
        preflight["cost_cap_usd"],
        preflight["retries"],
    ) == (1, 1, 0.25, 0)
    assert pilot["retries"] == main["retries"] == 2


def test_clean_execution_environment_removes_credentials_before_children(monkeypatch):
    from scripts.run_commandcode_v16 import clean_execution_environment

    monkeypatch.setenv("UNRELATED_API_KEY", "another-memory-only-test")
    with clean_execution_environment():
        assert "UNRELATED_API_KEY" not in os.environ and "CMD_API_KEY" not in os.environ
    assert os.environ["UNRELATED_API_KEY"] == "another-memory-only-test"


def test_runner_entrypoint_loads_without_package_search_path_override():
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "scripts/run_commandcode_v16.py", "--help"],
        capture_output=True,
        timeout=30,
    )
    assert result.returncode == 0
