from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
from typing import Protocol


class EmbeddingProviderError(RuntimeError):
    pass


@dataclass(frozen=True)
class EmbeddingUsage:
    prompt_tokens: int | None
    total_tokens: int | None

    def to_dict(self) -> dict[str, int]:
        payload: dict[str, int] = {}
        if self.prompt_tokens is not None:
            payload["prompt_tokens"] = self.prompt_tokens
        if self.total_tokens is not None:
            payload["total_tokens"] = self.total_tokens
        return payload


@dataclass(frozen=True)
class EmbeddedSource:
    source_hash: str
    provider: str
    configured_model: str
    observed_model: str | None
    request_id: str | None
    dimensions: int
    vector: tuple[float, ...]
    usage: EmbeddingUsage | None = None


class EmbeddingProvider(Protocol):
    provider_name: str
    configured_model: str

    def embed_source(self, *, source_text: str) -> EmbeddedSource: ...


def hash_source_text(source_text: str) -> str:
    return hashlib.sha256(source_text.encode("utf-8")).hexdigest()


def cosine_similarity(
    left_vector: tuple[float, ...], right_vector: tuple[float, ...]
) -> float:
    if len(left_vector) != len(right_vector):
        raise EmbeddingProviderError("Embedding vectors must have equal dimensions.")

    left_norm = math.sqrt(sum(value * value for value in left_vector))
    right_norm = math.sqrt(sum(value * value for value in right_vector))
    if left_norm == 0.0 or right_norm == 0.0:
        raise EmbeddingProviderError("Embedding vectors must be non-zero.")

    dot_product = sum(a * b for a, b in zip(left_vector, right_vector))
    return dot_product / (left_norm * right_norm)
