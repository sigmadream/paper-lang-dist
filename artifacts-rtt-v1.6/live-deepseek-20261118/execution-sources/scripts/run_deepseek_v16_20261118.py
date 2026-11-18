"""DeepSeek 대체 캠페인을 오프라인으로 준비하고 명시적 실행만 허용합니다."""

import argparse
from contextlib import contextmanager
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import json
import os
from pathlib import Path
import shutil
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from rttdist import hops_experiment as core
from rttdist.experiment_io import digest, read_json, timestamp, write_json
from rttdist.providers import (
    APIProvider,
    create_provider as real_provider_factory,
    file_lock,
)
from scripts.integration_commandcode import evaluation_environment, secret_audit

OUTPUT = ROOT / "artifacts-rtt-v1.6/live-deepseek-20261118"
CAMPAIGN_ID = "commandcode-deepseek_v4_pro-v16-20261118"
MODEL_ID = "deepseek/deepseek-v4-pro"
GENERATION = {"max_tokens": 16384, "reasoning_effort": "low"}
PHASES = {
    "preflight": {
        "max_calls": 1,
        "max_transport_attempts": 1,
        "cost_cap_usd": 0.24,
        "max_request_cost_usd": 0.12,
        "retries": 0,
    },
    "pilot": {
        "max_calls": 144,
        "max_transport_attempts": 432,
        "cost_cap_usd": 49.62,
        "max_request_cost_usd": 0.25,
        "retries": 2,
    },
    "main": {
        "max_calls": 3600,
        "max_transport_attempts": 10800,
        "cost_cap_usd": 49.32,
        "max_request_cost_usd": 0.25,
        "retries": 2,
    },
}


def assert_destination(path):
    expected = (ROOT / "artifacts-rtt-v1.6/live-deepseek-20261118").resolve()
    if OUTPUT.resolve() != expected or not Path(path).resolve().is_relative_to(
        expected
    ):
        raise ValueError("새 캠페인 전용 경로 밖에는 기록할 수 없습니다")


def phase_settings(config, phase):
    if phase not in PHASES:
        raise ValueError("지정한 실험 단계만 허용합니다")
    return {**deepcopy(config), **PHASES[phase]}


@contextmanager
def clean_execution_environment():
    with evaluation_environment():
        yield


class IsolatedProvider:
    def __init__(self, provider, token):
        self.provider = provider
        self.token = token

    def complete(self, payload, folder):
        assert_destination(folder)
        assert_sources()
        if "CMD_API_KEY" in os.environ:
            raise ValueError("호출 전 인증 환경 격리가 필요합니다")
        os.environ["CMD_API_KEY"] = self.token
        try:
            return self.provider.complete(payload, folder)
        finally:
            os.environ.pop("CMD_API_KEY", None)


def config_paths():
    return (
        ROOT / "configs/v1.6/campaigns/commandcode_deepseek_v4_pro_20261118.yaml",
        ROOT / "configs/v1.6/providers/commandcode_deepseek_v4_pro_20261118.yaml",
    )


def load_config():
    cfg = core.load_hops_config(*config_paths())
    assert_destination(core.campaign_root(cfg))
    llm = cfg["llm"]
    if (
        Path(cfg["output_root"]).resolve() != OUTPUT.resolve()
        or cfg["campaign_id"] != CAMPAIGN_ID
        or llm.get("provider") != "compatible"
        or llm.get("protocol") != "chat_completions"
        or llm.get("model") != MODEL_ID
        or llm.get("allowed_response_models") != []
        or llm.get("base_url") != "https://api.commandcode.ai/provider/v1"
        or llm.get("request_path") != "/chat/completions"
        or llm.get("generation") != GENERATION
        or llm.get("max_input_tokens") != 32768
        or cfg.get("phase_budget_policy") != PHASES
        or cfg.get("budget")
        != {
            "max_logical_requests": 3600,
            "max_transport_attempts": 10800,
            "cost_cap_usd": 49.32,
        }
    ):
        raise ValueError("DeepSeek 전용 설정·경로·단계 한도가 다릅니다")
    if any(llm.get(k) != v for k, v in PHASES["main"].items()):
        raise ValueError("본 실험 공급자 예산이 다릅니다")
    wrapper = cfg.get("execution_wrapper", {})
    if wrapper.get("path") != "scripts/run_deepseek_v16_20261118.py" or wrapper.get(
        "sha256"
    ) != digest(Path(__file__).read_bytes()):
        raise ValueError("새 래퍼 해시가 설정과 다릅니다")
    return cfg


def record_event(event, **values):
    assert_destination(OUTPUT)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    entry = {"at": timestamp(), "event": event, **values}
    with (OUTPUT / "progress.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(entry, ensure_ascii=False) + "\n")
    write_json(OUTPUT / "status.json", entry)
    print(json.dumps(entry, ensure_ascii=False), flush=True)


def legacy_paths():
    old = ROOT / "artifacts-rtt-v1.6/live-commandcode-20261117"
    return [
        ROOT / "scripts/run_commandcode_v16.py",
        *(
            ROOT / f"configs/v1.6/campaigns/commandcode_{m}_20261117.yaml"
            for m in ("glm53", "deepseek_v4_pro")
        ),
        *(
            ROOT / f"configs/v1.6/providers/commandcode_{m}_experiment.yaml"
            for m in ("glm53", "deepseek_v4_pro")
        ),
        old / "source-manifest.json",
        old / "incident-524.json",
        *old.glob("commandcode-*/main_design.json"),
        *old.glob("commandcode-*/*/provider_ledger.jsonl"),
        *old.glob("commandcode-*/*/provider_ledger.jsonl.state.json"),
    ]


def assert_sources():
    assert_destination(OUTPUT)
    manifest = read_json(OUTPUT / "source-manifest.json")
    for name, expected in manifest["files"].items():
        for path in (ROOT / name, OUTPUT / "execution-sources" / name):
            if not path.is_file() or digest(path.read_bytes()) != expected:
                raise ValueError("준비한 실행 소스·설정·사본이 변경되었습니다: " + name)
    for name, expected in manifest.get("legacy_hashes", {}).items():
        path = ROOT / name
        if not path.is_file() or digest(path.read_bytes()) != expected:
            raise ValueError("보존한 기존 캠페인 근거가 변경되었습니다: " + name)
    return manifest


def prepare():
    with (
        clean_execution_environment(),
        patch(
            "socket.getaddrinfo",
            side_effect=RuntimeError("오프라인 준비 중 DNS는 금지됩니다"),
        ),
        patch(
            "socket.socket.connect",
            side_effect=RuntimeError("오프라인 준비 중 네트워크는 금지됩니다"),
        ),
    ):
        return prepare_offline()


def prepare_offline():
    assert_destination(OUTPUT)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if (OUTPUT / "source-manifest.json").exists():
        return assert_sources()
    cfg = load_config()
    validation = read_json(cfg["validation"])
    data = core._validated_inputs(cfg, validation)
    environment = core.collect_hops_environment(cfg)
    core._check_validation_environment(validation, environment)
    bound = (32768 * 1.32 + 16384 * 3.96) / 1e6
    for phase in PHASES:
        provider = real_provider_factory(phase_settings(cfg["llm"], phase))
        if (
            not isinstance(provider, APIProvider)
            or provider.maximum_request_cost() < bound
        ):
            raise ValueError(
                "v1.6 공급자 경로 또는 보수적 요청 예약을 확인할 수 없습니다"
            )
    old = read_json(
        ROOT / "artifacts-rtt-v1.6/live-commandcode-20261117/incident-524.json"
    )
    deep_old = sum(
        Decimal(p["conservative_spent_plus_reserved_usd"])
        for p in old["models"]["deepseek_v4_pro"]["phases"].values()
    )
    new_cap = sum(Decimal(str(p["cost_cap_usd"])) for p in PHASES.values())
    allocated_bound = Decimal("100.25") + deep_old + new_cap
    if allocated_bound > Decimal("200.50"):
        raise ValueError("기존 실행·불명 예약을 포함한 전체 비용 상한을 넘습니다")
    files = {
        *ROOT.glob("src/rttdist/**/*.py"),
        *config_paths(),
        Path(__file__),
        ROOT / "tests/integration/test_deepseek_restart_runner.py",
        ROOT / "scripts/integration_commandcode.py",
        ROOT / "scripts/report_v16.py",
        ROOT / "scripts/verify_v16_reproducibility.py",
        *(ROOT / name for name in (*core.VALIDATOR_SOURCES, *core.INDEPENDENT_SOURCES)),
        ROOT / "configs/v1.6/experiment.yaml",
        ROOT / "pyproject.toml",
        ROOT / "uv.lock",
        Path(cfg["selection"]),
        Path(cfg["validation"]),
        Path(cfg["corpus_root"]) / "manifest.json",
    }
    hashes = {}
    for path in sorted(p.resolve() for p in files):
        name = path.relative_to(ROOT).as_posix()
        hashes[name] = digest(path.read_bytes())
        destination = OUTPUT / "execution-sources" / name
        assert_destination(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, destination)
    manifest = {
        "created_at": timestamp(),
        "offline_preparation_passed": True,
        "live_execution_started": False,
        "independent_review": "유료 실행 전 필수 기술 검토이며 현재 미확인입니다",
        "campaign_id": CAMPAIGN_ID,
        "files": hashes,
        "legacy_hashes": {
            p.relative_to(ROOT).as_posix(): digest(p.read_bytes())
            for p in legacy_paths()
        },
        "environment": environment,
        "proposed_contract_hash": core.build_run_contract(cfg, data, environment)[
            "contract_hash"
        ],
        "phase_budget_policy": PHASES,
        "maximum_total_cost_cap_usd": 200.50,
        "new_total_cost_cap_usd": str(new_cap),
        "old_deepseek_spent_plus_reserved_usd": str(deep_old),
        "conservative_allocated_total_usd": str(allocated_bound),
        "peak_request_price_bound_usd": bound,
        "provider_class": "APIProvider",
        "preflight_count": {"prior_campaign": 1, "new_campaign": 1, "new_executed": 0},
        "call_limits_scope": "새 계획 캠페인별 한도이며 기존 중단 캠페인은 별도 공개합니다",
    }
    write_json(OUTPUT / "source-manifest.json", manifest)
    assert_sources()
    record_event("offline_preparation_complete", files=len(hashes), live=False)
    return manifest


def assert_no_unknown_requests():
    campaign = OUTPUT / CAMPAIGN_ID
    for path in campaign.glob("*/provider_ledger.jsonl.state.json"):
        for value in read_json(path)["requests"].values():
            if value.get("status") in ("inflight", "unknown") or value.get(
                "uncertain_reserved_usd"
            ):
                raise ValueError(
                    "새 캠페인에 결과 불명 요청이 있어 자동 재생성을 차단합니다"
                )


def require_review(path):
    if not path:
        raise ValueError("공급자 수정의 독립 검토 근거가 필요합니다")
    evidence = read_json(path)
    if evidence.get("passed") is not True or not evidence.get("reviewer"):
        raise ValueError("독립 검토 통과 근거가 필요합니다")
    report = (ROOT / evidence.get("report_path", "")).resolve()
    sources = evidence.get("source_hashes", {})
    if (
        not report.is_relative_to(ROOT.resolve())
        or not report.is_file()
        or digest(report.read_bytes()) != evidence.get("report_sha256")
        or "src/rttdist/providers.py" not in sources
        or any(
            not (ROOT / name).resolve().is_relative_to(ROOT.resolve())
            or not (ROOT / name).is_file()
            or digest((ROOT / name).read_bytes()) != expected
            for name, expected in sources.items()
        )
    ):
        raise ValueError("독립 검토 보고서 또는 검토한 소스 해시가 다릅니다")
    return evidence


def assert_live_date():
    if datetime.now(timezone(timedelta(hours=9))).date() < date(2026, 11, 18):
        raise ValueError("2026-11-17에는 유료 실행을 금지합니다")


def preflight(cfg, token):
    root = core.campaign_root(cfg)
    assert_destination(root)
    path = root / "preflight.json"
    if path.exists():
        saved = read_json(path)
        if saved.get("passed") is not True or saved.get("actual_model") != MODEL_ID:
            raise ValueError("실패한 사전 점검을 새 생성으로 덮어쓰지 않습니다")
        return saved
    folder = root / "preflight"
    provider = IsolatedProvider(
        real_provider_factory(
            phase_settings(cfg["llm"], "preflight"), folder / "provider_ledger.jsonl"
        ),
        token,
    )
    response = provider.complete(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Return exactly OK, with no additional text.",
                }
            ],
            "logical_request": {
                "campaign": CAMPAIGN_ID,
                "phase": "preflight",
                "problem": "authentication",
                "route": "preflight",
                "repeat": 1,
                "step": 0,
            },
        },
        folder / "request",
    )
    result = {
        "passed": response["text"].strip() == "OK"
        and response["model_evidence"]["status"] == "exact",
        "live": True,
        "comparison_class": "direct_api",
        "generation_profile": cfg["llm"]["generation_profile"],
        **{
            k: response[k]
            for k in (
                "actual_model",
                "model_evidence",
                "requested_generation",
                "sent_generation",
                "effective_generation",
                "cost_usd",
                "cost_source",
                "raw_response_path",
                "request_id",
            )
        },
    }
    write_json(path, result)
    if not result["passed"]:
        raise ValueError("새 캠페인의 사전 점검을 통과하지 못했습니다")
    record_event("preflight_complete", actual_model=result["actual_model"])
    return result


@contextmanager
def installed_hooks(token):
    original_factory = core.create_provider
    original_observation = core.run_hops_observation

    def factory(config, ledger=None):
        assert_destination(ledger)
        phase = Path(ledger).parent.name
        provider = real_provider_factory(phase_settings(config, phase), ledger)
        if not isinstance(provider, APIProvider):
            raise ValueError("v1.6 APIProvider만 허용합니다")
        return IsolatedProvider(provider, token)

    def observation(cfg, job, provider, folder):
        assert_destination(folder)
        assert_sources()
        value = original_observation(cfg, job, provider, folder)
        count = len(
            list(
                (OUTPUT / CAMPAIGN_ID / job["phase"]).glob(
                    "*/*/attempt-*/observation.json"
                )
            )
        )
        record_event(
            "slot_complete",
            phase=job["phase"],
            saved=count,
            problem=job["problem_id"],
            route=job["route"],
            repeat=job["repeat"],
        )
        if job["phase"] == "main" and count % 75 == 0:
            record_event("main_milestone", saved=count, planned=300)
        assert_no_unknown_requests()
        return value

    core.create_provider = factory
    core.run_hops_observation = observation
    try:
        yield
    finally:
        core.create_provider = original_factory
        core.run_hops_observation = original_observation


def reproduce(cfg):
    from scripts.verify_v16_reproducibility import verify_v16_reproducibility

    return verify_v16_reproducibility(cfg, None)


def execute(token):
    assert_sources()
    cfg = load_config()
    assert_no_unknown_requests()
    with installed_hooks(token):
        checked = preflight(cfg, token)
        core.run_hops_campaign(cfg, "pilot")
        pilot = read_json(core.campaign_root(cfg) / "pilot/completion_audit.json")
        record_event("pilot_complete", audit=pilot)
        design = core.freeze_main_design(
            cfg, pilot, read_json(cfg["validation"]), checked
        )
        record_event("freeze_complete", contract_hash=design["contract_hash"])
        core.run_hops_campaign(cfg, "main")
        assert_sources()
        summary = core.report_hops_campaign(cfg, "main")
        reproduced = reproduce(cfg)
        record_event(
            "report_complete",
            complete_by_threshold=summary["complete_by_threshold"],
            reproducibility=reproduced["passed"],
        )
    return 0


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--prepare", action="store_true")
    mode.add_argument("--run", action="store_true")
    parser.add_argument("--review-evidence")
    args = parser.parse_args(argv)
    assert_destination(OUTPUT)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with file_lock(OUTPUT / "execution.lock", blocking=False):
        if not args.run:
            prepare()
            return 0
        assert_live_date()
        manifest = assert_sources()
        review = require_review(args.review_evidence)
        cfg = load_config()
        assert_no_unknown_requests()
        token = os.environ.pop("CMD_API_KEY", None)
        if not token:
            raise ValueError("명시한 실행 프로세스에 CMD_API_KEY가 필요합니다")
        with clean_execution_environment():
            write_json(
                OUTPUT / "execution-evidence.json",
                {
                    "at": timestamp(),
                    "source_manifest_sha256": digest(manifest),
                    "review_evidence": review,
                    "campaign_id": cfg["campaign_id"],
                },
            )
            try:
                return execute(token)
            except Exception as exc:
                record_event(
                    "execution_blocked",
                    exception_type=type(exc).__name__,
                    observations_preserved=True,
                )
                raise SystemExit(
                    "실행을 중지하였습니다. 저장한 관측·원장과 단계 로그를 확인해 주십시오"
                ) from None
            finally:
                passed = secret_audit(OUTPUT, token)
                write_json(
                    OUTPUT / "secret-audit.json", {"passed": passed, "at": timestamp()}
                )
                if not passed:
                    raise SystemExit(
                        "비밀정보 저장 감사를 통과하지 못하여 중지하였습니다"
                    )


if __name__ == "__main__":
    raise SystemExit(main())
