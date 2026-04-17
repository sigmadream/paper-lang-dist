from __future__ import annotations

from rttdist.metrics import compute_metric_deltas

SEED_CPP = """int solve(int x) {
    if (x > 0) {
        return x;
    }
    return 0;
}
"""

PREVIOUS_JAVA = """class Main {
    static int solve(int x) {
        if (x > 0) {
            return x;
        }
        return 0;
    }
}
"""

CURRENT_JAVA = """class Main {
    static int helper(int x) {
        if (x > 10) {
            return x - 1;
        }
        return x;
    }

    static int solve(int x) {
        if (x > 0) {
            return helper(x);
        }
        return 0;
    }
}
"""

CURRENT_PYTHON = """def solve(x):
    if x > 0:
        return x
    return 0
"""


def test_metric_deltas_include_seed_cpp_and_previous_iteration_baselines() -> None:
    result = compute_metric_deltas(
        current_language="java",
        current_source=CURRENT_JAVA,
        seed_cpp_source=SEED_CPP,
        previous_source=PREVIOUS_JAVA,
    )

    assert result.current.metrics == {
        "loc": 14,
        "token_count": 55,
        "cyclomatic_complexity": 4,
        "function_count": 2,
        "max_nesting_depth": 1,
    }
    assert result.seed_cpp.metrics == {
        "loc": 6,
        "token_count": 22,
        "cyclomatic_complexity": 2,
        "function_count": 1,
        "max_nesting_depth": 1,
    }
    assert result.previous is not None
    assert result.previous.language == "java"
    assert result.previous.metrics == {
        "loc": 8,
        "token_count": 27,
        "cyclomatic_complexity": 2,
        "function_count": 1,
        "max_nesting_depth": 1,
    }
    assert result.delta_vs_seed_cpp.to_dict() == {
        "loc": 8,
        "token_count": 33,
        "cyclomatic_complexity": 2,
        "function_count": 1,
        "max_nesting_depth": 0,
    }
    assert result.delta_vs_previous is not None
    assert result.delta_vs_previous.to_dict() == {
        "loc": 6,
        "token_count": 28,
        "cyclomatic_complexity": 2,
        "function_count": 1,
        "max_nesting_depth": 0,
    }
    assert result.to_dict() == {
        "metric_set": "v1",
        "current": {
            "language": "java",
            "metric_set": "v1",
            "metrics": {
                "loc": 14,
                "token_count": 55,
                "cyclomatic_complexity": 4,
                "function_count": 2,
                "max_nesting_depth": 1,
            },
        },
        "seed_cpp": {
            "language": "cpp",
            "metric_set": "v1",
            "metrics": {
                "loc": 6,
                "token_count": 22,
                "cyclomatic_complexity": 2,
                "function_count": 1,
                "max_nesting_depth": 1,
            },
        },
        "previous": {
            "language": "java",
            "metric_set": "v1",
            "metrics": {
                "loc": 8,
                "token_count": 27,
                "cyclomatic_complexity": 2,
                "function_count": 1,
                "max_nesting_depth": 1,
            },
        },
        "delta_vs_seed_cpp": {
            "loc": 8,
            "token_count": 33,
            "cyclomatic_complexity": 2,
            "function_count": 1,
            "max_nesting_depth": 0,
        },
        "delta_vs_previous": {
            "loc": 6,
            "token_count": 28,
            "cyclomatic_complexity": 2,
            "function_count": 1,
            "max_nesting_depth": 0,
        },
    }


def test_metric_deltas_allow_seed_only_comparison() -> None:
    result = compute_metric_deltas(
        current_language="python",
        current_source=CURRENT_PYTHON,
        seed_cpp_source=SEED_CPP,
    )

    assert result.current.metrics == {
        "loc": 4,
        "token_count": 15,
        "cyclomatic_complexity": 2,
        "function_count": 1,
        "max_nesting_depth": 1,
    }
    assert result.delta_vs_seed_cpp.to_dict() == {
        "loc": -2,
        "token_count": -7,
        "cyclomatic_complexity": 0,
        "function_count": 0,
        "max_nesting_depth": 0,
    }
    assert result.previous is None
    assert result.delta_vs_previous is None
