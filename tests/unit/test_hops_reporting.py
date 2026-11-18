"""승인된 홉 지표·완전성·대응 재표집 계약을 검증합니다."""

from copy import deepcopy
from itertools import combinations

import pytest

from rttdist import hops_reporting as reporting

ROUTES = [f"cpp-via-{language}" for language in ("python", "java", "haskell", "prolog")]


def record(problem="p1", route=ROUTES[0], attempt=1, reached=2, category="success"):
    outcome = {
        "success": category == "success",
        "category": category,
        "reached_step": reached if category == "success" else None,
        "unique_state_count_at_reach": 11,
        "sym_adj": 0.95,
        "sym_origin": 0.7,
    }
    return {
        "problem_id": problem,
        "route": route,
        "attempt": attempt,
        "outcomes": {key: deepcopy(outcome) for key in ("0.80", "0.85", "0.90")},
        "confirmation_status": "failed" if category == "success" else None,
        "translation_steps": 12,
        "d_n": 999,
        "steps": [],
    }


def contract(ids=None, repeats=3, routes=None):
    return {
        "protocol": "rtt-hops-v1.6",
        "schema_version": "observation-v1.6",
        "problem_ids": ids or ["p1"],
        "routes": routes or ROUTES[:1],
        "repeats": repeats,
        "thresholds": [0.8, 0.85, 0.9],
        "threshold": 0.85,
        "analysis": {"bootstrap_replicates": 10000, "bootstrap_seed": 20261117},
    }


def summarize(records, cfg=None, manifest=None):
    return reporting.summarize_hops(
        records, manifest or {"problems": []}, cfg or contract()
    )


def test_hops_use_reached_step_not_states_or_calls():
    result = summarize(
        [
            record(reached=2),
            record(attempt=2, reached=4),
            record(attempt=3, category="hop_limit"),
        ]
    )
    route = result["routes"][ROUTES[0]]
    assert route["P"] == pytest.approx(2 / 3)
    assert route["H"] == 3
    assert route["D"] == 4.5
    assert route["planned"] == route["valid"] == 3
    assert route["confirmation"]["failed"] == 2
    assert route["confirmation"]["assessable"] == 2
    assert route["confirmation"]["retention_rate"] == 0
    assert route["categories"]["functional_failure"] == 0


def test_threshold_completeness_and_missing_slots_are_separate():
    rows = [record(attempt=i) for i in range(1, 4)]
    rows[0]["outcomes"]["0.90"].update(
        success=False, category="invalid", reached_step=None
    )
    result = summarize(rows)
    assert result["complete_by_threshold"] == {
        "0.80": True,
        "0.85": True,
        "0.90": False,
    }
    assert result["by_threshold"]["0.90"]["routes"][ROUTES[0]]["invalid"] == 1
    partial = summarize(rows[:2])
    assert partial["routes"][ROUTES[0]]["incomplete"] == 1
    assert not partial["confirmatory_eligible"]


def test_zero_success_and_zero_denominators_stay_missing():
    result = summarize([record(attempt=i, category="hop_limit") for i in range(1, 4)])
    route = result["routes"][ROUTES[0]]
    assert route["P"] == 0
    assert route["H"] is route["D"] is None
    assert route["missing_reason"] == "no_success"
    assert route["confirmation"]["retention_rate"] is None
    assert route["confirmation"]["unavailable_rate"] is None


def test_pooled_and_equal_problem_weight_rates_are_disclosed():
    rows = [record(), record(attempt=2), record("p2", category="hop_limit")]
    route = summarize(rows, contract(["p1", "p2"], repeats=2))["routes"][ROUTES[0]]
    assert route["P"] == pytest.approx(2 / 3)
    assert route["P_problem_mean"] == 0.5


def test_paired_problem_blocks_and_all_eighteen_comparisons():
    ids = [f"p{i}" for i in range(15)]
    rows = [
        record(p, r, a, 2 + 2 * j + 2 * (i % 2))
        for i, p in enumerate(ids)
        for j, r in enumerate(ROUTES)
        for a in range(1, 6)
    ]
    boot = reporting.bootstrap_routes(
        rows, ids, list(combinations(ROUTES, 2)), 10000, 20261117
    )
    assert boot["block_count"] == 15
    assert boot["replicates"] == 10000
    assert boot["family_size"] == 18
    assert len(boot["comparisons"]) == 18
    assert boot["comparisons"][0]["interval_kind"] == "bonferroni_18"
    d = next(x for x in boot["comparisons"] if x["metric"] == "D")
    assert d["difference"] == pytest.approx(-2)
    assert d["interval"] == pytest.approx([-2, -2])
    result = summarize(rows, contract(ids, 5, ROUTES))
    assert result["confirmatory_eligible"]
    assert result["ranking"]["full_order_supported"]
    assert (
        result["by_threshold"]["0.80"]["bootstrap"]["comparisons"][0]["interval_kind"]
        == "unadjusted_95"
    )
    rows[0]["comparison_class"] = "sdk_exploratory"
    assert not summarize(rows, contract(ids, 5, ROUTES))["confirmatory_eligible"]


def test_undefined_bootstrap_samples_are_not_silently_dropped():
    rows = [
        record("a"),
        record("b", category="hop_limit"),
        record("a", ROUTES[1]),
        record("b", ROUTES[1]),
    ]
    boot = reporting.bootstrap_routes(rows, ["a", "b"], [ROUTES[:2]], 10000, 7)
    for item in boot["comparisons"]:
        if item["metric"] in ("H", "D"):
            assert 0 < item["missing_fraction"] < 1
            assert item["interval"] is None
            assert item["interval_reason"] == "undefined_bootstrap_samples"
        else:
            assert item["interval"] is not None


def test_direction_phase_and_similarity_denominators():
    row = record()
    row["steps"] = [
        {
            "step": 1,
            "kind": "discovery",
            "language": "python",
            "evaluation_status": "success",
        },
        {
            "step": 2,
            "kind": "discovery",
            "language": "cpp",
            "evaluation_status": "success",
            "sym_adj": 0.95,
        },
        {
            "step": 3,
            "kind": "confirmation",
            "language": "python",
            "evaluation_status": "wrong_answer",
        },
    ]
    route = summarize([row])["routes"][ROUTES[0]]
    assert route["similarities"]["first_restoration"]["n"] == 1
    assert route["similarities"]["origin_at_reach"]["n"] == 1
    assert route["stage_pass_rates"][-1]["passed"] == 0
    assert route["stage_pass_rates"][-1]["phase"] == "confirmation"
    assert route["categories"]["success"] == 1


def test_duplicate_or_invalid_success_hops_block_audit():
    assert not reporting.audit_campaign([record(), record()], contract())["passed"]
    bad = record(reached=12)
    assert not reporting.audit_campaign([bad], contract())["passed"]


def test_recursive_groups_are_descriptive_with_haskell_controls():
    manifest = {
        "problems": [
            {"problem_id": "p1", "recursive": True},
            {"problem_id": "p2", "recursive": False},
        ]
    }
    rows = [record(p, r) for p in ("p1", "p2") for r in ROUTES]
    result = reporting.summarize_recursive_groups(rows, manifest)
    assert result["descriptive_only"]
    assert result["groups"]["recursive"]["problem_count"] == 1
    assert len(result["groups"]["recursive"]["haskell_minus_controls"]) == 3


def test_malformed_flags_and_mixed_profiles_cannot_be_pooled():
    rows = [record(), record(attempt=2)]
    rows[0]["profile_id"] = "a"
    rows[1]["profile_id"] = "b"
    with pytest.raises(ValueError, match="프로파일"):
        summarize(rows)


def test_confirmation_unavailable_and_origin_are_success_conditioned():
    rows = [
        record(),
        record(attempt=2),
        record(attempt=3, category="functional_failure"),
    ]
    rows[0]["confirmation_status"] = "passed"
    rows[1]["confirmation_status"] = "unavailable"
    result = summarize(rows)["routes"][ROUTES[0]]
    assert result["confirmation"]["retention_rate"] == 1
    assert result["confirmation"]["unavailable_rate"] == 0.5
    assert result["similarities"]["origin_at_reach"]["n"] == 2


def test_core_observation_evidence_is_checked_when_present():
    row = record()
    row.update(schema_version="observation-v1.6", protocol="rtt-hops-v1.6")
    row["translation_steps"] = 2
    row["steps"] = [
        {"step": 1, "evaluation_status": "wrong_answer"},
        {"step": 2, "evaluation_status": "success", "sym_adj": 0.95},
    ]
    assert not reporting.audit_campaign([row], contract())["passed"]


def test_top_level_pilot_scope_overrides_frozen_main_config():
    cfg = contract(["p1", "p2"], 5)
    frozen = {
        "protocol": "rtt-hops-v1.6",
        "config": cfg,
        "problem_ids": ["p1"],
        "repeats": 1,
    }
    result = summarize([record()], frozen)
    assert result["routes"][ROUTES[0]]["planned"] == 1
    assert result["complete_by_threshold"]["0.85"]


def test_infrastructure_stage_is_unavailable_and_calls_are_not_hops():
    row = record()
    row["steps"] = [
        {
            "step": 1,
            "kind": "discovery",
            "language": "python",
            "evaluation_status": "infrastructure_error",
            "transport_attempts": 3,
        }
    ]
    route = summarize([row])["routes"][ROUTES[0]]
    assert route["stage_pass_rates"][0]["assessable"] == 0
    assert route["stage_pass_rates"][0]["unavailable"] == 1
    assert route["stage_pass_rates"][0]["attempts"] == 1
    assert route["stage_pass_rates"][0]["passed"] == 0
    assert route["stage_pass_rates"][0]["pass_rate"] is None
    assert route["call_accounting"]["discovery"]["logical_requests"] == 1
    assert route["call_accounting"]["discovery"]["transport_attempts"] == 3
    assert route["call_accounting"]["discovery"]["retries"] == 2
    assert route["H"] == 2


@pytest.mark.parametrize(
    "status",
    ["compile_timeout", "compile_error", "timeout", "runtime_error", "wrong_answer"],
)
@pytest.mark.parametrize("phase", ["discovery", "confirmation"])
def test_evaluator_functional_failures_count_in_stage_denominator(status, phase):
    rows = reporting._stage_rates(
        [
            {
                "route": ROUTES[0],
                "steps": [
                    {
                        "step": 1,
                        "language": "python",
                        "kind": phase,
                        "evaluation_status": status,
                    }
                ],
            }
        ]
    )
    assert rows == [
        {
            "phase": phase,
            "step": 1,
            "direction": "cpp->python",
            "attempts": 1,
            "assessable": 1,
            "unavailable": 0,
            "passed": 0,
            "pass_rate": 0,
        }
    ]


def test_legacy_fps_outcomes_are_not_implicitly_converted():
    from tests.unit.test_fps_reporting import rec

    old = rec("p1", ROUTES[0], 1, "success", 3)
    with pytest.raises(ValueError, match="FPS"):
        summarize([old])


def test_success_hops_must_match_first_reach_evidence():
    row = record(reached=4)
    row.update(
        schema_version="observation-v1.6", protocol="rtt-hops-v1.6", translation_steps=4
    )
    row["steps"] = [
        {
            "step": step,
            "evaluation_status": "success",
            "sym_adj": 0.95 if step % 2 == 0 else None,
        }
        for step in range(1, 5)
    ]
    assert not reporting.audit_campaign([row], contract())["passed"]


def test_ranking_support_does_not_depend_on_route_input_order():
    ids = [f"p{i}" for i in range(15)]
    rows = [
        record(p, route, attempt, 2 + 2 * index)
        for p in ids
        for index, route in enumerate(ROUTES)
        for attempt in range(1, 6)
    ]
    result = summarize(rows, contract(ids, 5, list(reversed(ROUTES))))
    assert result["ranking"]["full_order_supported"]
