from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Protocol

import lizard

SUPPORTED_METRIC_LANGUAGES: Final[frozenset[str]] = frozenset(
    {"c", "cpp", "java", "python"}
)
V1_METRIC_NAMES: Final[tuple[str, ...]] = (
    "loc",
    "token_count",
    "cyclomatic_complexity",
    "function_count",
    "max_nesting_depth",
)

_LANGUAGE_FILENAMES: Final[dict[str, str]] = {
    "c": "snippet.c",
    "cpp": "snippet.cpp",
    "java": "Main.java",
    "python": "snippet.py",
}


class MetricExtractionError(ValueError):
    pass


@dataclass(frozen=True)
class MetricSnapshot:
    language: str
    loc: int
    token_count: int
    cyclomatic_complexity: int
    function_count: int
    max_nesting_depth: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "language": self.language,
            "metric_set": "v1",
            "metrics": self.metrics,
        }

    @property
    def metrics(self) -> dict[str, int]:
        return {name: int(getattr(self, name)) for name in V1_METRIC_NAMES}

    def metric_value(self, metric_name: str) -> int:
        normalized_metric = _normalize_metric_name(metric_name)
        return self.metrics[normalized_metric]

    def delta_from(self, baseline: MetricSnapshot) -> MetricDelta:
        return MetricDelta(
            **{
                name: self.metric_value(name) - baseline.metric_value(name)
                for name in V1_METRIC_NAMES
            }
        )


@dataclass(frozen=True)
class MetricDelta:
    loc: int
    token_count: int
    cyclomatic_complexity: int
    function_count: int
    max_nesting_depth: int

    def to_dict(self) -> dict[str, int]:
        return {name: int(getattr(self, name)) for name in V1_METRIC_NAMES}


@dataclass(frozen=True)
class MetricDeltaResult:
    current: MetricSnapshot
    seed_cpp: MetricSnapshot
    previous: MetricSnapshot | None
    delta_vs_seed_cpp: MetricDelta
    delta_vs_previous: MetricDelta | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_set": "v1",
            "current": self.current.to_dict(),
            "seed_cpp": self.seed_cpp.to_dict(),
            "previous": None if self.previous is None else self.previous.to_dict(),
            "delta_vs_seed_cpp": self.delta_vs_seed_cpp.to_dict(),
            "delta_vs_previous": None
            if self.delta_vs_previous is None
            else self.delta_vs_previous.to_dict(),
        }


class MetricExtractor(Protocol):
    def extract(self, *, language: str, source: str) -> MetricSnapshot: ...


class LizardMetricExtractor:
    def extract(self, *, language: str, source: str) -> MetricSnapshot:
        normalized_language = _normalize_language(language)
        validated_source = _validate_source(source)
        analyzer = lizard.FileAnalyzer(lizard.get_extensions(["nd"]))
        analysis = analyzer.analyze_source_code(
            _LANGUAGE_FILENAMES[normalized_language],
            validated_source,
        )
        functions = tuple(analysis.function_list)

        return MetricSnapshot(
            language=normalized_language,
            loc=int(analysis.nloc),
            token_count=int(analysis.token_count),
            cyclomatic_complexity=sum(
                int(function.cyclomatic_complexity) for function in functions
            ),
            function_count=len(functions),
            max_nesting_depth=max(
                (int(function.max_nesting_depth) for function in functions),
                default=0,
            ),
        )


DEFAULT_METRIC_EXTRACTOR: Final[MetricExtractor] = LizardMetricExtractor()


def extract_v1_metrics(
    language: str,
    source: str,
    *,
    extractor: MetricExtractor = DEFAULT_METRIC_EXTRACTOR,
) -> MetricSnapshot:
    return extractor.extract(language=language, source=source)


def extract_metric_value(
    language: str,
    source: str,
    metric_name: str,
    *,
    extractor: MetricExtractor = DEFAULT_METRIC_EXTRACTOR,
) -> int:
    snapshot = extract_v1_metrics(language, source, extractor=extractor)
    return snapshot.metric_value(metric_name)


def compute_metric_deltas(
    *,
    current_language: str,
    current_source: str,
    seed_cpp_source: str,
    previous_source: str | None = None,
    previous_language: str | None = None,
    extractor: MetricExtractor = DEFAULT_METRIC_EXTRACTOR,
) -> MetricDeltaResult:
    if previous_source is None and previous_language is not None:
        raise MetricExtractionError(
            "`previous_language` requires `previous_source` to be provided."
        )

    current = extract_v1_metrics(current_language, current_source, extractor=extractor)
    seed_cpp = extract_v1_metrics("cpp", seed_cpp_source, extractor=extractor)

    previous: MetricSnapshot | None = None
    delta_vs_previous: MetricDelta | None = None
    if previous_source is not None:
        baseline_language = previous_language or current.language
        previous = extract_v1_metrics(
            baseline_language,
            previous_source,
            extractor=extractor,
        )
        delta_vs_previous = current.delta_from(previous)

    return MetricDeltaResult(
        current=current,
        seed_cpp=seed_cpp,
        previous=previous,
        delta_vs_seed_cpp=current.delta_from(seed_cpp),
        delta_vs_previous=delta_vs_previous,
    )


def _normalize_language(language: str) -> str:
    if not isinstance(language, str) or not language.strip():
        raise MetricExtractionError("`language` must be a non-empty string.")

    normalized = language.strip().lower()
    if normalized not in SUPPORTED_METRIC_LANGUAGES:
        supported = ", ".join(sorted(SUPPORTED_METRIC_LANGUAGES))
        raise MetricExtractionError(
            f"Unsupported metric language `{language}`. Supported: {supported}."
        )
    return normalized


def _normalize_metric_name(metric_name: str) -> str:
    if not isinstance(metric_name, str) or not metric_name.strip():
        raise MetricExtractionError("`metric_name` must be a non-empty string.")

    normalized = metric_name.strip().lower()
    if normalized not in V1_METRIC_NAMES:
        supported = ", ".join(V1_METRIC_NAMES)
        raise MetricExtractionError(
            f"Unsupported metric `{metric_name}`. Supported metrics: {supported}."
        )
    return normalized


def _validate_source(source: str) -> str:
    if not isinstance(source, str) or not source.strip():
        raise MetricExtractionError("`source` must be a non-empty string.")
    return source
