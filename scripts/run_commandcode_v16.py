"""동결된 실행 명세로 두 Command Code 캠페인을 직렬 수행합니다."""

import argparse
from contextlib import contextmanager
from copy import deepcopy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from rttdist import hops_experiment as core
from rttdist.experiment_io import digest, read_json, timestamp, write_json
from rttdist.providers import create_provider as real_provider_factory, file_lock
from scripts.integration_commandcode import evaluation_environment, secret_audit

OUTPUT = ROOT / "artifacts-rtt-v1.6/live-commandcode-20261117"
ORCA = Path("C:/Users/sigma/AppData/Local/Programs/orca/resources/bin/orca.exe")
SENDER = "orca_session_id:214186a0-6f74-42a4-a8b7-99544ce78c9c"
TASK_ID = "task_53f0881763e3"
DISPATCH_ID = "ctx_975659451552"
MODELS = {
    "glm53": {
        "id": "zai-org/GLM-5.3",
        "pricing": {
            "input_per_million": 1.40,
            "output_per_million": 4.40,
            "cached_input_per_million": 0.26,
        },
        "generation": {
            "temperature": 0.6,
            "top_p": 0.95,
            "max_tokens": 16384,
            "reasoning_effort": "low",
        },
    },
    "deepseek_v4_pro": {
        "id": "deepseek/deepseek-v4-pro",
        "pricing": {
            "input_per_million": 1.32,
            "output_per_million": 3.96,
            "cached_input_per_million": 0.044,
        },
        "generation": {"max_tokens": 16384, "reasoning_effort": "low"},
    },
}


@contextmanager
def clean_execution_environment():
    with evaluation_environment():
        yield


class IsolatedProvider:
    def __init__(self, provider, token):
        self.provider = provider
        self.token = token

    def complete(self, payload, folder):
        if "CMD_API_KEY" in os.environ:
            raise ValueError("API 호출 전 인증 환경이 격리되지 않았습니다")
        os.environ["CMD_API_KEY"] = self.token
        try:
            return self.provider.complete(payload, folder)
        finally:
            os.environ.pop("CMD_API_KEY", None)


def phase_settings(config, phase):
    config = deepcopy(config)
    if phase == "preflight":
        config.update(
            max_calls=1, max_transport_attempts=1, cost_cap_usd=0.25, retries=0
        )
    elif phase == "pilot":
        config.update(
            max_calls=144, max_transport_attempts=432, cost_cap_usd=50, retries=2
        )
    elif phase == "main":
        config.update(
            max_calls=3600, max_transport_attempts=10800, cost_cap_usd=50, retries=2
        )
    else:
        raise ValueError("승인되지 않은 실행 단계입니다")
    if config.get("max_request_cost_usd") != 0.25:
        raise ValueError("요청별 최대 비용 예약은 0.25달러여야 합니다")
    return config


def paths_for(model):
    return (
        ROOT / f"configs/v1.6/campaigns/commandcode_{model}_20261117.yaml",
        ROOT / f"configs/v1.6/providers/commandcode_{model}_experiment.yaml",
    )


def log_event(event, **values):
    entry = {"at": timestamp(), "event": event, **values}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with (OUTPUT / "progress.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(entry, ensure_ascii=False) + "\n")
    write_json(OUTPUT / "status.json", entry)
    print(json.dumps(entry, ensure_ascii=False), flush=True)


def notify(event, model, body, blocked=False):
    path = OUTPUT / "notifications.json"
    saved = read_json(path) if path.exists() else {}
    key = model + "/" + event
    if key in saved:
        return
    command = [
        str(ORCA),
        "orchestration",
        "send",
        "--from",
        SENDER,
        "--type",
        "escalation" if blocked else "status",
        "--subject",
        f"{model}: {event}",
        "--body",
        body,
        "--task-id",
        TASK_ID,
        "--dispatch-id",
        DISPATCH_ID,
    ]
    proc = subprocess.run(
        command,
        capture_output=True,
        timeout=30,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    saved[key] = {"at": timestamp(), "exit_code": proc.returncode}
    write_json(path, saved)
    log_event(
        "coordinator_notification",
        model=model,
        milestone=event,
        exit_code=proc.returncode,
    )


def assert_sources():
    manifest = read_json(OUTPUT / "source-manifest.json")
    changed = [
        name
        for name, expected in manifest["files"].items()
        if not (ROOT / name).is_file() or digest((ROOT / name).read_bytes()) != expected
    ]
    if changed:
        raise ValueError(
            "동결한 실행 소스·설정이 변경되었습니다: " + ", ".join(changed)
        )


def prepare():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if (OUTPUT / "source-manifest.json").exists():
        assert_sources()
        return read_json(OUTPUT / "source-manifest.json")
    base = core.load_hops_config(ROOT / "configs/v1.6/experiment.yaml")
    wrapper = {
        "path": "scripts/run_commandcode_v16.py",
        "sha256": digest(Path(__file__).read_bytes()),
        "authentication_policy": "키는 메모리에 보관하고 provider.complete 동안에만 주입하며 평가·JPlag는 허용 목록 환경으로 수행합니다",
        "serial_execution": True,
    }
    files = [
        *ROOT.glob("src/rttdist/*.py"),
        *(ROOT / "src/rttdist").glob("**/*.py"),
        ROOT / "scripts/run_commandcode_v16.py",
        ROOT / "scripts/integration_commandcode.py",
        ROOT / "scripts/report_v16.py",
        ROOT / "scripts/verify_v16_reproducibility.py",
        ROOT / "scripts/prepare_v16_corpus.py",
        ROOT / "scripts/validate_v16_corpus.py",
        ROOT / "pyproject.toml",
        ROOT / "uv.lock",
        ROOT / base["selection"],
        ROOT / base["validation"],
        Path(base["corpus_root"]) / "manifest.json",
        *(ROOT / name for name in core.INDEPENDENT_SOURCES),
    ]
    checks = {}
    for model, spec in MODELS.items():
        config_path, provider_path = paths_for(model)
        provider = {
            "provider": "compatible",
            "protocol": "chat_completions",
            "base_url": "https://api.commandcode.ai/provider/v1",
            "request_path": "/chat/completions",
            "auth": {"type": "bearer", "api_key_env": "CMD_API_KEY"},
            "model": spec["id"],
            "allowed_response_models": [],
            "generation_profile": {
                "name": f"commandcode-{model}-v16-low-16384",
                "supported_options": list(spec["generation"]),
                "option_values": {"reasoning_effort": ["low"]},
            },
            "generation": spec["generation"],
            "request_timeout": 180,
            "retries": 2,
            "max_calls": 3600,
            "max_transport_attempts": 10800,
            "cost_cap_usd": 50,
            "max_request_cost_usd": 0.25,
            "max_input_tokens": 32768,
            "pricing": spec["pricing"],
        }
        cfg = deepcopy(base)
        cfg.update(
            output_root=str(OUTPUT),
            campaign_id=f"commandcode-{model}-v16-20261117",
            profile_id=provider["generation_profile"]["name"],
            provider_config=str(provider_path),
            llm={},
            execution_wrapper=wrapper,
            phase_budget_policy={
                "preflight": {
                    "max_calls": 1,
                    "max_transport_attempts": 1,
                    "cost_cap_usd": 0.25,
                },
                "pilot": {
                    "max_calls": 144,
                    "max_transport_attempts": 432,
                    "cost_cap_usd": 50,
                },
                "main": {
                    "max_calls": 3600,
                    "max_transport_attempts": 10800,
                    "cost_cap_usd": 50,
                },
            },
        )
        cfg["budget"] = {
            "max_logical_requests": 3600,
            "max_transport_attempts": 10800,
            "cost_cap_usd": 50,
        }
        config_path.parent.mkdir(parents=True, exist_ok=True)
        provider_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(
            "# 승인된 실제 실험 전용 설정이며 공통 판정 조건을 유지합니다.\n"
            + yaml.safe_dump(cfg, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        provider_path.write_text(
            "# 본 실험 전용입니다. 기존 연동 점검 응답을 재사용하지 않습니다.\n"
            + yaml.safe_dump(provider, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        loaded = core.load_hops_config(config_path, provider_path)
        validation = read_json(loaded["validation"])
        manifest = core._validated_inputs(loaded, validation)
        environment = core.collect_hops_environment(loaded)
        core._check_validation_environment(validation, environment)
        provider_instance = real_provider_factory(provider)
        maximum = provider_instance.maximum_request_cost()
        pricing_bound = (
            32768 * provider["pricing"]["input_per_million"]
            + 16384 * provider["pricing"]["output_per_million"]
        ) / 1e6
        if maximum != 0.25 or pricing_bound > 0.25:
            raise ValueError("요청 예약이 공식 단가의 최대 입출력을 덮지 못합니다")
        checks[model] = {
            "passed": True,
            "environment": environment,
            "validation_sha256": digest(Path(loaded["validation"]).read_bytes()),
            "manifest_sha256": digest(manifest),
            "contract_hash": core.build_run_contract(loaded, manifest, environment)[
                "contract_hash"
            ],
            "maximum_request_reservation_usd": maximum,
            "price_bound_usd": pricing_bound,
            "disk_free_bytes": shutil.disk_usage(OUTPUT).free,
        }
        files.extend([config_path, provider_path])
    snapshots = OUTPUT / "execution-sources"
    hashes = {}
    for path in sorted(set(path.resolve() for path in files)):
        name = path.relative_to(ROOT).as_posix()
        hashes[name] = digest(path.read_bytes())
        destination = snapshots / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, destination)
    result = {
        "created_at": timestamp(),
        "files": hashes,
        "checks": checks,
        "wrapper": wrapper,
        "maximum_total_cost_cap_usd": 200.50,
        "command": "uv run --env-file C:/Users/sigma/works/paper-lang-dist/.env --no-sync python scripts/run_commandcode_v16.py --run",
    }
    write_json(OUTPUT / "source-manifest.json", result)
    log_event(
        "preparation_complete",
        models=list(MODELS),
        source_files=len(hashes),
        maximum_total_cost_cap_usd=200.50,
    )
    return result


def preflight(model, cfg, token):
    path = core.campaign_root(cfg) / "preflight.json"
    if path.exists():
        saved = read_json(path)
        if saved.get("passed") is True:
            return saved
        raise ValueError(
            "기존 사전 점검이 통과하지 못했습니다. 새 생성으로 덮어쓰지 않습니다"
        )
    folder = core.campaign_root(cfg) / "preflight"
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
                "campaign": cfg["campaign_id"],
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
        and response["model_evidence"]["valid"],
        "live": True,
        "actual_model": response["actual_model"],
        "model_evidence": response["model_evidence"],
        "comparison_class": "direct_api",
        "generation_profile": cfg["llm"]["generation_profile"],
        "requested_generation": response["requested_generation"],
        "sent_generation": response["sent_generation"],
        "effective_generation": response["effective_generation"],
        "cost_usd": response["cost_usd"],
        "cost_source": response["cost_source"],
        "raw_response_path": response["raw_response_path"],
        "request_id": response["request_id"],
        "at": timestamp(),
    }
    write_json(path, result)
    if not result["passed"]:
        raise ValueError("새 생성 프로파일의 사전 점검이 통과하지 못했습니다")
    notify(
        "preflight_complete",
        model,
        f"새 본 실험 프로파일로 실제 사전 점검을 통과했습니다. 응답 모델은 {result['actual_model']}이며 기존 연동 점검 캐시를 사용하지 않았습니다.",
    )
    log_event("preflight_complete", model=model, actual_model=result["actual_model"])
    return result


def install_hooks(token):
    original_observation = core.run_hops_observation
    counters = {}

    def factory(config, ledger=None):
        phase = Path(ledger).parent.name
        return IsolatedProvider(
            real_provider_factory(phase_settings(config, phase), ledger=ledger), token
        )

    def observation(cfg, job, provider, folder):
        assert_sources()
        record = original_observation(cfg, job, provider, folder)
        key = (job["campaign_id"], job["phase"])
        counters[key] = counters.get(key, 0) + 1
        count = counters[key]
        model = (
            "glm53"
            if job["campaign_id"].startswith("commandcode-glm53-")
            else "deepseek_v4_pro"
        )
        log_event(
            "slot_complete",
            model=model,
            phase=job["phase"],
            completed=count,
            problem_id=job["problem_id"],
            route=job["route"],
            repeat=job["repeat"],
            outcomes={k: v["category"] for k, v in record["outcomes"].items()},
            translation_steps=record["translation_steps"],
            reason=record.get("reason"),
        )
        if job["phase"] == "main" and count % 75 == 0:
            notify(
                f"main_{count:03}",
                model,
                f"본 실험 계획 300슬롯 중 {count}슬롯의 관측 저장을 완료했습니다. 기능 실패와 인프라 중단을 그대로 보존하며 임계치별 완전성은 최종 감사에서 확인합니다.",
            )
        return record

    core.create_provider = factory
    core.run_hops_observation = observation


def ledger_summary(root):
    totals = {
        "logical_requests": 0,
        "transport_attempts": 0,
        "estimated_cost_usd": 0.0,
        "reported_cost_usd": None,
        "unknown_cost_requests": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
    }
    for path in Path(root).glob("*/provider_ledger.jsonl.state.json"):
        state = read_json(path)
        totals["logical_requests"] += len(state["requests"])
        totals["transport_attempts"] += len(state["attempts"])
        for entry in state["requests"].values():
            cost = entry.get("cost_usd")
            if cost is None:
                totals["unknown_cost_requests"] += 1
            elif entry.get("cost_source") in ("estimated", "provider_estimated"):
                totals["estimated_cost_usd"] += cost
            elif entry.get("cost_source") == "reported":
                totals["reported_cost_usd"] = (totals["reported_cost_usd"] or 0) + cost
            for name in ("prompt_tokens", "completion_tokens"):
                totals[name] += (entry.get("usage") or {}).get(name) or 0
    return totals


def write_final_report():
    rows = []
    summaries = {}
    for model in MODELS:
        config_path, provider_path = paths_for(model)
        cfg = core.load_hops_config(config_path, provider_path)
        root = core.campaign_root(cfg)
        entry = {
            "campaign_id": cfg["campaign_id"],
            "campaign_path": str(root),
            "generation": cfg["llm"]["generation"],
            "phases": {},
            "ledger": ledger_summary(root),
        }
        for phase, planned in (("pilot", 12), ("main", 300)):
            path = root / phase / "completion_audit.json"
            audit = (
                read_json(path)
                if path.exists()
                else {
                    "observation_count": len(
                        list((root / phase).glob("*/*/attempt-*/observation.json"))
                    ),
                    "planned": planned,
                    "passed": False,
                    "complete_by_threshold": {},
                }
            )
            entry["phases"][phase] = audit
            rows.append(
                f"| {model} | {phase} | {audit['observation_count']}/{planned} | {audit.get('passed', False)} | {json.dumps(audit.get('complete_by_threshold', {}), ensure_ascii=False)} |"
            )
        summary_path = root / "main/summary.json"
        if summary_path.exists():
            main_summary = read_json(summary_path)
            entry["primary_routes"] = {
                route: {
                    key: values.get(key)
                    for key in ("P", "H", "D", "valid", "successes")
                }
                for route, values in main_summary["routes"].items()
            }
            entry["recursive_groups"] = main_summary.get("recursive_groups")
            reproduction = root / "main/report/reproducibility.json"
            entry["reproducibility"] = (
                read_json(reproduction) if reproduction.exists() else None
            )
        blocker = root / "blocker.json"
        if blocker.exists():
            entry["blocker"] = read_json(blocker)
        summaries[model] = entry
    write_json(
        OUTPUT / "summary.json",
        {
            "models": summaries,
            "maximum_total_cost_cap_usd": 200.50,
            "updated_at": timestamp(),
        },
    )
    text = (
        "# Command Code 두 모델 실제 실험 실행 보고\n\n실제 저장 관측과 감사 결과만 집계합니다. 300슬롯 수집 종료와 임계치별 완전성은 구분합니다.\n\n| 모델 | 단계 | 실제/계획 슬롯 | 구조 감사 | 임계치별 완전성 |\n|---|---|---|---|---|\n"
        + "\n".join(rows)
        + "\n\n## 생성 조건과 계약\n\nGLM은 temperature 0.6·top_p 0.95·출력 상한 16384·reasoning_effort low를 요청합니다. DeepSeek는 공식 추론 모드의 sampling 옵션 무시 제약에 따라 출력 상한 16384·reasoning_effort low만 요청합니다. 두 모델 모두 seed 지원 근거가 없어 전달하지 않으며 실효 설정 미보고는 null입니다. 따라서 모델별 별도 프로파일이며 동일한 low를 동일한 실제 추론량으로 주장하지 않습니다.\n\n지원 근거·조회일은 execution-plan.md와 sources.json, 동결 소스·설정·환경·자료 근거는 source-manifest.json과 execution-sources/에 있습니다. 본 실험 계약과 캠페인 원자료는 모델별 캠페인 디렉터리에 보존합니다. 기존 smoke 응답을 재사용하지 않습니다.\n\n## 비용과 사용량\n\n모델별 preflight 상한 0.25달러, pilot와 main 상한 각각 50달러로 전체 중단 상한은 200.50달러입니다. 단가에 따른 추정값과 실제 청구 보고값을 구분하며 미보고 청구액은 null입니다. 단계별 원장과 응답 사용량을 그대로 보존합니다.\n\n```json\n"
        + json.dumps(summaries, ensure_ascii=False, indent=2)
        + "\n```\n\n## 실행과 한계\n\n실행 명령은 `uv run --env-file C:/Users/sigma/works/paper-lang-dist/.env --no-sync python scripts/run_commandcode_v16.py --run`입니다. 키는 하위 프로세스 메모리에만 보관하고 공급자 호출 직후 환경에서 제거하며 평가·JPlag에는 전달하지 않습니다. 진행·명령 종료 상태는 progress.jsonl과 run.log에 보관합니다. 각 본 실험의 공식 보고 디렉터리에 주 임계치 P/H/D, 민감도, 확인, 재귀군과 원자료 근거를 제공합니다.\n\n차단 사유가 있으면 해당 campaign의 blocker.json에 실제 근거를 남깁니다. 무효 슬롯을 교체하거나 실패 관측을 삭제하지 않으며 파일럿의 모든 임계치가 완전하지 않으면 본 실험을 동결하지 않습니다.\n"
    )
    (OUTPUT / "report.md").write_text(text, encoding="utf-8")
    return summaries


def run(token):
    assert_sources()
    install_hooks(token)
    failed = False
    for model in MODELS:
        config_path, provider_path = paths_for(model)
        cfg = core.load_hops_config(config_path, provider_path)
        root = core.campaign_root(cfg)
        stage = "preflight"
        try:
            assert_sources()
            provider_preflight = preflight(model, cfg, token)
            stage = "pilot"
            log_event("pilot_started", model=model)
            core.run_hops_campaign(cfg, "pilot")
            pilot_audit = read_json(root / "pilot/completion_audit.json")
            notify(
                "pilot_complete",
                model,
                f"실제 파일럿 {pilot_audit['observation_count']}/12슬롯을 저장했습니다. 구조 감사={pilot_audit['passed']}, 임계치 완전성={json.dumps(pilot_audit['complete_by_threshold'])}입니다.",
            )
            stage = "freeze"
            design = core.freeze_main_design(
                cfg, pilot_audit, read_json(cfg["validation"]), provider_preflight
            )
            notify(
                "freeze_complete",
                model,
                f"실제 파일럿·기준 구현·모델 확인 관문을 통과하여 본 실험 계약 {design['contract_hash']}를 동결했습니다. 추가 승인 없이 300슬롯을 직렬 실행합니다.",
            )
            log_event(
                "freeze_complete", model=model, contract_hash=design["contract_hash"]
            )
            stage = "main"
            core.run_hops_campaign(cfg, "main")
            stage = "report"
            assert_sources()
            main_summary = core.report_hops_campaign(cfg, "main")
            from scripts.verify_v16_reproducibility import verify_v16_reproducibility

            reproduced = verify_v16_reproducibility(cfg, None)
            notify(
                "report_complete",
                model,
                f"본 실험 관측 저장과 공식 보고를 마쳤습니다. 임계치 완전성={json.dumps(main_summary['complete_by_threshold'])}, 외부 호출 차단 수치 재현={reproduced['passed']}입니다.",
            )
            log_event(
                "report_complete",
                model=model,
                complete_by_threshold=main_summary["complete_by_threshold"],
                reproducibility=reproduced["passed"],
            )
        except Exception as exc:
            failed = True
            error = {
                "at": timestamp(),
                "stage": stage,
                "exception_type": type(exc).__name__,
                "reason": str(exc),
                "observations_preserved": True,
                "regeneration_performed": False,
            }
            write_json(root / "blocker.json", error)
            log_event("campaign_blocked", model=model, **error)
            notify(
                "blocked_" + stage,
                model,
                f"{stage} 단계가 차단되었습니다: {type(exc).__name__}: {exc}. 실제 자료와 실패 관측을 보존했고 관문을 우회하지 않았습니다.",
                blocked=True,
            )
        write_final_report()
    passed_audit = secret_audit(OUTPUT, token)
    write_json(
        OUTPUT / "secret-audit.json", {"passed": passed_audit, "at": timestamp()}
    )
    log_event("execution_finished", failed=failed, secret_audit_passed=passed_audit)
    return 1 if failed or not passed_audit else 0


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    token = os.environ.pop("CMD_API_KEY", None)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with (
        file_lock(OUTPUT / "execution.lock", blocking=False),
        clean_execution_environment(),
    ):
        if args.prepare:
            prepare()
            return 0
        if args.run:
            if not token:
                raise SystemExit("지정한 실행 프로세스에 CMD_API_KEY가 필요합니다")
            return run(token)
    parser.error("--prepare 또는 --run을 지정해 주십시오")


if __name__ == "__main__":
    raise SystemExit(main())
