from __future__ import annotations

from dataclasses import dataclass

from rttdist.artifacts import MockOpenAIMessage

SEED_LANGUAGE = "cpp"
PROMPT_TEMPLATE_VERSION = "rtt.prompts.v1"

LANGUAGE_LABELS = {
    "cpp": "C++",
    "c": "C",
    "java": "Java",
    "python": "Python",
}


class PromptTemplateError(ValueError):
    pass


@dataclass(frozen=True)
class PromptBundle:
    direction: str
    source_language: str
    target_language: str
    messages: tuple[MockOpenAIMessage, ...]


def build_cpp_to_target_prompt(
    *,
    problem_id: str,
    target_language: str,
    problem_statement: str,
    sample_input: str,
    sample_output: str,
    source_code: str,
) -> PromptBundle:
    normalized_target = _normalize_language(
        target_language, field_name="target_language"
    )

    return _build_prompt_bundle(
        direction="seed_to_target",
        source_language=SEED_LANGUAGE,
        target_language=normalized_target,
        problem_id=problem_id,
        problem_statement=problem_statement,
        sample_input=sample_input,
        sample_output=sample_output,
        source_code=source_code,
    )


def build_target_to_cpp_prompt(
    *,
    problem_id: str,
    source_language: str,
    problem_statement: str,
    sample_input: str,
    sample_output: str,
    source_code: str,
) -> PromptBundle:
    normalized_source = _normalize_language(
        source_language, field_name="source_language"
    )
    if normalized_source == SEED_LANGUAGE:
        raise PromptTemplateError(
            "`source_language` must not be `cpp` for roundtrip prompts."
        )

    return _build_prompt_bundle(
        direction="target_to_roundtrip_cpp",
        source_language=normalized_source,
        target_language=SEED_LANGUAGE,
        problem_id=problem_id,
        problem_statement=problem_statement,
        sample_input=sample_input,
        sample_output=sample_output,
        source_code=source_code,
    )


def _build_prompt_bundle(
    *,
    direction: str,
    source_language: str,
    target_language: str,
    problem_id: str,
    problem_statement: str,
    sample_input: str,
    sample_output: str,
    source_code: str,
) -> PromptBundle:
    normalized_problem_id = _normalize_text(problem_id, field_name="problem_id")
    normalized_statement = _normalize_text(
        problem_statement, field_name="problem_statement"
    )
    normalized_input = _normalize_text(sample_input, field_name="sample_input")
    normalized_output = _normalize_text(sample_output, field_name="sample_output")
    normalized_source = _normalize_text(source_code, field_name="source_code")

    source_label = _language_label(source_language)
    target_label = _language_label(target_language)

    system_message = MockOpenAIMessage(
        role="system",
        content=(
            "You are a deterministic code translator for round-trip translation experiments. "
            "Preserve behavior exactly. Return only one source file with no explanation."
        ),
    )
    user_message = MockOpenAIMessage(
        role="user",
        content=(
            f"[TASK]\n"
            f"Direction: {direction}\n"
            f"Problem ID: {normalized_problem_id}\n"
            f"Translate from {source_label} to {target_label}.\n\n"
            "[CONSTRAINTS]\n"
            "- Preserve exact input/output behavior for the provided sample.\n"
            "- Produce exactly one compilable source file in the target language.\n"
            "- Do not include markdown fences, comments about the translation, or prose.\n"
            "- Output code only.\n\n"
            "[PROBLEM STATEMENT]\n"
            f"{normalized_statement}\n\n"
            "[SAMPLE INPUT]\n"
            f"{normalized_input}\n\n"
            "[EXPECTED OUTPUT]\n"
            f"{normalized_output}\n\n"
            f"[SOURCE CODE - {source_label}]\n"
            f"```{source_language}\n{normalized_source}\n```"
        ),
    )
    return PromptBundle(
        direction=direction,
        source_language=source_language,
        target_language=target_language,
        messages=(system_message, user_message),
    )


def _normalize_text(value: str, *, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PromptTemplateError(f"`{field_name}` must be a non-empty string.")
    return value.strip()


def _normalize_language(value: str, *, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PromptTemplateError(f"`{field_name}` must be a non-empty string.")
    normalized = value.strip().lower()
    if normalized not in LANGUAGE_LABELS:
        supported = ", ".join(sorted(LANGUAGE_LABELS))
        raise PromptTemplateError(
            f"Unsupported language `{value}` for `{field_name}`. Supported: {supported}."
        )
    return normalized


def _language_label(language: str) -> str:
    return LANGUAGE_LABELS[language]
