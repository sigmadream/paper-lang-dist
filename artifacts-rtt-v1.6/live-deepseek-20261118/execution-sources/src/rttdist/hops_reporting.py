"""v1.6 홉 관측의 통계·감사·보고 기능을 제공합니다."""

from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import hashlib
import json

import numpy as np

CATEGORIES = ("success", "functional_failure", "hop_limit", "invalid", "incomplete")
VALID = set(CATEGORIES[:3])
METRICS = ("P", "H", "D")
EXPECTED_ROUTES = [f"cpp-via-{x}" for x in ("python", "java", "haskell", "prolog")]
SECRET_KEYS = {
    "api_key",
    "authorization",
    "access_token",
    "refresh_token",
    "token",
    "password",
    "secret",
    "client_secret",
    "cookie",
    "x-api-key",
}


def public_data(value):
    """공개 입력과 재현 묶음에서 인증값을 동일하게 제외합니다."""
    if isinstance(value, dict):
        return {
            key: "[비공개]" if key.lower() in SECRET_KEYS else public_data(item)
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [public_data(item) for item in value]
    return value


def _key(value):
    return f"{float(value):.2f}"


def _settings(contract):
    if "config" not in contract:
        return contract
    keys = (
        "problem_ids",
        "routes",
        "repeats",
        "thresholds",
        "primary_threshold",
        "protocol",
        "schema_version",
    )
    return {
        **contract["config"],
        **{key: contract[key] for key in keys if key in contract},
    }


def _routes(contract):
    return [
        r if isinstance(r, str) else f"{r[0]}-via-{r[1]}"
        for r in _settings(contract)["routes"]
    ]


def _outcome(record, threshold):
    outcomes = record.get("outcomes", {})
    return next(
        (o for k, o in outcomes.items() if _key(k) == threshold),
        {"success": False, "category": "incomplete"},
    )


def _slot(record):
    return (
        record["problem_id"],
        record["route"],
        record.get("attempt", record.get("repeat")),
    )


def _hash(value):
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode()
    ).hexdigest()


def _ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def _distribution(values):
    values = [float(v) for v in values if v is not None]
    if not values:
        return {
            "n": 0,
            "mean": None,
            "median": None,
            "q1": None,
            "q3": None,
            "values": [],
        }
    return {
        "n": len(values),
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "q1": float(np.quantile(values, 0.25)),
        "q3": float(np.quantile(values, 0.75)),
        "values": values,
    }


def _metrics(records, threshold):
    outcomes = [_outcome(r, threshold) for r in records]
    valid = [o for o in outcomes if o["category"] in VALID]
    hits = [o for o in valid if o.get("success")]
    p = _ratio(len(hits), len(valid))
    h = _ratio(sum(o["reached_step"] for o in hits), len(hits))
    return {"P": p, "H": h, "D": h / p if h is not None and p else None}


def _stage_rates(records):
    grouped = defaultdict(list)
    for record in records:
        previous = record.get("seed_language", record["route"].split("-via-")[0])
        for step in record.get("steps", []):
            language = step.get("language", "unknown")
            phase = step.get("kind", step.get("phase", "discovery"))
            phase = "discovery" if phase == "search" else phase
            status = step.get(
                "evaluation_status", (step.get("evaluation") or {}).get("status")
            )
            functional = step.get("functional")
            assessed_statuses = {
                "success",
                "wrong_answer",
                "runtime_error",
                "timeout",
                "compile_error",
                "compile_timeout",
                "compilation_error",
                "format_error",
            }
            passed = (
                (status == "success" if status in assessed_statuses else None)
                if status is not None
                else functional
            )
            grouped[(phase, step["step"], f"{previous}->{language}")].append(
                (record, passed)
            )
            previous = language
    result = []
    for (phase, step, direction), rows in sorted(
        grouped.items(), key=lambda x: (x[0][1], x[0][0], x[0][2])
    ):
        assessed = [p for _, p in rows if p is not None]
        result.append(
            {
                "phase": phase,
                "step": step,
                "direction": direction,
                "attempts": len(rows),
                "assessable": len(assessed),
                "unavailable": len(rows) - len(assessed),
                "passed": sum(assessed),
                "pass_rate": _ratio(sum(assessed), len(assessed)),
            }
        )
    return result


def _call_accounting(records):
    result = {}
    for kind in ("discovery", "confirmation"):
        steps = [
            s
            for r in records
            for s in r.get("steps", [])
            if s.get("kind", s.get("phase", "discovery")).replace("search", "discovery")
            == kind
        ]
        attempts = [
            (
                len(s["transport_attempts"])
                if isinstance(s.get("transport_attempts"), list)
                else s.get("transport_attempts")
            )
            for s in steps
        ]
        known = [value for value in attempts if value is not None]
        costs = [s.get("cost_usd") for s in steps]
        result[kind] = {
            "logical_requests": len(steps),
            "transport_attempts": sum(known) if len(known) == len(steps) else None,
            "known_transport_attempts": sum(known),
            "transport_unknown_requests": len(steps) - len(known),
            "retries": (
                sum(max(0, value - 1) for value in known)
                if len(known) == len(steps)
                else None
            ),
            "cost_usd": sum(costs) if all(v is not None for v in costs) else None,
            "known_cost_usd": sum(v for v in costs if v is not None),
            "scope": "관측 단계에 보존된 요청의 집계입니다. 단계 생성 전 실패한 통신과 전체 과금량은 공급자 원장을 별도로 대조해야 합니다.",
        }
    return result


def _route_summary(records, ids, planned, threshold):
    outcomes = [_outcome(r, threshold) for r in records]
    categories = Counter(o["category"] for o in outcomes)
    categories["incomplete"] += max(0, planned - len(records))
    hits = [
        (r, o)
        for r, o in zip(records, outcomes)
        if o.get("success") and o["category"] == "success"
    ]
    counts = {k: categories[k] for k in CATEGORIES}
    per_problem = {
        p: {
            **_metrics([r for r in records if r["problem_id"] == p], threshold),
            "valid": sum(
                _outcome(r, threshold)["category"] in VALID
                for r in records
                if r["problem_id"] == p
            ),
            "success": sum(
                _outcome(r, threshold).get("success", False)
                for r in records
                if r["problem_id"] == p
            ),
        }
        for p in ids
    }
    problem_ps = [s["P"] for s in per_problem.values() if s["P"] is not None]
    confirmation = Counter(
        (
            r.get("confirmation_status")
            if r.get("confirmation_status") in ("passed", "failed")
            else "unavailable"
        )
        for r, _ in hits
    )
    assessable = confirmation["passed"] + confirmation["failed"]
    first = [
        s.get("sym_adj") for r in records for s in r.get("steps", []) if s["step"] == 2
    ]
    all_sim = [s.get("sym_adj") for r in records for s in r.get("steps", [])]
    reasons = Counter(
        o.get("reason") or o["category"]
        for o in outcomes
        if o["category"] not in ("success", "incomplete")
    )
    return {
        **_metrics(records, threshold),
        "planned": planned,
        "recorded": len(records),
        "valid": sum(categories[k] for k in VALID),
        "success": len(hits),
        "invalid": counts["invalid"],
        "incomplete": counts["incomplete"],
        "categories": counts,
        "missing_reason": "no_success" if not hits else None,
        "P_problem_mean": float(np.mean(problem_ps)) if problem_ps else None,
        "per_problem": per_problem,
        "confirmation": (
            {
                "primary_successes": len(hits),
                "passed": confirmation["passed"],
                "failed": confirmation["failed"],
                "unavailable": confirmation["unavailable"],
                "assessable": assessable,
                "retention_rate": _ratio(confirmation["passed"], assessable),
                "unavailable_rate": _ratio(confirmation["unavailable"], len(hits)),
            }
            if threshold == "0.85"
            else None
        ),
        "failure_reasons": dict(sorted(reasons.items())),
        "stage_pass_rates": _stage_rates(records),
        "call_accounting": _call_accounting(records),
        "similarities": {
            "first_restoration": _distribution(first),
            "adjacent_at_reach": _distribution([o.get("sym_adj") for _, o in hits]),
            "origin_at_reach": _distribution([o.get("sym_origin") for _, o in hits]),
            "all_steps": _distribution(all_sim),
            "all_steps_scope": "전체 단계 관측값이며 오래 진행한 시도에 더 큰 가중치가 부여됩니다.",
            "origin_scope": "해당 임계치 성공 시도마다 도달 시점 원본 대비 값 1개입니다.",
        },
        "unique_states_at_reach": _distribution(
            [o.get("unique_state_count_at_reach") for _, o in hits]
        ),
        "translation_steps_total": sum(r.get("translation_steps", 0) for r in records),
    }


def audit_campaign(records, contract):
    """계획 슬롯·임계치별 유효성과 집계에 필요한 구조를 검사합니다."""
    cfg = _settings(contract)
    thresholds = [_key(t) for t in cfg.get("thresholds", [0.8, 0.85, 0.9])]
    ids, routes, repeats = cfg["problem_ids"], _routes(contract), cfg["repeats"]
    expected = {(p, r, a) for p in ids for r in routes for a in range(1, repeats + 1)}
    actual = [_slot(r) for r in records]
    errors = []
    for field in ("profile_id", "campaign_id", "phase", "provider", "model"):
        values = {r[field] for r in records if r.get(field) is not None}
        if len(values) > 1:
            errors.append(
                "서로 다른 실행·모델·프로파일 관측을 합산할 수 없습니다: " + field
            )
    if len(set(actual)) != len(actual):
        errors.append("관측 키가 중복됩니다.")
    if set(actual) - expected:
        errors.append("계획에 없는 관측이 있습니다.")
    version = cfg.get("protocol", cfg.get("experiment_version"))
    if version != "rtt-hops-v1.6":
        errors.append("v1.6 프로토콜이 아닙니다.")
    if _key(cfg.get("primary_threshold", cfg.get("threshold", 0.85))) != "0.85":
        errors.append("v1.6 주 임계치는 0.85여야 합니다.")
    for r in records:
        if (
            r.get("protocol", "rtt-hops-v1.6") != "rtt-hops-v1.6"
            or r.get("schema_version", "observation-v1.6") != "observation-v1.6"
        ):
            errors.append("과거 스키마 관측은 v1.6으로 변환할 수 없습니다.")
        if (
            contract.get("contract_hash")
            and r.get("contract_hash") != contract["contract_hash"]
        ):
            errors.append("관측 계약 해시가 다릅니다.")
        # 실제 스키마 관측에서는 단계 근거까지 검사하며 소규모 합성 입력과 구분합니다.
        strict = r.get("schema_version") == "observation-v1.6"
        steps = r.get("steps", [])
        if strict and (
            r.get("translation_steps") != len(steps)
            or len(steps) > 12
            or [s.get("step") for s in steps] != list(range(1, len(steps) + 1))
        ):
            errors.append("실행 관측의 단계 수 또는 순서가 맞지 않습니다.")
        for key in thresholds:
            outcome = _outcome(r, key)
            if "d_n" in outcome:
                errors.append("기존 FPS 결과는 홉 관측으로 자동 변환하지 않습니다.")
            category = outcome.get("category")
            if category not in CATEGORIES or bool(outcome.get("success")) != (
                category == "success"
            ):
                errors.append(f"{_slot(r)} {key}: 성공·분류가 일치하지 않습니다.")
            reached = outcome.get("reached_step")
            if category == "success" and reached not in (2, 4, 6, 8, 10):
                errors.append(f"{_slot(r)} {key}: 성공 홉이 허용 범위 밖입니다.")
            if strict and category == "success" and reached in (2, 4, 6, 8, 10):
                if reached > len(steps) or any(
                    s.get("evaluation_status") != "success" for s in steps[:reached]
                ):
                    errors.append("도달 이전 단계의 기능 통과 근거가 부족합니다.")
                elif steps[reached - 1].get("sym_adj") is None or steps[reached - 1][
                    "sym_adj"
                ] < float(key):
                    errors.append("도달 단계의 인접 유사도 근거가 부족합니다.")
                if any(
                    s.get("step", 1) % 2 == 0
                    and s.get("sym_adj") is not None
                    and s["sym_adj"] >= float(key)
                    for s in steps[: reached - 1]
                ):
                    errors.append("reached_step이 최초 도달 단계와 다릅니다.")
            if category != "success" and reached is not None:
                errors.append(f"{_slot(r)} {key}: 미성공 결과에 성공 홉이 있습니다.")
    complete = {
        k: not errors
        and set(actual) == expected
        and all(_outcome(r, k)["category"] in VALID for r in records)
        for k in thresholds
    }
    return {
        "passed": not errors,
        "errors": errors,
        "expected": len(expected),
        "observation_count": len(records),
        "missing_slots": [list(s) for s in sorted(expected - set(actual))],
        "collection_finished": set(actual) == expected
        and all(
            _outcome(r, k)["category"] != "incomplete"
            for r in records
            for k in thresholds
        ),
        "complete_by_threshold": complete,
        "scope": "계획 슬롯과 관측 구조의 감사이며 실행 출력·JPlag 원본 감사와 구분합니다.",
    }


def _interval(values, alpha):
    missing = float(np.mean(~np.isfinite(values)))
    if missing:
        return {
            "interval": None,
            "missing_fraction": missing,
            "interval_reason": "undefined_bootstrap_samples",
        }
    return {
        "interval": [float(v) for v in np.quantile(values, [alpha / 2, 1 - alpha / 2])],
        "missing_fraction": 0.0,
        "interval_reason": None,
    }


def _bootstrap(records, problem_ids, pairs, replicates, seed, threshold, corrected):
    if replicates < 1 or not problem_ids or len(set(problem_ids)) != len(problem_ids):
        raise ValueError(
            "재표집 횟수는 양수이며 문제 ID 목록은 비어 있지 않고 중복이 없어야 합니다."
        )
    routes = list(dict.fromkeys(r for pair in pairs for r in pair))
    if not routes:
        routes = sorted({r["route"] for r in records})
    draws = np.random.default_rng(seed).integers(
        0, len(problem_ids), size=(replicates, len(problem_ids))
    )
    samples, estimates = {}, {}
    alpha = 0.05 / 18 if corrected else 0.05
    for route in routes:
        block = []
        rr = [
            r for r in records if r["route"] == route and r["problem_id"] in problem_ids
        ]
        for problem in problem_ids:
            outcomes = [
                _outcome(r, threshold) for r in rr if r["problem_id"] == problem
            ]
            successes = [o for o in outcomes if o["category"] == "success"]
            block.append(
                [
                    sum(o["category"] in VALID for o in outcomes),
                    len(successes),
                    sum(o["reached_step"] for o in successes),
                ]
            )
        totals = np.asarray(block, dtype=float)[draws].sum(axis=1)
        with np.errstate(divide="ignore", invalid="ignore"):
            p = totals[:, 1] / totals[:, 0]
            h = totals[:, 2] / totals[:, 1]
            samples[route] = {"P": p, "H": h, "D": h / p}
        estimates[route] = _metrics(rr, threshold)
    comparisons = []
    for left, right in pairs:
        for metric in METRICS:
            a, b = estimates[left][metric], estimates[right][metric]
            comparisons.append(
                {
                    "left": left,
                    "right": right,
                    "metric": metric,
                    "difference": a - b if a is not None and b is not None else None,
                    **_interval(samples[left][metric] - samples[right][metric], alpha),
                    "interval_kind": "bonferroni_18" if corrected else "unadjusted_95",
                    "confidence_level": 1 - alpha,
                }
            )
    return {
        "threshold": threshold,
        "replicates": replicates,
        "seed": seed,
        "block_count": len(problem_ids),
        "block_unit": "problem_all_routes_all_repeats",
        "family_size": 18 if corrected else None,
        "comparisons": comparisons,
        "routes": {
            r: {m: _interval(samples[r][m], 0.05) for m in METRICS} for r in routes
        },
        "route_interval_kind": "unadjusted_95_descriptive",
    }


def bootstrap_routes(records, problem_ids, pairs, replicates, seed):
    """주 임계치의 동일 문제 블록으로 18개 대응 비교를 재표집합니다."""
    return _bootstrap(records, problem_ids, pairs, replicates, seed, "0.85", True)


def summarize_recursive_groups(records, manifest):
    problems = manifest.get("problems", []) if isinstance(manifest, dict) else manifest
    groups = {}
    for name, recursive in (("recursive", True), ("comparison", False)):
        ids = [
            p["problem_id"]
            for p in problems
            if bool(p.get("recursive", p.get("is_recursive", False))) == recursive
        ]
        subset = [r for r in records if r["problem_id"] in ids]
        routes = sorted({r["route"] for r in subset})
        summaries = {
            r: _route_summary(
                [x for x in subset if x["route"] == r],
                ids,
                sum(x["route"] == r for x in subset),
                "0.85",
            )
            for r in routes
        }
        haskell = next((r for r in routes if r.endswith("-via-haskell")), None)
        differences = []
        if haskell:
            for route in routes:
                if route != haskell:
                    differences.append(
                        {
                            "control": route,
                            **{
                                m: (
                                    summaries[haskell][m] - summaries[route][m]
                                    if summaries[haskell][m] is not None
                                    and summaries[route][m] is not None
                                    else None
                                )
                                for m in METRICS
                            },
                        }
                    )
        groups[name] = {
            "problem_ids": ids,
            "problem_count": len(ids),
            "routes": summaries,
            "haskell_minus_controls": differences,
        }
    return {
        "descriptive_only": True,
        "interpretation": "재귀 구현군 3문제와 비교군 12문제의 탐색적 기술통계입니다. 언어 패러다임의 인과 효과나 우월성을 확정하지 않습니다.",
        "groups": groups,
    }


def _ranking(routes, bootstrap, eligible):
    observed = sorted(
        (r for r in routes if routes[r]["D"] is not None), key=lambda r: routes[r]["D"]
    )
    uncertain, supported = [], []
    for left, right in zip(EXPECTED_ROUTES, EXPECTED_ROUTES[1:]):
        item = next(
            (
                c
                for c in (bootstrap or {}).get("comparisons", [])
                if {c["left"], c["right"]} == {left, right} and c["metric"] == "D"
            ),
            None,
        )
        interval = item["interval"] if item else None
        if interval is not None and item["left"] != left:
            interval = [-interval[1], -interval[0]]
        good = (
            eligible and item is not None and interval is not None and interval[1] < 0
        )
        (supported if good else uncertain).append([left, right])
    return {
        "observed_D_ascending": observed,
        "expected_order": EXPECTED_ROUTES,
        "full_order_supported": bool(eligible and not uncertain),
        "supported_adjacent_pairs": supported,
        "uncertain_adjacent_pairs": uncertain,
        "scope": "해당 모델·제공자·프로파일 실행에 한정합니다.",
    }


def summarize_hops(records, manifest, contract):
    """반올림 없이 단일 실행의 통계와 모든 보고 입력을 생성합니다."""
    records = sorted(public_data(records), key=_slot)
    manifest, contract = public_data(manifest), public_data(contract)
    audit = audit_campaign(records, contract)
    if not audit["passed"]:
        raise ValueError("; ".join(audit["errors"]))
    cfg = _settings(contract)
    ids, routes = cfg["problem_ids"], _routes(contract)
    primary = _key(cfg.get("primary_threshold", cfg.get("threshold", 0.85)))
    analysis = cfg.get("analysis") or {}
    replicates = analysis.get("bootstrap_replicates", 10000)
    seed = analysis.get("bootstrap_seed", cfg.get("schedule_seed", 20261117))
    pairs = list(combinations(routes, 2))
    exploratory = cfg.get(
        "comparison_class", contract.get("comparison_class")
    ) == "sdk_exploratory" or any(
        r.get("comparison_class") == "sdk_exploratory" for r in records
    )
    fixed = (
        len(ids) == 15
        and len(routes) == 4
        and set(routes) == set(EXPECTED_ROUTES)
        and cfg["repeats"] == 5
    )
    by_threshold = {}
    for key, complete in audit["complete_by_threshold"].items():
        summaries = {
            route: _route_summary(
                [r for r in records if r["route"] == route],
                ids,
                len(ids) * cfg["repeats"],
                key,
            )
            for route in routes
        }
        eligible = (
            key == primary
            and complete
            and fixed
            and not exploratory
            and replicates == 10000
        )
        boot = (
            _bootstrap(records, ids, pairs, replicates, seed, key, eligible)
            if records
            else None
        )
        by_threshold[key] = {
            "routes": summaries,
            "complete": complete,
            "confirmatory_eligible": eligible,
            "bootstrap": boot,
            "interval_use": (
                "confirmatory_18_comparisons" if eligible else "descriptive_unadjusted"
            ),
            "ranking": _ranking(summaries, boot, eligible),
        }
    annotations = []
    for r in records:
        if r["route"].endswith("-via-haskell"):
            for s in r.get("steps", []):
                if s.get("language") == "haskell":
                    annotations.append(
                        {
                            "problem_id": r["problem_id"],
                            "route": r["route"],
                            "attempt": _slot(r)[2],
                            "step": s["step"],
                            "source_sha256": s.get("source_sha256"),
                            "source_path": s.get("source_path"),
                            "evidence_location": None,
                            "recursive": "unconfirmed",
                            "accumulator": "unconfirmed",
                            "list_processing": "unconfirmed",
                            "explicit_state": "unconfirmed",
                            "automatic_result": "unconfirmed",
                            "review_result": "unreviewed",
                        }
                    )
    selected = by_threshold[primary]
    summary = {
        "schema_version": "summary-v1.6",
        "protocol": "rtt-hops-v1.6",
        "primary_threshold": primary,
        "routes": selected["routes"],
        "by_threshold": by_threshold,
        "complete_by_threshold": audit["complete_by_threshold"],
        "confirmatory_eligible": selected["confirmatory_eligible"],
        "comparison_class": "sdk_exploratory" if exploratory else "direct_api",
        "ranking": selected["ranking"],
        "audit": audit,
        "recursive_groups": summarize_recursive_groups(records, manifest),
        "code_annotations": annotations,
        "contract": contract,
        "manifest": manifest,
        "observations": records,
        "data_hashes": {
            "records": _hash(records),
            "manifest": _hash(manifest),
            "contract": _hash(contract),
        },
        "reporter_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "metadata": {
            "model": cfg.get("llm", {}),
            "campaign_id": cfg.get("campaign_id"),
            "profile_id": cfg.get("profile_id"),
            "actual_models": sorted(
                {
                    s["actual_model"]
                    for r in records
                    for s in r.get("steps", [])
                    if s.get("actual_model")
                }
            ),
            "model_evidence": [
                {
                    "problem_id": r["problem_id"],
                    "route": r["route"],
                    "attempt": _slot(r)[2],
                    "step": s["step"],
                    "actual_model": s.get("actual_model"),
                    "model_evidence": s.get("model_evidence"),
                    "requested_generation": s.get("requested_generation"),
                    "sent_generation": s.get("sent_generation"),
                    "effective_generation": s.get("effective_generation"),
                    "effective_generation_missing_reason": s.get(
                        "effective_generation_missing_reason"
                    ),
                }
                for r in records
                for s in r.get("steps", [])
            ],
        },
        "interpretation": "D는 모델·코퍼스·프롬프트·평가 조건에 의존하는 조작적 지표입니다. 기능 검사 통과는 평가 입력 범위에서의 보존 근거이며 의미 동등성 증명이 아닙니다.",
    }
    return summary
