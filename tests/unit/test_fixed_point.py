from __future__ import annotations

from rttdist.fixed_point import (
    classify_cpp_history,
    classify_hash_history,
    compute_residual_similarity,
)
from rttdist.normalize import hash_normalized_cpp_tokens


def test_adjacent_hash_match_classifies_fixed_point() -> None:
    first = "int main(){ return 0; }"
    second = "int main() { // same after normalization\nreturn 0; }"

    status = classify_hash_history(
        [hash_normalized_cpp_tokens(first), hash_normalized_cpp_tokens(second)]
    )

    assert status == "fixed_point"


def test_two_cycle_history_classifies_oscillation() -> None:
    a = "int main(){return 0;}"
    b = "int main(){return 1;}"

    assert classify_cpp_history([a, b, a, b]) == "oscillation"


def test_non_repeating_history_continues() -> None:
    history = [
        hash_normalized_cpp_tokens("int main(){return 0;}"),
        hash_normalized_cpp_tokens("int main(){return 1;}"),
        hash_normalized_cpp_tokens("int main(){return 2;}"),
    ]

    assert classify_hash_history(history) == "continue"


def test_residual_similarity_matches_cpp_token_similarity() -> None:
    seed = "int main(){return 1 + 2;}"
    candidate = "int main(){return 1 + 3;}"

    assert compute_residual_similarity(seed, candidate) == 10 / 11
