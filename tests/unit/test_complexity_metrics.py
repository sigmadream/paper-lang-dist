from __future__ import annotations

import pytest

from rttdist.metrics import (
    MetricExtractionError,
    V1_METRIC_NAMES,
    extract_metric_value,
    extract_v1_metrics,
)

LANGUAGE_SAMPLES = {
    "c": "int f(int* a, int n){\n    for(int i=0;i<n;i++){\n        if(a[i]>0){\n            foo(a[i]);\n        }\n        else {\n            return 0;\n        }\n    }\n    return a[0];\n}\n",
    "cpp": "int f(int* a, int n){\n    for(int i=0;i<n;i++){\n        if(a[i]>0){\n            foo(a[i]);\n        }\n        else {\n            return 0;\n        }\n    }\n    return a[0];\n}\n",
    "java": "class Main {\n    static int f(int[] a) {\n        for (int i = 0; i < a.length; i++) {\n            if (a[i] > 0) {\n                foo(a[i]);\n            } else {\n                return 0;\n            }\n        }\n        return a[0];\n    }\n}\n",
    "python": "def f(a):\n    for i in range(len(a)):\n        if a[i] > 0:\n            foo(a[i])\n        else:\n            return 0\n    return a[0]\n",
}

EXPECTED_METRICS = {
    "c": {
        "loc": 11,
        "token_count": 59,
        "cyclomatic_complexity": 3,
        "function_count": 1,
        "max_nesting_depth": 2,
    },
    "cpp": {
        "loc": 11,
        "token_count": 59,
        "cyclomatic_complexity": 3,
        "function_count": 1,
        "max_nesting_depth": 2,
    },
    "java": {
        "loc": 12,
        "token_count": 64,
        "cyclomatic_complexity": 3,
        "function_count": 1,
        "max_nesting_depth": 2,
    },
    "python": {
        "loc": 7,
        "token_count": 41,
        "cyclomatic_complexity": 3,
        "function_count": 1,
        "max_nesting_depth": 2,
    },
}


@pytest.mark.parametrize("language", ["c", "cpp", "java", "python"])
def test_supported_languages_return_full_v1_metric_set(language: str) -> None:
    snapshot = extract_v1_metrics(language, LANGUAGE_SAMPLES[language])

    assert snapshot.language == language
    assert tuple(snapshot.metrics) == V1_METRIC_NAMES
    assert snapshot.metrics == EXPECTED_METRICS[language]
    assert snapshot.to_dict() == {
        "language": language,
        "metric_set": "v1",
        "metrics": EXPECTED_METRICS[language],
    }


def test_java_boilerplate_and_python_brevity_stay_visible_in_separate_metrics() -> None:
    cpp_metrics = extract_v1_metrics("cpp", LANGUAGE_SAMPLES["cpp"])
    java_metrics = extract_v1_metrics("java", LANGUAGE_SAMPLES["java"])
    python_metrics = extract_v1_metrics("python", LANGUAGE_SAMPLES["python"])

    assert java_metrics.loc > cpp_metrics.loc
    assert java_metrics.token_count > cpp_metrics.token_count
    assert python_metrics.loc < cpp_metrics.loc
    assert python_metrics.token_count < cpp_metrics.token_count
    assert java_metrics.cyclomatic_complexity == cpp_metrics.cyclomatic_complexity
    assert python_metrics.max_nesting_depth == cpp_metrics.max_nesting_depth


def test_unsupported_language_request_fails_deterministically() -> None:
    with pytest.raises(MetricExtractionError) as exc_info:
        extract_v1_metrics("ruby", "def f(x)\n  x\nend\n")

    assert (
        str(exc_info.value)
        == "Unsupported metric language `ruby`. Supported: c, cpp, java, python."
    )


def test_unsupported_metric_request_fails_deterministically() -> None:
    with pytest.raises(MetricExtractionError) as exc_info:
        extract_metric_value("cpp", LANGUAGE_SAMPLES["cpp"], "halstead_volume")

    assert str(exc_info.value) == (
        "Unsupported metric `halstead_volume`. Supported metrics: "
        "loc, token_count, cyclomatic_complexity, function_count, max_nesting_depth."
    )
