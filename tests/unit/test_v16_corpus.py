"""v1.6 고정 코퍼스의 공개 계약을 검증합니다."""

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
IDS = [
    "IPOP_11729",
    "IPOP_2110",
    "IPOP_1992",
    "IPOP_2579",
    "IPOP_5567",
    "IPOP_10988",
    "IPOP_1929",
    "IPOP_2609",
    "IPOP_9012",
    "LC_0053",
    "LC_0062",
    "IPOP_9663",
    "LC_0242",
    "LC_0283",
    "LC_0338",
]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def selection():
    return json.loads(
        (ROOT / "papers/v1.6/data/selection.json").read_text(encoding="utf-8")
    )


def test_selection_keeps_fifteen_with_three_recursive_replacements():
    value = selection()
    assert [p["problem_id"] for p in value["problems"]] == IDS
    assert value["replacements"] == {
        "IPOP_1436": "IPOP_11729",
        "IPOP_2217": "IPOP_1992",
        "LC_0217": "IPOP_9663",
    }
    assert {p["problem_id"] for p in value["problems"] if p["recursive"]} == {
        "IPOP_11729",
        "IPOP_1992",
        "IPOP_9663",
    }


def test_iterative_gcd_is_not_recursive_group():
    gcd = next(p for p in selection()["problems"] if p["problem_id"] == "IPOP_2609")
    assert gcd["group"] == "comparison"
    assert gcd["recursive"] is False
    assert gcd["recursion_kind"] == "iterative_euclid"


def test_prepare_preserves_originals_and_has_all_references(tmp_path):
    prepare = load_script("prepare_v16_corpus").prepare_corpus
    target = tmp_path / "corpus"
    manifest = prepare(
        ROOT / "papers/v1.6/data/selection.json", ROOT / "problem", target
    )
    assert manifest["problem_ids"] == IDS
    for pid in IDS:
        for name in ["statement.md", "reference.cpp"]:
            assert (target / pid / name).read_bytes() == (
                ROOT / "problem" / pid / name
            ).read_bytes()
        assert len(list((target / pid / "evaluation").glob("*.inp"))) == 13
        for ext in ["cpp", "py", "java", "hs", "pl"]:
            assert (target / pid / f"reference.{ext}").is_file()
    assert len(manifest["file_hashes"]) > 75


@pytest.mark.parametrize("missing", ["reference.pl", "evaluation/case_01.out"])
def test_missing_reference_or_case_blocks_freeze(tmp_path, missing):
    prepare = load_script("prepare_v16_corpus").prepare_corpus
    validator = load_script("validate_v16_corpus").validate_corpus
    target = tmp_path / "corpus"
    prepare(ROOT / "papers/v1.6/data/selection.json", ROOT / "problem", target)
    path = target / IDS[0] / missing
    if not path.exists():
        path = next((target / IDS[0] / "evaluation").glob("*.out"))
    path.unlink()
    value = validator(
        {
            "corpus_root": str(target),
            "problem_ids": IDS,
            "runtime": {"tools": {}, "compile_timeout": 180, "fixture_timeout": 5},
            "validation": str(tmp_path / "validation.json"),
        }
    )
    assert value["passed"] is False
    assert value["expected_references"] == 75
    assert value["expected_cases"] == 975
    assert value["errors"]


def prepared_config(tmp_path):
    target = tmp_path / "corpus"
    load_script("prepare_v16_corpus").prepare_corpus(
        ROOT / "papers/v1.6/data/selection.json", ROOT / "problem", target
    )
    return {
        "corpus_root": str(target),
        "problem_ids": IDS,
        "runtime": {
            "tools": {language: "python" for language in selection()["languages"]},
            "compile_timeout": 180,
            "fixture_timeout": 5,
        },
        "validation": str(tmp_path / "validation.json"),
    }


def fake_execution(*args):
    return {
        "status": "success",
        "compile": {"seconds": 0.01},
        "cases": [{"status": "success", "seconds": 0.01} for _ in range(13)],
    }


def fake_tools(monkeypatch, validator):
    monkeypatch.setattr(validator.shutil, "which", lambda tool: "C:/tools/python.exe")
    monkeypatch.setattr(
        validator,
        "process",
        lambda *args: {"exit_code": 0, "timed_out": False},
    )
    monkeypatch.setattr(validator, "evaluate", fake_execution)
    monkeypatch.setattr(
        validator,
        "independent_checks",
        lambda corpus: {"passed": True, "results": []},
    )


def test_missing_language_is_reported_for_all_fifteen_problems(tmp_path, monkeypatch):
    cfg = prepared_config(tmp_path)
    cfg["runtime"]["tools"].pop("prolog")
    validator = load_script("validate_v16_corpus")
    fake_tools(monkeypatch, validator)
    value = validator.validate_corpus(cfg)
    assert value["passed"] is False
    assert value["executed_cases"] == 780
    assert len(value["results"]) == 75
    missing = [result for result in value["results"] if result["language"] == "prolog"]
    assert len(missing) == 15
    assert all(result["status"] == "unavailable" for result in missing)


def test_all_references_and_cases_are_required(tmp_path, monkeypatch):
    cfg = prepared_config(tmp_path)
    validator = load_script("validate_v16_corpus")
    fake_tools(monkeypatch, validator)
    complete = validator.validate_corpus(cfg)
    assert complete["passed"] is True
    assert complete["reference_count"] == 75
    assert complete["evaluation_count"] == 975
    manifest = json.loads(
        (Path(cfg["corpus_root"]) / "manifest.json").read_text(encoding="utf-8")
    )
    assert complete["file_hashes"] == {
        **manifest["file_hashes"],
        "manifest.json": complete["manifest_sha256"],
    }
    assert len(complete["manifest_sha256"]) == 64

    def incomplete_execution(*args):
        value = fake_execution()
        value["cases"].pop()
        return value

    monkeypatch.setattr(validator, "evaluate", incomplete_execution)
    partial = validator.validate_corpus(cfg)
    assert partial["passed"] is False
    assert partial["executed_cases"] == 900


def test_fixture_timeout_cannot_be_relaxed(tmp_path, monkeypatch):
    cfg = prepared_config(tmp_path)
    cfg["runtime"]["fixture_timeout"] = 10
    validator = load_script("validate_v16_corpus")
    fake_tools(monkeypatch, validator)
    value = validator.validate_corpus(cfg)
    assert value["passed"] is False
    assert value["executed_cases"] == 0


def test_corpus_mutation_is_rejected_before_execution(tmp_path, monkeypatch):
    cfg = prepared_config(tmp_path)
    target = Path(cfg["corpus_root"]) / IDS[0] / "reference.py"
    target.write_text("print(0)\n", encoding="utf-8")
    validator = load_script("validate_v16_corpus")
    fake_tools(monkeypatch, validator)
    value = validator.validate_corpus(cfg)
    assert value["passed"] is False
    assert value["executed_cases"] == 0
    assert any("해시" in error for error in value["errors"])


def test_prepare_rejects_public_evaluation_overlap(tmp_path):
    module = load_script("prepare_v16_corpus")
    target = tmp_path / "problem"
    (target / "evaluation").mkdir(parents=True)
    (target / "prompt_examples").mkdir()
    for number in range(13):
        (target / "evaluation" / f"{number}.inp").write_text(str(number))
        (target / "evaluation" / f"{number}.out").write_text(str(number))
    (target / "prompt_examples/one.inp").write_text(" 0 \n")
    (target / "prompt_examples/one.out").write_text("0\n")
    with pytest.raises(ValueError, match="공개 예시"):
        module.check_fixtures(target)


def test_prepare_is_idempotent_and_does_not_overwrite_changed_corpus(tmp_path):
    cfg = prepared_config(tmp_path)
    prepare = load_script("prepare_v16_corpus").prepare_corpus
    target = Path(cfg["corpus_root"])
    manifest = prepare(
        ROOT / "papers/v1.6/data/selection.json", ROOT / "problem", target
    )
    assert manifest["problem_ids"] == IDS
    reference = target / IDS[0] / "reference.cpp"
    reference.write_text("변경된 자료", encoding="utf-8")
    with pytest.raises(ValueError, match="별도 경로"):
        prepare(ROOT / "papers/v1.6/data/selection.json", ROOT / "problem", target)
    assert reference.read_text(encoding="utf-8") == "변경된 자료"
