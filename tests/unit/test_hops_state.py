import importlib.util

import pytest


def state():
    assert importlib.util.find_spec("rttdist.hops_state"), "홉 상태 전이가 필요합니다."
    from rttdist.hops_state import HopsState

    return HopsState("A", [0.8, 0.85, 0.9], 0.85, 10, 1)


def step(s, n, score=0.86, status="success", source=None):
    return s.record_step(
        "python" if n % 2 else "cpp",
        source or f"source-{n}",
        status,
        {"sym_adj": score, "sym_origin": 0.4} if not n % 2 else None,
        "measured" if not n % 2 else None,
    )


def test_equal_unique_states_do_not_imply_equal_reached_hops():
    early, late = state(), state()
    step(early, 1, source="B")
    step(early, 2, source="C")
    for n in range(1, 5):
        step(late, n, score=0.1 if n == 2 else 0.86, source="B" if n % 2 else "C")
    assert early.outcomes()["0.85"]["unique_state_count_at_reach"] == 3
    assert late.outcomes()["0.85"]["unique_state_count_at_reach"] == 3
    assert early.outcomes()["0.85"]["reached_step"] == 2
    assert late.outcomes()["0.85"]["reached_step"] == 4


def test_tenth_hop_with_eleven_states_can_succeed():
    s = state()
    for n in range(1, 11):
        step(s, n, score=0.95 if n == 10 else 0.1)
    assert s.outcomes()["0.90"]["reached_step"] == 10
    assert s.outcomes()["0.90"]["unique_state_count_at_reach"] == 11
    assert s.next_step_kind() == "confirmation"
    step(s, 11)
    step(s, 12)
    assert s.confirmation_status == "passed"
    assert s.next_step_kind() == "stop"


def test_all_thresholds_reached_early_still_requires_next_roundtrip():
    s = state()
    step(s, 1)
    step(s, 2, score=0.95)
    assert s.next_step_kind() == "discovery"
    step(s, 3)
    step(s, 4, score=0.95)
    assert s.confirmation_status == "passed"
    assert s.next_step_kind() == "stop"


def test_later_functional_failure_preserves_primary_and_changes_unreached_only():
    s = state()
    step(s, 1)
    step(s, 2)
    original = s.outcomes()["0.85"]
    step(s, 3, status="wrong_answer")
    assert s.outcomes()["0.85"] == original
    assert s.outcomes()["0.90"]["category"] == "functional_failure"
    assert s.confirmation_status == "failed"


@pytest.mark.parametrize(
    "failure,confirmation",
    [("wrong_answer", "failed"), ("infrastructure_error", "unavailable")],
)
def test_discovery_frozen_before_confirmation_failure(failure, confirmation):
    s = state()
    for n in range(1, 11):
        step(s, n, score=0.86 if n == 10 else 0.1)
    frozen = s.outcomes()
    assert frozen["0.90"]["category"] == "hop_limit"
    step(s, 11, status=failure)
    assert s.outcomes() == frozen
    assert s.confirmation_status == confirmation


def test_twelfth_hop_cannot_add_discovery_success():
    s = state()
    for n in range(1, 13):
        step(s, n, score=0.95 if n == 12 else 0.86 if n == 10 else 0.1)
    assert s.outcomes()["0.90"]["category"] == "hop_limit"
    assert s.outcomes()["0.90"]["reached_step"] is None
    assert s.confirmation_status == "passed"


def test_functional_failure_precedes_similarity_success():
    s = state()
    step(s, 1)
    step(s, 2, score=0.95, status="wrong_answer")
    assert all(o["category"] == "functional_failure" for o in s.outcomes().values())


def test_similarity_unavailable_and_budget_are_invalid_not_failure():
    s = state()
    step(s, 1)
    step(s, 2)
    step(s, 3)
    s.record_step("cpp", "bad-measurement", "success", None, "unavailable")
    assert s.outcomes()["0.85"]["success"]
    assert s.outcomes()["0.90"]["category"] == "invalid"
    assert s.confirmation_status == "unavailable"
    other = state()
    other.abort("observation_wall_clock")
    assert other.outcomes()["0.85"]["category"] == "invalid"


def test_low_confirmation_does_not_erase_success_and_newline_identity():
    s = state()
    step(s, 1, source="B\r\n")
    step(s, 2, score=0.95, source="A")
    step(s, 3, source="B\n")
    step(s, 4, score=0.1, source="A")
    assert s.confirmation_status == "failed"
    assert s.outcomes()["0.85"]["success"]
    assert len(s.states) == 2


def test_final_tenth_comparison_precedes_hop_limit():
    s = state()
    for n in range(1, 11):
        step(s, n, score=0.1)
    assert all(o["category"] == "hop_limit" for o in s.outcomes().values())
    assert s.translation_steps == 10
    assert s.next_step_kind() == "stop"
