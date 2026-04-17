from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Any, Protocol

from openai import OpenAI

from rttdist.artifacts import (
    MockOpenAIChoice,
    MockOpenAIMessage,
    MockOpenAIRequest,
    MockOpenAIResponse,
    MockOpenAIUsage,
)
from rttdist.config import PINNED_OPENAI_MODEL, SUPPORTED_OPENAI_MODELS
from rttdist.embedding import (
    EmbeddedSource,
    EmbeddingProvider,
    EmbeddingProviderError,
    EmbeddingUsage,
    hash_source_text,
)
from rttdist.extract import (
    SourceExtractionError as ExtractionPrimitiveError,
    extract_single_file_source as extract_single_file_source_primitive,
)
from rttdist.prompts import (
    PromptTemplateError,
    build_translation_prompt,
)


class OpenAIClientError(RuntimeError):
    pass


class OpenAIResponseParseError(OpenAIClientError):
    pass


class OpenAIEmbeddingResponseParseError(OpenAIClientError):
    pass


class SourceExtractionError(OpenAIClientError):
    pass


class ChatCompletionsTransport(Protocol):
    def create_chat_completion(self, payload: dict[str, Any]) -> dict[str, Any]: ...


@dataclass(frozen=True)
class OpenAIEmbeddingTransportResponse:
    payload: dict[str, Any]
    request_id: str | None


class EmbeddingsTransport(Protocol):
    def create_embedding(
        self, payload: dict[str, Any]
    ) -> OpenAIEmbeddingTransportResponse: ...


@dataclass(frozen=True)
class TranslationResult:
    request: MockOpenAIRequest
    response: MockOpenAIResponse
    extracted_source: str


@dataclass(frozen=True)
class OpenAIEmbeddingResult:
    configured_model: str
    observed_model: str
    request_id: str | None
    dimensions: int
    vector: tuple[float, ...]
    usage: EmbeddingUsage | None


class OpenAITranslationClient:
    def __init__(
        self,
        *,
        model: str = PINNED_OPENAI_MODEL,
        temperature: float = 0.0,
        transport: ChatCompletionsTransport | None = None,
    ) -> None:
        if model not in SUPPORTED_OPENAI_MODELS:
            supported = ", ".join(sorted(SUPPORTED_OPENAI_MODELS))
            raise OpenAIClientError(
                "Model is pinned to an approved set for reproducibility and must be one of: "
                f"{supported}."
            )
        if float(temperature) != 0.0:
            raise OpenAIClientError(
                "Temperature must be 0 for deterministic translations."
            )

        self._model = model
        self._temperature = 0.0
        self._transport = transport or _build_default_transport()

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
        return self.translate(
            problem_id=problem_id,
            source_language="cpp",
            target_language=target_language,
            problem_statement=problem_statement,
            sample_input=sample_input,
            sample_output=sample_output,
            source_code=source_code,
            iteration_index=iteration_index,
            direction="seed_to_target",
        )

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
        return self.translate(
            problem_id=problem_id,
            source_language=source_language,
            target_language="cpp",
            problem_statement=problem_statement,
            sample_input=sample_input,
            sample_output=sample_output,
            source_code=source_code,
            iteration_index=iteration_index,
            direction="target_to_seed",
        )

    def translate(
        self,
        *,
        problem_id: str,
        source_language: str,
        target_language: str,
        problem_statement: str,
        sample_input: str,
        sample_output: str,
        source_code: str,
        iteration_index: int,
        direction: str = "source_to_target",
    ) -> TranslationResult:
        try:
            prompt = build_translation_prompt(
                problem_id=problem_id,
                source_language=source_language,
                target_language=target_language,
                problem_statement=problem_statement,
                sample_input=sample_input,
                sample_output=sample_output,
                source_code=source_code,
                direction=direction,
            )
        except PromptTemplateError as exc:
            raise OpenAIClientError(str(exc)) from exc

        metadata = {
            "direction": prompt.direction,
            "problem_id": problem_id,
            "source_language": prompt.source_language,
            "target_language": prompt.target_language,
            "iteration_index": iteration_index,
        }
        request = MockOpenAIRequest(
            model=self._model,
            temperature=self._temperature,
            messages=prompt.messages,
            metadata=metadata,
        )
        return self._translate(request)

    def _translate(self, request: MockOpenAIRequest) -> TranslationResult:
        payload = request.to_dict()
        try:
            response_payload = self._transport.create_chat_completion(payload)
        except OpenAIClientError as exc:
            _attach_translation_debug_payloads(exc, request_payload=payload)
            raise
        except Exception as exc:
            wrapped = OpenAIClientError(str(exc))
            _attach_translation_debug_payloads(wrapped, request_payload=payload)
            raise wrapped from exc

        try:
            response = parse_openai_response(response_payload)
        except OpenAIResponseParseError as exc:
            _attach_translation_debug_payloads(
                exc,
                request_payload=payload,
                response_payload=response_payload,
            )
            raise

        try:
            extracted_source = extract_single_file_source(response)
        except SourceExtractionError as exc:
            _attach_translation_debug_payloads(
                exc,
                request_payload=payload,
                response_payload=response.to_dict(),
            )
            raise

        return TranslationResult(
            request=request,
            response=response,
            extracted_source=extracted_source,
        )


def parse_openai_response(raw_response: dict[str, Any]) -> MockOpenAIResponse:
    if not isinstance(raw_response, dict):
        raise OpenAIResponseParseError("OpenAI response payload must be a mapping.")

    response_id = raw_response.get("id")
    if not isinstance(response_id, str) or not response_id.strip():
        raise OpenAIResponseParseError(
            "OpenAI response `id` must be a non-empty string."
        )

    model = raw_response.get("model")
    if not isinstance(model, str) or not model.strip():
        raise OpenAIResponseParseError(
            "OpenAI response `model` must be a non-empty string."
        )

    raw_choices = raw_response.get("choices")
    if not isinstance(raw_choices, list) or not raw_choices:
        raise OpenAIResponseParseError(
            "OpenAI response must contain at least one `choices` entry."
        )

    choices: list[MockOpenAIChoice] = []
    for raw_choice in raw_choices:
        if not isinstance(raw_choice, dict):
            raise OpenAIResponseParseError("Each `choices` entry must be a mapping.")

        index = raw_choice.get("index")
        if not isinstance(index, int) or isinstance(index, bool):
            raise OpenAIResponseParseError("`choices[].index` must be an integer.")

        finish_reason = raw_choice.get("finish_reason")
        if not isinstance(finish_reason, str) or not finish_reason.strip():
            raise OpenAIResponseParseError(
                "`choices[].finish_reason` must be a non-empty string."
            )

        raw_message = raw_choice.get("message")
        if not isinstance(raw_message, dict):
            raise OpenAIResponseParseError("`choices[].message` must be a mapping.")

        role = raw_message.get("role")
        content = raw_message.get("content")
        if not isinstance(role, str) or not role.strip():
            raise OpenAIResponseParseError(
                "`choices[].message.role` must be a non-empty string."
            )
        if not isinstance(content, str) or not content.strip():
            raise OpenAIResponseParseError(
                "`choices[].message.content` must be a non-empty string."
            )

        choices.append(
            MockOpenAIChoice(
                index=index,
                message=MockOpenAIMessage(role=role.strip(), content=content),
                finish_reason=finish_reason.strip(),
            )
        )

    raw_usage = raw_response.get("usage")
    if not isinstance(raw_usage, dict):
        raise OpenAIResponseParseError("OpenAI response `usage` must be a mapping.")

    prompt_tokens = _parse_usage_token(raw_usage, field_name="prompt_tokens")
    completion_tokens = _parse_usage_token(raw_usage, field_name="completion_tokens")
    total_tokens = _parse_usage_token(raw_usage, field_name="total_tokens")

    return MockOpenAIResponse(
        response_id=response_id.strip(),
        model=model.strip(),
        choices=tuple(choices),
        usage=MockOpenAIUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
        ),
    )


def parse_openai_embedding_response(
    *,
    raw_response: dict[str, Any],
    configured_model: str,
    fallback_request_id: str | None = None,
) -> OpenAIEmbeddingResult:
    if not isinstance(raw_response, dict):
        raise OpenAIEmbeddingResponseParseError(
            "OpenAI embedding response payload must be a mapping."
        )

    model = raw_response.get("model")
    if not isinstance(model, str) or not model.strip():
        raise OpenAIEmbeddingResponseParseError(
            "OpenAI embedding response `model` must be a non-empty string."
        )

    data = raw_response.get("data")
    if not isinstance(data, list) or len(data) != 1:
        raise OpenAIEmbeddingResponseParseError(
            "OpenAI embedding response must contain exactly one data entry."
        )
    item = data[0]
    if not isinstance(item, dict):
        raise OpenAIEmbeddingResponseParseError(
            "OpenAI embedding response data entry must be a mapping."
        )

    embedding_value = item.get("embedding")
    if not isinstance(embedding_value, list) or not embedding_value:
        raise OpenAIEmbeddingResponseParseError(
            "OpenAI embedding response `data[0].embedding` must be a non-empty list."
        )

    parsed_vector: list[float] = []
    for value in embedding_value:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise OpenAIEmbeddingResponseParseError(
                "OpenAI embedding vector values must be numeric."
            )
        parsed_vector.append(float(value))

    usage_payload = raw_response.get("usage")
    usage = _parse_openai_embedding_usage(usage_payload)

    request_id = _optional_text(raw_response.get("request_id"))
    if request_id is None:
        request_id = _optional_text(fallback_request_id)

    return OpenAIEmbeddingResult(
        configured_model=configured_model,
        observed_model=model.strip(),
        request_id=request_id,
        dimensions=len(parsed_vector),
        vector=tuple(parsed_vector),
        usage=usage,
    )


def extract_single_file_source(response: MockOpenAIResponse | str) -> str:
    try:
        return extract_single_file_source_primitive(response)
    except ExtractionPrimitiveError as exc:
        raise SourceExtractionError(str(exc)) from exc


def _parse_usage_token(raw_usage: dict[str, Any], *, field_name: str) -> int:
    value = raw_usage.get(field_name)
    if not isinstance(value, int) or isinstance(value, bool):
        raise OpenAIResponseParseError(f"`usage.{field_name}` must be an integer.")
    if value < 0:
        raise OpenAIResponseParseError(f"`usage.{field_name}` must be >= 0.")
    return value


def _parse_openai_embedding_usage(raw_usage: Any) -> EmbeddingUsage | None:
    if raw_usage is None:
        return None
    if not isinstance(raw_usage, dict):
        raise OpenAIEmbeddingResponseParseError(
            "OpenAI embedding response `usage` must be a mapping when provided."
        )

    prompt_tokens = raw_usage.get("prompt_tokens")
    total_tokens = raw_usage.get("total_tokens")
    parsed_prompt_tokens: int | None = None
    parsed_total_tokens: int | None = None

    if prompt_tokens is not None:
        if (
            not isinstance(prompt_tokens, int)
            or isinstance(prompt_tokens, bool)
            or prompt_tokens < 0
        ):
            raise OpenAIEmbeddingResponseParseError(
                "OpenAI embedding usage `prompt_tokens` must be an integer >= 0."
            )
        parsed_prompt_tokens = prompt_tokens

    if total_tokens is not None:
        if (
            not isinstance(total_tokens, int)
            or isinstance(total_tokens, bool)
            or total_tokens < 0
        ):
            raise OpenAIEmbeddingResponseParseError(
                "OpenAI embedding usage `total_tokens` must be an integer >= 0."
            )
        parsed_total_tokens = total_tokens

    if parsed_prompt_tokens is None and parsed_total_tokens is None:
        return None
    return EmbeddingUsage(
        prompt_tokens=parsed_prompt_tokens,
        total_tokens=parsed_total_tokens,
    )


def _build_default_transport() -> ChatCompletionsTransport:
    fixture_path = os.environ.get("RTTDIST_OPENAI_MOCK_RESPONSES")
    if fixture_path:
        return _FixtureChatCompletionsTransport(Path(fixture_path))
    return _OpenAIChatCompletionsTransport()


@dataclass(frozen=True)
class _FixtureResponseEntry:
    match: dict[str, Any]
    content: str
    response_id: str | None = None
    prompt_tokens: int = 0
    completion_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


class _FixtureChatCompletionsTransport:
    def __init__(self, fixture_path: Path) -> None:
        self._fixture_path = Path(fixture_path).resolve()
        self._responses = self._load_fixture(self._fixture_path)

    def create_chat_completion(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise OpenAIClientError("Mock transport payload must be a mapping.")

        metadata = payload.get("metadata")
        if not isinstance(metadata, dict):
            raise OpenAIClientError(
                "Mock transport payload must include request metadata."
            )

        for index, entry in enumerate(self._responses, start=1):
            if all(metadata.get(key) == value for key, value in entry.match.items()):
                model = payload.get("model")
                if not isinstance(model, str) or not model.strip():
                    raise OpenAIClientError(
                        "Mock transport payload must include a non-empty model."
                    )
                return {
                    "id": entry.response_id or f"mock-response-{index:03d}",
                    "model": model,
                    "choices": [
                        {
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": _render_mock_response_content(entry.content),
                            },
                            "finish_reason": "stop",
                        }
                    ],
                    "usage": {
                        "prompt_tokens": entry.prompt_tokens,
                        "completion_tokens": entry.completion_tokens,
                        "total_tokens": entry.total_tokens,
                    },
                }

        raise OpenAIClientError(
            "No mock OpenAI response matched request metadata from "
            f"{self._fixture_path}: {metadata}"
        )

    def _load_fixture(self, fixture_path: Path) -> tuple[_FixtureResponseEntry, ...]:
        try:
            raw_data = json.loads(fixture_path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise OpenAIClientError(
                f"Unable to read mock OpenAI fixture: {fixture_path}"
            ) from exc
        except json.JSONDecodeError as exc:
            raise OpenAIClientError(
                f"Invalid JSON in mock OpenAI fixture: {fixture_path}"
            ) from exc

        if not isinstance(raw_data, dict):
            raise OpenAIClientError(
                "Mock OpenAI fixture root must be a mapping with `responses`."
            )

        raw_responses = raw_data.get("responses")
        if not isinstance(raw_responses, list) or not raw_responses:
            raise OpenAIClientError(
                "Mock OpenAI fixture must define a non-empty `responses` list."
            )

        parsed: list[_FixtureResponseEntry] = []
        for index, raw_entry in enumerate(raw_responses):
            if not isinstance(raw_entry, dict):
                raise OpenAIClientError(
                    f"Mock OpenAI fixture response #{index} must be a mapping."
                )

            match = raw_entry.get("match")
            content = raw_entry.get("content")
            if not isinstance(match, dict) or not match:
                raise OpenAIClientError(
                    f"Mock OpenAI fixture response #{index} must define non-empty `match`."
                )
            if not isinstance(content, str) or not content.strip():
                raise OpenAIClientError(
                    f"Mock OpenAI fixture response #{index} must define non-empty `content`."
                )

            parsed.append(
                _FixtureResponseEntry(
                    match=dict(match),
                    content=content,
                    response_id=_optional_text(raw_entry.get("id")),
                    prompt_tokens=_optional_non_negative_int(
                        raw_entry.get("prompt_tokens"), default=0
                    ),
                    completion_tokens=_optional_non_negative_int(
                        raw_entry.get("completion_tokens"), default=0
                    ),
                )
            )

        return tuple(parsed)


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise OpenAIClientError("Optional mock fixture text values must be non-empty.")
    return value.strip()


def _optional_non_negative_int(value: Any, *, default: int) -> int:
    if value is None:
        return default
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise OpenAIClientError(
            "Optional mock fixture token values must be integers >= 0."
        )
    return value


def _render_mock_response_content(content: str) -> str:
    stripped = content.strip()
    if stripped.startswith("```") and stripped.endswith("```"):
        return stripped
    return f"```\n{stripped}\n```"


def _attach_translation_debug_payloads(
    exc: Exception,
    *,
    request_payload: dict[str, Any],
    response_payload: dict[str, Any] | None = None,
) -> None:
    setattr(exc, "request_payload", request_payload)
    if response_payload is not None:
        setattr(exc, "response_payload", response_payload)


def _attach_embedding_debug_payloads(
    exc: Exception,
    *,
    request_payload: dict[str, Any],
    response_payload: dict[str, Any] | None = None,
) -> None:
    setattr(exc, "request_payload", request_payload)
    if response_payload is not None:
        setattr(exc, "response_payload", response_payload)


class _OpenAIChatCompletionsTransport:
    def __init__(self) -> None:
        self._client = OpenAI()

    def create_chat_completion(self, payload: dict[str, Any]) -> dict[str, Any]:
        request_payload = dict(payload)
        request_payload.pop("metadata", None)
        response = self._client.chat.completions.create(**request_payload)
        return response.model_dump(mode="python")


class _OpenAIEmbeddingsTransport:
    def __init__(self) -> None:
        self._client = OpenAI()

    def create_embedding(
        self, payload: dict[str, Any]
    ) -> OpenAIEmbeddingTransportResponse:
        response = self._client.embeddings.create(**dict(payload))
        request_id = _extract_openai_request_id(response)
        return OpenAIEmbeddingTransportResponse(
            payload=response.model_dump(mode="python"),
            request_id=request_id,
        )


def _extract_openai_request_id(response: Any) -> str | None:
    for attribute_name in ("_request_id", "request_id"):
        attribute_value = getattr(response, attribute_name, None)
        if isinstance(attribute_value, str) and attribute_value.strip():
            return attribute_value.strip()

    headers = getattr(response, "headers", None)
    if isinstance(headers, dict):
        for key in ("x-request-id", "request-id"):
            header_value = headers.get(key)
            if isinstance(header_value, str) and header_value.strip():
                return header_value.strip()
    return None


DEFAULT_OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


class OpenAIFinalSimilarityProvider(EmbeddingProvider):
    provider_name = "openai"

    def __init__(
        self,
        *,
        model: str = DEFAULT_OPENAI_EMBEDDING_MODEL,
        transport: EmbeddingsTransport | None = None,
    ) -> None:
        if not isinstance(model, str) or not model.strip():
            raise OpenAIClientError("Embedding model must be a non-empty string.")
        self.configured_model = model.strip()
        self._transport = transport or _OpenAIEmbeddingsTransport()

    def embed_source(self, *, source_text: str) -> EmbeddedSource:
        if not isinstance(source_text, str) or not source_text.strip():
            raise EmbeddingProviderError("Embedding source text must be non-empty.")

        payload = {
            "model": self.configured_model,
            "input": source_text,
            "encoding_format": "float",
        }
        try:
            response = self._transport.create_embedding(payload)
        except OpenAIClientError as exc:
            _attach_embedding_debug_payloads(exc, request_payload=payload)
            raise
        except Exception as exc:
            wrapped = OpenAIClientError(str(exc))
            _attach_embedding_debug_payloads(wrapped, request_payload=payload)
            raise wrapped from exc

        try:
            parsed = parse_openai_embedding_response(
                raw_response=response.payload,
                configured_model=self.configured_model,
                fallback_request_id=response.request_id,
            )
        except OpenAIEmbeddingResponseParseError as exc:
            _attach_embedding_debug_payloads(
                exc,
                request_payload=payload,
                response_payload=response.payload,
            )
            raise

        return EmbeddedSource(
            source_hash=hash_source_text(source_text),
            provider=self.provider_name,
            configured_model=parsed.configured_model,
            observed_model=parsed.observed_model,
            request_id=parsed.request_id,
            dimensions=parsed.dimensions,
            vector=parsed.vector,
            usage=parsed.usage,
        )
