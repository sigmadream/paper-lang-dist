from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from rttdist.config import load_experiment_config

REPO_ROOT = Path(__file__).resolve().parents[2]
MINIMAL_CONFIG_PATH = REPO_ROOT / "tests" / "fixtures" / "config" / "minimal.yaml"
MOCK_RESPONSES_PATH = (
    REPO_ROOT / "tests" / "fixtures" / "e2e" / "smoke_openai_responses.json"
)


def test_smoke_workflow_runs_validate_run_resume_and_report(tmp_path: Path) -> None:
    config_path, output_root = _write_temp_config(tmp_path)
    run_id = "smoke-e2e"
    env = _cli_env()

    validate = _run_cli("validate-corpus", "--config", str(config_path), env=env)
    assert validate.returncode == 0, validate.stderr
    assert "Found 2 problem(s):" in validate.stdout
    assert "IPOP_1436" in validate.stdout
    assert "IPOP_2579" in validate.stdout

    run = _run_cli(
        "run",
        "--config",
        str(config_path),
        "--run-id",
        run_id,
        env=env,
    )
    assert run.returncode == 0, run.stderr
    assert f"Run completed: {run_id}" in run.stdout
    assert "Summary generated successfully." in run.stdout

    summary_json_path = output_root / run_id / "summary.json"
    summary_markdown_path = output_root / run_id / "summary.md"
    assert summary_json_path.is_file()
    assert summary_markdown_path.is_file()

    summary = json.loads(summary_json_path.read_text(encoding="utf-8"))
    assert summary["run_id"] == run_id
    assert summary["result_count"] == 6

    expected_pairs = {
        ("IPOP_1436", "c"),
        ("IPOP_1436", "java"),
        ("IPOP_1436", "python"),
        ("IPOP_2579", "c"),
        ("IPOP_2579", "java"),
        ("IPOP_2579", "python"),
    }
    assert {
        (entry["problem_id"], entry["target_language"]) for entry in summary["results"]
    } == expected_pairs

    for entry in summary["results"]:
        assert entry["final_status"] == "success"
        assert entry["convergence_outcome"] == "fixed_point"
        assert entry["residual_similarity"]["availability"] == "measured"
        assert entry["semantic_summary"]["overall"] == "pass"
        assert entry["artifacts"]["run_manifest_path"].startswith(f"{run_id}/")
        assert entry["artifacts"]["final_iteration_directory"].startswith(f"{run_id}/")
        assert entry["artifacts"]["final_execution_path"].startswith(f"{run_id}/")
        assert entry["artifacts"]["final_metrics_path"].startswith(f"{run_id}/")

    markdown = summary_markdown_path.read_text(encoding="utf-8")
    assert f"# Run Summary: {run_id}" in markdown
    assert "| IPOP_1436 | cpp->c | success |" in markdown
    assert "| IPOP_2579 | cpp->python | success |" in markdown

    resume = _run_cli(
        "resume",
        "--config",
        str(config_path),
        "--run-id",
        run_id,
        env=env,
    )
    assert resume.returncode == 0, resume.stderr
    assert f"Resume completed: {run_id}" in resume.stdout
    assert "Summary generated successfully." in resume.stdout

    report = _run_cli(
        "report",
        "--run-id",
        run_id,
        env=env,
        cwd=tmp_path,
    )
    assert report.returncode == 0, report.stderr
    assert "Report generated successfully." in report.stdout
    assert str(summary_json_path) in report.stdout
    assert str(summary_markdown_path) in report.stdout


def test_smoke_workflow_runs_non_default_seed_language_with_reporting(
    tmp_path: Path,
) -> None:
    seed_corpus_root = _write_temp_seed_corpus(tmp_path, problem_ids=("IPOP_1436",))
    config_path, output_root = _write_temp_config(
        tmp_path,
        problem_ids=("IPOP_1436",),
        seed_language="python",
        target_languages=("cpp",),
        corpus_root=seed_corpus_root,
    )
    run_id = "smoke-e2e-python-seed"
    env = _cli_env()

    validate = _run_cli("validate-corpus", "--config", str(config_path), env=env)
    assert validate.returncode == 0, validate.stderr
    assert "Seed language: python" in validate.stdout

    run = _run_cli(
        "run",
        "--config",
        str(config_path),
        "--run-id",
        run_id,
        env=env,
    )
    assert run.returncode == 0, run.stderr
    assert f"Run completed: {run_id}" in run.stdout
    assert "Summary generated successfully." in run.stdout

    summary_json_path = output_root / run_id / "summary.json"
    summary_markdown_path = output_root / run_id / "summary.md"
    assert summary_json_path.is_file()
    assert summary_markdown_path.is_file()

    summary = json.loads(summary_json_path.read_text(encoding="utf-8"))
    assert summary["schema_version"] == "report_summary.v2"
    assert summary["run_id"] == run_id
    assert summary["result_count"] == 1

    entry = summary["results"][0]
    assert entry["problem_id"] == "IPOP_1436"
    assert entry["seed_language"] == "python"
    assert entry["target_language"] == "cpp"
    assert entry["ordered_pair_key"] == "python->cpp"
    assert entry["final_status"] == "success"
    assert entry["convergence_outcome"] == "fixed_point"
    assert entry["residual_similarity"]["availability"] == "unavailable"
    assert entry["residual_similarity"]["reason"] == "seed_language_not_cpp"
    assert entry["residual_similarity"]["failure"]["status"] == "success"
    assert entry["residual_similarity"]["failure"]["stage"] == "convergence"
    assert entry["final_similarity"]["availability"] == "measured"
    assert isinstance(entry["final_similarity"]["value"]["score"], float)
    assert entry["final_similarity"]["value"]["provider"] == "openai"

    markdown = summary_markdown_path.read_text(encoding="utf-8")
    assert f"# Run Summary: {run_id}" in markdown
    assert "| IPOP_1436 | python->cpp | success |" in markdown
    resume = _run_cli(
        "resume",
        "--config",
        str(config_path),
        "--run-id",
        run_id,
        env=env,
    )
    assert resume.returncode == 0, resume.stderr
    assert f"Resume completed: {run_id}" in resume.stdout
    assert "Summary generated successfully." in resume.stdout

    report = _run_cli(
        "report",
        "--run-id",
        run_id,
        env=env,
        cwd=tmp_path,
    )
    assert report.returncode == 0, report.stderr
    assert "Report generated successfully." in report.stdout
    assert str(summary_json_path) in report.stdout
    assert str(summary_markdown_path) in report.stdout


def test_smoke_workflow_surfaces_missing_toolchain_dependency_cleanly(
    tmp_path: Path,
) -> None:
    config_path, output_root = _write_temp_config(tmp_path, target_languages=("c",))
    run_id = "missing-toolchain"
    env = _cli_env()

    empty_bin = tmp_path / "empty-bin"
    empty_bin.mkdir()
    env["PATH"] = str(empty_bin)

    run = _run_cli(
        "run",
        "--config",
        str(config_path),
        "--run-id",
        run_id,
        env=env,
    )
    assert run.returncode == 0, run.stderr
    assert "Missing toolchain executable: gcc." in run.stdout

    summary = json.loads(
        (output_root / run_id / "summary.json").read_text(encoding="utf-8")
    )
    assert summary["result_count"] == 2
    assert {entry["final_status"] for entry in summary["results"]} == {"compile_error"}


def test_smoke_config_validation_rejects_same_seed_and_target_language(
    tmp_path: Path,
) -> None:
    config_path, _ = _write_temp_config(
        tmp_path,
        seed_language="python",
        target_languages=("python",),
    )
    env = _cli_env()

    validate = _run_cli("validate-corpus", "--config", str(config_path), env=env)
    assert validate.returncode != 0
    assert "Config validation failed" in validate.stderr
    assert "seed_language" in validate.stderr
    assert "must differ" in validate.stderr


def _write_temp_config(
    tmp_path: Path,
    *,
    problem_ids: tuple[str, ...] | None = None,
    seed_language: str | None = None,
    target_languages: tuple[str, ...] | None = None,
    corpus_root: Path | None = None,
) -> tuple[Path, Path]:
    base_config = load_experiment_config(MINIMAL_CONFIG_PATH)
    selected_problem_ids = problem_ids or base_config.problem_ids
    selected_seed = seed_language or base_config.seed_language
    selected_targets = target_languages or base_config.target_languages
    selected_corpus_root = corpus_root or base_config.corpus_root
    output_root = tmp_path / "artifacts"
    config_path = tmp_path / "smoke.yaml"

    lines = ["provider: openai", "problem_ids:"]
    lines.extend(f"  - {problem_id}" for problem_id in selected_problem_ids)
    lines.append(f"seed_language: {selected_seed}")
    lines.append("target_languages:")
    lines.extend(f"  - {language}" for language in selected_targets)
    lines.extend(
        [
            "openai:",
            f"  model: {base_config.openai.model}",
            f"  temperature: {int(base_config.openai.temperature)}",
            "runtime:",
            f"  max_iterations: {base_config.runtime.max_iterations}",
            f"  timeout_seconds: {base_config.runtime.timeout_seconds}",
            f"output_root: {output_root.as_posix()}",
            f"problem_root: {base_config.problem_root.as_posix()}",
            f"corpus_root: {selected_corpus_root.as_posix()}",
        ]
    )
    config_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return config_path, output_root


def _write_temp_seed_corpus(tmp_path: Path, *, problem_ids: tuple[str, ...]) -> Path:
    corpus_root = tmp_path / "corpus" / "solutions"
    programs = {
        "IPOP_1436": (
            "import sys\n"
            "\n"
            "\n"
            "def main() -> None:\n"
            "    data = sys.stdin.read().strip()\n"
            "    if not data:\n"
            "        return\n"
            "\n"
            "    n = int(data)\n"
            "    count = 0\n"
            "    value = 665\n"
            "    while count < n:\n"
            "        value += 1\n"
            '        if "666" in str(value):\n'
            "            count += 1\n"
            "\n"
            '    sys.stdout.write(f"{value}\\n")\n'
            "\n"
            "\n"
            'if __name__ == "__main__":\n'
            "    main()\n"
        ),
        "IPOP_2579": (
            "import sys\n"
            "\n"
            "\n"
            "def main() -> None:\n"
            "    data = sys.stdin.read().strip().split()\n"
            "    if not data:\n"
            "        return\n"
            "\n"
            "    n = int(data[0])\n"
            "    values = [0] + [int(value) for value in data[1 : 1 + n]]\n"
            "    dp = [0] * (n + 1)\n"
            "\n"
            "    if n >= 1:\n"
            "        dp[1] = values[1]\n"
            "    if n >= 2:\n"
            "        dp[2] = values[1] + values[2]\n"
            "    for index in range(3, n + 1):\n"
            "        dp[index] = max(dp[index - 2], dp[index - 3] + values[index - 1]) + values[index]\n"
            "\n"
            '    sys.stdout.write(f"{dp[n]}\\n")\n'
            "\n"
            "\n"
            'if __name__ == "__main__":\n'
            "    main()\n"
        ),
    }
    for problem_id in problem_ids:
        source = programs[problem_id]
        seed_path = corpus_root / problem_id / "reference.py"
        seed_path.parent.mkdir(parents=True, exist_ok=True)
        seed_path.write_text(source, encoding="utf-8")
    return corpus_root


def _cli_env() -> dict[str, str]:
    env = os.environ.copy()
    env["RTTDIST_OPENAI_MOCK_RESPONSES"] = str(MOCK_RESPONSES_PATH)
    existing_pythonpath = env.get("PYTHONPATH", "")
    src_path = str(REPO_ROOT / "src")
    env["PYTHONPATH"] = (
        src_path
        if not existing_pythonpath
        else f"{src_path}{os.pathsep}{existing_pythonpath}"
    )
    return env


def _run_cli(
    *args: str,
    env: dict[str, str],
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "rttdist.cli", *args],
        cwd=cwd or REPO_ROOT,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
