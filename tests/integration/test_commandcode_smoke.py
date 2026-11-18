import json
import os
from pathlib import Path

import pytest
import yaml


def test_smoke_runs_five_requests_and_never_exposes_key_to_evaluation(
    tmp_path, monkeypatch
):
    from scripts import integration_commandcode as smoke

    cfg = yaml.safe_load(
        Path("configs/v1.6/providers/commandcode_glm53.yaml").read_text(
            encoding="utf-8"
        )
    )
    calls = []
    evaluated = []

    class FakeProvider:
        def complete(self, payload, folder):
            assert os.environ.get("CMD_API_KEY") == "in-memory-test"
            calls.append(payload)
            text = "OK" if len(calls) == 1 else "```\nsource\n```"
            return {
                "text": text,
                "finish_reason": "stop",
                "requested_model": cfg["model"],
                "actual_model": cfg["model"],
                "model_evidence": {"status": "exact", "valid": True},
                "usage": {"prompt_tokens": 2, "completion_tokens": 3},
                "cost_usd": 0.01,
                "cost_source": "estimated",
                "request_id": str(len(calls)),
            }

    monkeypatch.setattr(smoke, "create_provider", lambda *a, **k: FakeProvider())

    def evaluate(source, language, problem, folder, runtime):
        assert "CMD_API_KEY" not in os.environ
        evaluated.append(language)
        return {
            "status": "success",
            "cases": [{"status": "success"} for _ in range(13)],
        }

    monkeypatch.setattr(smoke, "evaluate", evaluate)
    experiment = yaml.safe_load(
        Path("configs/v1.6/experiment.yaml").read_text(encoding="utf-8")
    )
    result = smoke.run_model(
        cfg, tmp_path / "glm53", experiment, Path("data/rtt-v1.6"), "in-memory-test"
    )
    assert len(calls) == 5 and all(
        call["logical_request"]["phase"] == "integration_smoke" for call in calls
    )
    assert evaluated == ["python", "cpp", "haskell", "cpp"]
    assert result["passed"] and len(result["routes"]) == 2
    assert "CMD_API_KEY" not in os.environ
    assert all(
        "in-memory-test" not in path.read_text() for path in tmp_path.rglob("*.json")
    )


def test_smoke_refuses_flash_or_large_call_budget():
    from scripts.integration_commandcode import validate_smoke_config

    cfg = yaml.safe_load(
        Path("configs/v1.6/providers/commandcode_glm53.yaml").read_text(
            encoding="utf-8"
        )
    )
    cfg["model"] = "z-ai/glm-5.3-flash"
    with pytest.raises(ValueError):
        validate_smoke_config(cfg)
    cfg["model"] = "zai-org/GLM-5.3"
    cfg["max_calls"] = 7
    with pytest.raises(ValueError):
        validate_smoke_config(cfg)


def test_secret_audit_handles_its_own_locked_one_byte_file(tmp_path):
    from rttdist.providers import file_lock
    from scripts.integration_commandcode import secret_audit

    (tmp_path / "safe.json").write_text('{"safe": true}')
    with file_lock(tmp_path / "integration.lock"):
        assert secret_audit(tmp_path, "in-memory-test") is True
    (tmp_path / "leak.txt").write_text("in-memory-test")
    assert secret_audit(tmp_path, "in-memory-test") is False
