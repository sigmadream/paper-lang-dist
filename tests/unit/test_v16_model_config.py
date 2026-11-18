from copy import deepcopy

import pytest


def test_derive_v16_config_changes_only_provider_and_output():
    from scripts.make_model_config import derive_model_config

    base = {
        "experiment_version": "rtt-hops-v1.6",
        "problem_ids": list(range(15)),
        "routes": [
            ["cpp", "python"],
            ["cpp", "java"],
            ["cpp", "haskell"],
            ["cpp", "prolog"],
        ],
        "thresholds": [0.8, 0.85, 0.9],
        "max_hops": 10,
        "llm": {},
        "output_root": "old",
    }
    original = deepcopy(base)
    derived = derive_model_config(
        base,
        {
            "provider": "openai",
            "protocol": "responses",
            "base_url": "https://api.openai.com/v1",
            "model": None,
        },
        "chosen",
        "new",
    )
    assert {
        key: value
        for key, value in derived.items()
        if key not in ("llm", "output_root")
    } == {
        key: value for key, value in base.items() if key not in ("llm", "output_root")
    }
    assert derived["llm"]["model"] == "chosen" and derived["output_root"] == "new"
    assert base == original
    with pytest.raises(ValueError, match="protected|공통"):
        derive_model_config(base, {"model": "test", "max_hops": 2}, "chosen")
