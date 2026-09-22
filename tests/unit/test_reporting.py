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
        "rtt_distance": {"availability": "measured", "value": 1, "unit": "completed_full_routes", "definition": "one route = cpp->python->cpp"},
        "convergence_status": "fixed_point",
        "language_route": ["cpp", "python", "cpp"],
        "translation_count_per_cycle": 2,
        "attempted_translation_count": 2,
        "completed_translation_count": 2,
        "failed_translation_count": 0,
        "translation_count": {"per_cycle": 2, "attempted": 2, "completed": 2, "failed": 0, "unit": "translations"},
        "translation_steps": [
            {"step_index": 1, "source_language": "cpp", "target_language": "python", "status": "completed"},
            {"step_index": 2, "source_language": "python", "target_language": "cpp", "status": "completed"},
        ],
        "distance_metrics": {
            "schema_version": 1,
            "change_count": {"available": True, "status": "measured", "value": 1, "unit": "completed_full_routes", "canonical_source": "rtt_distance"},
            "residual_similarity": {"available": True, "status": "measured", "metric": "sorensen_dice_token_multiset", "value": 1.0, "unit": "ratio", "source_language": "cpp"},
            "semantic_preservation": {"available": True, "status": "pass", "overall_passed": True, "final_roundtrip_passed": True, "route_had_degradation": False, "canonical_source": "evaluation_checks"},
            "complexity_delta": {"available": False, "status": "unavailable", "tool": "lizard", "reason": "optional_tool_not_configured_or_not_installed", "metrics": {}},
        },
        "conversion_log_path": "run/IPOP/cpp-to-python/iterations/iter-001/conversion.log",
    }), encoding="utf-8")
    (iter_dir / "conversion.log").write_text("translation_count_per_cycle=2\n", encoding="utf-8")
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
            "language_route": ["cpp", "python", "cpp"],
            "route_key": "cpp->python->cpp",
        },
        "iterations": [{"artifact_paths": {
            "iteration_directory": "run/IPOP/cpp-to-python/iterations/iter-001",
            "execution_result_path": "run/IPOP/cpp-to-python/iterations/iter-001/execution.json",
            "metrics_path": "run/IPOP/cpp-to-python/iterations/iter-001/metrics.json",
            "roundtrip_source_path": "run/IPOP/cpp-to-python/iterations/iter-001/roundtrip.cpp",
        },
            "translation_count_per_cycle": 2,
            "attempted_translation_count": 2,
            "completed_translation_count": 2,
            "failed_translation_count": 0,
            "conversion_log_path": "run/IPOP/cpp-to-python/iterations/iter-001/conversion.log",
        }],
        "final": final.to_dict(),
    }
    (run_dir / "run.json").write_text(json.dumps(manifest), encoding="utf-8")

    summary = generate_run_summary(output_root=output_root, run_id="run")
    entry = summary["results"][0]
    assert entry["rtt_route_key"] == "cpp->python->cpp"
    assert entry["rtt_distance"]["value"] == 1
    assert entry["translation_count_per_cycle"] == 2
    assert entry["completed_translation_count"] == 2
    assert entry["failed_translation_count"] == 0
    assert entry["distance_metrics"]["change_count"]["value"] == 1
    assert entry["distance_metrics"]["residual_similarity"]["value"] == 1.0
    assert entry["distance_metrics"]["semantic_preservation"]["status"] == "pass"
    assert entry["distance_metrics"]["complexity_delta"]["status"] == "unavailable"
    assert entry["artifacts"]["final_conversion_log_path"] == "run/IPOP/cpp-to-python/iterations/iter-001/conversion.log"

    artifacts = write_run_summary(output_root=output_root, run_id="run")
    markdown = artifacts.summary_markdown_path.read_text(encoding="utf-8")
    assert "Translations per RTT cycle: 2" in markdown
    assert "Completed translations in final iteration: 2" in markdown
    assert "Semantic preservation: pass" in markdown
    assert "Legacy semantic summary (raw execution): pass" in markdown
    assert "Residual similarity: measured 1.000000" in markdown
    assert "Complexity delta: unavailable (optional_tool_not_configured_or_not_installed)" in markdown


def test_summary_legacy_null_rtt_distance_fallback_is_unavailable(tmp_path: Path) -> None:
    output_root = tmp_path / "artifacts"
    run_dir = output_root / "run" / "IPOP" / "cpp-to-python"
    iter_dir = run_dir / "iterations" / "iter-001"
    iter_dir.mkdir(parents=True)
    (iter_dir / "roundtrip.cpp").write_text("", encoding="utf-8")
    (iter_dir / "metrics.json").write_text(json.dumps({
        "rtt_distance": None,
        "convergence_status": "continue",
        "language_route": ["cpp", "python", "cpp"],
        "translation_count": {"per_cycle": 2, "attempted": 1, "completed": 0, "failed": 1, "unit": "translations"},
        "translation_steps": [{"step_index": 1, "source_language": "cpp", "target_language": "python", "status": "translation_failed"}],
        "conversion_log_path": "run/IPOP/cpp-to-python/iterations/iter-001/conversion.log",
    }), encoding="utf-8")
    (iter_dir / "conversion.log").write_text("translation_count_per_cycle=2\n", encoding="utf-8")
    (iter_dir / "execution.json").write_text(json.dumps({"steps": []}), encoding="utf-8")
    final = FailureRecord(status=FailureStatus.API_ERROR, stage="step_001_cpp_to_python_translation", iteration_index=1, message="api failed.")
    manifest = {
        "metadata": {
            "problem": {"problem_id": "IPOP"},
            "seed_language": "cpp",
            "target_language": "python",
            "language_route": ["cpp", "python", "cpp"],
            "route_key": "cpp->python->cpp",
        },
        "iterations": [{"artifact_paths": {
            "iteration_directory": "run/IPOP/cpp-to-python/iterations/iter-001",
            "execution_result_path": "run/IPOP/cpp-to-python/iterations/iter-001/execution.json",
            "metrics_path": "run/IPOP/cpp-to-python/iterations/iter-001/metrics.json",
            "roundtrip_source_path": "run/IPOP/cpp-to-python/iterations/iter-001/roundtrip.cpp",
        },
            "translation_count_per_cycle": 2,
            "attempted_translation_count": 1,
            "completed_translation_count": 0,
            "failed_translation_count": 1,
            "conversion_log_path": "run/IPOP/cpp-to-python/iterations/iter-001/conversion.log",
        }],
        "final": final.to_dict(),
    }
    (run_dir / "run.json").write_text(json.dumps(manifest), encoding="utf-8")

    summary = generate_run_summary(output_root=output_root, run_id="run")
    entry = summary["results"][0]

    assert entry["rtt_distance"]["availability"] == "unavailable"
    assert entry["rtt_distance"]["reason"] == "legacy_rtt_distance_missing"
    assert entry["distance_metrics"]["change_count"]["available"] is False
    assert entry["distance_metrics"]["change_count"]["reason"] == "legacy_rtt_distance_missing"
    aggregate = summary["rtt_route_aggregates"]["cpp->python->cpp"]
    assert aggregate["rtt_distance"]["unavailable_count"] == 1
    assert aggregate["rtt_distance"]["measured_count"] == 0
