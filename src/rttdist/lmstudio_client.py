from __future__ import annotations

from dataclasses import dataclass
import json
import math
from typing import Any, Protocol
from urllib import error, request

from rttdist.artifacts import (
    LLMChoice,
    LLMMessage,
    LLMRequest,
    LLMResponse,
    LLMUsage,
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
    request: LLMRequest
    response: LLMResponse
    extracted_source: str


class LMStudioTranslationClient:
    def __init__(
        self,
        *,
        model: str,
        temperature: float = 0.0,
        host: str = DEFAULT_LMSTUDIO_HOST,
        transport: LMStudioChatTransport | None = None,
        prompt_template_version: str = "rtt.prompts.v1",
        provider_name: str = 'lmstudio',
    ) -> None:
        if not isinstance(model, str) or not model.strip():
            raise LMStudioClientError("Model must be a non-empty string.")
        if isinstance(temperature, bool) or not isinstance(temperature, (int, float)) or not math.isfinite(temperature) or temperature < 0:
            raise LMStudioClientError(
                "Temperature must be finite and nonnegative."
            )
        if not isinstance(host, str) or not host.strip():
            raise LMStudioClientError("Host must be a non-empty string.")

        self._model = model.strip()
        self._provider_name = provider_name
        self._prompt_template_version = prompt_template_version
        self._temperature = float(temperature)
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
                template_version=self._prompt_template_version,
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
            "provider": self._provider_name,
        }
        if self._prompt_template_version != "rtt.prompts.v1":
            metadata["prompt_template_version"] = self._prompt_template_version
        request_payload = LLMRequest(
            model=self._model,
            temperature=self._temperature,
            messages=prompt.messages,
            metadata=metadata,
        )
        return self._translate(request_payload)

    def _translate(self, request_payload: LLMRequest) -> TranslationResult:
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
            if request_payload.metadata.get('target_language') in ('haskell','prolog'):
                from rttdist.extract import extract_single_file_source_text
                extracted_source = extract_single_file_source_text(response.choices[0].message.content,preserve_unfenced=True)
            else:
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
    return _LMStudioHTTPTransport(host=host)


def parse_lmstudio_response(raw_response: dict[str, Any]) -> LLMResponse:
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

    choices: list[LLMChoice] = []
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
            LLMChoice(
                index=index,
                message=LLMMessage(role=role.strip(), content=content),
                finish_reason=finish_reason.strip(),
            )
        )

    raw_usage = raw_response.get("usage")
    if not isinstance(raw_usage, dict):
        raw_usage = {}

    prompt_tokens = _parse_usage_token(raw_usage, field_name="prompt_tokens")
    completion_tokens = _parse_usage_token(raw_usage, field_name="completion_tokens")
    total_tokens = _parse_usage_token(raw_usage, field_name="total_tokens")

    return LLMResponse(
        response_id=response_id.strip(),
        model=model.strip(),
        choices=tuple(choices),
        usage=LLMUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
        ),
    )


def extract_single_file_source(response: LLMResponse | str) -> str:
    try:
        return extract_single_file_source_primitive(response)
    except ExtractionPrimitiveError as exc:
        raise SourceExtractionError(str(exc)) from exc


def _parse_usage_token(raw_usage: dict[str, Any], *, field_name: str) -> int | None:
    value = raw_usage.get(field_name)
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool):
        return None
    if value < 0:
        return None
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


def _attach_translation_debug_payloads(
    exc: Exception,
    *,
    request_payload: dict[str, Any],
    response_payload: dict[str, Any] | None = None,
) -> None:
    setattr(exc, "request_payload", request_payload)
    if response_payload is not None:
        setattr(exc, "response_payload", response_payload)
