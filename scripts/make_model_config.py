"""Derive a per-model campaign config from a base config, byte-identical elsewhere.

The cross-model comparison in the paper is only valid if every campaign differs in
exactly two places: `llm` and `output_root`. Hand-copying a config per model makes
that impossible to guarantee, so this script derives the file and refuses to write
one that differs anywhere else.

Usage:
    python scripts/make_model_config.py --base fps_v2.yaml \
        --model GLM-5.2 --model-id GLM-5.2 \
        --endpoint https://host/v1 --api-key-env RTT_API_KEY \
        --output fps_v2_glm52.yaml [--pricing-in 0.6 --pricing-out 2.2 --cost-cap 30]
"""
import argparse
import copy
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rttdist.fps_experiment import load_config  # noqa: E402

MUTABLE = ("llm", "output_root")


def slug(text):
    return "".join(ch for ch in text.lower() if ch.isalnum())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="fps_v2.yaml")
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", required=True, help="model name as reported in the paper")
    parser.add_argument("--model-id", required=True, help="model id sent to the API")
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--api-key-env", default="RTT_API_KEY")
    parser.add_argument("--output-root", default=None)
    parser.add_argument("--temperature", type=float, default=None)
    parser.add_argument("--pricing-in", type=float, default=None)
    parser.add_argument("--pricing-out", type=float, default=None)
    parser.add_argument("--pricing-cached", type=float, default=None)
    parser.add_argument("--cost-cap", type=float, default=None)
    args = parser.parse_args()

    base_path = Path(args.base)
    base = yaml.safe_load(base_path.read_text(encoding="utf-8"))
    derived = copy.deepcopy(base)

    derived["output_root"] = args.output_root or f"artifacts-fps-v3-{slug(args.model)}"
    llm = derived["llm"]
    llm["model"] = args.model_id
    llm["expected_model"] = args.model_id
    llm["endpoint"] = args.endpoint
    llm["api_key_env"] = args.api_key_env
    if args.temperature is not None:
        llm.setdefault("generation", {})["temperature"] = args.temperature
    if args.pricing_in is not None or args.pricing_out is not None or args.pricing_cached is not None:
        if args.pricing_in is None or args.pricing_out is None:
            parser.error("--pricing-in and --pricing-out must be given together")
        llm["pricing"] = {"input_per_million": args.pricing_in, "output_per_million": args.pricing_out}
        if args.pricing_cached is not None:
            llm["pricing"]["cached_input_per_million"] = args.pricing_cached
    if args.cost_cap is not None:
        if "pricing" not in llm:
            parser.error("--cost-cap requires pricing")
        llm["cost_cap_usd"] = args.cost_cap

    for key in base:
        if key in MUTABLE:
            continue
        if derived[key] != base[key]:
            parser.error(f"derived config changed protected field {key!r}")

    output = Path(args.output)
    header = (
        f"# Derived from {base_path.name} by scripts/make_model_config.py.\n"
        f"# Model: {args.model} (id {args.model_id}); output_root: {derived['output_root']}.\n"
        f"# Only `llm` and `output_root` differ from the base config.\n"
    )
    output.write_text(header + yaml.safe_dump(derived, allow_unicode=True, sort_keys=False), encoding="utf-8")

    cfg = load_config(output)
    differing = [key for key in base if derived[key] != base[key]]
    print(f"wrote {output}")
    print(f"differing fields: {differing}")
    print(f"routes: {cfg['routes']}  repeats: {cfg['repeats']}  problems: {len(cfg['problem_ids'])}")


if __name__ == "__main__":
    main()
