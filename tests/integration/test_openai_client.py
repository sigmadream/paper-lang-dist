from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
import hashlib

import pytest

from rttdist.config import PINNED_OPENAI_MODEL
from rttdist.embedding import EmbeddingUsage
from rttdist import openai_client as openai_client_module
from rttdist.openai_client import (
    OpenAIClientError,
    OpenAIEmbeddingResponseParseError,
    OpenAIEmbeddingTransportResponse,
    OpenAIFinalSimilarityProvider,
    OpenAITranslationClient,
    SourceExtractionError,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
CURATED_PROBLEM_ROOT = (
    REPO_ROOT / "tests" / "fixtures" / "curated_problem" / "IPOP_1436"
)


class FakeTransport:
    def __init__(self, responses: list[dict[str, object]]) -> None:
        self._responses = responses
        self.requests: list[dict[str, object]] = []

    def create_chat_completion(self, payload: dict[str, object]) -> dict[str, object]:
        self.requests.append(payload)
        if not self._responses:
            raise AssertionError("No mocked OpenAI response available.")
        response = self._responses.pop(0)
        if not isinstance(response, dict):
            raise AssertionError("Mocked OpenAI response must be a mapping.")
        return response


class FakeEmbeddingTransport:
    def __init__(self, responses: list[OpenAIEmbeddingTransportResponse]) -> None:
        self._responses = responses
        self.requests: list[dict[str, object]] = []

    def create_embedding(
        self, payload: dict[str, object]
    ) -> OpenAIEmbeddingTransportResponse:
        self.requests.append(payload)
        if not self._responses:
            raise AssertionError("No mocked embedding response available.")
        return self._responses.pop(0)


def test_generic_translation_client_translates_ordered_language_pairs() -> None:
    statement, sample_input, sample_output, seed_cpp = _load_curated_problem_text()
    transport = FakeTransport(
        responses=[
            _build_response("```python\ndef solve():\n    print(666)\n```"),
            _build_response(
                "```cpp\n#include <iostream>\nint main(){ std::cout << 666 << '\\n'; }\n```"
            ),
        ]
    )
    client = OpenAITranslationClient(transport=transport)

    to_python = client.translate(
        problem_id="IPOP_1436",
        source_language="cpp",
        target_language="python",
        problem_statement=statement,
        sample_input=sample_input,
        sample_output=sample_output,
        source_code=seed_cpp,
        iteration_index=1,
        direction="seed_to_target",
    )
    back_to_cpp = client.translate(
        problem_id="IPOP_1436",
        source_language="python",
        target_language="cpp",
        problem_statement=statement,
        sample_input=sample_input,
        sample_output=sample_output,
        source_code=to_python.extracted_source,
        iteration_index=1,
        direction="target_to_seed",
    )

    assert len(transport.requests) == 2
    first_request = to_python.request.to_dict()
    second_request = back_to_cpp.request.to_dict()
    assert first_request == transport.requests[0]
    assert second_request == transport.requests[1]
    assert first_request["metadata"]["iteration_index"] == "1"
    assert second_request["metadata"]["iteration_index"] == "1"

    assert to_python.request.model == PINNED_OPENAI_MODEL
    assert to_python.request.temperature == 0.0
    assert to_python.request.metadata["direction"] == "seed_to_target"
    assert to_python.request.metadata["source_language"] == "cpp"
    assert to_python.request.metadata["target_language"] == "python"
    assert back_to_cpp.request.metadata["direction"] == "target_to_seed"
    assert back_to_cpp.request.metadata["source_language"] == "python"
    assert back_to_cpp.request.metadata["target_language"] == "cpp"

    assert to_python.extracted_source == "def solve():\n    print(666)"
    assert "#include <iostream>" in back_to_cpp.extracted_source


def test_client_rejects_non_deterministic_model_or_temperature() -> None:
    with pytest.raises(OpenAIClientError) as model_excinfo:
        OpenAITranslationClient(model="gpt-4.1-mini")
    assert "pinned" in str(model_excinfo.value)

    with pytest.raises(OpenAIClientError) as temperature_excinfo:
        OpenAITranslationClient(temperature=0.5)
    assert "Temperature must be 0" in str(temperature_excinfo.value)


@pytest.mark.parametrize("model", ["gpt-5.4", "gpt-5.4-mini", "gpt-5.3-codex"])
def test_client_accepts_approved_models(model: str) -> None:
    client = OpenAITranslationClient(model=model, transport=FakeTransport(responses=[]))
    assert client is not None


def test_client_recovers_longest_unfenced_code_span_with_surrounding_prose() -> None:
    statement, sample_input, sample_output, seed_cpp = _load_curated_problem_text()
    transport = FakeTransport(
        responses=[
            _build_response(
                "Here is the translated program.\n"
                "Use it as-is.\n\n"
                "def solve():\n"
                "    value = 666\n"
                "    print(value)\n\n"
                "This version preserves the sample behavior."
            )
        ]
    )
    client = OpenAITranslationClient(transport=transport)

    result = client.translate_cpp_to_target(
        problem_id="IPOP_1436",
        target_language="python",
        problem_statement=statement,
        sample_input=sample_input,
        sample_output=sample_output,
        source_code=seed_cpp,
        iteration_index=1,
    )

    assert result.extracted_source == "def solve():\n    value = 666\n    print(value)"


def test_client_merges_unfenced_code_spans_split_only_by_blank_lines() -> None:
    statement, sample_input, sample_output, seed_cpp = _load_curated_problem_text()
    transport = FakeTransport(
        responses=[
            _build_response(
                "import sys\n\n"
                "input = sys.stdin.read\n\n"
                "n = int(input().strip())\n\n"
                "count = 0\n"
                "value = 665\n"
                "while count < n:\n"
                "    value += 1\n"
                "    if '666' in str(value):\n"
                "        count += 1\n\n"
                "print(value)"
            )
        ]
    )
    client = OpenAITranslationClient(transport=transport)

    result = client.translate_cpp_to_target(
        problem_id="IPOP_1436",
        target_language="python",
        problem_statement=statement,
        sample_input=sample_input,
        sample_output=sample_output,
        source_code=seed_cpp,
        iteration_index=1,
    )

    assert result.extracted_source == (
        "import sys\n\n"
        "input = sys.stdin.read\n\n"
        "n = int(input().strip())\n\n"
        "count = 0\n"
        "value = 665\n"
        "while count < n:\n"
        "    value += 1\n"
        "    if '666' in str(value):\n"
        "        count += 1\n\n"
        "print(value)"
    )


def test_source_extraction_error_keeps_request_and_response_payloads() -> None:
    statement, sample_input, sample_output, seed_cpp = _load_curated_problem_text()
    transport = FakeTransport(
        responses=[
            _build_response(
                "No code can be provided in this answer. Please rewrite manually."
            )
        ]
    )
    client = OpenAITranslationClient(transport=transport)

    with pytest.raises(SourceExtractionError) as excinfo:
        client.translate_cpp_to_target(
            problem_id="IPOP_1436",
            target_language="python",
            problem_statement=statement,
            sample_input=sample_input,
            sample_output=sample_output,
            source_code=seed_cpp,
            iteration_index=1,
        )

    request_payload = getattr(excinfo.value, "request_payload", None)
    response_payload = getattr(excinfo.value, "response_payload", None)
    assert isinstance(request_payload, dict)
    assert isinstance(response_payload, dict)
    assert request_payload["metadata"]["iteration_index"] == "1"
    assert response_payload["choices"][0]["message"]["content"].startswith("No code")


def test_default_openai_transport_strips_metadata_before_api_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    class FakeResponse:
        def model_dump(self, *, mode: str) -> dict[str, object]:
            assert mode == "python"
            return {
                "id": "resp-1",
                "model": PINNED_OPENAI_MODEL,
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": "```python\nprint(666)\n```",
                        },
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": 1,
                    "completion_tokens": 1,
                    "total_tokens": 2,
                },
            }

    class FakeCompletions:
        def create(self, **kwargs: object) -> FakeResponse:
            captured.update(kwargs)
            return FakeResponse()

    class FakeOpenAI:
        def __init__(self) -> None:
            self.chat = SimpleNamespace(completions=FakeCompletions())

    monkeypatch.setattr(openai_client_module, "OpenAI", FakeOpenAI)

    transport = openai_client_module._OpenAIChatCompletionsTransport()
    payload = {
        "model": PINNED_OPENAI_MODEL,
        "temperature": 0.0,
        "messages": [{"role": "user", "content": "hello"}],
        "metadata": {"iteration_index": "1"},
    }

    response = transport.create_chat_completion(payload)

    assert response["id"] == "resp-1"
    assert "metadata" not in captured
    assert payload["metadata"] == {"iteration_index": "1"}


def test_embedding_provider_normalizes_vectors_and_provenance() -> None:
    transport = FakeEmbeddingTransport(
        responses=[
            OpenAIEmbeddingTransportResponse(
                payload={
                    "model": "text-embedding-3-large",
                    "data": [
                        {
                            "embedding": [0.1, -0.2, 0.4],
                            "index": 0,
                            "object": "embedding",
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 11,
                        "total_tokens": 11,
                    },
                },
                request_id="req_seed_001",
            )
        ]
    )
    provider = OpenAIFinalSimilarityProvider(
        model="text-embedding-3-large",
        transport=transport,
    )

    result = provider.embed_source(source_text="int main(){return 0;}")

    assert transport.requests == [
        {
            "model": "text-embedding-3-large",
            "input": "int main(){return 0;}",
            "encoding_format": "float",
        }
    ]
    assert result.provider == "openai"
    assert result.configured_model == "text-embedding-3-large"
    assert result.observed_model == "text-embedding-3-large"
    assert result.request_id == "req_seed_001"
    assert result.dimensions == 3
    assert result.vector == (0.1, -0.2, 0.4)
    assert (
        result.source_hash
        == hashlib.sha256("int main(){return 0;}".encode("utf-8")).hexdigest()
    )
    assert result.usage == EmbeddingUsage(prompt_tokens=11, total_tokens=11)


def test_embedding_provider_parse_error_keeps_request_and_response_payloads() -> None:
    transport = FakeEmbeddingTransport(
        responses=[
            OpenAIEmbeddingTransportResponse(
                payload={
                    "model": "text-embedding-3-large",
                    "data": [],
                },
                request_id="req_bad_001",
            )
        ]
    )
    provider = OpenAIFinalSimilarityProvider(transport=transport)

    with pytest.raises(OpenAIEmbeddingResponseParseError) as excinfo:
        provider.embed_source(source_text="int main(){return 0;}")

    request_payload = getattr(excinfo.value, "request_payload", None)
    response_payload = getattr(excinfo.value, "response_payload", None)
    assert isinstance(request_payload, dict)
    assert isinstance(response_payload, dict)
    assert request_payload["encoding_format"] == "float"
    assert response_payload["model"] == "text-embedding-3-large"


def _load_curated_problem_text() -> tuple[str, str, str, str]:
    statement = (
        (CURATED_PROBLEM_ROOT / "statement.md").read_text(encoding="utf-8").strip()
    )
    sample_input = (CURATED_PROBLEM_ROOT / "1.inp").read_text(encoding="utf-8").strip()
    sample_output = (CURATED_PROBLEM_ROOT / "1.out").read_text(encoding="utf-8").strip()
    seed_cpp = (
        (CURATED_PROBLEM_ROOT / "reference.cpp").read_text(encoding="utf-8").rstrip()
    )
    return statement, sample_input, sample_output, seed_cpp


def _build_response(content: str) -> dict[str, object]:
    return {
        "id": "mock-response-001",
        "model": PINNED_OPENAI_MODEL,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 5,
            "total_tokens": 15,
        },
    }
