from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest
import yaml

from rttdist.config import (
    ConfigValidationError,
    SUPPORTED_OPENAI_MODELS,
    SUPPORTED_TARGET_LANGUAGES,
    ExperimentConfig,
    OllamaConfig,
    OpenAIConfig,
    RuntimeConfig,
    _yaml_safe_loader_with_duplicate_check,
    load_experiment_config,
)
from rttdist.corpus import CorpusValidationError, validate_corpus


REPO_ROOT = Path(__file__).resolve().parents[2]
MINIMAL_CONFIG_PATH = REPO_ROOT / "tests" / "fixtures" / "config" / "minimal.yaml"


def test_loads_minimal_yaml_schema() -> None:
    config = load_experiment_config(MINIMAL_CONFIG_PATH)

    assert config.problem_ids == ("IPOP_1436", "IPOP_2579")
    assert getattr(config, "seed_language") == "cpp"
    assert set(config.target_languages).issubset(SUPPORTED_TARGET_LANGUAGES)
    assert config.openai.model == "gpt-5.4"
    assert config.openai.temperature == 0.0
    assert config.provider == "openai"
    assert isinstance(config.ollama, OllamaConfig)
    assert config.runtime.max_iterations == 20
    assert config.runtime.timeout_seconds == 30
    assert config.output_root == (REPO_ROOT / "artifacts").resolve()
    assert config.problem_root == (REPO_ROOT / "problem").resolve()
    assert config.corpus_root == (REPO_ROOT / "corpus" / "solutions").resolve()


def test_rejects_unsupported_target_language(tmp_path: Path) -> None:
    config_path = tmp_path / "invalid-language.yaml"
    config_path.write_text(
        "\n".join(
            [
                "problem_ids:",
                "  - IPOP_1436",
                "seed_language: cpp",
                "target_languages:",
                "  - rust",
                "openai:",
                "  model: gpt-5.4",
                "  temperature: 0",
                "runtime:",
                "  max_iterations: 20",
                "  timeout_seconds: 30",
                "output_root: artifacts",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ConfigValidationError) as excinfo:
        load_experiment_config(config_path)

    assert "unsupported" in str(excinfo.value).lower()


def test_rejects_duplicate_yaml_mapping_keys(tmp_path: Path) -> None:
    config_path = tmp_path / "dup-keys.yaml"
    config_path.write_text(
        "\n".join(
            [
                "problem_ids:",
                "  - IPOP_1436",
                "seed_language: cpp",
                "target_languages:",
                "  - python",
                "openai:",
                "  model: gpt-5.4",
                "  temperature: 0",
                "openai:",
                "  model: gpt-5.4",
                "  temperature: 0",
                "runtime:",
                "  max_iterations: 20",
                "  timeout_seconds: 30",
                "output_root: artifacts",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ConfigValidationError) as excinfo:
        load_experiment_config(config_path)

    assert "duplicate" in str(excinfo.value).lower()


def test_duplicate_key_loader_does_not_mutate_global_safe_loader() -> None:
    assert _yaml_safe_loader_with_duplicate_check is not yaml.SafeLoader
    assert yaml.safe_load("value: 1\nvalue: 2\n") == {"value": 2}


def test_rejects_duplicate_target_languages(tmp_path: Path) -> None:
    config_path = tmp_path / "dup-langs.yaml"
    config_path.write_text(
        "\n".join(
            [
                "problem_ids:",
                "  - IPOP_1436",
                "seed_language: cpp",
                "target_languages:",
                "  - c",
                "  - python",
                "  - c",
                "openai:",
                "  model: gpt-5.4",
                "  temperature: 0",
                "runtime:",
                "  max_iterations: 20",
                "  timeout_seconds: 30",
                "output_root: artifacts",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ConfigValidationError) as excinfo:
        load_experiment_config(config_path)

    assert "duplicate" in str(excinfo.value).lower()
    assert "c" in str(excinfo.value)


def test_rejects_case_normalized_duplicate_target_languages(tmp_path: Path) -> None:
    config_path = tmp_path / "case-dup-langs.yaml"
    config_path.write_text(
        "\n".join(
            [
                "problem_ids:",
                "  - IPOP_1436",
                "seed_language: cpp",
                "target_languages:",
                "  - C",
                "  - c",
                "openai:",
                "  model: gpt-5.4",
                "  temperature: 0",
                "runtime:",
                "  max_iterations: 20",
                "  timeout_seconds: 30",
                "output_root: artifacts",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ConfigValidationError) as excinfo:
        load_experiment_config(config_path)

    assert "duplicate" in str(excinfo.value).lower()


@pytest.mark.parametrize("model", ["gpt-5.4", "gpt-5.4-mini", "gpt-5.3-codex"])
def test_accepts_approved_openai_models(tmp_path: Path, model: str) -> None:
    config_path = tmp_path / f"openai-{model}.yaml"
    config_path.write_text(
        "\n".join(
            [
                "provider: openai",
                "problem_ids:",
                "  - IPOP_1436",
                "seed_language: cpp",
                "target_languages:",
                "  - python",
                "openai:",
                f"  model: {model}",
                "  temperature: 0",
                "runtime:",
                "  max_iterations: 1",
                "  timeout_seconds: 30",
                "output_root: artifacts",
            ]
        ),
        encoding="utf-8",
    )

    config = load_experiment_config(config_path)
    assert config.openai.model == model


def test_rejects_unapproved_openai_model(tmp_path: Path) -> None:
    config_path = tmp_path / "openai-unsupported.yaml"
    config_path.write_text(
        "\n".join(
            [
                "provider: openai",
                "problem_ids:",
                "  - IPOP_1436",
                "seed_language: cpp",
                "target_languages:",
                "  - python",
                "openai:",
                "  model: gpt-4.1-mini",
                "  temperature: 0",
                "runtime:",
                "  max_iterations: 1",
                "  timeout_seconds: 30",
                "output_root: artifacts",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ConfigValidationError) as excinfo:
        load_experiment_config(config_path)

    for allowed in SUPPORTED_OPENAI_MODELS:
        assert allowed in str(excinfo.value)


def test_loads_ollama_provider_config(tmp_path: Path) -> None:
    config_path = tmp_path / "ollama.yaml"
    config_path.write_text(
        "\n".join(
            [
                "provider: ollama",
                "problem_ids:",
                "  - IPOP_1436",
                "seed_language: cpp",
                "target_languages:",
                "  - python",
                "ollama:",
                "  model: qwen2.5-coder:7b",
                "  temperature: 0",
                "  host: http://localhost:11434",
                "runtime:",
                "  max_iterations: 5",
                "  timeout_seconds: 30",
                "output_root: artifacts",
            ]
        ),
        encoding="utf-8",
    )

    config = load_experiment_config(config_path)

    assert config.provider == "ollama"
    assert config.ollama.model == "qwen2.5-coder:7b"
    assert config.ollama.temperature == 0.0
    assert config.ollama.host == "http://localhost:11434"
    assert config.openai.model == "gpt-5.4"


def test_rejects_missing_ollama_section_when_provider_is_ollama(tmp_path: Path) -> None:
    config_path = tmp_path / "missing-ollama.yaml"
    config_path.write_text(
        "\n".join(
            [
                "provider: ollama",
                "problem_ids:",
                "  - IPOP_1436",
                "seed_language: cpp",
                "target_languages:",
                "  - python",
                "runtime:",
                "  max_iterations: 5",
                "  timeout_seconds: 30",
                "output_root: artifacts",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ConfigValidationError) as excinfo:
        load_experiment_config(config_path)

    assert "ollama" in str(excinfo.value).lower()
