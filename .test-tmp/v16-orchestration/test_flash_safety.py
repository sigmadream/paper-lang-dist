"""신규 Flash 관문 검사를 최종 통합 검사 파일에 합치기 전에 실행합니다."""

import io
import json
import os
import sys
import tempfile
from copy import deepcopy
from pathlib import Path

import pytest

sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path.cwd() / "src"))


def test_flash_rejects_wrong_peak_pricing(monkeypatch):
    from scripts import run_deepseek_v41_flash_20261118 as runner

    cfg = runner.core.load_hops_config(*runner.config_paths())
    cfg["execution_wrapper"]["sha256"] = runner.digest(
        open(runner.__file__, "rb").read()
    )
    cfg["llm"]["pricing"]["input_per_million"] = 0.15
    monkeypatch.setattr(runner.core, "load_hops_config", lambda *args: cfg)
    with pytest.raises(ValueError):
        runner.load_config()


def test_flash_budget_recomputes_both_prior_ledgers():
    from scripts import run_deepseek_v41_flash_20261118 as runner

    evidence = runner.prior_budget_evidence()
    assert evidence["new_total_cost_cap_usd"] == "98.13"
    assert evidence["conservative_allocated_total_usd"] == "200.465729120"
    assert (
        evidence["prior_campaigns"]["20261117"]["spent_plus_reserved_usd"]
        == "1.045928856"
    )
    assert (
        evidence["prior_campaigns"]["20261118"]["spent_plus_reserved_usd"]
        == "1.039800264"
    )
    assert evidence["prior_campaigns"]["20261117"]["logical_requests"] == 99
    assert evidence["prior_campaigns"]["20261118"]["logical_requests"] == 147


@pytest.fixture
def flash_short_path():
    with tempfile.TemporaryDirectory(prefix="f-") as temporary:
        yield Path(temporary)


@pytest.mark.parametrize(
    "actual_model",
    [
        "deepseek/deepseek-v4-pro",
        "deepseek/deepseek-v4.1-flash-fast",
        "deepseek/deepseek-v4.1-flash-ultrafast",
    ],
)
def test_flash_wrong_model_is_preserved_and_never_accepted(
    flash_short_path, monkeypatch, actual_model
):
    from scripts import run_deepseek_v41_flash_20261118 as runner
    from rttdist.providers import ProviderError

    tmp_path = flash_short_path
    cfg = runner.core.load_hops_config(*runner.config_paths())["llm"]
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setattr(
        runner, "OUTPUT", tmp_path / "artifacts-rtt-v1.6/live-ds41f-20261118"
    )
    monkeypatch.setattr(runner, "assert_sources", lambda: {})
    calls = []

    def send(req, timeout):
        wire = json.loads(req.data)
        assert wire["model"] == "deepseek/deepseek-v4.1-flash"
        assert wire["max_tokens"] == 16384 and wire["reasoning_effort"] == "low"
        assert not {"temperature", "top_p", "seed"} & wire.keys()
        assert req.full_url == "https://api.commandcode.ai/provider/v1/chat/completions"
        calls.append(1)
        return io.BytesIO(
            json.dumps(
                {
                    "model": actual_model,
                    "choices": [
                        {"message": {"content": "OK"}, "finish_reason": "stop"}
                    ],
                    "usage": {
                        "prompt_tokens": 1000,
                        "completion_tokens": 100,
                        "prompt_tokens_details": {"cached_tokens": 200},
                    },
                }
            ).encode()
        )

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    folder = runner.OUTPUT / runner.CAMPAIGN_ID / "preflight"
    provider = runner.IsolatedProvider(
        runner.real_provider_factory(
            runner.phase_settings(cfg, "preflight"), folder / "provider_ledger.jsonl"
        ),
        "memory-only-test",
    )
    for _ in range(2):
        with pytest.raises(ProviderError):
            provider.complete({"messages": []}, folder / "request")
    saved = runner.read_json(folder / "request/response.json")
    assert saved["actual_model"] == actual_model
    assert saved["cost_usd"] == pytest.approx(0.0003612)
    assert saved["effective_generation"] is None
    assert len(calls) == 1 and "CMD_API_KEY" not in os.environ


@pytest.fixture
def flash_review(tmp_path, monkeypatch):
    from scripts import run_deepseek_v41_flash_20261118 as runner

    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setattr(
        runner, "OUTPUT", tmp_path / "artifacts-rtt-v1.6/live-ds41f-20261118"
    )
    files = {}
    for name in (
        "scripts/run_deepseek_v41_flash_20261118.py",
        "src/rttdist/providers.py",
        "configs/v1.6/providers/commandcode_deepseek_v41_flash_20261118.yaml",
        "configs/v1.6/campaigns/commandcode_deepseek_v41_flash_20261118.yaml",
        "tests/integration/test_deepseek_flash_runner.py",
    ):
        source = tmp_path / name
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("검토할 새 파일입니다", encoding="utf-8")
        files[name] = runner.digest(source.read_bytes())
        snapshot = runner.OUTPUT / "execution-sources" / name
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes(source.read_bytes())
    manifest = runner.OUTPUT / "source-manifest.json"
    runner.write_json(manifest, {"files": files, "campaign_id": runner.CAMPAIGN_ID})
    report = runner.OUTPUT / "독립검토.md"
    report.write_text("별도 검토자가 검토한 보고서입니다", encoding="utf-8")
    evidence = {
        "passed": True,
        "reviewer": "별도 Orca 독립 검토자",
        "reviewer_session_id": "orca_session_id:separate-test-reviewer",
        "campaign_id": runner.CAMPAIGN_ID,
        "model_id": runner.MODEL_ID,
        "report_path": report.relative_to(tmp_path).as_posix(),
        "report_sha256": runner.digest(report.read_bytes()),
        "source_hashes": files,
        "prepared_manifest_path": manifest.relative_to(tmp_path).as_posix(),
        "prepared_manifest_sha256": runner.digest(manifest.read_bytes()),
    }
    return runner, evidence


@pytest.mark.parametrize(
    "field",
    ["campaign_id", "model_id", "prepared_manifest_sha256", "reviewer_session_id"],
)
def test_flash_review_rejects_missing_campaign_binding(flash_review, field):
    runner, evidence = flash_review
    path = runner.OUTPUT / "검토.json"
    runner.write_json(path, evidence)
    runner.require_review(path)
    del evidence[field]
    runner.write_json(path, evidence)
    with pytest.raises(ValueError, match="검토"):
        runner.require_review(path)


def test_flash_review_rejects_partial_sources_and_self_review(flash_review):
    runner, evidence = flash_review
    path = runner.OUTPUT / "검토.json"
    changed = deepcopy(evidence)
    changed["source_hashes"] = {
        "src/rttdist/providers.py": evidence["source_hashes"][
            "src/rttdist/providers.py"
        ]
    }
    runner.write_json(path, changed)
    with pytest.raises(ValueError, match="검토"):
        runner.require_review(path)
    evidence["reviewer_session_id"] = (
        "orca_session_id:c31b6f22-31ba-4537-96bb-7e5799e46a0f"
    )
    runner.write_json(path, evidence)
    with pytest.raises(ValueError, match="검토"):
        runner.require_review(path)
