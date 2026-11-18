import io
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.error import HTTPError

import pytest


@pytest.fixture
def runner(monkeypatch):
    from scripts import run_deepseek_v16_20261118 as module

    with tempfile.TemporaryDirectory(prefix="ds-") as temporary:
        root = Path(temporary)
        monkeypatch.setattr(module, "ROOT", root)
        monkeypatch.setattr(
            module, "OUTPUT", root / "artifacts-rtt-v1.6/live-deepseek-20261118"
        )
        monkeypatch.setattr(module, "assert_sources", lambda: {})
        yield module


def provider_config():
    return {
        "provider": "compatible",
        "protocol": "chat_completions",
        "base_url": "https://api.commandcode.ai/provider/v1",
        "model": "deepseek/deepseek-v4-pro",
        "generation_profile": {"supported_options": ["max_tokens", "reasoning_effort"]},
        "generation": {"max_tokens": 16384, "reasoning_effort": "low"},
        "pricing": {"input_per_million": 1.32, "output_per_million": 3.96},
        "max_input_tokens": 32768,
        "max_request_cost_usd": 0.25,
        "auth": {"type": "bearer", "api_key_env": "CMD_API_KEY"},
    }


def test_phase_caps_and_reservations_are_independent(runner):
    for phase, expected in {
        "preflight": (1, 1, 0.24, 0.12, 0),
        "pilot": (144, 432, 49.62, 0.25, 2),
        "main": (3600, 10800, 49.32, 0.25, 2),
    }.items():
        cfg = runner.phase_settings(provider_config(), phase)
        assert (
            tuple(
                cfg[k]
                for k in (
                    "max_calls",
                    "max_transport_attempts",
                    "cost_cap_usd",
                    "max_request_cost_usd",
                    "retries",
                )
            )
            == expected
        )
    assert provider_config()["max_request_cost_usd"] == 0.25
    with pytest.raises(ValueError):
        runner.phase_settings(provider_config(), "smoke")


def test_provider_auth_is_removed_and_same_cache_is_reused(runner, monkeypatch):
    calls = []

    def send(req, timeout):
        assert os.environ["CMD_API_KEY"] == "memory-only-test"
        calls.append(1)
        return io.BytesIO(
            b'{"model":"deepseek/deepseek-v4-pro","choices":[{"message":{"content":"OK"},"finish_reason":"stop"}]}'
        )

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    folder = runner.OUTPUT / runner.CAMPAIGN_ID / "preflight"
    provider = runner.IsolatedProvider(
        runner.real_provider_factory(
            runner.phase_settings(provider_config(), "preflight"),
            folder / "provider_ledger.jsonl",
        ),
        "memory-only-test",
    )
    from rttdist.providers import APIProvider, CompatibleProvider

    assert isinstance(provider.provider, APIProvider)
    assert not isinstance(provider.provider, CompatibleProvider)
    first = provider.complete({"messages": []}, folder / "request")
    second = provider.complete({"messages": []}, folder / "request")
    assert first == second and len(calls) == 1
    assert "CMD_API_KEY" not in os.environ
    assert all("memory-only-test" not in p.read_text() for p in folder.rglob("*.json"))


def test_auth_is_removed_when_complete_raises(runner):
    class Broken:
        def complete(self, payload, folder):
            assert os.environ["CMD_API_KEY"] == "memory-only-test"
            raise RuntimeError("모의 오류입니다")

    with pytest.raises(RuntimeError):
        runner.IsolatedProvider(Broken(), "memory-only-test").complete(
            {}, runner.OUTPUT / runner.CAMPAIGN_ID / "main/slot/step-01"
        )
    assert "CMD_API_KEY" not in os.environ


def test_evaluation_subprocess_does_not_inherit_credentials(runner, monkeypatch):
    monkeypatch.setenv("CMD_API_KEY", "memory-only-test")
    monkeypatch.setenv("UNRELATED_API_KEY", "another-memory-only-test")
    with runner.clean_execution_environment():
        child = subprocess.run(
            [
                sys.executable,
                "-c",
                "import os; assert 'CMD_API_KEY' not in os.environ; assert 'UNRELATED_API_KEY' not in os.environ",
            ],
            capture_output=True,
            timeout=30,
        )
        assert child.returncode == 0
    assert os.environ["UNRELATED_API_KEY"] == "another-memory-only-test"


def test_guard_rejects_prior_root_and_directory_escape(runner):
    with pytest.raises(ValueError):
        runner.assert_destination(
            runner.ROOT / "artifacts-rtt-v1.6/live-commandcode-20261117/changed.json"
        )
    with pytest.raises(ValueError):
        runner.assert_destination(runner.OUTPUT / ".." / "outside.json")
    runner.assert_destination(runner.OUTPUT / runner.CAMPAIGN_ID / "pilot/request.json")


def test_source_guard_detects_change_and_missing_snapshot(tmp_path, monkeypatch):
    from scripts import run_deepseek_v16_20261118 as runner

    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setattr(
        runner,
        "OUTPUT",
        tmp_path / "artifacts-rtt-v1.6/live-deepseek-20261118",
    )
    source = tmp_path / "providers.py"
    source.write_text("before", encoding="utf-8")
    snapshot = runner.OUTPUT / "execution-sources/providers.py"
    snapshot.parent.mkdir(parents=True)
    snapshot.write_bytes(source.read_bytes())
    runner.write_json(
        runner.OUTPUT / "source-manifest.json",
        {"files": {"providers.py": runner.digest(source.read_bytes())}},
    )
    runner.assert_sources()
    source.write_text("after", encoding="utf-8")
    with pytest.raises(ValueError):
        runner.assert_sources()
    source.write_text("before", encoding="utf-8")
    snapshot.unlink()
    with pytest.raises(ValueError):
        runner.assert_sources()


def test_default_mode_prepares_without_live_call_or_token_access(runner, monkeypatch):
    calls = []
    monkeypatch.setenv("CMD_API_KEY", "unused-memory-only-test")
    monkeypatch.setattr(runner, "prepare", lambda: calls.append("prepare"))
    monkeypatch.setattr(
        runner, "execute", lambda *a: pytest.fail("실제 실행은 금지됩니다")
    )
    assert runner.main([]) == 0
    assert calls == ["prepare"]
    assert os.environ["CMD_API_KEY"] == "unused-memory-only-test"


def test_run_requires_independent_review_before_token_access(runner, monkeypatch):
    monkeypatch.setenv("CMD_API_KEY", "unused-memory-only-test")
    monkeypatch.setattr(runner, "assert_live_date", lambda: None)
    monkeypatch.setattr(
        runner, "execute", lambda *a: pytest.fail("검토 관문을 우회하였습니다")
    )
    with pytest.raises(ValueError, match="검토"):
        runner.main(["--run"])
    assert os.environ["CMD_API_KEY"] == "unused-memory-only-test"


def test_offline_prepare_rejects_http_before_dns(runner, monkeypatch):
    from urllib.request import urlopen

    monkeypatch.setattr(
        "socket.getaddrinfo", lambda *a, **k: pytest.fail("DNS 호출은 금지됩니다")
    )
    monkeypatch.setattr(
        runner, "prepare_offline", lambda: urlopen("https://example.invalid/")
    )
    with pytest.raises(RuntimeError, match="오프라인"):
        runner.prepare()


def test_pilot_cap_reserves_before_transport_and_leaves_auth_clean(runner, monkeypatch):
    from rttdist.providers import CostCapReached

    monkeypatch.setattr(
        "rttdist.providers.request.urlopen",
        lambda *a, **k: pytest.fail("예산 초과 전송입니다"),
    )
    folder = runner.OUTPUT / runner.CAMPAIGN_ID / "pilot"
    runner.write_json(
        folder / "provider_ledger.jsonl.state.json",
        {
            "requests": {"prior": {"status": "completed", "cost_usd": 49.50}},
            "attempts": [],
        },
    )
    provider = runner.IsolatedProvider(
        runner.real_provider_factory(
            runner.phase_settings(provider_config(), "pilot"),
            folder / "provider_ledger.jsonl",
        ),
        "memory-only-test",
    )
    with pytest.raises(CostCapReached):
        provider.complete({"messages": []}, folder / "request")
    assert "CMD_API_KEY" not in os.environ


def test_http_524_is_not_resent_or_replayed(runner, monkeypatch):
    from rttdist.providers import UnknownRequestState

    calls = []

    def send(req, timeout):
        calls.append(1)
        raise HTTPError(req.full_url, 524, "timed out", {}, io.BytesIO(b""))

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    folder = runner.OUTPUT / runner.CAMPAIGN_ID / "main"
    provider = runner.IsolatedProvider(
        runner.real_provider_factory(
            runner.phase_settings(provider_config(), "main"),
            folder / "provider_ledger.jsonl",
        ),
        "memory-only-test",
    )
    for _ in range(2):
        with pytest.raises(UnknownRequestState):
            provider.complete({"messages": []}, folder / "slot/step-01")
    assert len(calls) == 1 and "CMD_API_KEY" not in os.environ


def test_unknown_ledger_blocks_campaign_resume(runner):
    folder = runner.OUTPUT / runner.CAMPAIGN_ID / "main"
    runner.write_json(
        folder / "provider_ledger.jsonl.state.json",
        {
            "requests": {"logical-key": {"status": "inflight", "reserved_usd": 0.25}},
            "attempts": [],
        },
    )
    with pytest.raises(ValueError, match="불명"):
        runner.assert_no_unknown_requests()


def test_real_core_paths_are_called_in_order_and_hooks_restore(runner, monkeypatch):
    called = []
    cfg = {
        "campaign_id": runner.CAMPAIGN_ID,
        "output_root": str(runner.OUTPUT),
        "validation": "validation.json",
    }
    monkeypatch.setattr(runner, "load_config", lambda: cfg)
    monkeypatch.setattr(runner, "preflight", lambda *a: {"passed": True})
    monkeypatch.setattr(
        runner, "read_json", lambda p: {"passed": True, "observation_count": 12}
    )
    monkeypatch.setattr(runner, "assert_no_unknown_requests", lambda: None)
    monkeypatch.setattr(runner, "record_event", lambda *a, **k: None)
    monkeypatch.setattr(runner, "reproduce", lambda *a: {"passed": True})
    monkeypatch.setattr(runner.core, "run_hops_campaign", lambda c, p: called.append(p))
    monkeypatch.setattr(
        runner.core,
        "freeze_main_design",
        lambda *a: called.append("freeze") or {"contract_hash": "test"},
    )
    monkeypatch.setattr(
        runner.core,
        "report_hops_campaign",
        lambda *a: called.append("report") or {"complete_by_threshold": {}},
    )
    original_factory = runner.core.create_provider
    original_observation = runner.core.run_hops_observation
    assert runner.execute("memory-only-test") == 0
    assert called == ["pilot", "freeze", "main", "report"]
    assert runner.core.create_provider is original_factory
    assert runner.core.run_hops_observation is original_observation


def test_review_evidence_must_match_current_provider_and_report(runner):
    provider = runner.ROOT / "src/rttdist/providers.py"
    provider.parent.mkdir(parents=True)
    provider.write_text("reviewed", encoding="utf-8")
    report = runner.ROOT / "review.md"
    report.write_text("검토를 통과하였습니다.", encoding="utf-8")
    evidence = runner.ROOT / "review.json"
    runner.write_json(
        evidence,
        {
            "passed": True,
            "reviewer": "독립 검토자",
            "report_path": "review.md",
            "report_sha256": runner.digest(report.read_bytes()),
            "source_hashes": {
                "src/rttdist/providers.py": runner.digest(provider.read_bytes())
            },
        },
    )
    runner.require_review(evidence)
    provider.write_text("changed after review", encoding="utf-8")
    with pytest.raises(ValueError, match="검토"):
        runner.require_review(evidence)


def test_cli_entrypoint_supports_help_without_live_call():
    result = subprocess.run(
        [sys.executable, "scripts/run_deepseek_v16_20261118.py", "--help"],
        capture_output=True,
        timeout=30,
    )
    assert result.returncode == 0


def test_new_campaign_keeps_problem_protocol_and_uses_api_provider():
    from scripts import run_deepseek_v16_20261118 as runner
    from rttdist.providers import APIProvider

    cfg = runner.load_config()
    previous = runner.core.load_hops_config(
        runner.ROOT / "configs/v1.6/campaigns/commandcode_deepseek_v4_pro_20261117.yaml"
    )
    changed = {
        "output_root",
        "campaign_id",
        "provider_config",
        "execution_wrapper",
        "phase_budget_policy",
        "budget",
        "llm",
    }
    assert {k: v for k, v in cfg.items() if k not in changed} == {
        k: v for k, v in previous.items() if k not in changed
    }
    assert len(runner.core.build_hops_schedule(cfg, "pilot")) == 12
    assert len(runner.core.build_hops_schedule(cfg, "main")) == 300
    provider = runner.real_provider_factory(cfg["llm"])
    assert isinstance(provider, APIProvider)
    price_bound = (32768 * 1.32 + 16384 * 3.96) / 1e6
    assert price_bound < runner.PHASES["preflight"]["max_request_cost_usd"] <= 0.24
