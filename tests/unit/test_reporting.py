import json
from pathlib import Path

from rttdist.failure_taxonomy import FailureRecord, FailureStatus
from rttdist.reporting import generate_run_summary, write_run_summary


def test_summary_reports_only_rtt_distance_and_semantics(tmp_path: Path) -> None:
    output_root = tmp_path / "artifacts"
    run_dir = output_root / "run" / "IPOP" / "cpp-to-python"
    iter_dir = run_dir / "iterations" / "iter-001"
    iter_dir.mkdir(parents=True)
    (iter_dir / "roundtrip.cpp").write_text("int main(){return 0;}\n", encoding="utf-8")
    (iter_dir / "metrics.json").write_text(json.dumps({
        "rtt_distance": {"availability": "measured", "value": 1, "unit": "completed_full_routes", "definition": "one route = cpp->c->java->python->cpp"},
        "convergence_status": "fixed_point",
        "language_route": ["cpp", "c", "java", "python", "cpp"],
        "translation_count_per_cycle": 4,
        "attempted_translation_count": 4,
        "completed_translation_count": 4,
        "failed_translation_count": 0,
        "translation_count": {"per_cycle": 4, "attempted": 4, "completed": 4, "failed": 0, "unit": "translations"},
        "translation_steps": [
            {"step_index": 1, "source_language": "cpp", "target_language": "c", "status": "completed"},
            {"step_index": 2, "source_language": "c", "target_language": "java", "status": "completed"},
            {"step_index": 3, "source_language": "java", "target_language": "python", "status": "completed"},
            {"step_index": 4, "source_language": "python", "target_language": "cpp", "status": "completed"},
        ],
        "conversion_log_path": "run/IPOP/cpp-to-python/iterations/iter-001/conversion.log",
    }), encoding="utf-8")
    (iter_dir / "conversion.log").write_text("translation_count_per_cycle=4\n", encoding="utf-8")
    (iter_dir / "execution.json").write_text(json.dumps({
        "steps": [
            {"status": "success", "fixture_results": []},
            {"status": "success", "fixture_results": []},
        ]
    }), encoding="utf-8")
    final = FailureRecord(status=FailureStatus.SUCCESS, stage="convergence", iteration_index=1, message="Fixed point reached.", details={"convergence_status": "fixed_point"})
    manifest = {
        "metadata": {
            "problem": {"problem_id": "IPOP"},
            "seed_language": "cpp",
            "target_language": "python",
            "language_route": ["cpp", "c", "java", "python", "cpp"],
            "route_key": "cpp->c->java->python->cpp",
        },
        "iterations": [{"artifact_paths": {
            "iteration_directory": "run/IPOP/cpp-to-python/iterations/iter-001",
            "execution_result_path": "run/IPOP/cpp-to-python/iterations/iter-001/execution.json",
            "metrics_path": "run/IPOP/cpp-to-python/iterations/iter-001/metrics.json",
            "roundtrip_source_path": "run/IPOP/cpp-to-python/iterations/iter-001/roundtrip.cpp",
        },
            "translation_count_per_cycle": 4,
            "attempted_translation_count": 4,
            "completed_translation_count": 4,
            "failed_translation_count": 0,
            "conversion_log_path": "run/IPOP/cpp-to-python/iterations/iter-001/conversion.log",
        }],
        "final": final.to_dict(),
    }
    (run_dir / "run.json").write_text(json.dumps(manifest), encoding="utf-8")

    summary = generate_run_summary(output_root=output_root, run_id="run")
    entry = summary["results"][0]
    assert entry["rtt_route_key"] == "cpp->c->java->python->cpp"
    assert entry["rtt_distance"]["value"] == 1
    assert entry["translation_count_per_cycle"] == 4
    assert entry["completed_translation_count"] == 4
    assert entry["failed_translation_count"] == 0
    assert entry["artifacts"]["final_conversion_log_path"] == "run/IPOP/cpp-to-python/iterations/iter-001/conversion.log"
    assert "ast" + "_distance" not in entry
    assert "residual" + "_similarity" not in entry
    assert "com" + "plexity_deltas" not in entry

    artifacts = write_run_summary(output_root=output_root, run_id="run")
    markdown = artifacts.summary_markdown_path.read_text(encoding="utf-8")
    assert "Translations per RTT cycle: 4" in markdown
    assert "Completed translations in final iteration: 4" in markdown
    assert "A" + "ST" not in markdown
