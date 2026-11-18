"""종료한 유료 실행의 원장과 보존 근거만 읽어 감사 결과를 작성합니다."""

from collections import Counter
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts import run_deepseek_v16_20261118 as runner


def read(path, default=None):
    return (
        json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else default
    )


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def main():
    output = runner.OUTPUT
    if not (output / "run.exitcode").is_file():
        raise ValueError("래퍼 종료 코드가 없어 종료 후 감사를 수행할 수 없습니다")
    manifest = runner.assert_sources()
    review = runner.require_review(output / "independent-review.json")
    manifest_matches = (
        file_hash(output / "source-manifest.json") == review["prepared_manifest_sha256"]
    )
    campaign = output / runner.CAMPAIGN_ID
    result = {
        "at": runner.timestamp(),
        "설명": "래퍼 종료 후 기존 파일을 수정하거나 새 요청을 생성하지 않고 감사하였습니다.",
        "wrapper_exitcode": int(
            (output / "run.exitcode").read_text(encoding="utf-8-sig").strip()
        ),
        "status": read(output / "status.json"),
        "source_guard_passed": True,
        "review_guard_passed": True,
        "prepared_manifest_hash_matches": manifest_matches,
        "source_files": len(manifest["files"]),
        "legacy_protected_files": len(manifest["legacy_hashes"]),
        "phases": {},
    }
    total_cost = Decimal(0)
    total_reserved = Decimal(0)
    for phase, planned in (("preflight", 1), ("pilot", 12), ("main", 300)):
        folder = campaign / phase
        state = read(
            folder / "provider_ledger.jsonl.state.json",
            {"requests": {}, "attempts": []},
        )
        requests = state["requests"]
        values = list(requests.values())
        attempts = state["attempts"]
        responses = [
            read(Path(value["folder"]) / "response.json")
            for value in values
            if (Path(value["folder"]) / "response.json").is_file()
        ]
        observations = [
            read(path) for path in folder.glob("*/*/attempt-*/observation.json")
        ]
        cost = sum(
            (Decimal(str(value.get("cost_usd") or 0)) for value in values), Decimal(0)
        )
        reserved = sum(
            (
                Decimal(str(value.get("reserved_usd") or 0))
                + Decimal(str(value.get("uncertain_reserved_usd") or 0))
                for value in values
            ),
            Decimal(0),
        )
        unresolved = []
        for call_id, value in requests.items():
            if value.get("status") in ("unknown", "inflight") or value.get(
                "uncertain_reserved_usd"
            ):
                request_folder = Path(value["folder"])
                unresolved.append(
                    {
                        "call_id": call_id,
                        "status": value["status"],
                        "logical_request": value.get("logical_request"),
                        "folder": str(request_folder),
                        "reserved_usd": value.get("reserved_usd"),
                        "uncertain_reserved_usd": value.get("uncertain_reserved_usd"),
                        "response_exists": (request_folder / "response.json").is_file(),
                        "raw_response_exists": (
                            request_folder / "response_body.txt"
                        ).is_file(),
                        "attempts": [
                            item for item in attempts if item["call_id"] == call_id
                        ],
                        "error": read(request_folder / "api_errors.json"),
                    }
                )
        result["phases"][phase] = {
            "planned_slots": planned,
            "saved_slots": (
                len(observations)
                if phase != "preflight"
                else int(bool(read(campaign / "preflight.json", {}).get("passed")))
            ),
            "logical_requests": len(requests),
            "transport_attempts": len(attempts),
            "request_states": dict(Counter(value["status"] for value in values)),
            "attempt_states": dict(Counter(item["status"] for item in attempts)),
            "responses": len(responses),
            "actual_models": dict(
                Counter(value.get("actual_model") for value in responses)
            ),
            "model_evidence": dict(
                Counter(
                    value.get("model_evidence", {}).get("status") for value in responses
                )
            ),
            "generation_evidence": {
                field: sorted(
                    {
                        json.dumps(value.get(field), ensure_ascii=False, sort_keys=True)
                        for value in responses
                    }
                )
                for field in (
                    "requested_generation",
                    "sent_generation",
                    "effective_generation",
                )
            },
            "prompt_tokens": sum(
                value.get("usage", {}).get("prompt_tokens", 0) for value in values
            ),
            "completion_tokens": sum(
                value.get("usage", {}).get("completion_tokens", 0) for value in values
            ),
            "cached_tokens": sum(
                value.get("usage", {})
                .get("prompt_tokens_details", {})
                .get("cached_tokens", 0)
                for value in values
            ),
            "known_estimated_cost_usd": str(cost),
            "reserved_usd": str(reserved),
            "unresolved_requests": unresolved,
            "terminal_states": dict(
                Counter(value.get("status") for value in observations)
            ),
            "outcomes_by_threshold": {
                threshold: dict(
                    Counter(
                        value.get("outcomes", {})
                        .get(threshold, {})
                        .get("category", "missing")
                        for value in observations
                    )
                )
                for threshold in ("0.80", "0.85", "0.90")
            },
            "completion_audit": read(folder / "completion_audit.json"),
        }
        total_cost += cost
        total_reserved += reserved
    old_root = ROOT / "artifacts-rtt-v1.6/live-commandcode-20261117"
    old = read(old_root / "incident-524.json")
    old_hashes = old["original_artifact_hashes_after"]
    differences = [
        name
        for name, expected in old_hashes.items()
        if file_hash(old_root / name) != expected
    ]
    result.update(
        {
            "known_estimated_cost_usd": str(total_cost),
            "reserved_usd": str(total_reserved),
            "reported_account_charge_usd": None,
            "original_artifact_count": len(old_hashes),
            "original_artifact_hash_differences": differences,
            "original_artifacts_unchanged": not differences,
            "main_design": read(campaign / "main_design.json"),
            "main_summary_exists": (campaign / "main/summary.json").is_file(),
            "reproducibility": read(campaign / "main/report/reproducibility.json"),
            "secret_audit": read(output / "secret-audit.json"),
            "preflight": read(campaign / "preflight.json"),
            "new_cost_cap_usd": "99.18",
            "maximum_total_cost_cap_usd": "200.50",
            "old_known_estimated_and_reserved_usd": old[
                "old_total_spent_plus_reserved_usd"
            ],
        }
    )
    runner.write_json(output / "종료후-감사.json", result)
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "wrapper_exitcode",
                    "known_estimated_cost_usd",
                    "reserved_usd",
                    "original_artifact_count",
                    "original_artifacts_unchanged",
                    "secret_audit",
                )
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
