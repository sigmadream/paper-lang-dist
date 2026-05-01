from __future__ import annotations

import pytest

from rttdist.artifacts import (
    LLMChoice,
    LLMMessage,
    LLMResponse,
    LLMUsage,
)
from rttdist.lmstudio_client import SourceExtractionError, extract_single_file_source
from rttdist.prompts import build_translation_prompt


def test_generic_translation_prompt_is_deterministic_and_explicit() -> None:
    bundle = build_translation_prompt(
        problem_id="IPOP_1436",
        source_language="cpp",
        target_language="python",
        problem_statement="Given N, print the Nth integer containing 666.",
        sample_input="1",
        sample_output="666",
        source_code="#include <iostream>\nint main(){return 0;}",
        direction="seed_to_target",
    )

    assert bundle.direction == "seed_to_target"
    assert bundle.source_language == "cpp"
    assert bundle.target_language == "python"
    assert [message.role for message in bundle.messages] == ["system", "user"]

    prompt = bundle.messages[1].content
    assert "Direction: seed_to_target" in prompt
    assert "Translate from C++ to Python." in prompt
    assert (
        "Produce exactly one compilable source file in the target language." in prompt
    )
    assert "Output code only." in prompt
    assert "[PROBLEM STATEMENT]" in prompt
    assert "[SAMPLE INPUT]" in prompt
    assert "[EXPECTED OUTPUT]" in prompt
    assert "```cpp" in prompt


def test_target_to_cpp_prompt_is_deterministic_and_explicit() -> None:
    bundle = build_translation_prompt(
        problem_id="IPOP_1436",
        source_language="java",
        target_language="cpp",
        problem_statement="Given N, print the Nth integer containing 666.",
        sample_input="1",
        sample_output="666",
        source_code="public class Main { public static void main(String[] args) {} }",
        direction="target_to_seed",
    )

    prompt = bundle.messages[1].content
    assert bundle.direction == "target_to_seed"
    assert bundle.source_language == "java"
    assert bundle.target_language == "cpp"
    assert "Direction: target_to_seed" in prompt
    assert "Translate from Java to C++." in prompt
    assert "```java" in prompt


def test_extract_single_file_source_strips_fence_and_prose() -> None:
    response = _response_from_content(
        "I translated the file below.\n\n"
        "```python\n"
        "def solve():\n"
        "    print(666)\n"
        "```\n"
        "This should preserve behavior."
    )

    extracted = extract_single_file_source(response)

    assert extracted == "def solve():\n    print(666)"


def test_extract_single_file_source_rejects_multiple_fences() -> None:
    response = _response_from_content(
        "```python\nprint(1)\n```\n```python\nprint(2)\n```"
    )

    with pytest.raises(SourceExtractionError) as excinfo:
        extract_single_file_source(response)

    assert "multiple fenced code blocks" in str(excinfo.value)


def test_extract_single_file_source_rejects_unrecoverable_prose_only() -> None:
    response = _response_from_content("Here is your translation. It should work well.")

    with pytest.raises(SourceExtractionError) as excinfo:
        extract_single_file_source(response)

    assert "recoverable single-file source code" in str(excinfo.value)


def _response_from_content(content: str) -> LLMResponse:
    return LLMResponse(
        response_id="response-001",
        model="gpt-5.4",
        choices=(
            LLMChoice(
                index=0,
                message=LLMMessage(role="assistant", content=content),
                finish_reason="stop",
            ),
        ),
        usage=LLMUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
    )
