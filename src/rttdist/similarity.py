"""Directional token similarities on the experiment's normalized token stream."""
from collections import Counter
from difflib import SequenceMatcher

from rttdist.normalize import normalize_cpp_tokens


def token_multiset_dice(a, b):
    n = len(a) + len(b)
    return 2 * sum((Counter(a) & Counter(b)).values()) / n if n else 1.0


def token_sequence_ratio(a, b):
    return SequenceMatcher(isjunk=None, a=a, b=b, autojunk=False).ratio()


def token_deltas(reference, candidate):
    a, b = normalize_cpp_tokens(reference), normalize_cpp_tokens(candidate)
    return {name: {"metric": name, "status": "measured", "value": 1 - fn(a, b),
                   "reason": None, "reference": "seed_source", "candidate": "stabilized_source"}
            for name, fn in (("token_multiset_dice", token_multiset_dice),
                             ("token_sequence_ratio", token_sequence_ratio))}
