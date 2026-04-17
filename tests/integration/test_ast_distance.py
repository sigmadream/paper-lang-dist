from __future__ import annotations

from rttdist.ast_ir import parse_to_ir
from rttdist.ast_metrics import (
    compute_apted_tree_distance,
    compute_roundtrip_ast_distance_metrics,
)


def test_structurally_equivalent_c_and_java_trees_have_zero_distance() -> None:
    c_source = (
        "int f(int* a, int n){ for(int i=0;i<n;i++){ if(a[i]>0){ foo(a[i]); } "
        "else { return 0; } } return a[0]; }"
    )
    java_source = (
        "class Main { static int f(int[] a){ for(int i=0;i<a.length;i++){ "
        "if(a[i]>0){ foo(a[i]); } else { return 0; } } return a[0]; } }"
    )

    c_ir = parse_to_ir("c", c_source)
    java_ir = parse_to_ir("java", java_source)

    assert compute_apted_tree_distance(c_ir, java_ir) == 0


def test_roundtrip_ast_distance_metrics_returns_seed_and_roundtrip_distances() -> None:
    seed_cpp = (
        "int f(int* a, int n){ for(int i=0;i<n;i++){ if(a[i]>0){ foo(a[i]); } "
        "else { return 0; } } return a[0]; }"
    )
    target_python = (
        "def f(a):\n"
        "    for i in range(len(a)):\n"
        "        if a[i] > 0:\n"
        "            foo(a[i])\n"
        "        else:\n"
        "            return 0\n"
        "    return a[0]\n"
    )
    roundtrip_cpp = seed_cpp

    result = compute_roundtrip_ast_distance_metrics(
        seed_cpp_source=seed_cpp,
        target_language="python",
        target_source=target_python,
        roundtrip_cpp_source=roundtrip_cpp,
    )

    assert result.status == "ok"
    assert result.parse_status == {
        "seed_cpp": "ok",
        "target": "ok",
        "roundtrip_cpp": "ok",
    }
    assert result.parser_failures == {}
    assert result.distance_to_seed_cpp == 6
    assert result.distance_to_roundtrip_cpp == 6


def test_parser_failure_is_reported_in_metric_payload_instead_of_raising() -> None:
    seed_cpp = "int main(){ return 0; }"
    roundtrip_cpp = "int main(){ return 0; }"
    invalid_python = "def solve(:\n    return 0\n"

    result = compute_roundtrip_ast_distance_metrics(
        seed_cpp_source=seed_cpp,
        target_language="python",
        target_source=invalid_python,
        roundtrip_cpp_source=roundtrip_cpp,
    )

    assert result.status == "parser_failure"
    assert result.distance_to_seed_cpp is None
    assert result.distance_to_roundtrip_cpp is None
    assert result.parse_status == {
        "seed_cpp": "ok",
        "target": "parser_failure",
        "roundtrip_cpp": "ok",
    }
    assert "target" in result.parser_failures
    assert "Failed to parse `python` source" in result.parser_failures["target"]
