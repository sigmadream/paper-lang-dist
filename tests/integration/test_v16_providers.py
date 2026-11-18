import asyncio
import copy
import io
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from rttdist.providers import create_provider, ProviderError
from tests.unit.test_provider_ledger import config


def test_responses_url_does_not_duplicate_and_payload_is_protocol_specific(
    tmp_path, monkeypatch
):
    captured = []

    def send(req, timeout):
        captured.append(req)
        return io.BytesIO(
            b'{"id":"r","model":"test","status":"completed","output":[{"type":"message","role":"assistant","content":[{"type":"output_text","text":"print(1)"}]}]}'
        )

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    result = create_provider(
        config(
            provider="openai",
            protocol="responses",
            base_url="https://api.openai.com/v1/responses",
        )
    ).complete(
        {
            "messages": [
                {"role": "system", "content": "Translate"},
                {"role": "user", "content": "x"},
            ]
        },
        tmp_path / "call",
    )
    assert captured[0].full_url == "https://api.openai.com/v1/responses"
    body = json.loads(captured[0].data)
    assert body["instructions"] == "Translate" and body["max_output_tokens"] == 20
    assert "messages" not in body and result["text"] == "print(1)"


def test_static_preflight_does_not_read_credentials_or_call_network(monkeypatch):
    from scripts.preflight_v16 import preflight_provider

    monkeypatch.setattr(
        "rttdist.providers.request.urlopen",
        lambda *a, **k: pytest.fail("network forbidden"),
    )
    monkeypatch.setattr(
        "rttdist.providers.os.environ.get",
        lambda *a, **k: pytest.fail("credential lookup forbidden"),
    )
    result = preflight_provider(
        config(auth={"type": "bearer", "api_key_env": "OPENAI_API_KEY"})
    )
    assert result["passed"] and result["live"] is False
    assert result["model_evidence"]["status"] == "missing"
    assert result["actual_model"] is None


def test_preflight_cli_resolves_provider_flag_from_current_directory():
    import subprocess
    import sys

    proc = subprocess.run(
        [
            sys.executable,
            "scripts/preflight_v16.py",
            "--config",
            "configs/v1.6/experiment.yaml",
            "--provider-config",
            "configs/v1.6/providers/openai.yaml",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert proc.returncode == 1
    result = json.loads(proc.stdout)
    assert result["passed"] is False and "model" in result["reason"]
    assert not proc.stderr


def test_provider_templates_require_model_and_keep_correct_service_paths():
    from scripts.preflight_v16 import preflight_provider

    for name, expected in [
        ("openai", "https://api.openai.com/v1"),
        ("zai", "https://api.z.ai/api/paas/v4"),
        ("opencode", "https://opencode.ai/inference/openai/v1"),
        ("opencode_go", "https://opencode.ai/inference/go/openai/v1"),
    ]:
        cfg = yaml.safe_load(
            Path(f"configs/v1.6/providers/{name}.yaml").read_text(encoding="utf-8")
        )
        assert cfg["base_url"] == expected and cfg["model"] is None
        assert not preflight_provider(cfg)["passed"]
        cfg["model"] = "user-selected-model"
        assert preflight_provider(cfg)["passed"]


def test_all_provider_templates_preserve_common_experiment_conditions():
    from rttdist.hops_experiment import load_hops_config

    base = load_hops_config("configs/v1.6/experiment.yaml")
    protected = [
        "problem_ids",
        "routes",
        "thresholds",
        "threshold",
        "max_hops",
        "repeats",
        "confirmation_roundtrips",
    ]
    for name in ("openai", "zai", "opencode", "opencode_go", "copilot", "compatible"):
        cfg = load_hops_config(
            "configs/v1.6/experiment.yaml",
            Path(f"configs/v1.6/providers/{name}.yaml").resolve(),
        )
        assert {key: cfg[key] for key in protected} == {
            key: base[key] for key in protected
        }


def test_registered_custom_adapter_still_receives_protocol_config(monkeypatch):
    from rttdist.providers import PROVIDER_FACTORIES

    sentinel = object()
    monkeypatch.setitem(
        PROVIDER_FACTORIES, "custom_v16", lambda config, ledger=None: sentinel
    )
    assert (
        create_provider({"provider": "custom_v16", "protocol": "custom_protocol"})
        is sentinel
    )


def test_live_preflight_mock_records_smoke_without_main_artifacts(
    tmp_path, monkeypatch
):
    from scripts.preflight_v16 import preflight_provider

    monkeypatch.setattr(
        "rttdist.providers.request.urlopen",
        lambda *a, **k: io.BytesIO(
            b'{"id":"smoke","model":"test","choices":[{"message":{"content":"OK"},"finish_reason":"stop"}]}'
        ),
    )
    result = preflight_provider(config(preflight_root=str(tmp_path)), live=True)
    assert (
        result["passed"]
        and result["live"]
        and result["model_evidence"]["status"] == "exact"
    )
    ledgers = list(tmp_path.rglob("smoke_ledger.jsonl"))
    assert len(ledgers) == 1
    entry = json.loads(ledgers[0].read_text())
    assert entry["logical_request"]["phase"] == "smoke"
    assert not list(tmp_path.rglob("observation.json"))


def test_sdk_missing_dependency_is_a_clear_offline_diagnostic(monkeypatch):
    from scripts.preflight_v16 import preflight_provider

    monkeypatch.setattr("rttdist.copilot_provider.sdk_available", lambda: False)
    result = preflight_provider(
        config(
            provider="copilot",
            protocol="copilot_sdk",
            generation={},
            generation_profile={"supported_options": []},
        )
    )
    assert not result["passed"] and "github-copilot-sdk" in result["reason"]


@pytest.mark.parametrize("stage", ["success", "session", "response", "mismatch"])
def test_copilot_isolated_new_sessions_no_tools_and_no_assumed_model_id(
    tmp_path, monkeypatch, stage
):
    from rttdist import copilot_provider

    sessions, clients, turns = [], [], []

    class FakeSession:
        def __init__(self, cfg):
            self.cfg = cfg
            self.session_id = cfg["session_id"]

        def on(self, handler):
            self.handler = handler

        async def send_and_wait(self, payload, timeout):
            turns.append(payload)
            if stage == "response":
                raise TimeoutError("sdk-private-token")
            assert not list(Path(self.cfg["working_directory"]).iterdir())
            return SimpleNamespace(
                data=SimpleNamespace(
                    content="print(1)", model="other" if stage == "mismatch" else None
                )
            )

        async def disconnect(self):
            pass

    class FakeClient:
        def __init__(self, options):
            clients.append(options)

        async def start(self):
            pass

        async def get_status(self):
            return SimpleNamespace(version="test-cli", protocolVersion=1)

        async def get_auth_status(self):
            return SimpleNamespace(isAuthenticated=True)

        async def list_models(self):
            return [SimpleNamespace(id="test")]

        async def create_session(self, cfg):
            sessions.append(cfg)
            if stage == "session":
                raise RuntimeError("sdk-private-token")
            return FakeSession(cfg)

        async def stop(self):
            pass

    monkeypatch.setattr(
        copilot_provider,
        "load_sdk",
        lambda: (FakeClient, lambda **k: SimpleNamespace(**k)),
    )
    monkeypatch.setattr(copilot_provider, "sdk_version", lambda: "0.1.32")
    monkeypatch.setattr(copilot_provider.shutil, "which", lambda *a: "fake-copilot")
    monkeypatch.setenv("V16_COPILOT_TOKEN", "sdk-private-token")
    cfg = config(
        provider="copilot",
        protocol="copilot_sdk",
        auth={"type": "sdk", "api_key_env": "V16_COPILOT_TOKEN"},
        generation={},
        generation_profile={"supported_options": []},
    )
    provider = create_provider(cfg, tmp_path / "ledger.jsonl")
    if stage != "success":
        for _ in range(2):
            with pytest.raises(ProviderError):
                provider.complete(
                    {"messages": [{"role": "user", "content": "Translate"}]},
                    tmp_path / "one",
                )
        assert len(sessions) == 1 and len(turns) == (0 if stage == "session" else 1)
        assert all(
            "sdk-private-token" not in p.read_text()
            for p in tmp_path.rglob("*")
            if p.is_file()
        )
        if stage == "mismatch":
            saved = json.loads((tmp_path / "one" / "response.json").read_text())
            assert saved["model_evidence"]["status"] == "mismatch"
        return
    one = provider.complete(
        {"messages": [{"role": "user", "content": "Translate"}]}, tmp_path / "one"
    )
    provider.complete({"messages": []}, tmp_path / "two")
    provider.complete(
        {"messages": [{"role": "user", "content": "Translate"}]}, tmp_path / "one"
    )
    assert len(turns) == 2 and sessions[0]["session_id"] != sessions[1]["session_id"]
    assert sessions[0]["available_tools"] == [] and sessions[0]["mcp_servers"] == {}
    assert sessions[0]["system_message"]["mode"] == "replace"
    assert sessions[0]["infinite_sessions"] == {"enabled": False}
    assert one["actual_model"] is None and one["model_evidence"]["status"] == "missing"
    assert (
        one["execution_class"] == "sdk_exploratory"
        and one["internal_model_calls"] is None
    )
    assert one["sdk_turns"] == 1 and one["sdk_metadata"]["cli_version"] == "test-cli"
    assert all(
        "sdk-private-token" not in p.read_text()
        for p in tmp_path.rglob("*")
        if p.is_file()
    )
