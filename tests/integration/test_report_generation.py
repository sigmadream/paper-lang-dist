from pathlib import Path

from rttdist.reporting import generate_run_summary


def test_report_generation_module_uses_rtt_schema(tmp_path: Path) -> None:
    output_root = tmp_path / "artifacts"
    (output_root / "run").mkdir(parents=True)
    summary = generate_run_summary(output_root=output_root, run_id="run", run_results=())
    assert summary["schema_version"] == "report_summary.rtt.v1"
    assert summary["result_count"] == 0
