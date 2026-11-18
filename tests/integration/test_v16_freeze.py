from copy import deepcopy
from pathlib import Path

import pytest

from rttdist import hops_experiment as hops
from rttdist.experiment_io import digest, read_json, write_json

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_SOURCES = ("scripts/prepare_v16_corpus.py", "scripts/validate_v16_corpus.py")
ORACLE_SOURCES = (
    "problem/metadata/ipop19/tools/oracles.py",
    "problem/metadata/leetcode21/tools/oracles.py",
)


@pytest.fixture
def inputs(tmp_path, monkeypatch):
    cfg = hops.load_hops_config(
        Path(__file__).resolve().parents[2] / "configs/v1.6/experiment.yaml"
    )
    cfg.update(
        corpus_root=str(tmp_path / "corpus"),
        output_root=str(tmp_path / "out"),
        selection=str(tmp_path / "selection.json"),
    )
    cfg["llm"].update(
        model="test",
        generation_profile={
            "name": "test",
            "supported_options": list(cfg["llm"]["generation"]),
        },
    )
    corpus = Path(cfg["corpus_root"])
    corpus.mkdir()
    (corpus / "mock-data").write_text("모의 동결 자료", encoding="utf-8")
    independent_results = []
    for pid in cfg["problem_ids"]:
        evaluation = corpus / pid / "evaluation"
        evaluation.mkdir(parents=True)
        for number in range(1, 14):
            inp = evaluation / f"case{number:02}.inp"
            out = inp.with_suffix(".out")
            inp.write_text(f"모의 입력 {pid} {number}\n", encoding="utf-8")
            out.write_text("모의 정답\n", encoding="utf-8")
            independent_results.append(
                {
                    "problem_id": pid,
                    "case": inp.stem,
                    "passed": True,
                    "input_sha256": digest(inp.read_bytes()),
                    "expected_sha256": digest(out.read_bytes()),
                    "computed_sha256": digest("모의 정답".encode("utf-8")),
                    "methods": "명시적 모의 독립 검증 근거",
                }
            )
    manifest = {
        "file_hashes": {
            p.relative_to(corpus).as_posix(): digest(p.read_bytes())
            for p in corpus.rglob("*")
            if p.is_file()
        }
    }
    write_json(corpus / "manifest.json", manifest)
    write_json(
        cfg["selection"], {"problems": [{"problem_id": p} for p in cfg["problem_ids"]]}
    )
    environment = {"tools": {"cpp": {"version": "mock"}}, "mock": True}
    monkeypatch.setattr(
        hops, "collect_hops_environment", lambda cfg: environment, raising=False
    )
    validation = {
        "passed": True,
        "expected_references": 75,
        "expected_cases": 975,
        "executed_cases": 975,
        "passed_cases": 975,
        "runtime": cfg["runtime"],
        "validator_source_hashes": {
            name: digest((ROOT / name).read_bytes()) for name in VALIDATOR_SOURCES
        },
        "independent_checks": {
            "passed": True,
            "source_hashes": {
                name: digest((ROOT / name).read_bytes()) for name in ORACLE_SOURCES
            },
            "results": independent_results,
        },
        "file_hashes": {
            **manifest["file_hashes"],
            "manifest.json": digest((corpus / "manifest.json").read_bytes()),
        },
        "results": [
            {
                "problem_id": p,
                "language": language,
                "status": "success",
                "case_count": 13,
                "passed_cases": 13,
            }
            for p in cfg["problem_ids"]
            for language in cfg["runtime"]["tools"]
        ],
    }
    contract = hops.build_run_contract(cfg, manifest, environment)
    pilot = {
        "passed": True,
        "observation_count": 12,
        "contract_hash": contract["contract_hash"],
        "complete_by_threshold": {"0.80": True, "0.85": True, "0.90": True},
    }
    preflight = {
        "passed": True,
        "live": True,
        "actual_model": "test",
        "model_evidence": {"status": "exact", "valid": True},
        "generation_profile": cfg["llm"]["generation_profile"],
        "comparison_class": "direct_api",
        "environment": environment,
    }
    return cfg, pilot, validation, preflight


@pytest.mark.parametrize("incomplete", ["all", "0.80", "0.85", "0.90", "missing"])
def test_structural_pilot_completion_cannot_replace_threshold_completeness(
    inputs, incomplete
):
    cfg, pilot, validation, preflight = inputs
    if incomplete == "missing":
        pilot.pop("complete_by_threshold")
    else:
        for key in pilot["complete_by_threshold"]:
            if incomplete == "all" or key == incomplete:
                pilot["complete_by_threshold"][key] = False
    with pytest.raises(ValueError, match="임계치"):
        hops.freeze_main_design(cfg, pilot, validation, preflight)


@pytest.mark.parametrize("invalid", [True, False])
def test_actual_campaign_audit_blocks_invalid_pilot_but_accepts_functional_failures(
    inputs, monkeypatch, invalid
):
    from rttdist.providers import ProviderError
    from tests.integration.test_hops_experiment import MockProvider

    cfg, unused_pilot, validation, preflight = inputs
    root = Path(cfg["corpus_root"])
    for pid in cfg["pilot_problem_ids"]:
        problem = root / pid
        problem.mkdir(parents=True, exist_ok=True)
        (problem / "reference.cpp").write_text("origin", encoding="utf-8")
        (problem / "statement.md").write_text("모의 명세", encoding="utf-8")
    manifest = {
        "file_hashes": {
            p.relative_to(root).as_posix(): digest(p.read_bytes())
            for p in root.rglob("*")
            if p.is_file() and p.name != "manifest.json"
        }
    }
    write_json(root / "manifest.json", manifest)
    validation["file_hashes"] = {
        **manifest["file_hashes"],
        "manifest.json": digest((root / "manifest.json").read_bytes()),
    }
    cfg["validation"] = str(root.parent / "validation.json")
    write_json(cfg["validation"], validation)

    class OfflineProvider(MockProvider):
        def complete(self, payload, folder):
            if invalid:
                raise ProviderError("모의 기반시설 장애")
            return super().complete(payload, folder)

    monkeypatch.setattr(hops, "create_provider", lambda *a, **k: OfflineProvider())
    monkeypatch.setattr(hops, "evaluate", lambda *a: {"status": "wrong_answer"})
    records = hops.run_hops_campaign(cfg, "pilot")
    assert len(records) == 12
    audit = read_json(hops.campaign_root(cfg) / "pilot/completion_audit.json")
    assert audit["passed"] and audit["collection_finished"]
    assert all(
        value is (not invalid) for value in audit["complete_by_threshold"].values()
    )
    if invalid:
        with pytest.raises(ValueError, match="임계치"):
            hops.freeze_main_design(cfg, audit, validation, preflight)
    else:
        assert hops.freeze_main_design(cfg, audit, validation, preflight)[
            "approved_for_main"
        ]


def test_freeze_mock_pilot_and_main_paths_are_independent(inputs):
    assert hasattr(hops, "freeze_main_design"), "본 실험 동결 관문이 필요합니다."
    cfg, pilot, validation, preflight = inputs
    design = hops.freeze_main_design(cfg, pilot, validation, preflight)
    root = Path(cfg["output_root"]) / cfg["campaign_id"]
    assert read_json(root / "main_design.json") == design
    assert design["approved_for_main"]
    assert design["main_attempts"] == 300
    assert design["max_logical_requests"] == 3600
    assert design["max_transport_attempts"] == 10800
    assert not (root / "main").exists()
    assert hops.freeze_main_design(cfg, pilot, validation, preflight) == design


@pytest.mark.parametrize(
    "missing",
    ["references", "pilot", "generation", "hashes", "budget", "static_only", "model"],
)
def test_missing_reference_pilot_profile_hashes_budget_or_model_blocks_freeze(
    inputs, missing
):
    assert hasattr(hops, "freeze_main_design"), "동결 검증이 필요합니다."
    cfg, pilot, validation, preflight = deepcopy(inputs)
    if missing == "references":
        validation["results"].pop()
    elif missing == "pilot":
        pilot["observation_count"] = 11
    elif missing == "generation":
        cfg["llm"]["generation_profile"] = None
    elif missing == "hashes":
        validation["file_hashes"] = {}
    elif missing == "budget":
        cfg["budget"] = {}
    elif missing == "static_only":
        preflight["live"] = False
    elif missing == "model":
        preflight["actual_model"] = "other"
    with pytest.raises(ValueError):
        hops.freeze_main_design(cfg, pilot, validation, preflight)


def test_unreported_sdk_can_freeze_exploratory_only(inputs):
    assert hasattr(hops, "freeze_main_design"), "SDK 동결 분리가 필요합니다."
    cfg, pilot, validation, preflight = inputs
    cfg["llm"]["protocol"] = "copilot_sdk"
    preflight.update(
        actual_model=None,
        model_evidence={"status": "missing", "valid": False},
        comparison_class="sdk_exploratory",
    )
    manifest = read_json(Path(cfg["corpus_root"]) / "manifest.json")
    pilot["contract_hash"] = hops.build_run_contract(
        cfg, manifest, preflight["environment"]
    )["contract_hash"]
    design = hops.freeze_main_design(cfg, pilot, validation, preflight)
    assert design["approved_for_main"]
    assert not design["confirmatory"]
    assert design["comparison_class"] == "sdk_exploratory"
    preflight.update(
        actual_model="other", model_evidence={"status": "mismatch", "valid": False}
    )
    with pytest.raises(ValueError):
        hops.freeze_main_design(cfg, pilot, validation, preflight)


def test_changed_pilot_conditions_or_corpus_cannot_freeze(inputs):
    assert hasattr(hops, "freeze_main_design"), "파일럿 조건 보존이 필요합니다."
    cfg, pilot, validation, preflight = inputs
    pilot["contract_hash"] = "different"
    with pytest.raises(ValueError, match="계약"):
        hops.freeze_main_design(cfg, pilot, validation, preflight)
    (Path(cfg["corpus_root"]) / "mock-data").write_text("변경", encoding="utf-8")
    with pytest.raises(ValueError):
        hops.freeze_main_design(cfg, pilot, validation, preflight)


def test_changed_tool_version_after_validation_blocks_freeze(inputs):
    cfg, pilot, validation, preflight = inputs
    validation["tool_versions"] = {
        "cpp": {"available": True, "stdout": "old compiler", "stderr": ""}
    }
    with pytest.raises(ValueError, match="도구"):
        hops.freeze_main_design(cfg, pilot, validation, preflight)


def test_real_copilot_config_empty_generation_freezes_exploratory(inputs):
    cfg, pilot, validation, preflight = inputs
    root = Path(__file__).resolve().parents[2]
    loaded = hops.load_hops_config(
        root / "configs/v1.6/experiment.yaml",
        root / "configs/v1.6/providers/copilot.yaml",
    )
    cfg["llm"] = loaded["llm"]
    cfg["llm"]["model"] = "selected-model"
    assert cfg["llm"]["generation"] == {}
    preflight.update(
        actual_model=None,
        model_evidence={"status": "missing", "valid": False},
        generation_profile=cfg["llm"]["generation_profile"],
        comparison_class="sdk_exploratory",
    )
    manifest = read_json(Path(cfg["corpus_root"]) / "manifest.json")
    pilot["contract_hash"] = hops.build_run_contract(
        cfg, manifest, preflight["environment"]
    )["contract_hash"]
    design = hops.freeze_main_design(cfg, pilot, validation, preflight)
    assert design["approved_for_main"]
    assert design["confirmatory"] is False
    assert design["comparison_class"] == "sdk_exploratory"
    assert design["contract"]["requested_generation"] == {}


@pytest.mark.parametrize("value", [None, [], "", "missing"])
def test_sdk_missing_or_malformed_generation_cannot_freeze(inputs, value):
    cfg, pilot, validation, preflight = inputs
    cfg["llm"]["protocol"] = "copilot_sdk"
    if value == "missing":
        cfg["llm"].pop("generation")
    else:
        cfg["llm"]["generation"] = value
    with pytest.raises(ValueError):
        hops.freeze_main_design(cfg, pilot, validation, preflight)


def test_direct_api_empty_generation_cannot_freeze(inputs):
    cfg, pilot, validation, preflight = inputs
    cfg["llm"]["generation"] = {}
    with pytest.raises(ValueError):
        hops.freeze_main_design(cfg, pilot, validation, preflight)


def test_mock_campaign_freeze_resume_and_shared_ledger(inputs, monkeypatch):
    assert hasattr(hops, "run_hops_campaign"), "캠페인 실행 연결이 필요합니다."
    cfg, pilot, validation, preflight = inputs
    cfg["validation"] = str(Path(cfg["corpus_root"]).parent / "validation.json")
    write_json(cfg["validation"], validation)
    manifest = read_json(Path(cfg["corpus_root"]) / "manifest.json")
    pilot["contract_hash"] = hops.build_run_contract(
        cfg, manifest, preflight["environment"]
    )["contract_hash"]
    hops.freeze_main_design(cfg, pilot, validation, preflight)
    ledgers = []
    monkeypatch.setattr(
        hops,
        "create_provider",
        lambda config, ledger=None: ledgers.append(ledger) or object(),
    )

    def observation(cfg, job, provider, folder):
        assert job["phase"] == "main"
        record = {
            **job,
            "outcomes": {
                k: {"success": False, "category": "hop_limit"}
                for k in ("0.80", "0.85", "0.90")
            },
            "evaluable": True,
            "terminal_status": "hop_limit",
        }
        write_json(Path(folder) / "observation.json", record)
        return record

    monkeypatch.setattr(hops, "run_hops_observation", observation)
    shards = [hops.run_hops_campaign(cfg, "main", f"{i}/3") for i in (1, 2, 3)]
    assert sum(map(len, shards)) == 300
    assert len(set(ledgers)) == 1
    assert all("main" not in ledger.name for ledger in ledgers)
    cfg["llm"]["generation"]["temperature"] = 0.2
    with pytest.raises(ValueError):
        hops.run_hops_campaign(cfg, "main")
