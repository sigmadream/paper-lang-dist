from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Protocol
from urllib import error, request

from rttdist.artifacts import MockOpenAIRequest
from rttdist.config import DEFAULT_OLLAMA_HOST
from rttdist.extract import SourceExtractionError as ExtractionPrimitiveError
from rttdist.extract import (
    extract_single_file_source as extract_single_file_source_primitive,
)
from rttdist.openai_client import (
    OpenAIResponseParseError,
    TranslationResult,
    parse_openai_response,
)
from rttdist.prompts import (
    PromptTemplateError,
    build_cpp_to_target_prompt,
    build_target_to_cpp_prompt,
)


class OllamaClientError(RuntimeError):
    pass


class OllamaResponseParseError(OllamaClientError):
    pass


class SourceExtractionError(OllamaClientError):
    pass


class OllamaChatTransport(Protocol):
    def create_chat_completion(self, payload: dict[str, Any]) -> dict[str, Any]: ...

    def list_models(self) -> dict[str, Any]: ...


def ensure_ollama_model_available(
    *,
    model: str,
    host: str = DEFAULT_OLLAMA_HOST,
    transport: OllamaChatTransport | None = None,
) -> None:
    normalized_model = model.strip() if isinstance(model, str) else ""
    if not normalized_model:
        raise OllamaClientError("Model must be a non-empty string.")

    normalized_host = host.strip().rstrip("/") if isinstance(host, str) else ""
    if not normalized_host:
        raise OllamaClientError("Host must be a non-empty string.")

    effective_transport = transport or _OllamaHTTPTransport(host=normalized_host)
    raw_response = effective_transport.list_models()
    if not isinstance(raw_response, dict):
        raise OllamaClientError("Ollama model list response must be a mapping.")

    raw_models = raw_response.get("models")
    if not isinstance(raw_models, list):
        raise OllamaClientError("Ollama model list response must include `models`.")

    installed_models: set[str] = set()
    for item in raw_models:
        if not isinstance(item, dict):
            continue
        for key in ("name", "model"):
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                installed_models.add(value.strip())

    if normalized_model in installed_models:
        return

    installed_text = ", ".join(sorted(installed_models)) or "none"
    raise OllamaClientError(
        f"Ollama model `{normalized_model}` is not installed at {normalized_host}. "
        f"Run `ollama pull {normalized_model}` first. Installed models: {installed_text}."
    )


class OllamaTranslationClient:
    def __init__(
        self,
        *,
        model: str,
        temperature: float = 0.0,
        host: str = DEFAULT_OLLAMA_HOST,
        transport: OllamaChatTransport | None = None,
    ) -> None:
        if not isinstance(model, str) or not model.strip():
            raise OllamaClientError("Model must be a non-empty string.")
        if float(temperature) != 0.0:
            raise OllamaClientError(
                "Temperature must be 0 for deterministic translations."
            )
        if not isinstance(host, str) or not host.strip():
            raise OllamaClientError("Host must be a non-empty string.")

        self._model = model.strip()
        self._temperature = 0.0
        self._host = host.strip().rstrip("/")
        self._transport = transport or _OllamaHTTPTransport(host=self._host)

    def translate_cpp_to_target(
        self,
        *,
        problem_id: str,
        target_language: str,
        problem_statement: str,
        sample_input: str,
        sample_output: str,
        source_code: str,
        iteration_index: int,
    ) -> TranslationResult:
        try:
            prompt = build_cpp_to_target_prompt(
                problem_id=problem_id,
                target_language=target_language,
                problem_statement=problem_statement,
                sample_input=sample_input,
                sample_output=sample_output,
                source_code=source_code,
            )
        except PromptTemplateError as exc:
            raise OllamaClientError(str(exc)) from exc

        request_payload = MockOpenAIRequest(
            model=self._model,
            temperature=self._temperature,
            messages=prompt.messages,
            metadata={
                "provider": "ollama",
                "direction": prompt.direction,
                "problem_id": problem_id,
                "seed_language": "cpp",
                "target_language": prompt.target_language,
                "iteration_index": iteration_index,
                "host": self._host,
            },
        )
        return self._translate(request_payload)

    def translate_target_to_cpp(
        self,
        *,
        problem_id: str,
        source_language: str,
        problem_statement: str,
        sample_input: str,
        sample_output: str,
        source_code: str,
        iteration_index: int,
    ) -> TranslationResult:
        try:
            prompt = build_target_to_cpp_prompt(
                problem_id=problem_id,
                source_language=source_language,
                problem_statement=problem_statement,
                sample_input=sample_input,
                sample_output=sample_output,
                source_code=source_code,
            )
        except PromptTemplateError as exc:
            raise OllamaClientError(str(exc)) from exc

        request_payload = MockOpenAIRequest(
            model=self._model,
            temperature=self._temperature,
            messages=prompt.messages,
            metadata={
                "provider": "ollama",
                "direction": prompt.direction,
                "problem_id": problem_id,
                "seed_language": "cpp",
                "source_language": prompt.source_language,
                "target_language": "cpp",
                "iteration_index": iteration_index,
                "host": self._host,
            },
        )
        return self._translate(request_payload)

    def _translate(self, request_payload: MockOpenAIRequest) -> TranslationResult:
        payload = request_payload.to_dict()
        try:
            raw_response = self._transport.create_chat_completion(payload)
        except OllamaClientError as exc:
            _attach_translation_debug_payloads(exc, request_payload=payload)
            raise
        except Exception as exc:
            wrapped = OllamaClientError(str(exc))
            _attach_translation_debug_payloads(wrapped, request_payload=payload)
            raise wrapped from exc

        try:
            normalized_response = normalize_ollama_response(
                raw_response, model=self._model
            )
        except OllamaResponseParseError as exc:
            _attach_translation_debug_payloads(
                exc,
                request_payload=payload,
                response_payload=raw_response,
            )
            raise

        try:
            response = parse_openai_response(normalized_response)
        except OpenAIResponseParseError as exc:
            wrapped = OllamaResponseParseError(str(exc))
            _attach_translation_debug_payloads(
                wrapped,
                request_payload=payload,
                response_payload=raw_response,
            )
            raise wrapped from exc

        try:
            extracted_source = extract_single_file_source_primitive(response)
        except ExtractionPrimitiveError as exc:
            wrapped = SourceExtractionError(str(exc))
            _attach_translation_debug_payloads(
                wrapped,
                request_payload=payload,
                response_payload=normalized_response,
            )
            raise wrapped from exc

        return TranslationResult(
            request=request_payload,
            response=response,
            extracted_source=extracted_source,
        )


def normalize_ollama_response(
    raw_response: dict[str, Any], *, model: str
) -> dict[str, Any]:
    if not isinstance(raw_response, dict):
        raise OllamaResponseParseError("Ollama response payload must be a mapping.")

    message = raw_response.get("message")
    if not isinstance(message, dict):
        raise OllamaResponseParseError("Ollama response must include `message`.")

    role = message.get("role", "assistant")
    content = message.get("content")
    if not isinstance(role, str) or not role.strip():
        raise OllamaResponseParseError("Ollama response message role is invalid.")
    if not isinstance(content, str) or not content.strip():
        raise OllamaResponseParseError(
            "Ollama response message content must be a non-empty string."
        )

    prompt_tokens = _optional_non_negative_int(raw_response.get("prompt_eval_count"))
    completion_tokens = _optional_non_negative_int(raw_response.get("eval_count"))
    finish_reason = raw_response.get("done_reason")
    if not isinstance(finish_reason, str) or not finish_reason.strip():
        finish_reason = "stop"

    response_model = raw_response.get("model")
    if not isinstance(response_model, str) or not response_model.strip():
        response_model = model

    response_id = raw_response.get("id")
    if not isinstance(response_id, str) or not response_id.strip():
        response_id = f"ollama-{response_model}-response"

    return {
        "id": response_id,
        "model": response_model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": role.strip(),
                    "content": content,
                },
                "finish_reason": finish_reason.strip(),
            }
        ],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
        },
    }


def _optional_non_negative_int(value: Any) -> int:
    if value is None:
        return 0
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise OllamaResponseParseError("Ollama token counts must be integers >= 0.")
    return value


@dataclass(frozen=True)
class _OllamaHTTPTransport:
    host: str

    def create_chat_completion(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise OllamaClientError("Ollama transport payload must be a mapping.")

        model = payload.get("model")
        messages = payload.get("messages")
        temperature = payload.get("temperature", 0.0)
        if not isinstance(model, str) or not model.strip():
            raise OllamaClientError("Ollama transport requires a non-empty model.")
        if not isinstance(messages, list) or not messages:
            raise OllamaClientError("Ollama transport requires non-empty messages.")

        body = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": float(temperature)},
        }
        return self._request_json("/api/chat", method="POST", body=body)

    def list_models(self) -> dict[str, Any]:
        return self._request_json("/api/tags", method="GET")

    def _request_json(
        self,
        path: str,
        *,
        method: str,
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        request_body = json.dumps(body).encode("utf-8") if body is not None else None
        headers = {"Content-Type": "application/json"} if body is not None else {}
        http_request = request.Request(
            url=f"{self.host}{path}",
            data=request_body,
            headers=headers,
            method=method,
        )

        try:
            with request.urlopen(http_request, timeout=120) as response:
                raw = response.read().decode("utf-8")
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace").strip()
            raise OllamaClientError(
                f"Ollama request failed with HTTP {exc.code}: {detail or exc.reason}"
            ) from exc
        except error.URLError as exc:
            raise OllamaClientError(
                f"Unable to reach Ollama at {self.host}: {exc.reason}"
            ) from exc
        except OSError as exc:
            raise OllamaClientError(f"Ollama request failed: {exc}") from exc

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise OllamaClientError("Ollama returned invalid JSON.") from exc
        if not isinstance(parsed, dict):
            raise OllamaClientError("Ollama response root must be a mapping.")
        return parsed


def _attach_translation_debug_payloads(
    exc: Exception,
    *,
    request_payload: dict[str, Any],
    response_payload: dict[str, Any] | None = None,
) -> None:
    setattr(exc, "request_payload", request_payload)
    if response_payload is not None:
        setattr(exc, "response_payload", response_payload)
