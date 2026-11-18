import pytest

from rttdist import providers


def test_chat_and_responses_normalize_without_claiming_effective_generation():
    from rttdist.provider_protocols import normalize_response

    metadata = {
        "model": "test",
        "provider": "openai",
        "generation": {"temperature": 0.6},
    }
    chat = normalize_response(
        "chat_completions",
        {
            "id": "c",
            "model": "test",
            "choices": [{"message": {"content": "print(1)"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 3, "completion_tokens": 2},
        },
        metadata,
    )
    responses = normalize_response(
        "responses",
        {
            "id": "r",
            "model": "test",
            "status": "completed",
            "output": [
                {"type": "reasoning", "summary": []},
                {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": "print(1)"}],
                },
            ],
            "usage": {"input_tokens": 3, "output_tokens": 2},
        },
        metadata,
    )
    assert chat["text"] == responses["text"] == "print(1)"
    assert chat["usage"]["prompt_tokens"] == responses["usage"]["prompt_tokens"] == 3
    assert (
        chat["effective_generation"] is None
        and responses["effective_generation"] is None
    )
    assert responses["usage_raw"] == {"input_tokens": 3, "output_tokens": 2}


def test_responses_maps_instructions_limit_reasoning_and_rejects_seed():
    from rttdist.provider_protocols import build_request

    profile = {"supported_options": ["max_tokens", "reasoning_effort"]}
    request = {
        "model": "test",
        "messages": [
            {"role": "system", "content": "Translate"},
            {"role": "user", "content": "x"},
        ],
        "generation": {"max_tokens": 100, "reasoning_effort": "low"},
    }
    result = build_request("responses", request, profile)
    assert result == {
        "model": "test",
        "instructions": "Translate",
        "input": [{"role": "user", "content": "x"}],
        "max_output_tokens": 100,
        "reasoning": {"effort": "low"},
    }
    request["generation"]["seed"] = 1
    with pytest.raises(ValueError, match="Unsupported generation"):
        build_request("responses", request, profile)


def test_chat_model_specific_limit_and_unknown_option_are_not_discarded():
    from rttdist.provider_protocols import build_request

    result = build_request(
        "chat_completions",
        {"model": "test", "messages": [], "max_tokens": 12},
        {
            "supported_options": ["max_tokens"],
            "output_limit_field": "max_completion_tokens",
        },
    )
    assert result["max_completion_tokens"] == 12 and "max_tokens" not in result
    with pytest.raises(ValueError, match="Unsupported"):
        build_request(
            "chat_completions", {"model": "test", "messages": [], "tools": []}, {}
        )


def test_models_require_exact_ids_or_explicit_aliases():
    assert providers.model_matches("org/test", "org/test", version="v1.6")
    assert not providers.model_matches("test", "org/test", version="v1.6")
    assert not providers.model_matches("org/test-new", "org/test", version="v1.6")
    assert providers.model_matches("test-2026", "test", ["test-2026"])


def test_incomplete_and_empty_received_response_is_not_transport_failure():
    from rttdist.provider_protocols import normalize_response

    result = normalize_response(
        "responses",
        {
            "model": "test",
            "status": "incomplete",
            "incomplete_details": {"reason": "max_output_tokens"},
            "output": [],
        },
        {"model": "test"},
    )
    assert result["text"] == "" and result["finish_reason"] == "length"


def test_opencode_estimated_report_is_not_mislabeled_as_billed_cost():
    from rttdist.provider_protocols import normalize_response

    result = normalize_response(
        "chat_completions",
        {
            "model": "test",
            "choices": [],
            "usage": {
                "cost": 0.1,
                "opencode": {"estimated": True, "billing_source": "byok"},
            },
        },
        {"model": "test"},
    )
    assert result["cost_usd"] == 0.1 and result["cost_source"] == "provider_estimated"
