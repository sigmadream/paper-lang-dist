"""진행 중 캠페인의 슬롯 이정표를 읽기 전용으로 감사합니다."""

import json
import sys
from collections import Counter
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path.cwd() / "src"))
from scripts import run_deepseek_v41_flash_20261118 as runner

milestone = int(sys.argv[1])
campaign = runner.OUTPUT / runner.CAMPAIGN_ID
manifest = runner.assert_sources()
runner.require_review(runner.OUTPUT / "independent-review.json")
phases = {}
for phase in ("preflight", "pilot", "main"):
    state = runner.read_json(campaign / phase / "provider_ledger.jsonl.state.json")
    responses = []
    for request in state["requests"].values():
        path = Path(request["folder"]) / "response.json"
        if path.is_file():
            responses.append(runner.read_json(path))
    known = sum(
        (Decimal(str(v.get("cost_usd") or 0)) for v in state["requests"].values()),
        Decimal(0),
    )
    reserved = sum(
        (
            Decimal(str(v.get("reserved_usd") or 0))
            + Decimal(str(v.get("uncertain_reserved_usd") or 0))
            for v in state["requests"].values()
        ),
        Decimal(0),
    )
    phases[phase] = {
        "logical_requests": len(state["requests"]),
        "transport_attempts": len(state["attempts"]),
        "states": dict(Counter(v["status"] for v in state["requests"].values())),
        "normal_responses": len(responses),
        "known_estimated_cost_usd": str(known),
        "current_reserved_usd": str(reserved),
        "all_models_exact": all(
            v["actual_model"] == runner.MODEL_ID
            and v["model_evidence"]["status"] == "exact"
            for v in responses
        ),
        "all_generation_as_planned": all(
            v["sent_generation"] == runner.GENERATION
            and v["effective_generation"] is None
            for v in responses
        ),
        "prompt_tokens": sum(
            (v.get("usage") or {}).get("prompt_tokens", 0)
            for v in state["requests"].values()
        ),
        "completion_tokens": sum(
            (v.get("usage") or {}).get("completion_tokens", 0)
            for v in state["requests"].values()
        ),
    }
saved = len(list((campaign / "main").glob("*/*/attempt-*/observation.json")))
assert saved >= milestone
result = {
    "at": runner.timestamp(),
    "milestone": milestone,
    "saved_main_slots": saved,
    "설명": "실행 중 읽기 전용 중간 감사입니다. 현재 inflight 예약은 종료 후 unknown 예약과 구분합니다.",
    "phases": phases,
    "source_guard_passed": True,
    "review_guard_passed": True,
    "manifest_sha256": runner.digest(
        (runner.OUTPUT / "source-manifest.json").read_bytes()
    ),
    "known_estimated_cost_usd": str(
        sum(
            (Decimal(p["known_estimated_cost_usd"]) for p in phases.values()),
            Decimal(0),
        )
    ),
    "current_reserved_usd": str(
        sum((Decimal(p["current_reserved_usd"]) for p in phases.values()), Decimal(0))
    ),
    "all_models_exact": all(p["all_models_exact"] for p in phases.values()),
    "all_generation_as_planned": all(
        p["all_generation_as_planned"] for p in phases.values()
    ),
}
runner.write_json(
    runner.OUTPUT / ("본실험-" + str(milestone) + "슬롯-중간감사.json"), result
)
print(json.dumps(result, ensure_ascii=False))
