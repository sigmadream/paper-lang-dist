import copy
import importlib.util
import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]


def module():
    assert importlib.util.find_spec(
        "rttdist.hops_experiment"
    ), "v1.6 설정 모듈이 필요합니다."
    from rttdist import hops_experiment

    return hops_experiment


def raw_config():
    path = ROOT / "configs/v1.6/experiment.yaml"
    assert path.is_file(), "v1.6 공통 설정이 필요합니다."
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def write_config(tmp_path, value):
    path = tmp_path / "experiment.yaml"
    path.write_text(yaml.safe_dump(value), encoding="utf-8")
    return path


def test_v16_version_and_fixed_counts():
    cfg = module().load_hops_config(ROOT / "configs/v1.6/experiment.yaml")
    assert cfg["experiment_version"] == "rtt-hops-v1.6"
    assert len(cfg["problem_ids"]) == 15
    assert len(cfg["routes"]) == 4
    assert cfg["repeats"] == 5
    assert cfg["max_hops"] == 10
    assert cfg["thresholds"] == [0.8, 0.85, 0.9]
    assert not Path(cfg["validation"]).is_relative_to(Path(cfg["corpus_root"]))
    assert cfg["runtime"]["tools"] == raw_config()["runtime"]["tools"]
    assert cfg["similarity"]["jar_sha256"]


@pytest.mark.parametrize(
    "key,value",
    [
        ("manuscript_version", "v1.5"),
        ("experiment_version", "fps-text-v2"),
        ("schema_version", "observation-v1.5"),
        ("problem_ids", list(range(14))),
        ("problem_ids", list(range(16))),
        ("problem_ids", ["duplicate"] * 15),
        ("max_hops", 9),
        ("max_hops", 12),
        ("threshold", 0.9),
        ("repeats", 4),
        ("confirmation_roundtrips", 2),
        ("runtime", {"fixture_timeout": 6}),
    ],
)
def test_rejects_changed_fixed_conditions(tmp_path, key, value):
    cfg = raw_config()
    cfg[key] = value
    with pytest.raises(ValueError):
        module().load_hops_config(write_config(tmp_path, cfg))


def test_provider_merge_cannot_override_conditions_and_paths_are_relative(tmp_path):
    raw = raw_config()
    path = write_config(tmp_path, raw)
    provider = tmp_path / "provider.yaml"
    provider.write_text(
        yaml.safe_dump(
            {"provider": "mock", "model": "test", "generation": {"seed": 7}}
        ),
        encoding="utf-8",
    )
    cfg = module().load_hops_config(path, provider)
    assert cfg["llm"]["model"] == "test"
    assert cfg["corpus_root"] == str((tmp_path / raw["corpus_root"]).resolve())
    assert cfg["repeats"] == 5
    provider.write_text(yaml.safe_dump({"repeats": 1}), encoding="utf-8")
    with pytest.raises(ValueError):
        module().load_hops_config(path, provider)


def test_contract_changes_with_inputs_and_preserves_missing_effective_settings():
    api = module()
    cfg = api.load_hops_config(ROOT / "configs/v1.6/experiment.yaml")
    first = api.build_run_contract(cfg, {"file_hashes": {"x": "one"}}, {"tools": {}})
    assert first["hashes"]["prompt"]
    assert "hops_reporting.py" in first["implementation_hashes"]
    changed = copy.deepcopy(cfg)
    changed["llm"]["generation"]["temperature"] = 0.2
    second = api.build_run_contract(
        changed, {"file_hashes": {"x": "one"}}, {"tools": {}}
    )
    assert first["contract_hash"] != second["contract_hash"]
    fixture = json.loads(
        (ROOT / "tests/fixtures/contracts/hops_v16.json").read_text(encoding="utf-8")
    )
    assert fixture["schema_version"] == cfg["schema_version"]
    assert fixture["effective_generation"] is None


def test_explicit_provider_argument_is_relative_to_cli_working_directory(
    tmp_path, monkeypatch
):
    folder = tmp_path / "configs"
    folder.mkdir()
    write_config(folder, raw_config())
    provider = tmp_path / "provider.yaml"
    provider.write_text(
        yaml.safe_dump({"provider": "mock", "model": "test"}), encoding="utf-8"
    )
    monkeypatch.chdir(tmp_path)
    cfg = module().load_hops_config("configs/experiment.yaml", "provider.yaml")
    assert cfg["llm"]["model"] == "test"


def test_sdk_config_missing_generation_cannot_inherit_common_defaults(tmp_path):
    config = write_config(tmp_path, raw_config())
    provider = tmp_path / "sdk.yaml"
    provider.write_text(
        yaml.safe_dump(
            {
                "provider": "copilot",
                "protocol": "copilot_sdk",
                "model": "test",
                "generation_profile": {"name": "sdk", "supported_options": []},
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        module().load_hops_config(config, provider)
