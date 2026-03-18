from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from rttdist.config import ConfigValidationError, load_experiment_config
from rttdist.corpus import CorpusValidationError, validate_corpus


REPO_ROOT = Path(__file__).resolve().parents[2]
MINIMAL_CONFIG_PATH = REPO_ROOT / "tests" / "fixtures" / "config" / "minimal.yaml"


def test_validation_reports_discovered_statement_fixture_pairs_and_seed(
    tmp_path: Path,
) -> None:
    config = load_experiment_config(MINIMAL_CONFIG_PATH)

    corpus_root = tmp_path / "corpus" / "solutions"
    seed_path_1436 = corpus_root / "IPOP_1436" / "reference.cpp"
    seed_path_1436.parent.mkdir(parents=True)
    seed_path_1436.write_text("int main() { return 0; }\n", encoding="utf-8")

    seed_path_2579 = corpus_root / "IPOP_2579" / "reference.cpp"
    seed_path_2579.parent.mkdir(parents=True)
    seed_path_2579.write_text("int main() { return 0; }\n", encoding="utf-8")

    config = replace(config, corpus_root=corpus_root.resolve())
    entries = validate_corpus(config)

    assert len(entries) == 2
    entry_ids = {entry.problem_id for entry in entries}
    assert entry_ids == {"IPOP_1436", "IPOP_2579"}


def test_fails_fast_when_statement_file_is_missing(tmp_path: Path) -> None:
    problem_root = tmp_path / "problem"
    problem_root.mkdir()

    fixture_dir = problem_root / "IPOP_1436"
    fixture_dir.mkdir()
    (fixture_dir / "1.inp").write_text("1\n", encoding="utf-8")
    (fixture_dir / "1.out").write_text("1\n", encoding="utf-8")

    corpus_root = tmp_path / "corpus" / "solutions"
    seed_path = corpus_root / "IPOP_1436" / "reference.cpp"
    seed_path.parent.mkdir(parents=True)
    seed_path.write_text("int main() { return 0; }\n", encoding="utf-8")

    base_config = load_experiment_config(MINIMAL_CONFIG_PATH)
    config = replace(
        base_config,
        problem_root=problem_root.resolve(),
        corpus_root=corpus_root.resolve(),
    )

    with pytest.raises(CorpusValidationError) as excinfo:
        validate_corpus(config)

    assert "Missing statement file" in str(excinfo.value)


def test_fails_fast_when_fixture_directory_is_missing(tmp_path: Path) -> None:
    problem_root = tmp_path / "problem"
    problem_root.mkdir()
    (problem_root / "IPOP_1436.md").write_text("statement", encoding="utf-8")

    corpus_root = tmp_path / "corpus" / "solutions"
    seed_path = corpus_root / "IPOP_1436" / "reference.cpp"
    seed_path.parent.mkdir(parents=True)
    seed_path.write_text("int main() { return 0; }\n", encoding="utf-8")

    base_config = load_experiment_config(MINIMAL_CONFIG_PATH)
    config = replace(
        base_config,
        problem_root=problem_root.resolve(),
        corpus_root=corpus_root.resolve(),
    )

    with pytest.raises(CorpusValidationError) as excinfo:
        validate_corpus(config)

    assert "Missing fixture directory" in str(excinfo.value)


def test_fails_fast_when_fixture_pair_is_missing(tmp_path: Path) -> None:
    problem_root = tmp_path / "problem"
    problem_root.mkdir()
    (problem_root / "IPOP_1436.md").write_text("statement", encoding="utf-8")

    fixture_dir = problem_root / "IPOP_1436"
    fixture_dir.mkdir()
    (fixture_dir / "1.inp").write_text("1\n", encoding="utf-8")

    corpus_root = tmp_path / "corpus" / "solutions"
    seed_path = corpus_root / "IPOP_1436" / "reference.cpp"
    seed_path.parent.mkdir(parents=True)
    seed_path.write_text("int main() { return 0; }\n", encoding="utf-8")

    base_config = load_experiment_config(MINIMAL_CONFIG_PATH)
    config = replace(
        base_config,
        problem_root=problem_root.resolve(),
        corpus_root=corpus_root.resolve(),
    )

    with pytest.raises(CorpusValidationError) as excinfo:
        validate_corpus(config)

    message = str(excinfo.value)
    assert "Missing fixture pair" in message
    assert "1.out" in message


@pytest.mark.parametrize(
    ("seed_language", "seed_filename"),
    (
        ("cpp", "reference.cpp"),
        ("c", "reference.c"),
        ("java", "reference.java"),
        ("python", "reference.py"),
    ),
)
def test_seed_language_selects_reference_filename(
    tmp_path: Path,
    seed_language: str,
    seed_filename: str,
) -> None:
    config = load_experiment_config(MINIMAL_CONFIG_PATH)
    corpus_root = tmp_path / "corpus" / "solutions"

    for problem_id in config.problem_ids:
        seed_path = corpus_root / problem_id / seed_filename
        seed_path.parent.mkdir(parents=True, exist_ok=True)
        seed_path.write_text("int main() { return 0; }\n", encoding="utf-8")

    entries = validate_corpus(
        replace(
            config,
            seed_language=seed_language,
            corpus_root=corpus_root.resolve(),
        )
    )

    assert len(entries) == len(config.problem_ids)
    assert all(entry.seed_path.name == seed_filename for entry in entries)


def test_seed_language_rejects_same_language_target_pair(tmp_path: Path) -> None:
    config_path = tmp_path / "invalid-seed-language.yaml"
    config_path.write_text(
        "\n".join(
            (
                "problem_ids:",
                "  - IPOP_1436",
                "seed_language: python",
                "target_languages:",
                "  - python",
                "openai:",
                "  model: gpt-5.4",
                "  temperature: 0",
                "runtime:",
                "  max_iterations: 20",
                "  timeout_seconds: 30",
                "output_root: ./artifacts",
                "problem_root: ./problem",
                "corpus_root: ./corpus/solutions",
                "",
            )
        ),
        encoding="utf-8",
    )

    with pytest.raises(ConfigValidationError) as excinfo:
        load_experiment_config(config_path)

    assert (
        str(excinfo.value)
        == "Invalid language pair: `seed_language` and `target_languages[0]` must differ, got 'python'."
    )


def test_reverse_direction_pair_python_to_cpp_is_accepted(tmp_path: Path) -> None:
    config_path = tmp_path / "reverse-direction.yaml"
    config_path.write_text(
        "\n".join(
            (
                "problem_ids:",
                "  - IPOP_1436",
                "seed_language: python",
                "target_languages:",
                "  - cpp",
                "openai:",
                "  model: gpt-5.4",
                "  temperature: 0",
                "runtime:",
                "  max_iterations: 20",
                "  timeout_seconds: 30",
                "output_root: ./artifacts",
                "problem_root: ./problem",
                "corpus_root: ./corpus/solutions",
                "",
            )
        ),
        encoding="utf-8",
    )

    config = load_experiment_config(config_path)

    assert config.seed_language == "python"
    assert config.target_languages == ("cpp",)
