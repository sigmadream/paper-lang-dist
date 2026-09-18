from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

SUPPORTED_EXPERIMENT_LANGUAGES = frozenset({"cpp", "c", "java", "python", "haskell", "prolog"})
SUPPORTED_TARGET_LANGUAGES = frozenset({"cpp", "c", "java", "python", "scala", "haskell", "prolog"})
REFERENCE_EXTENSION_BY_LANGUAGE = {
    "cpp": "cpp",
    "c": "c",
    "java": "java",
    "python": "py",
    "haskell": "hs",
    "prolog": "pl",
}
SUPPORTED_TRANSLATION_PROVIDERS = frozenset({"lmstudio", "openai_compatible"})
DEFAULT_LMSTUDIO_HOST = "http://localhost:1234/v1"
DEFAULT_LMSTUDIO_MODEL = "unspecified"


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
class LMStudioConfig:
    model: str
    temperature: float
    host: str
    max_tokens: int | None = None


@dataclass(frozen=True)
class RuntimeConfig:
    max_iterations: int
    timeout_seconds: int
    confirmation_cycles: int = 5
    stop_on_intermediate_failure: bool = True


@dataclass(frozen=True)
class ExperimentConfig:
    problem_ids: tuple[str, ...]
    seed_language: str
    target_languages: tuple[str, ...]
    lmstudio: LMStudioConfig
    runtime: RuntimeConfig
    output_root: Path
    problem_root: Path
    corpus_root: Path
    provider: str = "lmstudio"
    experiment_version: str | None = None
    dataset_index: Path | None = None
    prompt_template_version: str = "rtt.prompts.v1"
    llm: dict[str, Any] | None = None


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
            "problem_ids, seed_language, target_languages, lmstudio, runtime, output_root."
        )

    return _parse_config(raw_data, config_dir=resolved_config_path.parent)


def _parse_config(raw_data: dict[str, Any], config_dir: Path) -> ExperimentConfig:
    provider = _parse_provider(raw_data)
    problem_ids = _parse_problem_ids(raw_data)
    seed_language = _parse_seed_language(raw_data)
    target_languages = _parse_target_languages(raw_data)
    _validate_seed_target_language_pairs(
        seed_language=seed_language,
        target_languages=target_languages,
    )
    lmstudio = _parse_lmstudio_config(raw_data, provider=provider)
    runtime = _parse_runtime_config(raw_data)
    prompt_version = raw_data.get("prompt_template_version", "rtt.prompts.v1")
    if prompt_version not in ("rtt.prompts.v1", "rtt.prompts.v2", "rtt.prompts.abs.v1"):
        raise ConfigValidationError("Unsupported prompt_template_version.")

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
        seed_language=seed_language,
        target_languages=target_languages,
        lmstudio=lmstudio,
        runtime=runtime,
        output_root=output_root,
        problem_root=problem_root,
        corpus_root=corpus_root,
        provider=provider,
        prompt_template_version=prompt_version,
        experiment_version=raw_data.get("experiment_version"),
        dataset_index=(
            _resolve_path(raw_data["dataset_index"], key="dataset_index", base_dir=config_dir)
            if "dataset_index" in raw_data else None
        ),
        llm=raw_data.get('llm'),
    )


def _parse_provider(raw_data: dict[str, Any]) -> str:
    value = raw_data.get("provider", "lmstudio")
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
        supported = ", ".join(sorted(SUPPORTED_TARGET_LANGUAGES))
        raise ConfigValidationError(
            f"`target_languages` must be a non-empty list using: {supported}."
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


def _parse_seed_language(raw_data: dict[str, Any]) -> str:
    value = raw_data.get("seed_language")
    if not isinstance(value, str) or not value.strip():
        supported = ", ".join(sorted(SUPPORTED_EXPERIMENT_LANGUAGES))
        raise ConfigValidationError(
            f"`seed_language` must be a non-empty string using: {supported}."
        )

    normalized = value.strip().lower()
    if normalized not in SUPPORTED_EXPERIMENT_LANGUAGES:
        supported = ", ".join(sorted(SUPPORTED_EXPERIMENT_LANGUAGES))
        raise ConfigValidationError(
            "Unsupported seed language "
            f"`{value}`. Supported seed languages: {supported}."
        )

    return normalized


def _validate_seed_target_language_pairs(
    *,
    seed_language: str,
    target_languages: tuple[str, ...],
) -> None:
    for index, target_language in enumerate(target_languages):
        if seed_language == target_language:
            raise ConfigValidationError(
                "Invalid language pair: `seed_language` and "
                f"`target_languages[{index}]` must differ, got {seed_language!r}."
            )


def reference_filename_for_language(language: str) -> str:
    normalized = language.strip().lower() if isinstance(language, str) else ""
    extension = REFERENCE_EXTENSION_BY_LANGUAGE.get(normalized)
    if extension is None:
        supported = ", ".join(sorted(SUPPORTED_EXPERIMENT_LANGUAGES))
        raise ConfigValidationError(
            "Unsupported seed language "
            f"`{language}`. Supported seed languages: {supported}."
        )
    return f"reference.{extension}"


def _parse_lmstudio_config(raw_data: dict[str, Any], *, provider: str) -> LMStudioConfig:
    value = raw_data.get("lmstudio")
    common = raw_data.get('llm')
    if common is not None:
        if not isinstance(common, dict) or not common.get('model') or not common.get('endpoint'):
            raise ConfigValidationError('`llm` requires model and endpoint.')
        generation = common.get('generation', {})
        if not isinstance(generation, dict):
            raise ConfigValidationError('`llm.generation` must be a mapping.')
        value = {'model':common['model'], 'host':common['endpoint'],
                 'temperature':generation.get('temperature',0), 'max_tokens':generation.get('max_tokens')}
    elif provider == 'openai_compatible':
        raise ConfigValidationError('`openai_compatible` requires the common `llm` block.')
    if value is None:
        if provider == "lmstudio":
            raise ConfigValidationError(
                "`lmstudio` must be a mapping with `model`, optional `temperature`, and optional `host` when provider is `lmstudio`."
            )
        return LMStudioConfig(
            model=DEFAULT_LMSTUDIO_MODEL,
            temperature=0.0,
            host=DEFAULT_LMSTUDIO_HOST,
        )
    if not isinstance(value, dict):
        raise ConfigValidationError(
            "`lmstudio` must be a mapping with `model`, optional `temperature`, and optional `host`."
        )

    model_raw = value.get("model", DEFAULT_LMSTUDIO_MODEL)
    if not isinstance(model_raw, str) or not model_raw.strip():
        raise ConfigValidationError(
            "`lmstudio.model` must be a non-empty string when set."
        )

    host_raw = value.get("host", DEFAULT_LMSTUDIO_HOST)
    if not isinstance(host_raw, str) or not host_raw.strip():
        raise ConfigValidationError(
            "`lmstudio.host` must be a non-empty string when set."
        )

    temperature = value.get("temperature", 0)
    if not isinstance(temperature, (int, float)):
        raise ConfigValidationError("`lmstudio.temperature` must be a numeric value.")
    if float(temperature) != 0.0:
        raise ConfigValidationError(
            "`lmstudio.temperature` must be 0 for deterministic translations."
        )

    max_tokens = value.get("max_tokens")
    if max_tokens is not None and (type(max_tokens) is not int or max_tokens < 1):
        raise ConfigValidationError("`lmstudio.max_tokens` must be a positive integer.")
    return LMStudioConfig(
        model=model_raw.strip(),
        max_tokens=max_tokens,
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

    confirmation_cycles = value.get("confirmation_cycles", 5)
    if type(confirmation_cycles) is not int or not 0 <= confirmation_cycles <= 5:
        raise ConfigValidationError("`runtime.confirmation_cycles` must be in 0..5.")
    stop = value.get("stop_on_intermediate_failure", True)
    if type(stop) is not bool:
        raise ConfigValidationError("`runtime.stop_on_intermediate_failure` must be boolean.")
    return RuntimeConfig(
        max_iterations=max_iterations,
        confirmation_cycles=confirmation_cycles,
        stop_on_intermediate_failure=stop,
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
