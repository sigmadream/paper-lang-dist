"""보고 산출물과 호출 없는 재현성을 고정 합성 자료로 검증합니다."""

import csv
import json
from pathlib import Path
import socket
import sys
from types import SimpleNamespace

import pytest

from rttdist.hops_reporting import summarize_hops
from scripts import report_v16, verify_v16_reproducibility as verifier
from tests.unit.test_hops_reporting import ROUTES
from tests.integration.test_hops_experiment import setup as core_setup, MockProvider


def inputs():
    root = Path("tests/fixtures/hops_v16")
    data = report_v16.load_bundle(root)
    data["contract"]["llm"]["api_key"] = "DO-NOT-EXPORT"
    return data


def test_report_tables_figures_and_evidence_share_summary(tmp_path):
    data = inputs()
    summary = summarize_hops(data["records"], data["manifest"], data["contract"])
    result = report_v16.write_v16_report(summary, tmp_path)
    assert result["summary_sha256"]
    exported = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert exported["routes"][ROUTES[0]]["D"] == 4.5
    with (tmp_path / "thresholds.csv").open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert float(rows[1]["D"]) == 4.5
    assert (tmp_path / "metrics.png").stat().st_size > 1000
    assert (tmp_path / "protocol.pdf").stat().st_size > 1000
    assert (tmp_path / "similarities.csv").exists()
    assert (tmp_path / "recursive_groups.csv").exists()
    assert (tmp_path / "call_usage.csv").exists()
    evidence = json.loads((tmp_path / "evidence.json").read_text(encoding="utf-8"))
    assert "/routes/cpp-via-python/D" in evidence["fields"]
    for path in tmp_path.rglob("*"):
        if path.is_file() and path.suffix in (".json", ".jsonl", ".md", ".csv"):
            assert "DO-NOT-EXPORT" not in path.read_text(encoding="utf-8-sig")
    assert (tmp_path / "reproducibility_bundle" / "observations.json").exists()
    rebuilt = report_v16.load_bundle(tmp_path / "reproducibility_bundle")
    rebuilt_summary = summarize_hops(
        rebuilt["records"], rebuilt["manifest"], rebuilt["contract"]
    )
    assert report_v16.public_data(rebuilt_summary) == exported


def test_final_display_rounding_regression(tmp_path):
    data = inputs()
    summary = summarize_hops(data["records"], data["manifest"], data["contract"])
    fixture = json.loads(
        Path("tests/fixtures/hops_v16/presentation_regression.json").read_text(
            encoding="utf-8"
        )
    )
    for language in ("python", "java", "haskell"):
        summary["routes"][f"cpp-via-{language}"] = {
            **summary["routes"][ROUTES[0]],
            **fixture[language],
        }
    report_v16.write_v16_report(summary, tmp_path)
    prose = (tmp_path / "summary.md").read_text(encoding="utf-8")
    assert all(text in prose for text in fixture["expected"])


def test_offline_rebuild_twice_has_identical_numerical_outputs(tmp_path):
    result = verifier.verify_v16_reproducibility(
        {**inputs(), "report_destination": str(tmp_path)}, None
    )
    assert result["passed"]
    assert result["network_disabled"] and result["sdk_disabled"]
    assert result["summary_exactly_equal"] and result["csv_exactly_equal"]
    assert result["figure_inputs_exactly_equal"]
    again = verifier.verify_v16_reproducibility(
        {**inputs(), "report_destination": str(tmp_path)}, None
    )
    assert again == result


def test_offline_guard_blocks_socket_subprocess_and_loaded_sdk(monkeypatch):
    class FakeClient:
        def start(self):
            raise RuntimeError("차단되지 않은 호출입니다.")

    monkeypatch.setitem(
        sys.modules, "copilot", SimpleNamespace(CopilotClient=FakeClient)
    )
    with verifier.offline_reporting():
        with pytest.raises(AssertionError, match="차단"):
            socket.create_connection(("example.invalid", 443))
        with pytest.raises(AssertionError, match="차단"):
            FakeClient().start()


def test_saved_core_contract_and_selection_are_read(tmp_path):
    data = inputs()
    selection = tmp_path / "selection.json"
    selection.write_text(json.dumps(data["manifest"]), encoding="utf-8")
    root = tmp_path / "campaign" / "main"
    root.mkdir(parents=True)
    (root / "contract.json").write_text(
        json.dumps({"config": data["contract"], "protocol": "rtt-hops-v1.6"}),
        encoding="utf-8",
    )
    for row in data["records"]:
        folder = root / "p1" / row["route"] / f"attempt-{row['attempt']:02}"
        folder.mkdir(parents=True)
        (folder / "observation.json").write_text(json.dumps(row), encoding="utf-8")
    loaded = report_v16.load_report_inputs(
        {
            "output_root": str(tmp_path),
            "campaign_id": "campaign",
            "selection": str(selection),
        }
    )
    assert len(loaded["records"]) == 3
    summary = summarize_hops(loaded["records"], loaded["manifest"], loaded["contract"])
    assert summary["routes"][ROUTES[0]]["D"] == 4.5


def test_evaluator_compile_timeout_remains_assessed_failure_in_report(
    tmp_path, monkeypatch
):
    from rttdist import fps_execution

    problem = tmp_path / "problem"
    cases = problem / "evaluation"
    cases.mkdir(parents=True)
    (cases / "sample.inp").write_text("1\n", encoding="utf-8")
    (cases / "sample.out").write_text("1\n", encoding="utf-8")
    monkeypatch.setattr(
        fps_execution,
        "process",
        lambda *args, **kwargs: {
            "timed_out": True,
            "exit_code": None,
            "stdout": "",
            "stderr": "",
        },
    )
    evaluation = fps_execution.evaluate(
        "print(1)",
        "python",
        problem,
        tmp_path / "evaluated",
        {
            "minimum_evaluation_cases": 1,
            "tools": {"python": "mock-interpreter"},
            "compile_timeout": 180,
            "fixture_timeout": 5,
        },
    )
    assert evaluation["status"] == "compile_timeout"
    data = inputs()
    row = data["records"][0]
    row["steps"] = [
        {
            "step": 1,
            "kind": "discovery",
            "language": "python",
            "evaluation_status": evaluation["status"],
            "evaluation": evaluation,
        }
    ]
    row["translation_steps"] = 1
    row["confirmation_status"] = None
    for outcome in row["outcomes"].values():
        outcome.update(success=False, category="functional_failure", reached_step=None)
    summary = summarize_hops([row], data["manifest"], data["contract"])
    destination = tmp_path / "report"
    report_v16.write_v16_report(summary, destination)
    with (destination / "stages.csv").open(encoding="utf-8-sig", newline="") as stream:
        stages = list(csv.DictReader(stream))
    assert len(stages) == 1
    assert {
        key: stages[0][key]
        for key in ("attempts", "assessable", "unavailable", "passed", "pass_rate")
    } == {
        "attempts": "1",
        "assessable": "1",
        "unavailable": "0",
        "passed": "0",
        "pass_rate": "0.0",
    }


def test_core_observation_reports_and_reproduces_without_api(core_setup, tmp_path):
    from rttdist import hops_experiment as core

    cfg, job, folder = core_setup
    record = core.run_hops_observation(cfg, job, MockProvider(), folder)
    raw_csv = folder / "step-02" / "sym_adj" / "result" / "results.csv"
    raw_csv.parent.mkdir(parents=True, exist_ok=True)
    raw_csv.write_text("averageSimilarity\n0.95\n", encoding="utf-8")
    frozen = json.loads((folder / "contract.json").read_text(encoding="utf-8"))
    frozen.update(problem_ids=[job["problem_id"]], repeats=1)
    data = {
        "records": [record],
        "manifest": {
            "problems": [{"problem_id": job["problem_id"], "recursive": True}]
        },
        "contract": frozen,
        "report_destination": str(tmp_path / "core-report"),
    }
    result = verifier.verify_v16_reproducibility(data, None)
    assert result["passed"]
    summary = json.loads(
        (tmp_path / "core-report" / "summary.json").read_text(encoding="utf-8")
    )
    assert summary["routes"][ROUTES[0]]["H"] == 2
    assert summary["routes"][ROUTES[0]]["confirmation"]["passed"] == 1
    assert summary["metadata"]["actual_models"] == ["test"]
    raw_index = json.loads(
        (
            tmp_path / "core-report" / "reproducibility_bundle" / "raw_sources.json"
        ).read_text(encoding="utf-8")
    )
    assert any(
        item["source"] == str(raw_csv) and item["included"] for item in raw_index
    )
