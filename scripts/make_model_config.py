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


def derive_model_config(base, provider_config, model_id, output_root=None):
    """공통 실험 조건을 보존하며 v1.6 공급자 설정을 합성합니다."""
    provider = provider_config.get("llm", provider_config)
    if "llm" in provider_config and set(provider_config) != {"llm"}:
        raise ValueError("공통 실험 조건은 공급자 파일에서 변경할 수 없습니다")
    protected = set(base) - set(MUTABLE)
    if protected & set(provider):
        raise ValueError("공통 protected 설정은 공급자 파일에서 변경할 수 없습니다")
    if not isinstance(model_id, str) or not model_id.strip():
        raise ValueError("명시적인 모델 ID가 필요합니다")
    derived = copy.deepcopy(base)
    derived["llm"] = {**copy.deepcopy(provider), "model": model_id}
    derived["output_root"] = output_root or base.get("output_root", "artifacts-v1.6")
    return derived


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="fps_v2.yaml")
    parser.add_argument("--output", required=True)
    parser.add_argument(
        "--model", required=True, help="model name as reported in the paper"
    )
    parser.add_argument("--model-id", required=True, help="model id sent to the API")
    parser.add_argument("--endpoint")
    parser.add_argument("--provider-config", help="v1.6 공급자 프로파일 yaml")
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
    if args.provider_config:
        if base.get("experiment_version") != "rtt-hops-v1.6":
            parser.error("--provider-config는 v1.6 실험 설정과 함께 사용해 주세요")
        provider = yaml.safe_load(
            Path(args.provider_config).read_text(encoding="utf-8")
        )
        derived = derive_model_config(base, provider, args.model_id, args.output_root)
        llm = derived["llm"]
        if args.endpoint:
            llm["base_url"] = args.endpoint
        if args.temperature is not None:
            llm.setdefault("generation", {})["temperature"] = args.temperature
        if args.pricing_in is not None or args.pricing_out is not None:
            if args.pricing_in is None or args.pricing_out is None:
                parser.error("--pricing-in과 --pricing-out을 함께 지정해 주세요")
            llm["pricing"] = {
                "input_per_million": args.pricing_in,
                "output_per_million": args.pricing_out,
            }
            if args.pricing_cached is not None:
                llm["pricing"]["cached_input_per_million"] = args.pricing_cached
        if args.cost_cap is not None:
            llm["cost_cap_usd"] = args.cost_cap
        from rttdist.providers import create_provider

        create_provider(llm)
        output = Path(args.output)
        output.write_text(
            "# 공통 실험 조건을 보존한 v1.6 모델 설정입니다.\n"
            + yaml.safe_dump(derived, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        print(f"설정 저장: {output}")
        return
    if not args.endpoint:
        parser.error("기존 FPS 설정에는 --endpoint가 필요합니다")
    derived = copy.deepcopy(base)

    derived["output_root"] = args.output_root or f"artifacts-fps-v3-{slug(args.model)}"
    llm = derived["llm"]
    llm["model"] = args.model_id
    llm["expected_model"] = args.model_id
    llm["endpoint"] = args.endpoint
    llm["api_key_env"] = args.api_key_env
    if args.temperature is not None:
        llm.setdefault("generation", {})["temperature"] = args.temperature
    if (
        args.pricing_in is not None
        or args.pricing_out is not None
        or args.pricing_cached is not None
    ):
        if args.pricing_in is None or args.pricing_out is None:
            parser.error("--pricing-in and --pricing-out must be given together")
        llm["pricing"] = {
            "input_per_million": args.pricing_in,
            "output_per_million": args.pricing_out,
        }
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
    output.write_text(
        header + yaml.safe_dump(derived, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    cfg = load_config(output)
    differing = [key for key in base if derived[key] != base[key]]
    print(f"wrote {output}")
    print(f"differing fields: {differing}")
    print(
        f"routes: {cfg['routes']}  repeats: {cfg['repeats']}  problems: {len(cfg['problem_ids'])}"
    )


if __name__ == "__main__":
    main()
