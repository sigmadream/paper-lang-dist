"""실행 종료 후 원장·관측·검토·기존 불변을 감사합니다."""

import hashlib
import json
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from pathlib import Path

import psutil

sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path.cwd() / "src"))
from scripts import run_deepseek_v41_flash_20261118 as runner

OUTPUT = runner.OUTPUT
CAMPAIGN = OUTPUT / runner.CAMPAIGN_ID


def read(path, default=None):
    return runner.read_json(path) if path.is_file() else default


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def amount(value):
    return Decimal(str(value or 0))


assert (OUTPUT / "run.exitcode").is_file(), "유료 프로세스 종료 확인이 먼저 필요합니다"
phases = {}
for phase, planned in {"preflight": 1, "pilot": 12, "main": 300}.items():
    root = CAMPAIGN / phase
    state = read(
        root / "provider_ledger.jsonl.state.json", {"requests": {}, "attempts": []}
    )
    requests = state["requests"]
    responses = []
    unresolved = []
    for call_id, request in requests.items():
        folder = Path(request["folder"])
        response = read(folder / "response.json")
        if response is not None:
            responses.append(response)
        if request.get("status") in {"unknown", "inflight"} or request.get(
            "uncertain_reserved_usd"
        ):
            unresolved.append(
                {
                    "call_id": call_id,
                    "status": request.get("status"),
                    "logical_request": request.get("logical_request"),
                    "folder": str(folder),
                    "reserved_usd": request.get("reserved_usd"),
                    "uncertain_reserved_usd": request.get("uncertain_reserved_usd"),
                    "response_exists": (folder / "response.json").is_file(),
                    "raw_response_exists": (folder / "response_body.txt").is_file(),
                    "attempts": [
                        a for a in state["attempts"] if a.get("call_id") == call_id
                    ],
                    "transport_evidence": read(folder / "transport_attempts.json"),
                    "errors": read(folder / "api_errors.json"),
                }
            )
    observations = [
        runner.read_json(p) for p in root.glob("*/*/attempt-*/observation.json")
    ]
    outcomes = {
        threshold: dict(
            Counter(o["outcomes"][threshold]["category"] for o in observations)
        )
        for threshold in ("0.80", "0.85", "0.90")
    }
    usage = [r.get("usage") or {} for r in requests.values()]
    known = sum((amount(r.get("cost_usd")) for r in requests.values()), Decimal(0))
    reserved = sum(
        (
            amount(r.get("reserved_usd")) + amount(r.get("uncertain_reserved_usd"))
            for r in requests.values()
        ),
        Decimal(0),
    )
    phases[phase] = {
        "planned_slots": planned,
        "saved_slots": (
            int(read(CAMPAIGN / "preflight.json", {}).get("passed") is True)
            if phase == "preflight"
            else len(observations)
        ),
        "logical_requests": len(requests),
        "transport_attempts": len(state["attempts"]),
        "request_states": dict(Counter(r.get("status") for r in requests.values())),
        "attempt_states": dict(Counter(a.get("status") for a in state["attempts"])),
        "responses": len(responses),
        "actual_models": dict(Counter(r.get("actual_model") for r in responses)),
        "all_models_exact": all(
            r.get("actual_model") == runner.MODEL_ID
            and r.get("model_evidence", {}).get("status") == "exact"
            for r in responses
        ),
        "all_generation_as_planned": all(
            r.get("requested_generation") == runner.GENERATION
            and r.get("sent_generation") == runner.GENERATION
            and r.get("effective_generation") is None
            for r in responses
        ),
        "prompt_tokens": sum(u.get("prompt_tokens", 0) for u in usage),
        "completion_tokens": sum(u.get("completion_tokens", 0) for u in usage),
        "cached_tokens": sum(
            u.get("prompt_tokens_details", {}).get(
                "cached_tokens", u.get("prompt_cache_hit_tokens", 0)
            )
            for u in usage
        ),
        "known_estimated_cost_usd": str(known),
        "reserved_usd": str(reserved),
        "unresolved_requests": unresolved,
        "terminal_states": dict(
            Counter(o.get("terminal_status") for o in observations)
        ),
        "outcomes_by_threshold": outcomes,
        "completion_audit": read(root / "completion_audit.json"),
        "limits_passed": len(requests) <= runner.PHASES[phase]["max_calls"]
        and len(state["attempts"]) <= runner.PHASES[phase]["max_transport_attempts"]
        and known + reserved <= amount(runner.PHASES[phase]["cost_cap_usd"]),
        "ledger_sha256": (
            sha(root / "provider_ledger.jsonl")
            if (root / "provider_ledger.jsonl").is_file()
            else None
        ),
        "state_sha256": (
            sha(root / "provider_ledger.jsonl.state.json")
            if (root / "provider_ledger.jsonl.state.json").is_file()
            else None
        ),
    }

manifest = runner.assert_sources()
review = runner.require_review(OUTPUT / "independent-review.json")
baseline = runner.read_json(OUTPUT / "기존-보존기준.json")


def difference(item):
    name, expected = item
    path = runner.ROOT / name
    return name if not path.is_file() or sha(path) != expected else None


with ThreadPoolExecutor(max_workers=12) as pool:
    differences = [
        name for name in pool.map(difference, baseline["hashes"].items()) if name
    ]
runner.write_json(
    OUTPUT / "종료후-기존불변.json",
    {
        "at": runner.timestamp(),
        "checked_files": len(baseline["hashes"]),
        "baseline_sha256": sha(OUTPUT / "기존-보존기준.json"),
        "differences": differences,
        "passed": not differences,
    },
)
running = []
for process in psutil.process_iter(["pid", "name", "cmdline"]):
    try:
        arguments = process.info["cmdline"] or []
        if any(Path(a).name == "run_deepseek_v41_flash_20261118.py" for a in arguments):
            running.append(
                {
                    "pid": process.pid,
                    "name": process.info["name"],
                    "arguments": arguments,
                }
            )
    except psutil.NoSuchProcess, psutil.AccessDenied:
        pass
with runner.file_lock(OUTPUT / "execution.lock", blocking=False):
    lock_free = True
try:
    runner.assert_no_unknown_requests()
    unknown_guard_passed = True
except ValueError:
    unknown_guard_passed = False
known = sum(
    (amount(p["known_estimated_cost_usd"]) for p in phases.values()), Decimal(0)
)
reserved = sum((amount(p["reserved_usd"]) for p in phases.values()), Decimal(0))
exitcode = int((OUTPUT / "run.exitcode").read_text())
summary = read(CAMPAIGN / "main/summary.json")
reproduction = read(CAMPAIGN / "main/report/reproducibility.json")
budget = runner.prior_budget_evidence()
glm_root = (
    runner.ROOT
    / "artifacts-rtt-v1.6/live-commandcode-20261117/commandcode-glm53-v16-20261117"
)
glm_phases = {}
for phase in ("preflight", "pilot", "main"):
    state = runner.read_json(glm_root / phase / "provider_ledger.jsonl.state.json")
    values = list(state["requests"].values())
    glm_phases[phase] = {
        "logical_requests": len(values),
        "transport_attempts": len(state["attempts"]),
        "known_estimated_cost_usd": str(
            sum((amount(v.get("cost_usd")) for v in values), Decimal(0))
        ),
        "reserved_usd": str(
            sum(
                (
                    amount(v.get("reserved_usd"))
                    + amount(v.get("uncertain_reserved_usd"))
                    for v in values
                ),
                Decimal(0),
            )
        ),
        "prompt_tokens": sum(
            (v.get("usage") or {}).get("prompt_tokens", 0) for v in values
        ),
        "completion_tokens": sum(
            (v.get("usage") or {}).get("completion_tokens", 0) for v in values
        ),
    }
glm_total = sum(
    (
        amount(v["known_estimated_cost_usd"]) + amount(v["reserved_usd"])
        for v in glm_phases.values()
    ),
    Decimal(0),
)
secret_audit = read(OUTPUT / "secret-audit.json")
complete = (
    exitcode == 0
    and phases["main"]["saved_slots"] == 300
    and summary is not None
    and reproduction is not None
    and reproduction.get("passed") is True
    and unknown_guard_passed
    and all(
        p["all_models_exact"] and p["all_generation_as_planned"] and p["limits_passed"]
        for p in phases.values()
    )
    and (phases["pilot"]["completion_audit"] or {}).get("passed") is True
    and (phases["main"]["completion_audit"] or {}).get("passed") is True
)
result = {
    "at": runner.timestamp(),
    "설명": "실제 유료 실행 종료 후 감사이며 부분 수집을 전체 완료로 간주하지 않습니다.",
    "status": "succeeded" if complete else "failed",
    "execution_completed": complete,
    "analysis_complete_by_threshold": (phases["main"]["completion_audit"] or {}).get(
        "complete_by_threshold"
    ),
    "measurement_limitations": read(OUTPUT / "측정불가-감사.json"),
    "wrapper_exitcode": exitcode,
    "campaign_id": runner.CAMPAIGN_ID,
    "model_id": runner.MODEL_ID,
    "source_guard_passed": True,
    "review_guard_passed": True,
    "reviewer_session_id": review["reviewer_session_id"],
    "manifest_file_sha256": sha(OUTPUT / "source-manifest.json"),
    "manifest_object_digest": runner.digest(manifest),
    "execution_evidence_manifest_object_matches": read(
        OUTPUT / "execution-evidence.json", {}
    ).get("source_manifest_sha256")
    == runner.digest(manifest),
    "source_files": len(manifest["files"]),
    "legacy_guard_files": len(manifest["legacy_hashes"]),
    "phases": phases,
    "logical_requests": sum(p["logical_requests"] for p in phases.values()),
    "transport_attempts": sum(p["transport_attempts"] for p in phases.values()),
    "normal_responses": sum(p["responses"] for p in phases.values()),
    "known_estimated_cost_usd": str(known),
    "reserved_usd": str(reserved),
    "reported_account_charge_usd": None,
    "new_total_cost_cap_usd": "98.13",
    "maximum_total_cost_cap_usd": "200.50",
    "budget": budget,
    "preserved_glm_campaign": {
        "campaign_id": "commandcode-glm53-v16-20261117",
        "phases": glm_phases,
        "logical_requests": sum(v["logical_requests"] for v in glm_phases.values()),
        "transport_attempts": sum(v["transport_attempts"] for v in glm_phases.values()),
        "known_estimated_plus_reserved_usd": str(glm_total),
        "reported_account_charge_usd": None,
        "rerun": False,
    },
    "all_campaigns_known_estimated_plus_reserved_usd": str(
        glm_total + Decimal("1.045928856") + Decimal("1.039800264") + known + reserved
    ),
    "all_phase_limits_passed": all(p["limits_passed"] for p in phases.values()),
    "conservative_actual_estimated_plus_reserved_and_glm_allocation_usd": str(
        Decimal("100.25")
        + Decimal("1.045928856")
        + Decimal("1.039800264")
        + known
        + reserved
    ),
    "all_models_exact": all(p["all_models_exact"] for p in phases.values()),
    "all_generation_as_planned": all(
        p["all_generation_as_planned"] for p in phases.values()
    ),
    "unknown_guard_passed": unknown_guard_passed,
    "running_paid_wrapper_processes": running,
    "execution_lock_released": lock_free,
    "secret_audit": secret_audit,
    "preflight": read(CAMPAIGN / "preflight.json"),
    "main_design": read(CAMPAIGN / "main_design.json"),
    "main_summary_exists": summary is not None,
    "official_report_exists": (CAMPAIGN / "main/report/summary.json").exists(),
    "report_call_completed": any(
        json.loads(line).get("event") == "report_complete"
        for line in (OUTPUT / "progress.jsonl").read_text(encoding="utf-8").splitlines()
    ),
    "reproducibility": reproduction,
    "original_artifact_count": len(baseline["hashes"]),
    "original_artifact_hash_differences": differences,
    "original_artifacts_unchanged": not differences,
    "session": read(OUTPUT / "execution-session.json"),
    "run_log_sha256": sha(OUTPUT / "run.log"),
}
runner.write_json(OUTPUT / "종료후-감사.json", result)
print(
    json.dumps(
        {
            k: result[k]
            for k in (
                "status",
                "wrapper_exitcode",
                "logical_requests",
                "transport_attempts",
                "normal_responses",
                "known_estimated_cost_usd",
                "reserved_usd",
                "all_models_exact",
                "original_artifact_count",
                "original_artifacts_unchanged",
                "unknown_guard_passed",
                "running_paid_wrapper_processes",
                "execution_lock_released",
                "secret_audit",
            )
        },
        ensure_ascii=False,
    )
)
assert (
    not running and lock_free and not differences and result["all_phase_limits_passed"]
)
assert secret_audit and secret_audit["passed"] is True
