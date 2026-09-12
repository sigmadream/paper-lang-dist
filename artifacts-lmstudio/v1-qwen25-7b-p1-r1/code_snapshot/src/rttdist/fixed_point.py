from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

from rttdist.normalize import hash_normalized_cpp_tokens

ConvergenceStatus = Literal["fixed_point", "oscillation", "continue"]


def classify_hash_history(hash_history: Sequence[str]) -> ConvergenceStatus:
    if _has_adjacent_fixed_point(hash_history):
        return "fixed_point"
    if _has_two_cycle_oscillation(hash_history):
        return "oscillation"
    return "continue"


def classify_cpp_history(source_history: Sequence[str]) -> ConvergenceStatus:
    return classify_hash_history(
        [hash_normalized_cpp_tokens(source) for source in source_history]
    )


def _has_adjacent_fixed_point(hash_history: Sequence[str]) -> bool:
    if len(hash_history) < 2:
        return False
    return hash_history[-1] == hash_history[-2]


def _has_two_cycle_oscillation(hash_history: Sequence[str]) -> bool:
    if len(hash_history) < 4:
        return False
    return (
        hash_history[-1] == hash_history[-3]
        and hash_history[-2] == hash_history[-4]
        and hash_history[-1] != hash_history[-2]
    )
