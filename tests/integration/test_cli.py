"""Integration tests for CLI commands."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from textwrap import dedent

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]


class TestCLI:
    """Test cases for the CLI interface."""

    def test_help_exits_zero(self):
        """Test that --help exits with code 0."""
        result = subprocess.run(
            [sys.executable, "-m", "rttdist.cli", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "rttdist" in result.stdout
        assert "validate-corpus" in result.stdout
        assert "run" in result.stdout
        assert "resume" in result.stdout
        assert "report" in result.stdout

    def test_version_exits_zero(self):
        """Test that --version exits with code 0."""
        result = subprocess.run(
            [sys.executable, "-m", "rttdist.cli", "--version"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "rttdist" in result.stdout

    def test_invalid_command_exits_nonzero(self):
        """Test that an invalid command exits with non-zero code."""
        result = subprocess.run(
            [sys.executable, "-m", "rttdist.cli", "invalid-command"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert (
            "invalid choice" in result.stderr.lower()
            or "error" in result.stderr.lower()
        )

    def test_missing_required_arg_exits_nonzero(self):
        """Test that missing required arguments exit with non-zero code."""
        result = subprocess.run(
            [sys.executable, "-m", "rttdist.cli", "validate-corpus"],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert "error" in result.stderr.lower() or "required" in result.stderr.lower()

    def test_validate_corpus_subcommand_help(self):
        """Test that validate-corpus subcommand has proper help."""
        result = subprocess.run(
            [sys.executable, "-m", "rttdist.cli", "validate-corpus", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "config" in result.stdout

    def test_run_subcommand_help(self):
        """Test that run subcommand has proper help."""
        result = subprocess.run(
            [sys.executable, "-m", "rttdist.cli", "run", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "config" in result.stdout

    def test_resume_subcommand_help(self):
        """Test that resume subcommand has proper help."""
        result = subprocess.run(
            [sys.executable, "-m", "rttdist.cli", "resume", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "config" in result.stdout
        assert "run_id" in result.stdout

    def test_report_subcommand_help(self):
        """Test that report subcommand has proper help."""
        result = subprocess.run(
            [sys.executable, "-m", "rttdist.cli", "report", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "config" in result.stdout
        assert "run_id" in result.stdout

    def test_run_with_invalid_config_exits_nonzero(self):
        """Test that run with invalid config file exits with validation error."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "rttdist.cli",
                "run",
                "/nonexistent/path/config.yaml",
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0

    def test_validate_corpus_with_invalid_config_exits_nonzero(self):
        """Test that validate-corpus with invalid config exits with validation error."""
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "rttdist.cli",
                "validate-corpus",
                "/nonexistent/path/config.yaml",
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0

    def test_verbose_flag_accepted(self):
        """Test that -v/--verbose flag is accepted."""
        result = subprocess.run(
            [sys.executable, "-m", "rttdist.cli", "--verbose", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0

    def test_run_with_missing_ollama_model_fails_fast(self, tmp_path: Path):
        config_path = tmp_path / "missing-model.yaml"
        config_path.write_text(
            dedent(
                """
                provider: ollama
                problem_ids:
                  - IPOP_1436
                seed_language: cpp
                target_languages:
                  - python
                openai:
                  model: gpt-5.4
                  temperature: 0
                ollama:
                  model: definitely-missing-model
                  temperature: 0
                  host: http://localhost:11434
                runtime:
                  max_iterations: 1
                  timeout_seconds: 30
                output_root: {output_root}
                problem_root: {problem_root}
                corpus_root: {corpus_root}
                """
            )
            .format(
                output_root=(tmp_path / "artifacts-cli-test").as_posix(),
                problem_root=(REPO_ROOT / "problem").as_posix(),
                corpus_root=(REPO_ROOT / "corpus" / "solutions").as_posix(),
            )
            .strip()
            + "\n",
            encoding="utf-8",
        )

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "rttdist.cli",
                "run",
                "--config",
                str(config_path),
                "--run-id",
                "missing-model",
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode != 0
        assert "Ollama validation failed" in result.stderr
        assert "ollama pull definitely-missing-model" in result.stderr

    def test_validate_corpus_seed_language_rejects_same_language_pair(
        self,
        tmp_path: Path,
    ) -> None:
        config_path = tmp_path / "same-language.yaml"
        config_path.write_text(
            dedent(
                """
                problem_ids:
                  - IPOP_1436
                seed_language: cpp
                target_languages:
                  - cpp
                openai:
                  model: gpt-5.4
                  temperature: 0
                runtime:
                  max_iterations: 1
                  timeout_seconds: 30
                output_root: {output_root}
                problem_root: {problem_root}
                corpus_root: {corpus_root}
                """
            )
            .format(
                output_root=(tmp_path / "artifacts-cli-seed-validation").as_posix(),
                problem_root=(REPO_ROOT / "problem").as_posix(),
                corpus_root=(REPO_ROOT / "corpus" / "solutions").as_posix(),
            )
            .strip()
            + "\n",
            encoding="utf-8",
        )

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "rttdist.cli",
                "validate-corpus",
                "--config",
                str(config_path),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode != 0
        assert "Config validation failed" in result.stderr
        assert "seed_language" in result.stderr
        assert "must differ" in result.stderr

    def test_validate_corpus_seed_language_supports_non_default_seed_source(
        self,
        tmp_path: Path,
    ) -> None:
        problem_id = "SEED_LANG_CLI_001"
        problem_root = tmp_path / "problem"
        corpus_root = tmp_path / "corpus"
        fixture_dir = problem_root / problem_id
        seed_dir = corpus_root / problem_id

        fixture_dir.mkdir(parents=True)
        seed_dir.mkdir(parents=True)

        (problem_root / f"{problem_id}.md").write_text("statement\n", encoding="utf-8")
        (fixture_dir / "1.inp").write_text("1\n", encoding="utf-8")
        (fixture_dir / "1.out").write_text("1\n", encoding="utf-8")
        (seed_dir / "reference.py").write_text("print(1)\n", encoding="utf-8")

        config_path = tmp_path / "non-default-seed.yaml"
        config_path.write_text(
            dedent(
                """
                problem_ids:
                  - {problem_id}
                seed_language: python
                target_languages:
                  - c
                openai:
                  model: gpt-5.4
                  temperature: 0
                runtime:
                  max_iterations: 1
                  timeout_seconds: 30
                output_root: {output_root}
                problem_root: {problem_root}
                corpus_root: {corpus_root}
                """
            )
            .format(
                problem_id=problem_id,
                output_root=(tmp_path / "artifacts-cli-non-default-seed").as_posix(),
                problem_root=problem_root.as_posix(),
                corpus_root=corpus_root.as_posix(),
            )
            .strip()
            + "\n",
            encoding="utf-8",
        )

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "rttdist.cli",
                "validate-corpus",
                "--config",
                str(config_path),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, result.stderr
        assert "Seed language: python" in result.stdout
        assert "Found 1 problem(s):" in result.stdout
