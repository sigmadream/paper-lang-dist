from __future__ import annotations

from collections.abc import Sequence

from rttdist.fixed_point import (
    classify_dual_cpp_histories,
    classify_dual_hash_histories,
    classify_cpp_history,
    classify_hash_history,
    classify_overall_convergence,
    compute_residual_similarity,
)
from rttdist.normalize import hash_normalized_cpp_tokens


def _hashes(*sources: str) -> Sequence[str]:
    return [hash_normalized_cpp_tokens(source) for source in sources]


def test_adjacent_hash_match_classifies_fixed_point() -> None:
    first = "int main(){ return 0; }"
    second = "int main() { // same after normalization\nreturn 0; }"

    status = classify_hash_history(_hashes(first, second))

    assert status == "fixed_point"


def test_two_cycle_history_classifies_oscillation() -> None:
    a = "int main(){return 0;}"
    b = "int main(){return 1;}"

    assert classify_cpp_history([a, b, a, b]) == "oscillation"


def test_non_repeating_history_continues() -> None:
    history = _hashes(
        "int main(){return 0;}",
        "int main(){return 1;}",
        "int main(){return 2;}",
    )

    assert classify_hash_history(history) == "continue"


def test_residual_similarity_matches_cpp_token_similarity() -> None:
    seed = "int main(){return 1 + 2;}"
    candidate = "int main(){return 1 + 3;}"

    assert compute_residual_similarity(seed, candidate) == 10 / 11


def test_dual_state_overall_is_fixed_only_when_both_states_are_fixed() -> None:
    dual = classify_dual_cpp_histories(
        seed_source_history=[
            "int main(){return 0;}",
            "int main(){return 0;}",
        ],
        target_source_history=[
            "int solve(){return 1;}",
            "int solve(){return 1;}",
        ],
    )

    assert dual.seed_state == "fixed_point"
    assert dual.target_state == "fixed_point"
    assert dual.overall == "fixed_point"


def test_dual_state_overall_is_oscillation_if_either_state_oscillates() -> None:
    seed_hash_history = _hashes(
        "int main(){return 0;}",
        "int main(){return 1;}",
        "int main(){return 0;}",
        "int main(){return 1;}",
    )
    target_hash_history = _hashes("int solve(){return 7;}", "int solve(){return 7;}")

    dual = classify_dual_hash_histories(
        seed_hash_history=seed_hash_history,
        target_hash_history=target_hash_history,
    )

    assert dual.seed_state == "oscillation"
    assert dual.target_state == "fixed_point"
    assert dual.overall == "oscillation"


def test_dual_state_overall_is_continue_when_not_both_fixed_and_no_oscillation() -> (
    None
):
    assert (
        classify_overall_convergence(seed_state="fixed_point", target_state="continue")
        == "continue"
    )
    assert (
        classify_overall_convergence(seed_state="continue", target_state="continue")
        == "continue"
    )
