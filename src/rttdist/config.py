from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

SUPPORTED_TARGET_LANGUAGES = frozenset({"c", "java", "python"})
SUPPORTED_TRANSLATION_PROVIDERS = frozenset({"openai", "ollama"})
PINNED_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_OLLAMA_HOST = "http://localhost:11434"
DEFAULT_OLLAMA_MODEL = "qwen2.5-coder:7b"


class _DuplicateKeyError(yaml.YAMLError):
    pass


class _DuplicateKeySafeLoader(yaml.SafeLoader):
    pass


def _construct_mapping_with_duplicate_check(
    self: yaml.SafeLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = self.construct_object(key_node, deep=deep)
        if key in mapping:
            raise _DuplicateKeyError(f"Found duplicate key ({key!r}) in YAML mapping.")
        mapping[key] = self.construct_object(value_node, deep=deep)
    return mapping


_yaml_safe_loader_with_duplicate_check = _DuplicateKeySafeLoader
_yaml_safe_loader_with_duplicate_check.construct_mapping = (
    _construct_mapping_with_duplicate_check
)


class ConfigValidationError(ValueError):
    pass


@dataclass(frozen=True)
class OpenAIConfig:
    model: str
    temperature: float


@dataclass(frozen=True)
class OllamaConfig:
    model: str
    temperature: float
    host: str


@dataclass(frozen=True)
class RuntimeConfig:
    max_iterations: int
    timeout_seconds: int


@dataclass(frozen=True)
class ExperimentConfig:
    problem_ids: tuple[str, ...]
    target_languages: tuple[str, ...]
    openai: OpenAIConfig
    runtime: RuntimeConfig
    output_root: Path
    problem_root: Path
    corpus_root: Path
    provider: str = "openai"
    ollama: OllamaConfig = field(
        default_factory=lambda: OllamaConfig(
            model=DEFAULT_OLLAMA_MODEL,
            temperature=0.0,
            host=DEFAULT_OLLAMA_HOST,
        )
    )


def load_experiment_config(config_path: Path) -> ExperimentConfig:
    resolved_config_path = Path(config_path).resolve()
    try:
        raw_data = yaml.load(
            resolved_config_path.read_text(encoding="utf-8"),
            Loader=_yaml_safe_loader_with_duplicate_check,
        )
    except OSError as exc:
        raise ConfigValidationError(
            f"Unable to read config file: {resolved_config_path}"
        ) from exc
    except yaml.YAMLError as exc:
        raise ConfigValidationError(
            f"Invalid YAML syntax in config: {resolved_config_path}"
        ) from exc

    if not isinstance(raw_data, dict):
        raise ConfigValidationError(
            "Config root must be a mapping with keys: "
            "problem_ids, target_languages, openai, runtime, output_root."
        )

    return _parse_config(raw_data, config_dir=resolved_config_path.parent)


def _parse_config(raw_data: dict[str, Any], config_dir: Path) -> ExperimentConfig:
    provider = _parse_provider(raw_data)
    problem_ids = _parse_problem_ids(raw_data)
    target_languages = _parse_target_languages(raw_data)
    openai = _parse_openai_config(raw_data, provider=provider)
    ollama = _parse_ollama_config(raw_data, provider=provider)
    runtime = _parse_runtime_config(raw_data)

    output_root = _resolve_path(
        raw_data.get("output_root"), key="output_root", base_dir=config_dir
    )
    problem_root = _resolve_path(
        raw_data.get("problem_root", "problem"),
        key="problem_root",
        base_dir=config_dir,
    )
    corpus_root = _resolve_path(
        raw_data.get("corpus_root", "corpus/solutions"),
        key="corpus_root",
        base_dir=config_dir,
    )

    return ExperimentConfig(
        problem_ids=problem_ids,
        target_languages=target_languages,
        openai=openai,
        runtime=runtime,
        output_root=output_root,
        problem_root=problem_root,
        corpus_root=corpus_root,
        provider=provider,
        ollama=ollama,
    )


def _parse_provider(raw_data: dict[str, Any]) -> str:
    value = raw_data.get("provider", "openai")
    if not isinstance(value, str) or not value.strip():
        raise ConfigValidationError("`provider` must be a non-empty string when set.")

    normalized = value.strip().lower()
    if normalized not in SUPPORTED_TRANSLATION_PROVIDERS:
        supported = ", ".join(sorted(SUPPORTED_TRANSLATION_PROVIDERS))
        raise ConfigValidationError(
            f"Unsupported translation provider `{value}`. Supported providers: {supported}."
        )
    return normalized


def _parse_problem_ids(raw_data: dict[str, Any]) -> tuple[str, ...]:
    value = raw_data.get("problem_ids")
    if not isinstance(value, list) or not value:
        raise ConfigValidationError(
            "`problem_ids` must be a non-empty list of problem IDs."
        )

    parsed: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise ConfigValidationError(
                f"`problem_ids[{index}]` must be a non-empty string."
            )
        normalized = item.strip()
        if normalized in seen:
            raise ConfigValidationError(
                f"`problem_ids` contains duplicate entry: {normalized!r}."
            )
        seen.add(normalized)
        parsed.append(normalized)
    return tuple(parsed)


def _parse_target_languages(raw_data: dict[str, Any]) -> tuple[str, ...]:
    value = raw_data.get("target_languages")
    if not isinstance(value, list) or not value:
        raise ConfigValidationError(
            "`target_languages` must be a non-empty list using: c, java, python."
        )

    parsed: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise ConfigValidationError(
                f"`target_languages[{index}]` must be a non-empty string."
            )

        normalized = item.strip().lower()
        if normalized in seen:
            raise ConfigValidationError(
                f"`target_languages` contains duplicate entry: {normalized!r}."
            )
        seen.add(normalized)
        if normalized not in SUPPORTED_TARGET_LANGUAGES:
            supported = ", ".join(sorted(SUPPORTED_TARGET_LANGUAGES))
            raise ConfigValidationError(
                "Unsupported target language "
                f"`{item}`. Supported target languages: {supported}."
            )
        parsed.append(normalized)

    return tuple(parsed)


def _parse_openai_config(raw_data: dict[str, Any], *, provider: str) -> OpenAIConfig:
    value = raw_data.get("openai")
    if value is None:
        if provider == "ollama":
            return OpenAIConfig(model=PINNED_OPENAI_MODEL, temperature=0.0)
        raise ConfigValidationError(
            "`openai` must be a mapping with optional `model` and `temperature`."
        )
    if not isinstance(value, dict):
        raise ConfigValidationError(
            "`openai` must be a mapping with optional `model` and `temperature`."
        )

    model_raw = value.get("model", PINNED_OPENAI_MODEL)
    if not isinstance(model_raw, str) or not model_raw.strip():
        raise ConfigValidationError(
            "`openai.model` must be a non-empty string when set."
        )
    model = model_raw.strip()
    if model != PINNED_OPENAI_MODEL:
        raise ConfigValidationError(
            "`openai.model` is pinned for reproducibility and must be "
            f"`{PINNED_OPENAI_MODEL}`."
        )

    temperature = value.get("temperature", 0)
    if not isinstance(temperature, (int, float)):
        raise ConfigValidationError("`openai.temperature` must be a numeric value.")
    if float(temperature) != 0.0:
        raise ConfigValidationError(
            "`openai.temperature` must be 0 for deterministic translations."
        )

    return OpenAIConfig(model=model, temperature=0.0)


def _parse_ollama_config(raw_data: dict[str, Any], *, provider: str) -> OllamaConfig:
    value = raw_data.get("ollama")
    if value is None:
        if provider == "ollama":
            raise ConfigValidationError(
                "`ollama` must be a mapping with `model`, optional `temperature`, and optional `host` when provider is `ollama`."
            )
        return OllamaConfig(
            model=DEFAULT_OLLAMA_MODEL,
            temperature=0.0,
            host=DEFAULT_OLLAMA_HOST,
        )
    if not isinstance(value, dict):
        raise ConfigValidationError(
            "`ollama` must be a mapping with `model`, optional `temperature`, and optional `host`."
        )

    model_raw = value.get("model", DEFAULT_OLLAMA_MODEL)
    if not isinstance(model_raw, str) or not model_raw.strip():
        raise ConfigValidationError(
            "`ollama.model` must be a non-empty string when set."
        )

    host_raw = value.get("host", DEFAULT_OLLAMA_HOST)
    if not isinstance(host_raw, str) or not host_raw.strip():
        raise ConfigValidationError(
            "`ollama.host` must be a non-empty string when set."
        )

    temperature = value.get("temperature", 0)
    if not isinstance(temperature, (int, float)):
        raise ConfigValidationError("`ollama.temperature` must be a numeric value.")
    if float(temperature) != 0.0:
        raise ConfigValidationError(
            "`ollama.temperature` must be 0 for deterministic translations."
        )

    return OllamaConfig(
        model=model_raw.strip(),
        temperature=0.0,
        host=host_raw.strip(),
    )


def _parse_runtime_config(raw_data: dict[str, Any]) -> RuntimeConfig:
    value = raw_data.get("runtime")
    if not isinstance(value, dict):
        raise ConfigValidationError(
            "`runtime` must be a mapping with `max_iterations` and `timeout_seconds`."
        )

    max_iterations = value.get("max_iterations")
    if not isinstance(max_iterations, int) or isinstance(max_iterations, bool):
        raise ConfigValidationError("`runtime.max_iterations` must be an integer >= 1.")
    if max_iterations < 1:
        raise ConfigValidationError(
            f"`runtime.max_iterations` must be >= 1, got {max_iterations}."
        )

    timeout_seconds = value.get("timeout_seconds")
    if not isinstance(timeout_seconds, int) or isinstance(timeout_seconds, bool):
        raise ConfigValidationError(
            "`runtime.timeout_seconds` must be an integer >= 1."
        )
    if timeout_seconds < 1:
        raise ConfigValidationError(
            f"`runtime.timeout_seconds` must be >= 1, got {timeout_seconds}."
        )

    return RuntimeConfig(
        max_iterations=max_iterations,
        timeout_seconds=timeout_seconds,
    )


def _resolve_path(value: Any, *, key: str, base_dir: Path) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ConfigValidationError(f"`{key}` must be a non-empty path string.")

    path = Path(value.strip())
    if not path.is_absolute():
        path = (base_dir / path).resolve()
    else:
        path = path.resolve()

    return path
