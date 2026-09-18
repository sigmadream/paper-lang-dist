"""Continue a running pilot after its gate passes and write the audited v2 result."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from rttdist.experiment_io import read_json, timestamp, write_json

WORKSPACE = Path(__file__).resolve().parents[1]
ROOT = WORKSPACE / "artifacts-lmstudio/v2-a-quality-1"


def write_result():
    summary_path = ROOT / "v2-combined/summary.json"
    summary = read_json(summary_path)
    audit = read_json(ROOT / "v2-combined/completion_audit.json")
    if not summary["complete"] or not audit["passed"] or audit["observed"] != 360:
        raise ValueError("A complete audited 360-observation result is required")
    pilot = read_json(ROOT / "v2-a-quality-1-pilot/resources.json")
    resources = [read_json(ROOT / (meta["run_id"] + "/resources.json")) for meta in summary["run_metadata"]]
    lines = ["# v2-a-quality-1 실험 결과", "", f"집계 시각: {timestamp()}.", "",
             "40문제 × C/Java/Python 3경로 × 3회 = 360건. 예비 15건은 본 실험에서 제외했다.",
             "평가 입력 520개, P2 프롬프트, Qwen2.5-Coder 7B Q4_K_M, 순차 실행 조건이다.", "",
             "| 경로 | c=5 성공 / 평가 수 | 성공률 | 문제 단위 bootstrap 95% CI |",
             "| --- | ---: | ---: | --- |"]
    for route, agg in summary["rtt_route_aggregates"].items():
        s = agg["by_confirmation"]["5"]
        lines.append(f"| {route} | {s['success_count']} / {agg['evaluable_count']} | {s['p_sf']:.1%} | {s['p_sf_ci95']} |")
    lines += ["", "| 경로 | 종료 상태 | 건수 |", "| --- | --- | ---: |"]
    for route in summary["rtt_route_aggregates"]:
        counts = Counter(r["status"] for r in summary["observations"] if r["route"] == route)
        lines.extend(f"| {route} | {status} | {n} |" for status, n in sorted(counts.items()))
    main_calls = sum(r["logical_calls"] for r in resources)
    output_tokens = sum(r["completion_tokens_total"] for r in resources)
    lines += ["", f"본 실험 API 응답 {main_calls}개, 출력 {output_tokens:,}토큰. "
              f"예비 API 응답 {pilot['logical_calls']}개는 별도 보존했다.",
              f"본 실험 출력 절단 {sum(r['truncated'] for r in resources)}건, "
              f"기록된 API 오류 시도 {sum(r['api_errors'] for r in resources)}건.", "",
              "주 지표는 추가 확인 5회까지 기능을 보존한 고정점 성공률이다. "
              "tau와 토큰·AST 변화는 성공 조건부이며 실패에 0 또는 K를 대입하지 않는다.",
              "단일 모델·프롬프트와 40개 알고리즘 문제의 결과이므로 일반적인 언어 순위나 의미 동등성의 증명으로 해석하지 않는다. "
              "v1과는 원본·입력·프롬프트·스케줄 조건이 달라 테스트 강화만의 인과 효과로 해석할 수 없다.", "",
              "[실행 설계](EXPERIMENT_v2_log.md), "
              "[전체 지표 표](../artifacts-lmstudio/v2-a-quality-1/v2-combined/summary.md), "
              "[원본 집계 JSON](../artifacts-lmstudio/v2-a-quality-1/v2-combined/summary.json), "
              "[완료 감사](../artifacts-lmstudio/v2-a-quality-1/v2-combined/completion_audit.json).", ""]
    target = WORKSPACE / "docs/RESULT_v2.md"
    target.write_text("\n".join(lines), encoding="utf-8")
    write_json(ROOT / "v2-combined/result_provenance.json", {
        "created_at": timestamp(), "reporter_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "summary_sha256": hashlib.sha256(summary_path.read_bytes()).hexdigest(),
        "result_sha256": hashlib.sha256(target.read_bytes()).hexdigest()})


def main():
    os.chdir(WORKSPACE)
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    sys.stderr.reconfigure(encoding="utf-8", line_buffering=True)
    monitor = ROOT / "continuation_status.json"
    start = time.monotonic()
    try:
        while True:
            state = read_json(ROOT / "campaign_status.json")
            write_json(monitor, {"pid": os.getpid(), "status": "waiting_for_pilot", "updated_at": timestamp()})
            if state["status"] == "incomplete":
                raise RuntimeError(f"Pilot stopped: {state.get('error')}")
            if state["status"] == "pilot_complete" and (ROOT / "pilot_gate.json").exists():
                break
            if time.monotonic() - start > 86400:
                raise TimeoutError("Pilot did not finish within 24 hours")
            time.sleep(10)
        write_json(monitor, {"pid": os.getpid(), "status": "main_running", "updated_at": timestamp()})
        result = subprocess.run([sys.executable, "-X", "utf8", "-u", "scripts/run_v2.py", "--stage", "main"], check=False)
        if result.returncode:
            raise RuntimeError(f"Main driver exited {result.returncode}; preserve incomplete observations")
        write_result()
        write_json(monitor, {"pid": os.getpid(), "status": "complete", "updated_at": timestamp()})
    except Exception as exc:
        write_json(monitor, {"pid": os.getpid(), "status": "incomplete", "updated_at": timestamp(), "error": str(exc)})
        raise


if __name__ == "__main__":
    main()
