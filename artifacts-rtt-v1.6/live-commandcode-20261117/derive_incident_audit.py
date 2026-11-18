"""보존된 관측에서 HTTP 524의 분석 영향을 별도로 계산합니다."""

import copy
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump_json(path, value):
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def metrics(records, threshold, route):
    outcomes = [r["outcomes"][threshold] for r in records if r["route"] == route]
    counts = Counter(o["category"] for o in outcomes)
    valid = sum(counts[k] for k in ("success", "functional_failure", "hop_limit"))
    hits = [o for o in outcomes if o["success"]]
    probability = len(hits) / valid if valid else None
    hops = sum(o["reached_step"] for o in hits) / len(hits) if hits else None
    return {
        "threshold": threshold,
        "route": route,
        "recorded": len(outcomes),
        "valid": valid,
        "success": len(hits),
        "invalid": counts["invalid"],
        "incomplete": counts["incomplete"],
        "P": probability,
        "H": hops,
        "D": hops / probability if probability else None,
    }


def confirmation(records, route):
    hits = [
        r for r in records if r["route"] == route and r["outcomes"]["0.85"]["success"]
    ]
    counts = Counter(
        (
            r["confirmation_status"]
            if r["confirmation_status"] in ("passed", "failed")
            else "unavailable"
        )
        for r in hits
    )
    assessable = counts["passed"] + counts["failed"]
    return {
        "route": route,
        "primary_successes": len(hits),
        "passed": counts["passed"],
        "failed": counts["failed"],
        "unavailable": counts["unavailable"],
        "assessable": assessable,
        "retention_rate": counts["passed"] / assessable if assessable else None,
    }


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    incident = json.loads((ROOT / "incident-524.json").read_text(encoding="utf-8"))
    output = {
        "범위": "원관측을 수정하지 않는 프로토콜 감사 파생값입니다. 확증 추론과 모델 우열 판단에 사용하지 않습니다.",
        "실행상태": "유료 실행은 중지되어 있으며 이 스크립트는 네트워크·인증 환경에 접근하지 않습니다.",
        "script_sha256": digest(Path(__file__)),
        "incident_sha256": digest(ROOT / "incident-524.json"),
        "models": {},
        "changes": [],
    }
    for name, model in incident["models"].items():
        campaign = Path(model["campaign_path"])
        paths = sorted((campaign / "main").glob("*/*/attempt-*/observation.json"))
        before = {str(p): digest(p) for p in paths}
        raw = [json.loads(p.read_text(encoding="utf-8")) for p in paths]
        derived = copy.deepcopy(raw)
        for affected in incident["ambiguous_http_requests"]:
            if affected["model"] != name:
                continue
            logical = affected["logical_request"]
            index = next(
                i
                for i, r in enumerate(raw)
                if (r["problem_id"], r["route"], r["repeat"])
                == (logical["problem"], logical["route"], logical["repeat"])
            )
            original = raw[index]
            revised = derived[index]
            affected_step = logical["step"]
            initial = affected["attempts"][0]
            # at는 전송 시작 시각이며 HTTP 오류 수신 시각은 별도 저장되지 않았습니다.
            changed_thresholds = []
            for threshold, outcome in revised["outcomes"].items():
                if outcome["success"] and outcome["reached_step"] < affected_step:
                    continue
                outcome.update(
                    success=False,
                    category="invalid",
                    reason="ambiguous_http_524_automatic_resend",
                    reached_step=None,
                    reached_roundtrip=None,
                    unique_state_count_at_reach=None,
                    sym_adj=None,
                    sym_origin=None,
                )
                changed_thresholds.append(threshold)
            primary = original["outcomes"]["0.85"]
            confirmation_due = (
                primary["reached_step"] + 2 if primary["success"] else None
            )
            confirmation_completed_before = bool(
                confirmation_due
                and confirmation_due < affected_step
                and original["confirmation_status"] in ("passed", "failed")
                and any(s["step"] == confirmation_due for s in original["steps"])
            )
            if primary["success"] and not confirmation_completed_before:
                revised["confirmation_status"] = "unavailable"
                revised["confirmation_reason"] = "ambiguous_http_524_automatic_resend"
            state = json.loads(
                (campaign / "main/provider_ledger.jsonl.state.json").read_text(
                    encoding="utf-8"
                )
            )
            previous_receipts = [
                {
                    "step": state["requests"][a["call_id"]]["logical_request"]["step"],
                    "receipt": json.loads(
                        (
                            Path(state["requests"][a["call_id"]]["folder"])
                            / "receipt.json"
                        ).read_text(encoding="utf-8")
                    ),
                }
                for a in state["attempts"]
                if a["status"] == "received"
                and state["requests"][a["call_id"]]["logical_request"].get("problem")
                == logical["problem"]
                and state["requests"][a["call_id"]]["logical_request"].get("route")
                == logical["route"]
                and state["requests"][a["call_id"]]["logical_request"].get("repeat")
                == logical["repeat"]
                and state["requests"][a["call_id"]]["logical_request"]["step"]
                < affected_step
            ]
            output["changes"].append(
                {
                    "model": name,
                    "observation_path": str(paths[index]),
                    "original_observation_sha256": before[str(paths[index])],
                    "call_id": affected["call_id"],
                    "first_524_attempt_at": initial["at"],
                    "http_error_received_at": None,
                    "시각해석": "first_524_attempt_at은 해당 전송 시작 시각입니다. 오류 수신 시각으로 대체하지 않습니다.",
                    "excluded_steps": [
                        s["step"]
                        for s in original["steps"]
                        if s["step"] >= affected_step
                    ],
                    "excluded_response_request_id": affected["response_request_id"],
                    "raw_outcomes": original["outcomes"],
                    "derived_outcomes": revised["outcomes"],
                    "changed_thresholds": changed_thresholds,
                    "preserved_receipts_before_ambiguous_attempt": previous_receipts,
                    "confirmation_due_step": confirmation_due,
                    "recorded_step_numbers": [s["step"] for s in original["steps"]],
                    "confirmation_completed_before_524": confirmation_completed_before,
                    "raw_confirmation_status": original["confirmation_status"],
                    "derived_confirmation_status": revised["confirmation_status"],
                    "전환근거": "불명 전송 이후 재생성의 결과는 첫 생성의 기능 실패·확인 결과로 해석하지 않으며 이미 확정된 최초 도달은 유지합니다.",
                }
            )
        routes = ["cpp-via-python", "cpp-via-java", "cpp-via-haskell", "cpp-via-prolog"]
        rows = []
        confirmations = []
        for version, records in (("raw", raw), ("audit_derived", derived)):
            for threshold in ("0.80", "0.85", "0.90"):
                rows.extend(
                    {"version": version, **metrics(records, threshold, r)}
                    for r in routes
                )
            confirmations.extend(
                {"version": version, **confirmation(records, r)} for r in routes
            )
        if name == "glm53":
            for row in rows:
                if row["version"] != "raw":
                    continue
                official = next(
                    o
                    for o in model["threshold_rows"]
                    if o["threshold"] == row["threshold"] and o["route"] == row["route"]
                )
                for key in ("valid", "success", "invalid", "incomplete"):
                    assert row[key] == int(official[key]), (row, official)
                for key in ("P", "H", "D"):
                    expected = float(official[key]) if official[key] else None
                    assert row[key] == expected or (
                        row[key] is not None
                        and expected is not None
                        and abs(row[key] - expected) < 1e-12
                    )
            raw_primary = [
                r for r in rows if r["version"] == "raw" and r["threshold"] == "0.85"
            ]
            derived_primary = [
                {**r, "version": "raw"}
                for r in rows
                if r["version"] == "audit_derived" and r["threshold"] == "0.85"
            ]
            assert raw_primary == derived_primary
            output["glm_primary_085_route_metrics_unchanged"] = True
        after = {str(p): digest(p) for p in paths}
        assert before == after
        output["models"][name] = {
            "raw_observation_count": len(raw),
            "raw_terminal_statuses": dict(Counter(r["terminal_status"] for r in raw)),
            "raw_primary_categories": dict(
                Counter(r["outcomes"]["0.85"]["category"] for r in raw)
            ),
            "threshold_rows": rows,
            "confirmation_rows": confirmations,
            "observation_hashes": before,
            "original_observations_unchanged": True,
        }
        write_csv(ROOT / f"{name}-audit-thresholds.csv", rows)
        write_csv(ROOT / f"{name}-audit-confirmation.csv", confirmations)
    dump_json(ROOT / "audit-derived.json", output)
    print(
        json.dumps(
            {
                "passed": True,
                "glm_primary_085_route_metrics_unchanged": True,
                "changed_slots": len(output["changes"]),
            }
        )
    )


if __name__ == "__main__":
    main()
