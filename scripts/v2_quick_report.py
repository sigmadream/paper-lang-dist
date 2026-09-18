"""Snapshot completed main observations without model calls, AST work or bootstrap."""
from collections import Counter, defaultdict
from pathlib import Path
import argparse
import statistics

from rttdist.experiment_io import read_json, timestamp, write_json
from rttdist.reporting_v1 import load_selected


def build(root):
    metas = [read_json(p) for p in sorted(root.glob("*/run_metadata.json"))]
    runs = [m["run_id"] for m in metas if m["phase"] == "main"]
    if not runs:
        raise ValueError("No main observations have started")
    metadata, rows, exclusions = load_selected(root, runs, postprocess=False)
    targets = metadata[0]["target_languages"]
    groups = defaultdict(list)
    for row in rows:
        groups[row["run_id"], row["problem_id"]].append(row)
    complete_blocks = {key for key, values in groups.items()
                       if {r["route"] for r in values} == {"cpp-to-" + t for t in targets}}
    paired = [r for r in rows if (r["run_id"], r["problem_id"]) in complete_blocks]
    frozen = read_json(root / "frozen_design.json")
    revision = root / "execution_plan_revision.json"
    design = read_json(revision) if revision.exists() else frozen
    result = {"created_at": timestamp(), "scope": "provisional_completed_observations",
              "condition_hash": metadata[0]["condition_hash"], "runs_started": runs,
              "planned_observations": design["main_observations"], "completed_observations": len(rows),
              "remaining_observations": design["main_observations"] - len(rows),
              "main_repetitions": design["main_repetitions"],
              "complete_problem_run_blocks": len(complete_blocks),
              "complete_block_problem_count": len({key[1] for key in complete_blocks}),
              "statuses": dict(Counter(r["status"] for r in rows)), "routes": {},
              "notes": ["No additional model calls, AST measurements or bootstrap resampling.",
                        "Rates use only blocks with all routes completed; incomplete blocks are not failures.",
                        "This execution-order-dependent subset does not estimate the final full-corpus ranking.",
                        "p_SF is an observed success proportion, not a statistical p-value.",
                        "c=3 is a secondary view of the same completed c=5 protocol, not a shortened new experiment."]}
    for target in targets:
        route = "cpp-to-" + target
        group = [r for r in paired if r["route"] == route]
        stats = {"paired_evaluable": len(group), "all_completed": sum(r["route"] == route for r in rows),
                 "statuses": dict(Counter(r["status"] for r in group)), "confirmation": {}}
        for c in (3, 5):
            successes = [r for r in group if r["success"][str(c)]]
            stats["confirmation"][str(c)] = {
                "success": len(successes), "failure": len(group)-len(successes),
                "p_sf": len(successes)/len(group) if group else None,
                "tau_median_success_only": statistics.median(r["tau"] for r in successes) if successes else None}
        result["routes"][route] = stats
    return result


def write_report(root):
    result = build(root)
    target = root / "interim"
    write_json(target / "quick_summary.json", result)
    lines = ["# v2 잠정 결과", "", f"기준 시각(UTC): {result['created_at']}", "",
             f"본 실험 {result['completed_observations']}/{result['planned_observations']}건 종료. "
             f"아직 종료하지 않은 {result['remaining_observations']}건은 실패로 계산하지 않는다.",
             f"세 경로가 모두 끝난 동일 문제·반복 {result['complete_problem_run_blocks']}묶음"
             f"(고유 문제 {result['complete_block_problem_count']}개)만 아래 비교에 포함한다.", "",
             "| 경로 | 비교 분모 | c=3 성공 | c=5 성공 | c=5 성공률 | 성공 조건부 tau 중앙값(c=5) |",
             "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for route, s in result["routes"].items():
        a, b = s["confirmation"]["3"], s["confirmation"]["5"]
        rate = f"{b['p_sf']:.1%}" if b["p_sf"] is not None else "미정"
        lines.append(f"| {route} | {s['paired_evaluable']} | {a['success']} | {b['success']} | {rate} | {b['tau_median_success_only']} |")
    lines += ["", f"p_SF는 통계적 p값이 아니라 관측 성공률이다. 현재 전체 실험 반복은 {result['main_repetitions']}회다. "
              "최종 보고서의 2,000회 bootstrap은 저장된 결과의 재표집이며 추가 모델 호출이 아니다.",
              "c=3은 현재 c=5 실험에서 종료한 동일 관측의 보조 집계이며 실행 조건을 바꾸지 않았다.",
              "이 표는 실행 순서에 따른 일부 문제의 잠정 결과다. 전체 성공률이나 언어 순위를 확정하지 않는다.",
              "이 보고서는 모델 호출·AST 계산·bootstrap 없이 생성했다. 예비 결과는 포함하지 않는다.", ""]
    (target / "quick_summary.md").write_text("\n".join(lines), encoding="utf-8")
    print(target / "quick_summary.md")
    print(f"Completed {result['completed_observations']}/{result['planned_observations']}; paired blocks {result['complete_problem_run_blocks']}")
    for route, stats in result["routes"].items():
        print(route, stats)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("--root", type=Path, default=Path("artifacts-lmstudio/v2-a-quality-1"))
    args = parser.parse_args()
    write_report(args.root)
