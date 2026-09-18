"""Resume only the retained v2 main repetition under the user-amended plan."""
import os
from pathlib import Path
import sys

import yaml

from rttdist.config import load_experiment_config
from rttdist.experiment_io import read_json, timestamp, write_json
from rttdist.experiment_v1 import run_experiment
from rttdist.reporting_v1 import report_runs
from run_v2 import resource_report
from v1_checks import audit


def main():
    workspace = Path(__file__).resolve().parents[1]
    os.chdir(workspace)
    os.environ["PATH"] = os.pathsep.join([str(workspace / ".tools/gcc/bin"),
                                         str(workspace / ".tools/R/bin/x64"), os.environ["PATH"]])
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    sys.stderr.reconfigure(encoding="utf-8", line_buffering=True)
    config = load_experiment_config(workspace / "lmstudio_v2.yaml")
    raw = yaml.safe_load((workspace / "lmstudio_v2.yaml").read_text(encoding="utf-8"))
    root = config.output_root
    revision = read_json(root / "execution_plan_revision.json")
    if revision["main_repetitions"] != 1:
        raise ValueError("This driver requires the one-repetition amendment")
    run_id = revision["retained_run_id"]
    planned = len(config.problem_ids)*len(config.target_languages)
    state = {"status": "main_running", "run_id": run_id, "updated_at": timestamp(),
             "planned_main_observations": planned, "main_repetitions": 1,
             "plan_revision": "execution_plan_revision.json"}
    continuation = {"pid": os.getpid(), "status": "main_running", "updated_at": timestamp(),
                    "driver": "scripts/run_v2_single.py", "main_repetitions": 1}
    write_json(root / "campaign_status.json", state)
    write_json(root / "continuation_status.json", continuation)
    try:
        started = read_json(root / "main_started.json")["started_at"]
        run_raw = {**raw, "repeat_index": 1, "campaign_started_at": started}
        results = run_experiment(config, run_raw, run_id, resume=True)
        for _ in range(raw["recovery"]["max_resumes_per_route"]):
            if not any(r["status"] == "api_error" for r in results):
                break
            results = run_experiment(config, run_raw, run_id, resume=True)
        if len(results) != planned or any(r["status"] == "api_error" or r["details"].get("missing_toolchain") for r in results):
            raise RuntimeError("Unresolved infrastructure; retain incomplete observations")
        summary = report_runs(root, [run_id])
        audit(root / run_id / "summary.json")
        resources = resource_report(root / run_id)
        write_json(root / run_id / "resources.json", resources)
        from v2_quick_report import write_report
        write_report(root)
        lines = ["# v2 단일 반복 실험 결과", "", f"완료 시각(UTC): {timestamp()}.", "",
                 "사용자 요청으로 전체 반복을 3회에서 1회로 축소한 결과다. "
                 "40문제 × 3경로 = 120건이며 예비 15건은 포함하지 않는다. "
                 "고정점 후보 탐색 K=10과 추가 확인 c=5, 모델·프롬프트·평가 조건은 유지했다.", "",
                 "| 경로 | c=5 성공 / 평가 수 | 성공률 | 문제 단위 bootstrap 95% CI |",
                 "| --- | ---: | ---: | --- |"]
        for route, agg in summary["rtt_route_aggregates"].items():
            stat = agg["by_confirmation"]["5"]
            lines.append(f"| {route} | {stat['success_count']} / {agg['evaluable_count']} | {stat['p_sf']:.1%} | {stat['p_sf_ci95']} |")
        lines += ["", f"모델 응답 {resources['logical_calls']}개, API 오류 시도 {resources['api_errors']}건, 출력 절단 {resources['truncated']}건.",
                  "단일 반복에서는 실행 간 변동성을 평가하지 못한다. 40개 문제의 결과이며 모델·언어 전반의 순위로 일반화하지 않는다. "
                  "p_SF는 성공률이며 통계적 p값이 아니다. bootstrap은 저장된 결과의 재표집이다.", "",
                  f"[전체 지표](../artifacts-lmstudio/v2-a-quality-1/{run_id}/summary.md), "
                  f"[완료 감사](../artifacts-lmstudio/v2-a-quality-1/{run_id}/completion_audit.json), "
                  "[계획 개정](../artifacts-lmstudio/v2-a-quality-1/execution_plan_revision.json), "
                  "[실행 기록](EXPERIMENT_v2_log.md).", ""]
        (workspace / "docs/RESULT_v2.md").write_text("\n".join(lines), encoding="utf-8")
        state.update(status="complete", completed_main_observations=planned, updated_at=timestamp())
        continuation.update(status="complete", updated_at=timestamp())
        write_json(root / "campaign_status.json", state)
        write_json(root / "continuation_status.json", continuation)
    except Exception as exc:
        state.update(status="incomplete", error=f"{type(exc).__name__}: {exc}", updated_at=timestamp())
        continuation.update(status="incomplete", error=str(exc), updated_at=timestamp())
        write_json(root / "campaign_status.json", state)
        write_json(root / "continuation_status.json", continuation)
        raise


if __name__ == "__main__":
    main()
