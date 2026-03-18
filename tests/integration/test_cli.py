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
