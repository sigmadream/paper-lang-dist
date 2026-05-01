import json
import os
import subprocess
import sys
from pathlib import Path


def test_cli_validate_and_empty_report(tmp_path: Path) -> None:
    config = tmp_path / "config.yaml"
    problem_root = tmp_path / "problem"
    fixtures = problem_root / "IPOP"
    corpus = tmp_path / "corpus" / "IPOP"
    fixtures.mkdir(parents=True)
    corpus.mkdir(parents=True)
    (problem_root / "IPOP.md").write_text("print zero", encoding="utf-8")
    (corpus / "reference.cpp").write_text("int main(){return 0;}", encoding="utf-8")
    (fixtures / "1.inp").write_text("", encoding="utf-8")
    (fixtures / "1.out").write_text("", encoding="utf-8")
    config.write_text(f"""
provider: lmstudio
problem_ids: [IPOP]
seed_language: cpp
target_languages: [c, java, python]
lmstudio:
  model: local
  temperature: 0
  host: http://localhost:1234/v1
runtime:
  max_iterations: 1
  timeout_seconds: 1
output_root: {tmp_path / 'artifacts'}
problem_root: {tmp_path / 'problem'}
corpus_root: {tmp_path / 'corpus'}
""", encoding="utf-8")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path.cwd() / "src")
    validate = subprocess.run([sys.executable, "-m", "rttdist.cli", "validate-corpus", "--config", str(config)], text=True, capture_output=True, env=env)
    assert validate.returncode == 0
    report = subprocess.run([sys.executable, "-m", "rttdist.cli", "report", "--config", str(config), "--run-id", "missing"], text=True, capture_output=True, env=env)
    assert report.returncode == 0
    summary = json.loads((tmp_path / "artifacts" / "missing" / "summary.json").read_text(encoding="utf-8"))
    assert summary["schema_version"] == "report_summary.rtt.v1"
