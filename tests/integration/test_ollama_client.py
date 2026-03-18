from __future__ import annotations

from pathlib import Path
from typing import cast

import pytest

from rttdist.ollama_client import (
    OllamaClientError,
    OllamaResponseParseError,
    OllamaTranslationClient,
    ensure_ollama_model_available,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
CURATED_PROBLEM_ROOT = (
    REPO_ROOT / "tests" / "fixtures" / "curated_problem" / "IPOP_1436"
)


class FakeOllamaTransport:
    def __init__(
        self,
        responses: list[dict[str, object]],
        *,
        model_list_response: dict[str, object] | None = None,
    ) -> None:
        self._responses = responses
        self._model_list_response = model_list_response or {"models": []}
        self.requests: list[dict[str, object]] = []

    def create_chat_completion(self, payload: dict[str, object]) -> dict[str, object]:
        self.requests.append(payload)
        if not self._responses:
            raise AssertionError("No mocked Ollama response available.")
        response = self._responses.pop(0)
        if not isinstance(response, dict):
            raise AssertionError("Mocked Ollama response must be a mapping.")
        return response

    def list_models(self) -> dict[str, object]:
        return self._model_list_response


def test_ollama_client_translates_both_directions_with_mocked_transport() -> None:
    statement, sample_input, sample_output, seed_cpp = _load_curated_problem_text()
    transport = FakeOllamaTransport(
        responses=[
            _build_ollama_response("```python\ndef solve():\n    print(666)\n```"),
            _build_ollama_response(
                "```cpp\n#include <iostream>\nint main(){ std::cout << 666 << '\\n'; }\n```"
            ),
        ]
    )
    client = OllamaTranslationClient(
        model="qwen2.5-coder:7b",
        host="http://localhost:11434",
        transport=transport,
    )

    to_python = client.translate_cpp_to_target(
        problem_id="IPOP_1436",
        target_language="python",
        problem_statement=statement,
        sample_input=sample_input,
        sample_output=sample_output,
        source_code=seed_cpp,
        iteration_index=1,
    )
    back_to_cpp = client.translate_target_to_cpp(
        problem_id="IPOP_1436",
        source_language="python",
        problem_statement=statement,
        sample_input=sample_input,
        sample_output=sample_output,
        source_code=to_python.extracted_source,
        iteration_index=1,
    )

    assert len(transport.requests) == 2
    first_metadata = cast(dict[str, object], transport.requests[0]["metadata"])
    second_metadata = cast(dict[str, object], transport.requests[1]["metadata"])
    assert first_metadata["iteration_index"] == "1"
    assert second_metadata["iteration_index"] == "1"
    assert to_python.request.model == "qwen2.5-coder:7b"
    assert to_python.request.metadata["provider"] == "ollama"
    assert back_to_cpp.request.metadata["provider"] == "ollama"
    assert to_python.extracted_source == "def solve():\n    print(666)"
    assert "#include <iostream>" in back_to_cpp.extracted_source


def test_ollama_client_rejects_invalid_model_or_temperature() -> None:
    with pytest.raises(OllamaClientError):
        OllamaTranslationClient(model="")

    with pytest.raises(OllamaClientError):
        OllamaTranslationClient(model="qwen2.5-coder:7b", temperature=0.2)


def test_ollama_client_rejects_missing_message_content() -> None:
    transport = FakeOllamaTransport(
        responses=[{"model": "qwen2.5-coder:7b", "message": {"role": "assistant"}}]
    )
    client = OllamaTranslationClient(
        model="qwen2.5-coder:7b",
        transport=transport,
    )

    statement, sample_input, sample_output, seed_cpp = _load_curated_problem_text()
    with pytest.raises(OllamaResponseParseError):
        client.translate_cpp_to_target(
            problem_id="IPOP_1436",
            target_language="python",
            problem_statement=statement,
            sample_input=sample_input,
            sample_output=sample_output,
            source_code=seed_cpp,
            iteration_index=1,
        )


def test_ensure_ollama_model_available_accepts_installed_model() -> None:
    transport = FakeOllamaTransport(
        responses=[],
        model_list_response={
            "models": [
                {"name": "qwen2.5-coder:7b"},
                {"name": "qwen2.5:3b"},
            ]
        },
    )

    ensure_ollama_model_available(
        model="qwen2.5-coder:7b",
        transport=transport,
    )


def test_ensure_ollama_model_available_reports_missing_model_clearly() -> None:
    transport = FakeOllamaTransport(
        responses=[],
        model_list_response={
            "models": [
                {"name": "qwen2.5:3b"},
                {"name": "qwen3:latest"},
            ]
        },
    )

    with pytest.raises(OllamaClientError, match="ollama pull qwen2.5-coder:7b"):
        ensure_ollama_model_available(
            model="qwen2.5-coder:7b",
            host="http://localhost:11434",
            transport=transport,
        )


def test_ollama_parse_error_keeps_request_and_raw_response_payloads() -> None:
    transport = FakeOllamaTransport(
        responses=[{"model": "qwen2.5-coder:7b", "message": "not-a-mapping"}]
    )
    client = OllamaTranslationClient(
        model="qwen2.5-coder:7b",
        transport=transport,
    )

    statement, sample_input, sample_output, seed_cpp = _load_curated_problem_text()
    with pytest.raises(OllamaResponseParseError) as excinfo:
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
    assert response_payload["message"] == "not-a-mapping"


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


def _build_ollama_response(content: str) -> dict[str, object]:
    return {
        "model": "qwen2.5-coder:7b",
        "message": {"role": "assistant", "content": content},
        "done": True,
        "done_reason": "stop",
        "prompt_eval_count": 10,
        "eval_count": 5,
    }
