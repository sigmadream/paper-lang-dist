"""최초 도달 홉과 다음 왕복 확인을 분리하는 순수 상태 전이입니다."""

from copy import deepcopy
import math

from rttdist.experiment_io import digest


def threshold_key(value):
    return f"{float(value):.2f}"


class HopsState:
    def __init__(
        self, origin, thresholds, primary_threshold, max_hops, confirmation_roundtrips
    ):
        if isinstance(origin, dict):
            language, source = origin["language"], origin["source"]
        else:
            language, source = "cpp", origin
        if max_hops < 2 or max_hops % 2 or confirmation_roundtrips != 1:
            raise ValueError("짝수 탐색 상한과 확인 1왕복이 필요합니다.")
        self.primary_threshold = threshold_key(primary_threshold)
        self.max_hops = max_hops
        self.translation_steps = 0
        self.states = {}
        self._add_state(language, source, 0)
        self._outcomes = {
            threshold_key(t): {
                "success": False,
                "category": "incomplete",
                "reached_step": None,
                "reached_roundtrip": None,
                "unique_state_count_at_reach": None,
                "sym_adj": None,
                "sym_origin": None,
                "reason": None,
            }
            for t in sorted(set(thresholds))
        }
        if self.primary_threshold not in self._outcomes:
            raise ValueError("주 임계치가 임계치 목록에 있어야 합니다.")
        self.confirmation_status = None
        self.confirmation_reason = None
        self.confirmation_due = None
        self.terminal_status = None
        self.reason = None

    def _add_state(self, language, source, step):
        normalized = source.replace("\r\n", "\n").replace("\r", "\n")
        key = (language, digest(normalized.encode("utf-8")))
        duplicate = key in self.states
        self.states.setdefault(key, step)
        return duplicate, key[1]

    def outcomes(self):
        return deepcopy(self._outcomes)

    def next_step_kind(self):
        if self.terminal_status:
            return "stop"
        if self.translation_steps < self.max_hops:
            return "discovery"
        if self.confirmation_due and self.confirmation_status is None:
            return "confirmation"
        return "stop"

    def _finish_unreached(self, category, reason):
        for value in self._outcomes.values():
            if value["category"] == "incomplete":
                value.update(category=category, reason=reason)

    def abort(self, reason):
        self._finish_unreached("invalid", reason)
        if self.confirmation_due and self.confirmation_status is None:
            self.confirmation_status = "unavailable"
            self.confirmation_reason = reason
        self.terminal_status = "infrastructure_error"
        self.reason = reason

    def record_step(
        self,
        language,
        source,
        functional_status,
        similarity=None,
        similarity_status=None,
    ):
        kind = self.next_step_kind()
        if kind == "stop":
            raise ValueError("종료된 관측에 단계를 추가할 수 없습니다.")
        self.translation_steps += 1
        step = self.translation_steps
        duplicate, source_hash = self._add_state(language, source, step)
        item = {
            "step": step,
            "kind": kind,
            "duplicate": duplicate,
            "source_sha256": source_hash,
            "thresholds_reached": [],
        }
        if functional_status != "success":
            if functional_status in {
                "infrastructure_error",
                "provider_error",
                "tool_error",
                "unavailable",
            }:
                self.abort(functional_status)
            else:
                self._finish_unreached("functional_failure", functional_status)
                if self.confirmation_due and self.confirmation_status is None:
                    self.confirmation_status = "failed"
                    self.confirmation_reason = functional_status
                self.terminal_status = "functional_failure"
                self.reason = functional_status
            return item
        if step % 2 == 0:
            values = (
                similarity if isinstance(similarity, dict) else {"sym_adj": similarity}
            )
            adjacent = values.get("sym_adj")
            if (
                similarity_status not in (None, "measured")
                or not isinstance(adjacent, (int, float))
                or not math.isfinite(adjacent)
                or not 0 <= adjacent <= 1
            ):
                self.abort("similarity_unavailable")
                return item
            if kind == "discovery":
                for key, outcome in self._outcomes.items():
                    if outcome["category"] == "incomplete" and adjacent >= float(key):
                        outcome.update(
                            success=True,
                            category="success",
                            reached_step=step,
                            reached_roundtrip=step // 2,
                            unique_state_count_at_reach=len(self.states),
                            sym_adj=adjacent,
                            sym_origin=values.get("sym_origin"),
                        )
                        item["thresholds_reached"].append(key)
                        if key == self.primary_threshold:
                            self.confirmation_due = step + 2
            if self.confirmation_due == step:
                self.confirmation_status = (
                    "passed" if adjacent >= float(self.primary_threshold) else "failed"
                )
                self.confirmation_reason = (
                    None if self.confirmation_status == "passed" else "low_similarity"
                )
        if step == self.max_hops:
            self._finish_unreached("hop_limit", "hop_limit")
        all_reached = all(o["success"] for o in self._outcomes.values())
        if self.confirmation_status is not None and (
            all_reached or step >= self.max_hops
        ):
            self.terminal_status = "collection_complete"
        elif step >= self.max_hops and not self.confirmation_due:
            self.terminal_status = "hop_limit"
        return item
