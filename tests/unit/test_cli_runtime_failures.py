from __future__ import annotations

from pathlib import Path

from rttdist.cli import EXIT_RUNTIME_ERROR, main
from rttdist.config import ExperimentConfig, OpenAIConfig, RuntimeConfig


def test_run_returns_runtime_exit_code_with_deterministic_error_message(
    monkeypatch,
    capsys,
    tmp_path: Path,
) -> None:
    config = _build_config(tmp_path)
    monkeypatch.setattr("rttdist.cli._load_config", lambda _path: config)
    monkeypatch.setattr(
        "rttdist.cli._validate_corpus_entries", lambda _config: (object(),)
    )
    monkeypatch.setattr(
        "rttdist.cli.run_pipeline_service",
        lambda **_kwargs: (_ for _ in ()).throw(RuntimeError("mock pipeline failure")),
    )

    exit_code = main(["run", "--config", "dummy.yaml", "--run-id", "run-fail"])

    captured = capsys.readouterr()
    assert exit_code == EXIT_RUNTIME_ERROR
    assert "Pipeline execution failed: mock pipeline failure" in captured.err
    assert "Traceback" not in captured.err


def test_resume_returns_runtime_exit_code_with_deterministic_error_message(
    monkeypatch,
    capsys,
    tmp_path: Path,
) -> None:
    config = _build_config(tmp_path)
    monkeypatch.setattr("rttdist.cli._load_config", lambda _path: config)
    monkeypatch.setattr(
        "rttdist.cli._validate_corpus_entries", lambda _config: (object(),)
    )
    monkeypatch.setattr(
        "rttdist.cli.run_pipeline_service",
        lambda **_kwargs: (_ for _ in ()).throw(RuntimeError("mock resume failure")),
    )

    exit_code = main(["resume", "--config", "dummy.yaml", "--run-id", "resume-fail"])

    captured = capsys.readouterr()
    assert exit_code == EXIT_RUNTIME_ERROR
    assert "Resume failed: mock resume failure" in captured.err
    assert "Traceback" not in captured.err


def test_report_returns_runtime_exit_code_with_deterministic_error_message(
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.setattr(
        "rttdist.cli.write_run_summary",
        lambda **_kwargs: (_ for _ in ()).throw(RuntimeError("mock report failure")),
    )

    exit_code = main(["report", "--run-id", "report-fail"])

    captured = capsys.readouterr()
    assert exit_code == EXIT_RUNTIME_ERROR
    assert "Report generation failed: mock report failure" in captured.err
    assert "Traceback" not in captured.err


def _build_config(tmp_path: Path) -> ExperimentConfig:
    output_root = tmp_path / "artifacts"
    output_root.mkdir(parents=True, exist_ok=True)
    return ExperimentConfig(
        problem_ids=("IPOP_CLI",),
        seed_language="cpp",
        target_languages=("python",),
        openai=OpenAIConfig(model="gpt-5.4", temperature=0.0),
        runtime=RuntimeConfig(max_iterations=2, timeout_seconds=1),
        output_root=output_root,
        problem_root=tmp_path / "problem",
        corpus_root=tmp_path / "corpus" / "solutions",
    )
