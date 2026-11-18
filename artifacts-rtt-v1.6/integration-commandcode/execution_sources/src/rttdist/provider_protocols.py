"""전송과 독립적으로 요청을 만들고 공급자 응답을 정규화합니다."""

from copy import deepcopy
import math

GENERATION_OPTIONS = {
    "temperature",
    "top_p",
    "seed",
    "max_tokens",
    "max_completion_tokens",
    "max_output_tokens",
    "reasoning_effort",
    "reasoning",
    "thinking",
    "top_k",
    "repeat_penalty",
}


def model_evidence(actual, expected, aliases=None):
    if not isinstance(actual, str) or not actual.strip():
        status = "missing"
    elif actual == expected:
        status = "exact"
    elif actual in (aliases or []):
        status = "alias"
    else:
        status = "mismatch"
    return {
        "status": status,
        "valid": status in ("exact", "alias"),
        "requested": expected,
        "actual": actual,
        "allowed_response_models": list(aliases or []),
    }


def validate_generation(profile, requested):
    profile = profile or {}
    supported = set(
        profile.get("supported_options", ["temperature", "top_p", "max_tokens"])
    )
    unknown = set(requested) - supported
    if unknown:
        raise ValueError(
            f"Unsupported generation options: {sorted(unknown)}; 별도 프로파일이 필요합니다"
        )
    for name, value in requested.items():
        choices = profile.get("option_values", {}).get(name)
        if choices is not None and value not in choices:
            raise ValueError(f"Unsupported generation value for {name}")
        if name in ("temperature", "top_p", "repeat_penalty"):
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
            ):
                raise ValueError(f"Invalid generation value for {name}")
            maximum = (
                1 if name == "top_p" else 2 if name == "temperature" else float("inf")
            )
            if not 0 <= value <= maximum:
                raise ValueError(f"Invalid generation value for {name}")
        if name in (
            "max_tokens",
            "max_completion_tokens",
            "max_output_tokens",
            "top_k",
            "seed",
        ):
            if (
                isinstance(value, bool)
                or not isinstance(value, int)
                or (name != "seed" and value <= 0)
            ):
                raise ValueError(f"Invalid generation value for {name}")
        if name == "reasoning_effort" and value not in (
            "none",
            "minimal",
            "low",
            "medium",
            "high",
            "xhigh",
            "max",
        ):
            raise ValueError("Invalid reasoning_effort")
        if name == "thinking" and (
            not isinstance(value, dict)
            or value.get("type") not in ("enabled", "disabled")
        ):
            raise ValueError("Invalid thinking")
        if name == "reasoning" and (
            not isinstance(value, dict) or set(value) - {"effort", "summary"}
        ):
            raise ValueError("Invalid reasoning")
    limits = set(requested) & {
        "max_tokens",
        "max_completion_tokens",
        "max_output_tokens",
    }
    if len(limits) > 1 or (
        "reasoning" in requested and "reasoning_effort" in requested
    ):
        raise ValueError("Conflicting generation options")
    return deepcopy(requested)


def requested_generation(request):
    nested = request.get("generation", {})
    if not isinstance(nested, dict):
        raise ValueError("generation must be a mapping")
    return {**nested, **{k: v for k, v in request.items() if k in GENERATION_OPTIONS}}


def build_request(protocol, request, profile):
    if protocol not in ("chat_completions", "responses", "copilot_sdk"):
        raise ValueError("Unsupported protocol")
    unknown = (
        set(request)
        - GENERATION_OPTIONS
        - {
            "model",
            "messages",
            "input",
            "instructions",
            "generation",
            "logical_request",
        }
    )
    if unknown:
        raise ValueError(f"Unsupported request options: {sorted(unknown)}")
    model = request.get("model")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("명시적인 model ID가 필요합니다")
    generation = validate_generation(profile, requested_generation(request))
    body = {"model": model}
    if protocol == "responses":
        if "messages" in request and ("input" in request or "instructions" in request):
            raise ValueError("messages and input/instructions cannot be mixed")
        if "messages" in request:
            instructions, messages = [], []
            for message in request["messages"]:
                if message.get("role") in ("system", "developer"):
                    if not isinstance(message.get("content"), str):
                        raise ValueError("instructions content must be text")
                    instructions.append(message["content"])
                else:
                    messages.append(deepcopy(message))
            body["input"] = messages
            if instructions:
                body["instructions"] = "\n\n".join(instructions)
        else:
            body["input"] = deepcopy(request.get("input", []))
            if "instructions" in request:
                body["instructions"] = request["instructions"]
    else:
        if "input" in request or "instructions" in request:
            raise ValueError("messages are required for this protocol")
        body["messages"] = deepcopy(request.get("messages", []))
    for name, value in generation.items():
        target = name
        if name in ("max_tokens", "max_completion_tokens", "max_output_tokens"):
            target = (
                "max_output_tokens"
                if protocol == "responses"
                else (profile or {}).get("output_limit_field", "max_tokens")
            )
            allowed_limits = (
                {"max_tokens", "max_completion_tokens"}
                if protocol != "responses"
                else {"max_output_tokens"}
            )
            if target not in allowed_limits:
                raise ValueError("Unsupported output_limit_field")
        if protocol == "responses" and name == "reasoning_effort":
            body["reasoning"] = {"effort": value}
        else:
            body[target] = value
    return body


def normalize_response(protocol, raw, request_metadata):
    if not isinstance(raw, dict):
        raise ValueError("Response must be an object")
    metadata = request_metadata
    if raw.get("error"):
        raise ValueError("Provider reported a protocol error")
    if protocol == "chat_completions":
        choices = raw.get("choices")
        if not isinstance(choices, list):
            raise ValueError("choices must be a list")
        if len(choices) > 1:
            raise ValueError("Multiple completion choices are unsupported")
        choice = choices[0] if choices else {}
        text = choice.get("message", {}).get("content") or ""
        if not isinstance(text, str):
            raise ValueError("completion content must be text")
        finish = choice.get("finish_reason")
    elif protocol == "responses":
        output = raw.get("output")
        if not isinstance(output, list):
            raise ValueError("output must be a list")
        text = "".join(
            part["text"]
            for item in output
            if item.get("type") == "message"
            and item.get("role", "assistant") == "assistant"
            for part in item.get("content", [])
            if part.get("type") == "output_text"
        )
        status = raw.get("status")
        finish = (
            "stop"
            if status == "completed"
            else (
                "length"
                if raw.get("incomplete_details", {}).get("reason")
                == "max_output_tokens"
                else status
            )
        )
        if status in ("failed", "cancelled", "queued", "in_progress"):
            raise ValueError("Response did not complete")
    elif protocol == "copilot_sdk":
        text = raw.get("text", "")
        finish = raw.get("finish_reason")
    else:
        raise ValueError("Unsupported protocol")
    original_usage = deepcopy(raw.get("usage"))
    usage = deepcopy(original_usage)
    if isinstance(usage, dict) and "input_tokens" in usage:
        usage = {
            "prompt_tokens": usage.get("input_tokens"),
            "completion_tokens": usage.get("output_tokens"),
            "total_tokens": usage.get("total_tokens"),
            "prompt_tokens_details": deepcopy(usage.get("input_tokens_details")),
            "completion_tokens_details": deepcopy(usage.get("output_tokens_details")),
        }
    if usage is not None and not isinstance(usage, dict):
        raise ValueError("usage must be an object")
    reported_cost = (
        original_usage.get("cost") if isinstance(original_usage, dict) else None
    )
    cost_source = "reported" if reported_cost is not None else None
    if (
        cost_source
        and isinstance(original_usage.get("opencode"), dict)
        and original_usage["opencode"].get("estimated") is True
    ):
        cost_source = "provider_estimated"
    if reported_cost is not None and (
        isinstance(reported_cost, bool)
        or not isinstance(reported_cost, (float, int))
        or not math.isfinite(reported_cost)
        or reported_cost < 0
    ):
        raise ValueError("Invalid reported cost")
    requested_model = metadata.get("model", metadata.get("requested_model"))
    effective = raw.get("effective_generation")
    return {
        "text": text,
        "finish_reason": finish,
        "requested_model": requested_model,
        "actual_model": raw.get("model"),
        "model_evidence": model_evidence(
            raw.get("model"), requested_model, metadata.get("allowed_response_models")
        ),
        "usage": usage,
        "usage_raw": original_usage,
        "cost_usd": reported_cost,
        "cost_source": cost_source,
        "request_id": raw.get("id"),
        "requested_generation": deepcopy(metadata.get("generation", {})),
        "sent_generation": deepcopy(metadata.get("sent_generation", {})),
        "effective_generation": effective,
        "effective_generation_reason": (
            None
            if effective is not None
            else "서버가 실효 생성 설정을 보고하지 않았습니다"
        ),
        "raw_response_path": metadata.get("raw_response_path"),
        "protocol": protocol,
        "provider": metadata.get("provider"),
        "body": raw,
        "applied_generation": effective,
        "applied_generation_reason": "서버가 확인한 설정만 기록합니다",
    }
