import pytest

from rttdist.metrics import (
    COMPLEXITY_UNAVAILABLE_REASON,
    ZERO_TOKEN_DENOMINATOR_REASON,
    build_complexity_delta_unavailable,
    build_residual_similarity,
)


def test_residual_similarity_identical_cpp_sources() -> None:
    metric = build_residual_similarity("int main(){return 0;}", "int main(){return 0;}\n")

    assert metric["available"] is True
    assert metric["status"] == "measured"
    assert metric["metric"] == "sorensen_dice_token_multiset"
    assert metric["value"] == 1.0


def test_residual_similarity_partial_token_overlap() -> None:
    metric = build_residual_similarity("int main(){return 0;}", "int main(){return 1;}")

    assert metric["available"] is True
    assert metric["status"] == "measured"
    assert metric["value"] == pytest.approx(16 / 18)


def test_residual_similarity_empty_or_whitespace_input_unavailable() -> None:
    metric = build_residual_similarity("", "int main(){return 0;}")

    assert metric["available"] is False
    assert metric["status"] == "unavailable"
    assert metric["reason"] == "empty_or_whitespace_source"


def test_residual_similarity_both_zero_token_multisets_unavailable() -> None:
    metric = build_residual_similarity("/* reference comment */", "// candidate comment")

    assert metric["available"] is False
    assert metric["status"] == "unavailable"
    assert metric["reason"] == ZERO_TOKEN_DENOMINATOR_REASON


def test_residual_similarity_one_zero_token_multiset_is_measured_zero() -> None:
    metric = build_residual_similarity("/* reference comment */", "int main(){return 0;}")

    assert metric["available"] is True
    assert metric["status"] == "measured"
    assert metric["value"] == 0.0


def test_complexity_delta_default_unavailable_shape() -> None:
    metric = build_complexity_delta_unavailable()

    assert metric["available"] is False
    assert metric["status"] == "unavailable"
    assert metric["reason"] == COMPLEXITY_UNAVAILABLE_REASON
    assert metric["tool"] == "lizard"
    assert set(metric["metrics"]) == {
        "loc",
        "token_count",
        "cyclomatic",
        "function_count",
        "max_nesting",
    }
    for submetric in metric["metrics"].values():
        assert submetric == {
            "available": False,
            "status": "unavailable",
            "reason": COMPLEXITY_UNAVAILABLE_REASON,
        }
