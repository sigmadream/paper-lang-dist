from pathlib import Path
import subprocess
import sys

import pytest

from rttdist import cli, hops_experiment as hops
from rttdist.experiment_io import read_json, write_json
from tests.integration.test_hops_experiment import MockProvider, setup


def arguments(action):
    return [
        "hops",
        "--config",
        str(Path(__file__).resolve().parents[2] / "configs/v1.6/experiment.yaml"),
        "--phase",
        "pilot",
        "--action",
        action,
    ]


@pytest.mark.parametrize("action", ["run", "resume"])
def test_hops_run_resume_cli_connects(action, monkeypatch):
    calls = []
    monkeypatch.setattr(
        hops,
        "run_hops_campaign",
        lambda cfg, phase, shard=None: calls.append((phase, shard))
        or [{"evaluable": True}],
        raising=False,
    )
    assert cli.main(arguments(action)) == 0
    assert calls == [("pilot", None)]


def test_hops_report_cli_connects_reporter_without_provider(monkeypatch):
    calls = []
    monkeypatch.setattr(
        hops,
        "report_hops_campaign",
        lambda cfg, phase: calls.append(phase) or {"complete": False},
        raising=False,
    )
    monkeypatch.setattr(
        hops,
        "create_provider",
        lambda *a, **k: pytest.fail("보고는 공급자를 생성하지 않습니다."),
    )
    assert cli.main(arguments("report")) == 0
    assert calls == ["pilot"]


def test_hops_invalid_observation_cli_returns_error(monkeypatch):
    monkeypatch.setattr(hops, "run_hops_campaign", lambda *a: [{"evaluable": False}])
    assert cli.main(arguments("run")) == 2


def test_python_module_entrypoint_shows_hops_help():
    result = subprocess.run(
        [sys.executable, "-m", "rttdist", "hops", "--help"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert "--provider-config" in result.stdout
    assert "--phase" in result.stdout
    assert "--action" in result.stdout


def test_installed_console_entrypoint_still_shows_hops_help():
    executable = Path(sys.executable).with_name(
        "rttdist.exe" if sys.platform == "win32" else "rttdist"
    )
    result = subprocess.run(
        [str(executable), "hops", "--help"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert "--provider-config" in result.stdout


def test_offline_cli_report_writes_tables_figures_and_evidence(setup, monkeypatch):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot
    from scripts.verify_v16_reproducibility import offline_reporting

    cfg, job, unused_folder = setup
    root = hops.campaign_root(cfg) / "pilot"
    folder = root / job["problem_id"] / job["route"] / "attempt-01"
    hops.run_hops_observation(cfg, job, MockProvider(), folder)
    write_json(root / "contract.json", read_json(folder / "contract.json"))
    monkeypatch.setattr(hops, "load_hops_config", lambda *a: cfg)
    monkeypatch.setattr(
        hops, "create_provider", lambda *a, **k: pytest.fail("보고 중 공급자 호출 금지")
    )
    with offline_reporting():
        assert cli.main(arguments("report")) == 0
    destination = root / "report"
    for name in (
        "observations.csv",
        "thresholds.csv",
        "problems.csv",
        "failures.csv",
        "confirmation.csv",
        "stages.csv",
        "evidence.json",
        "summary.md",
    ):
        assert (destination / name).is_file(), name
    assert (destination / "metrics.png").stat().st_size > 1000
    assert (destination / "protocol.png").stat().st_size > 1000
