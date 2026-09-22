from __future__ import annotations

from pathlib import Path
from typing import Any
import hashlib

import pytest

from rttdist.artifacts import LLMResponse
from rttdist import lmstudio_client as lmstudio_client_module
from rttdist.lmstudio_client import (
    LMStudioClientError,
    LMStudioTranslationClient,
    SourceExtractionError,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
CURATED_PROBLEM_ROOT = (
    REPO_ROOT / "tests" / "fixtures" / "curated_problem" / "IPOP_1436"
)


class RecordingTransport:
    def __init__(self, responses: list[dict[str, object]]) -> None:
        self._responses = responses
        self.requests: list[dict[str, object]] = []

    def create_chat_completion(self, payload: dict[str, object]) -> dict[str, object]:
        self.requests.append(payload)
        if not self._responses:
            raise AssertionError("No scripted LM Studio response available.")
        response = self._responses.pop(0)
        if not isinstance(response, dict):
            raise AssertionError("Scripted LM Studio response must be a mapping.")
        return response


def test_generic_translation_client_translates_ordered_language_pairs() -> None:
    statement, sample_input, sample_output, seed_cpp = _load_curated_problem_text()
    transport = RecordingTransport(
        responses=[
            _build_response("```python\ndef solve():\n    print(666)\n```"),
            _build_response(
                "```cpp\n#include <iostream>\nint main(){ std::cout << 666 << '\\n'; }\n```"
            ),
        ]
    )
    client = LMStudioTranslationClient(model="gpt-5.4", transport=transport)

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
    assert first_request["metadata"]["iteration_index"] == 1
    assert second_request["metadata"]["iteration_index"] == 1

    assert to_python.request.model == "gpt-5.4"
    assert to_python.request.temperature == 0.0
    assert to_python.request.metadata["direction"] == "seed_to_target"
    assert to_python.request.metadata["source_language"] == "cpp"
    assert to_python.request.metadata["target_language"] == "python"
    assert back_to_cpp.request.metadata["direction"] == "target_to_seed"
    assert back_to_cpp.request.metadata["source_language"] == "python"
    assert back_to_cpp.request.metadata["target_language"] == "cpp"

    assert to_python.extracted_source == "def solve():\n    print(666)"
    assert "#include <iostream>" in back_to_cpp.extracted_source


def test_client_rejects_invalid_model_or_temperature() -> None:
    with pytest.raises(LMStudioClientError) as model_excinfo:
        LMStudioTranslationClient(model="")
    assert "Model must be a non-empty string" in str(model_excinfo.value)

    with pytest.raises(LMStudioClientError) as temperature_excinfo:
        LMStudioTranslationClient(model="test", temperature=0.5)
    assert "Temperature must be 0" in str(temperature_excinfo.value)


def test_client_recovers_longest_unfenced_code_span_with_surrounding_prose() -> None:
    statement, sample_input, sample_output, seed_cpp = _load_curated_problem_text()
    transport = RecordingTransport(
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
    client = LMStudioTranslationClient(model="gpt-5.4", transport=transport)

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


def test_source_extraction_error_keeps_request_and_response_payloads() -> None:
    statement, sample_input, sample_output, seed_cpp = _load_curated_problem_text()
    transport = RecordingTransport(
        responses=[
            _build_response(
                "No code can be provided in this answer. Please rewrite manually."
            )
        ]
    )
    client = LMStudioTranslationClient(model="gpt-5.4", transport=transport)

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
    assert request_payload["metadata"]["iteration_index"] == 1
    assert response_payload["choices"][0]["message"]["content"].startswith("No code")


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
        "id": "response-001",
        "model": "gpt-5.4",
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
