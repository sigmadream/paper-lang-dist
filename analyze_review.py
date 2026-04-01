#!/usr/bin/env python3
"""REVIEW.txt 표 2~4에 필요한 수치를 실험 로그에서 추출·집계하는 스크립트."""

import json
import statistics
from pathlib import Path

BASE = Path(__file__).parent

ollama_summary = json.loads(
    (BASE / "artifacts-real-ollama" / "smoke-ollama-001" / "summary.json").read_text()
)
openai_summary = json.loads(
    (BASE / "artifacts-real-openai" / "smoke-openai-001" / "summary.json").read_text()
)


def classify(results, model_name):
    """각 문제별로 표 2~4에 필요한 지표를 추출한다."""
    pairs = {"cpp->c": [], "cpp->java": [], "cpp->python": []}

    for r in results:
        key = r["ordered_pair_key"]
        if key not in pairs:
            continue

        pid = r["problem_id"]
        sem = r["semantic_summary"]
        target_passed = sem["target"]["passed"]
        roundtrip_passed = sem["roundtrip_cpp"]["passed"]
        overall_pass = sem["overall"] == "pass"

        # 1차 번역 성공: target이 실행 가능한 경우
        # target status가 success이거나 wrong_answer(실행은 됨)인 경우 "실행 가능"으로 본다
        target_status = sem["target"]["status"]
        fwd_success = target_status in ("success", "wrong_answer")

        # 역번역 성공: roundtrip_cpp가 실행 가능한 경우
        rt_status = sem["roundtrip_cpp"]["status"]
        rev_success = rt_status in ("success", "wrong_answer")

        # 의미 보존 성공: overall == "pass" (양쪽 모두 테스트 통과)
        semantic_pass = overall_pass

        # 고정점 도달
        conv = r["convergence_outcome"]
        fixed = conv == "fixed_point"

        # 반복 횟수
        iters = r["iteration_count"]

        # MOSS
        moss = r.get("moss_similarity", {})
        moss_avail = moss.get("availability") == "measured"
        moss_seed = moss.get("value", {}).get("seed_percentage") if moss_avail else None
        moss_rt = moss.get("value", {}).get("roundtrip_percentage") if moss_avail else None

        # Residual similarity
        resid = r.get("residual_similarity", {})
        resid_avail = resid.get("availability") == "measured"
        resid_val = resid.get("value") if resid_avail else None

        pairs[key].append({
            "problem_id": pid,
            "fwd_success": fwd_success,
            "rev_success": rev_success,
            "semantic_pass": semantic_pass,
            "fixed_point": fixed,
            "convergence": conv,
            "iterations": iters,
            "moss_seed": moss_seed,
            "moss_rt": moss_rt,
            "residual": resid_val,
            "final_status": r["final_status"],
        })

    return pairs


def print_table2(ollama_pairs, openai_pairs):
    """표 2: 단계별 성공률"""
    print("=" * 80)
    print("표 2) 모델 및 언어쌍별 RTT 단계 성공률")
    print("=" * 80)
    header = f"{'언어쌍':15s} {'모델':10s} {'1차번역성공':>12s} {'역번역성공':>10s} {'의미보존':>10s} {'고정점도달':>10s}"
    print(header)
    print("-" * 80)

    for pair_key, pair_label in [("cpp->c", "C++→C"), ("cpp->java", "C++→Java"), ("cpp->python", "C++→Python")]:
        for model, data in [("qwen2.5", ollama_pairs), ("gpt-5.4", openai_pairs)]:
            items = data[pair_key]
            n = len(items)
            fwd = sum(1 for x in items if x["fwd_success"])
            rev = sum(1 for x in items if x["rev_success"])
            sem = sum(1 for x in items if x["semantic_pass"])
            fp = sum(1 for x in items if x["fixed_point"])
            print(f"{pair_label:15s} {model:10s} {fwd:>5d}/{n:<5d} {rev:>4d}/{n:<4d} {sem:>5d}/{n:<5d} {fp:>4d}/{n:<4d}")
    print()


def print_table3(ollama_pairs, openai_pairs):
    """표 3: 고정점 반복 횟수의 분포"""
    print("=" * 80)
    print("표 3) 언어쌍별 고정점 반복 횟수의 분포")
    print("=" * 80)
    header = f"{'언어쌍':15s} {'모델':10s} {'도달률':>10s} {'전체 median[IQR]':>20s} {'도달사례 mean±SD':>25s}"
    print(header)
    print("-" * 80)

    for pair_key, pair_label in [("cpp->c", "C++→C"), ("cpp->java", "C++→Java"), ("cpp->python", "C++→Python")]:
        for model, data in [("qwen2.5", ollama_pairs), ("gpt-5.4", openai_pairs)]:
            items = data[pair_key]
            n = len(items)
            fp_count = sum(1 for x in items if x["fixed_point"])
            all_iters = [x["iterations"] for x in items]
            fp_iters = [x["iterations"] for x in items if x["fixed_point"]]

            # 전체 반복 횟수: median[IQR]
            med = statistics.median(all_iters)
            if len(all_iters) >= 2:
                q = statistics.quantiles(all_iters, n=4)
                iqr_str = f"{med:.0f} [{q[0]:.0f}–{q[2]:.0f}]"
            else:
                iqr_str = f"{med:.0f}"

            # 도달 사례 반복 횟수: mean±SD
            if len(fp_iters) >= 2:
                m = statistics.mean(fp_iters)
                s = statistics.stdev(fp_iters)
                fp_str = f"{m:.1f} ± {s:.1f}"
            elif len(fp_iters) == 1:
                fp_str = f"{fp_iters[0]:.1f}"
            else:
                fp_str = "N/A"

            print(f"{pair_label:15s} {model:10s} {fp_count:>4d}/{n:<4d} {iqr_str:>20s} {fp_str:>25s}")
    print()


def print_table4(ollama_pairs, openai_pairs):
    """표 4: MOSS 유사도 분포 (seed_percentage 기준)"""
    print("=" * 80)
    print("표 4) 언어쌍별 MOSS 유사도 분포 (seed_percentage 기준)")
    print("=" * 80)
    header = f"{'언어쌍':15s} {'모델':10s} {'MOSS mean±SD':>15s} {'median[IQR]':>15s} {'최소–최대':>12s}"
    print(header)
    print("-" * 80)

    for pair_key, pair_label in [("cpp->c", "C++→C"), ("cpp->java", "C++→Java"), ("cpp->python", "C++→Python")]:
        for model, data in [("qwen2.5", ollama_pairs), ("gpt-5.4", openai_pairs)]:
            items = data[pair_key]
            # MOSS seed percentage 값만 수집 (측정된 것)
            vals = [x["moss_seed"] for x in items if x["moss_seed"] is not None]

            if len(vals) >= 2:
                m = statistics.mean(vals)
                s = statistics.stdev(vals)
                med = statistics.median(vals)
                q = statistics.quantiles(vals, n=4) if len(vals) >= 4 else None
                iqr_str = f"{med:.0f} [{q[0]:.0f}–{q[2]:.0f}]" if q else f"{med:.0f}"
                rng = f"{min(vals):.0f}–{max(vals):.0f}"
                ms = f"{m:.1f} ± {s:.1f}"
            elif len(vals) == 1:
                ms = f"{vals[0]:.1f}"
                iqr_str = f"{vals[0]:.0f}"
                rng = f"{vals[0]:.0f}"
            else:
                ms = "N/A"
                iqr_str = "N/A"
                rng = "N/A"

            print(f"{pair_label:15s} {model:10s} {ms:>15s} {iqr_str:>15s} {rng:>12s}")

    print()
    print("--- Residual Similarity 분포 (참고) ---")
    print()
    header2 = f"{'언어쌍':15s} {'모델':10s} {'Resid mean±SD':>18s} {'median':>10s} {'최소–최대':>12s}"
    print(header2)
    print("-" * 70)

    for pair_key, pair_label in [("cpp->c", "C++→C"), ("cpp->java", "C++→Java"), ("cpp->python", "C++→Python")]:
        for model, data in [("qwen2.5", ollama_pairs), ("gpt-5.4", openai_pairs)]:
            items = data[pair_key]
            vals = [x["residual"] for x in items if x["residual"] is not None]

            if len(vals) >= 2:
                m = statistics.mean(vals)
                s = statistics.stdev(vals)
                med = statistics.median(vals)
                rng = f"{min(vals):.4f}–{max(vals):.4f}"
                ms = f"{m:.4f} ± {s:.4f}"
            elif len(vals) == 1:
                ms = f"{vals[0]:.4f}"
                med = vals[0]
                rng = f"{vals[0]:.4f}"
            else:
                ms = "N/A"
                med = None
                rng = "N/A"

            med_str = f"{med:.4f}" if med is not None else "N/A"
            print(f"{pair_label:15s} {model:10s} {ms:>18s} {med_str:>10s} {rng:>12s}")


def print_detail(ollama_pairs, openai_pairs):
    """문제별 상세 로그를 출력한다."""
    print()
    print("=" * 80)
    print("문제별 상세 로그")
    print("=" * 80)

    for pair_key, pair_label in [("cpp->c", "C++→C"), ("cpp->java", "C++→Java"), ("cpp->python", "C++→Python")]:
        print(f"\n--- {pair_label} ---")
        for model, data in [("qwen2.5", ollama_pairs), ("gpt-5.4", openai_pairs)]:
            print(f"  [{model}]")
            for x in sorted(data[pair_key], key=lambda d: d["problem_id"]):
                flags = []
                flags.append("fwd:O" if x["fwd_success"] else "fwd:X")
                flags.append("rev:O" if x["rev_success"] else "rev:X")
                flags.append("sem:O" if x["semantic_pass"] else "sem:X")
                flags.append("fp:O" if x["fixed_point"] else "fp:X")
                moss_s = f"MOSS={x['moss_seed']}%" if x["moss_seed"] is not None else "MOSS=N/A"
                resid_s = f"resid={x['residual']:.4f}" if x["residual"] is not None else "resid=N/A"
                print(f"    {x['problem_id']:12s} iter={x['iterations']:2d} {' '.join(flags):30s} {moss_s:12s} {resid_s:16s} [{x['final_status']}]")


if __name__ == "__main__":
    ollama_pairs = classify(ollama_summary["results"], "qwen2.5")
    openai_pairs = classify(openai_summary["results"], "gpt-5.4")

    print_table2(ollama_pairs, openai_pairs)
    print_table3(ollama_pairs, openai_pairs)
    print_table4(ollama_pairs, openai_pairs)
    print_detail(ollama_pairs, openai_pairs)
