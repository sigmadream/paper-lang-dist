from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Any, Protocol
from urllib import error, request

from rttdist.artifacts import (
    MockLLMChoice,
    MockLLMMessage,
    MockLLMRequest,
    MockLLMResponse,
    MockLLMUsage,
)
from rttdist.config import DEFAULT_LMSTUDIO_HOST
from rttdist.extract import (
    SourceExtractionError as ExtractionPrimitiveError,
    extract_single_file_source as extract_single_file_source_primitive,
)
from rttdist.prompts import (
    PromptTemplateError,
    build_translation_prompt,
)


class LMStudioClientError(RuntimeError):
    pass


class LMStudioResponseParseError(LMStudioClientError):
    pass


class SourceExtractionError(LMStudioClientError):
    pass


class LMStudioChatTransport(Protocol):
    def create_chat_completion(self, payload: dict[str, Any]) -> dict[str, Any]: ...


@dataclass(frozen=True)
class TranslationResult:
    request: MockLLMRequest
    response: MockLLMResponse
    extracted_source: str


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


class LMStudioTranslationClient:
    def __init__(
        self,
        *,
        model: str,
        temperature: float = 0.0,
        host: str = DEFAULT_LMSTUDIO_HOST,
        transport: LMStudioChatTransport | None = None,
    ) -> None:
        if not isinstance(model, str) or not model.strip():
            raise LMStudioClientError("Model must be a non-empty string.")
        if float(temperature) != 0.0:
            raise LMStudioClientError(
                "Temperature must be 0 for deterministic translations."
            )
        if not isinstance(host, str) or not host.strip():
            raise LMStudioClientError("Host must be a non-empty string.")

        self._model = model.strip()
        self._temperature = 0.0
        self._host = host.strip().rstrip("/")
        self._transport = transport or _build_default_transport(host=self._host)

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
            raise LMStudioClientError(str(exc)) from exc

        metadata = {
            "direction": prompt.direction,
            "problem_id": problem_id,
            "source_language": prompt.source_language,
            "target_language": prompt.target_language,
            "iteration_index": iteration_index,
            "provider": "lmstudio",
        }
        request_payload = MockLLMRequest(
            model=self._model,
            temperature=self._temperature,
            messages=prompt.messages,
            metadata=metadata,
        )
        return self._translate(request_payload)

    def _translate(self, request_payload: MockLLMRequest) -> TranslationResult:
        payload = request_payload.to_dict()
        try:
            response_payload = self._transport.create_chat_completion(payload)
        except LMStudioClientError as exc:
            _attach_translation_debug_payloads(exc, request_payload=payload)
            raise
        except Exception as exc:
            wrapped = LMStudioClientError(str(exc))
            _attach_translation_debug_payloads(wrapped, request_payload=payload)
            raise wrapped from exc

        try:
            response = parse_lmstudio_response(response_payload)
        except LMStudioResponseParseError as exc:
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
            request=request_payload,
            response=response,
            extracted_source=extracted_source,
        )


def _build_default_transport(*, host: str) -> LMStudioChatTransport:
    fixture_path = os.environ.get("RTTDIST_LLM_MOCK_RESPONSES")
    if fixture_path:
        return _FixtureChatCompletionsTransport(Path(fixture_path))
    return _LMStudioHTTPTransport(host=host)


class _FixtureChatCompletionsTransport:
    def __init__(self, fixture_path: Path) -> None:
        self._fixture_path = Path(fixture_path).resolve()
        self._responses = self._load_fixture(self._fixture_path)

    def create_chat_completion(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise LMStudioClientError("Mock transport payload must be a mapping.")

        metadata = payload.get("metadata")
        if not isinstance(metadata, dict):
            raise LMStudioClientError(
                "Mock transport payload must include request metadata."
            )

        for index, entry in enumerate(self._responses, start=1):
            if all(metadata.get(key) == value for key, value in entry.match.items()):
                model = payload.get("model")
                if not isinstance(model, str) or not model.strip():
                    raise LMStudioClientError(
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

        raise LMStudioClientError(
            "No mock LM Studio response matched request metadata from "
            f"{self._fixture_path}: {metadata}"
        )

    def _load_fixture(self, fixture_path: Path) -> tuple[_FixtureResponseEntry, ...]:
        try:
            raw_data = json.loads(fixture_path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise LMStudioClientError(
                f"Unable to read mock LM Studio fixture: {fixture_path}"
            ) from exc
        except json.JSONDecodeError as exc:
            raise LMStudioClientError(
                f"Invalid JSON in mock LM Studio fixture: {fixture_path}"
            ) from exc

        if not isinstance(raw_data, dict):
            raise LMStudioClientError(
                "Mock LM Studio fixture root must be a mapping with `responses`."
            )

        raw_responses = raw_data.get("responses")
        if not isinstance(raw_responses, list) or not raw_responses:
            raise LMStudioClientError(
                "Mock LM Studio fixture must define a non-empty `responses` list."
            )

        parsed: list[_FixtureResponseEntry] = []
        for index, raw_entry in enumerate(raw_responses):
            if not isinstance(raw_entry, dict):
                raise LMStudioClientError(
                    f"Mock LM Studio fixture response #{index} must be a mapping."
                )

            match = raw_entry.get("match")
            if not isinstance(match, dict):
                raise LMStudioClientError(
                    f"Mock LM Studio fixture response #{index} must include `match` mapping."
                )

            content = raw_entry.get("content")
            if not isinstance(content, str) or not content.strip():
                raise LMStudioClientError(
                    f"Mock LM Studio fixture response #{index} must include non-empty `content`."
                )

            parsed.append(
                _FixtureResponseEntry(
                    match=match,
                    content=content.strip(),
                    response_id=raw_entry.get("id"),
                    prompt_tokens=int(raw_entry.get("prompt_tokens", 0)),
                    completion_tokens=int(raw_entry.get("completion_tokens", 0)),
                )
            )
        return tuple(parsed)


def parse_lmstudio_response(raw_response: dict[str, Any]) -> MockLLMResponse:
    if not isinstance(raw_response, dict):
        raise LMStudioResponseParseError("LM Studio response payload must be a mapping.")

    response_id = raw_response.get("id")
    if not isinstance(response_id, str) or not response_id.strip():
        raise LMStudioResponseParseError(
            "LM Studio response `id` must be a non-empty string."
        )

    model = raw_response.get("model")
    if not isinstance(model, str) or not model.strip():
        raise LMStudioResponseParseError(
            "LM Studio response `model` must be a non-empty string."
        )

    raw_choices = raw_response.get("choices")
    if not isinstance(raw_choices, list) or not raw_choices:
        raise LMStudioResponseParseError(
            "LM Studio response must contain at least one `choices` entry."
        )

    choices: list[MockLLMChoice] = []
    for raw_choice in raw_choices:
        if not isinstance(raw_choice, dict):
            raise LMStudioResponseParseError("Each `choices` entry must be a mapping.")

        index = raw_choice.get("index")
        if not isinstance(index, int) or isinstance(index, bool):
            raise LMStudioResponseParseError("`choices[].index` must be an integer.")

        finish_reason = raw_choice.get("finish_reason")
        if not isinstance(finish_reason, str) or not finish_reason.strip():
            finish_reason = "stop"

        raw_message = raw_choice.get("message")
        if not isinstance(raw_message, dict):
            raise LMStudioResponseParseError("`choices[].message` must be a mapping.")

        role = raw_message.get("role")
        content = raw_message.get("content")
        if not isinstance(role, str) or not role.strip():
            raise LMStudioResponseParseError(
                "`choices[].message.role` must be a non-empty string."
            )
        if not isinstance(content, str) or not content.strip():
            raise LMStudioResponseParseError(
                "`choices[].message.content` must be a non-empty string."
            )

        choices.append(
            MockLLMChoice(
                index=index,
                message=MockLLMMessage(role=role.strip(), content=content),
                finish_reason=finish_reason.strip(),
            )
        )

    raw_usage = raw_response.get("usage")
    if not isinstance(raw_usage, dict):
        raw_usage = {}

    prompt_tokens = _parse_usage_token(raw_usage, field_name="prompt_tokens")
    completion_tokens = _parse_usage_token(raw_usage, field_name="completion_tokens")
    total_tokens = _parse_usage_token(raw_usage, field_name="total_tokens")

    if total_tokens == 0 and (prompt_tokens > 0 or completion_tokens > 0):
        total_tokens = prompt_tokens + completion_tokens

    return MockLLMResponse(
        response_id=response_id.strip(),
        model=model.strip(),
        choices=tuple(choices),
        usage=MockLLMUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
        ),
    )


def extract_single_file_source(response: MockLLMResponse | str) -> str:
    try:
        return extract_single_file_source_primitive(response)
    except ExtractionPrimitiveError as exc:
        raise SourceExtractionError(str(exc)) from exc


def _parse_usage_token(raw_usage: dict[str, Any], *, field_name: str) -> int:
    value = raw_usage.get(field_name)
    if value is None:
        return 0
    if not isinstance(value, int) or isinstance(value, bool):
        return 0
    if value < 0:
        return 0
    return value


@dataclass(frozen=True)
class _LMStudioHTTPTransport:
    host: str

    def create_chat_completion(self, payload: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise LMStudioClientError("LM Studio transport payload must be a mapping.")

        model = payload.get("model")
        messages = payload.get("messages")
        temperature = payload.get("temperature", 0.0)
        if not isinstance(model, str) or not model.strip():
            raise LMStudioClientError("LM Studio transport requires a non-empty model.")
        if not isinstance(messages, list) or not messages:
            raise LMStudioClientError("LM Studio transport requires non-empty messages.")

        body = {
            "model": model,
            "messages": messages,
            "stream": False,
            "temperature": float(temperature),
        }
        return self._request_json("/chat/completions", method="POST", body=body)

    def _request_json(
        self,
        path: str,
        *,
        method: str,
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        request_body = json.dumps(body).encode("utf-8") if body is not None else None
        headers = {"Content-Type": "application/json"} if body is not None else {}
        url = f"{self.host}{path}"
        http_request = request.Request(
            url=url,
            data=request_body,
            headers=headers,
            method=method,
        )

        try:
            with request.urlopen(http_request, timeout=300) as response:
                raw = response.read().decode("utf-8")
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace").strip()
            raise LMStudioClientError(
                f"LM Studio request failed with HTTP {exc.code}: {detail or exc.reason}"
            ) from exc
        except error.URLError as exc:
            raise LMStudioClientError(
                f"Unable to reach LM Studio at {self.host}: {exc.reason}"
            ) from exc
        except OSError as exc:
            raise LMStudioClientError(f"LM Studio request failed: {exc}") from exc

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise LMStudioClientError("LM Studio returned invalid JSON.") from exc
        if not isinstance(parsed, dict):
            raise LMStudioClientError("LM Studio response root must be a mapping.")
        return parsed


def _render_mock_response_content(content: str) -> str:
    # If content doesn't look like code, wrap it in a mock markdown block for extraction tests
    if "```" not in content and "def " not in content and "#include" not in content:
        return f"Here is the translated code:\n\n```cpp\n{content}\n```"
    return content


def _attach_translation_debug_payloads(
    exc: Exception,
    *,
    request_payload: dict[str, Any],
    response_payload: dict[str, Any] | None = None,
) -> None:
    setattr(exc, "request_payload", request_payload)
    if response_payload is not None:
        setattr(exc, "response_payload", response_payload)
