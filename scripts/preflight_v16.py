"""v1.6 공급자 설정을 오프라인으로 검사하고 명시한 경우에만 smoke 호출합니다."""

import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
import uuid

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rttdist.experiment_io import write_json
from rttdist.providers import create_provider, ProviderError


def preflight_provider(config, live=False):
    cfg = deepcopy(config.get("llm", config))
    result = {
        "passed": False,
        "live": bool(live),
        "actual_model": None,
        "model_evidence": {"status": "missing", "valid": False},
        "comparison_class": (
            "sdk_exploratory"
            if cfg.get("protocol") == "copilot_sdk" or cfg.get("provider") == "copilot"
            else "direct_api"
        ),
        "generation_profile": cfg.get("generation_profile"),
        "provider": cfg.get("provider"),
        "protocol": cfg.get("protocol"),
        "authentication_checked": False,
        "model_access_checked": False,
    }
    try:
        provider = create_provider(cfg)
        if result["comparison_class"] == "sdk_exploratory":
            from rttdist.copilot_provider import sdk_available, sdk_version, SDK_VERSION

            if not sdk_available():
                raise ValueError(
                    "github-copilot-sdk==0.1.32 선택 의존성이 설치되지 않았습니다"
                )
            if sdk_version() != SDK_VERSION:
                raise ValueError("github-copilot-sdk==0.1.32 버전이 필요합니다")
        result["passed"] = True
        result["reason"] = (
            "정적 설정 검사만 통과했습니다. 인증과 실제 모델은 미검증입니다"
        )
        if live:
            # 반복 점검은 새 smoke 실행으로 분리하며 pilot/main 응답을 재사용하지 않습니다.
            smoke_root = (
                Path(cfg.get("preflight_root", ".test-tmp/v16-preflight"))
                / uuid.uuid4().hex
            )
            smoke_cfg = {
                **cfg,
                "max_calls": 1,
                "max_transport_attempts": 1,
                "retries": 0,
            }
            provider = create_provider(
                smoke_cfg, ledger=smoke_root / "smoke_ledger.jsonl"
            )
            response = provider.complete(
                {
                    "messages": [
                        {"role": "user", "content": "Output only the word OK."}
                    ],
                    "logical_request": {
                        "campaign": smoke_root.name,
                        "phase": "smoke",
                        "problem": "connection",
                        "route": "smoke",
                        "repeat": 1,
                        "step": 1,
                    },
                },
                smoke_root / "request",
            )
            result.update(
                {
                    "passed": True,
                    "actual_model": response["actual_model"],
                    "model_evidence": response["model_evidence"],
                    "comparison_class": response["execution_class"],
                    "authentication_checked": True,
                    "model_access_checked": True,
                    "response_path": response["raw_response_path"],
                    "reason": "명시적으로 요청하신 smoke 호출을 수행했습니다",
                }
            )
            write_json(smoke_root / "preflight.json", result)
    except (ValueError, ProviderError) as exc:
        result.update({"passed": False, "reason": str(exc)})
    return result


def main():
    parser = argparse.ArgumentParser(
        description="v1.6 공급자 정적·명시적 live 사전 점검"
    )
    parser.add_argument("--config", required=True)
    parser.add_argument("--provider-config", required=True)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()
    # 공통 설정의 합성·불변 조건은 core 로더가 검사합니다.
    from rttdist.hops_experiment import load_hops_config

    cfg = load_hops_config(args.config, Path(args.provider_config).resolve())
    result = preflight_provider(cfg["llm"], live=args.live)
    if args.output:
        write_json(args.output, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
