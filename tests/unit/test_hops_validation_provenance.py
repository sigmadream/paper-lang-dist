from copy import deepcopy

import pytest

from rttdist import hops_experiment as hops
from rttdist.experiment_io import read_json, write_json
from tests.integration.test_v16_freeze import inputs, VALIDATOR_SOURCES, ORACLE_SOURCES


@pytest.mark.parametrize(
    "change",
    [
        "validator_hash",
        "validator_subset",
        "validator_arbitrary_path",
        "validator_missing",
        "oracle_hash",
        "oracle_subset",
        "oracle_arbitrary_path",
        "oracle_missing",
        "independent_failed",
        "case_failed",
        "case_missing",
        "case_extra",
        "case_duplicate",
        "case_unknown",
        "input_hash",
        "expected_hash",
        "computed_hash",
        "methods_missing",
    ],
)
def test_validation_requires_current_known_sources_and_all_independent_cases(
    inputs, change
):
    cfg, pilot, validation, preflight = inputs
    independent = validation["independent_checks"]
    if change == "validator_hash":
        validation["validator_source_hashes"][VALIDATOR_SOURCES[0]] = "changed"
    elif change == "validator_subset":
        validation["validator_source_hashes"].pop(VALIDATOR_SOURCES[1])
    elif change == "validator_arbitrary_path":
        validation["validator_source_hashes"] = {"pyproject.toml": "changed"}
    elif change == "validator_missing":
        validation.pop("validator_source_hashes")
    elif change == "oracle_hash":
        independent["source_hashes"][ORACLE_SOURCES[0]] = "changed"
    elif change == "oracle_subset":
        independent["source_hashes"].pop(ORACLE_SOURCES[1])
    elif change == "oracle_arbitrary_path":
        independent["source_hashes"] = {"../../arbitrary.py": "changed"}
    elif change == "oracle_missing":
        independent.pop("source_hashes")
    elif change == "independent_failed":
        independent["passed"] = False
    elif change == "case_failed":
        independent["results"][0]["passed"] = False
    elif change == "case_missing":
        independent["results"].pop()
    elif change == "case_extra":
        independent["results"].append(deepcopy(independent["results"][0]))
    elif change == "case_duplicate":
        independent["results"][-1] = deepcopy(independent["results"][0])
    elif change == "case_unknown":
        independent["results"][0]["problem_id"] = "unknown"
    elif change == "input_hash":
        independent["results"][0]["input_sha256"] = "changed"
    elif change == "expected_hash":
        independent["results"][0]["expected_sha256"] = "changed"
    elif change == "computed_hash":
        independent["results"][0]["computed_sha256"] = "changed"
    else:
        independent["results"][0].pop("methods")
    with pytest.raises(ValueError):
        hops._validated_inputs(cfg, validation)


def test_contract_contains_known_validation_and_oracle_source_hashes(inputs):
    cfg, pilot, validation, preflight = inputs
    manifest = read_json(hops.Path(cfg["corpus_root"]) / "manifest.json")
    contract = hops.build_run_contract(cfg, manifest, preflight["environment"])
    for name, expected in {
        **validation["validator_source_hashes"],
        **validation["independent_checks"]["source_hashes"],
    }.items():
        assert contract["implementation_hashes"].get(name) == expected


@pytest.mark.parametrize("source", [VALIDATOR_SOURCES[0], ORACLE_SOURCES[0]])
def test_changed_known_source_changes_contract_and_blocks_freeze_and_resume(
    inputs, monkeypatch, source
):
    cfg, pilot, validation, preflight = inputs
    cfg["validation"] = str(hops.Path(cfg["corpus_root"]).parent / "validation.json")
    write_json(cfg["validation"], validation)
    contract, root, environment = hops._prepare_campaign(cfg, "pilot")
    pilot["contract_hash"] = contract["contract_hash"]
    real_hashes = hops._source_hashes

    def changed(paths):
        result = real_hashes(paths)
        if source in result:
            result[source] = "changed"
        return result

    monkeypatch.setattr(hops, "_source_hashes", changed)
    current = hops.build_run_contract(
        cfg, read_json(hops.Path(cfg["corpus_root"]) / "manifest.json"), environment
    )
    assert current["contract_hash"] != contract["contract_hash"]
    with pytest.raises(ValueError, match="소스"):
        hops.freeze_main_design(cfg, pilot, validation, preflight)
    with pytest.raises(ValueError, match="소스"):
        hops._prepare_campaign(cfg, "pilot")
