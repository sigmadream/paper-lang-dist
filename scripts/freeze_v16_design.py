"""파일럿 감사·기준 구현·공급자 근거로 v1.6 본 실험을 동결합니다."""

import argparse

from rttdist.experiment_io import read_json
from rttdist.hops_experiment import (
    campaign_root,
    freeze_main_design,
    load_hops_config,
)


def main(argv=None):
    parser = argparse.ArgumentParser(description="v1.6 본 실험 계약 동결")
    parser.add_argument("--config", required=True)
    parser.add_argument("--provider-config", required=True)
    parser.add_argument("--pilot-audit")
    parser.add_argument("--provider-preflight", required=True)
    args = parser.parse_args(argv)
    try:
        cfg = load_hops_config(args.config, args.provider_config)
        pilot_path = (
            args.pilot_audit or campaign_root(cfg) / "pilot/completion_audit.json"
        )
        design = freeze_main_design(
            cfg,
            read_json(pilot_path),
            read_json(cfg["validation"]),
            read_json(args.provider_preflight),
        )
    except (OSError, ValueError, KeyError) as exc:
        print(f"동결할 수 없습니다: {exc}")
        return 1
    print(f"동결 파일: {campaign_root(cfg) / 'main_design.json'}")
    print(f"계약 해시: {design['contract_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
