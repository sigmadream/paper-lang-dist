from __future__ import annotations

from typing import Final
import re

from rttdist.artifacts import LLMResponse

_FENCED_CODE_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"```[^\n]*\n(.*?)```", re.DOTALL
)


class SourceExtractionError(RuntimeError):
    pass


def extract_single_file_source(response: LLMResponse | str) -> str:
    if isinstance(response, str):
        return extract_single_file_source_text(response)
    return extract_single_file_source_text(response.choices[0].message.content)


def extract_single_file_source_text(text: str, *, preserve_unfenced: bool = False) -> str:
    if not isinstance(text, str):
        raise SourceExtractionError(
            "Model response must be a string to extract source."
        )

    stripped_text = text.strip()
    if not stripped_text:
        raise SourceExtractionError(
            "Model response is empty; cannot extract source file."
        )

    fenced_blocks = _FENCED_CODE_PATTERN.findall(stripped_text)
    if len(fenced_blocks) > 1:
        raise SourceExtractionError(
            "Model response contains multiple fenced code blocks; expected exactly one source file."
        )
    if len(fenced_blocks) == 1:
        candidate = fenced_blocks[0].strip("\n")
        if not candidate.strip():
            raise SourceExtractionError(
                "Model response fenced block is empty; cannot extract source file."
            )
        return candidate

    # ABS supports layout-sensitive Haskell and Prolog facts: never drop lines
    # using the legacy C-like heuristic. The language compiler validates source.
    if preserve_unfenced:
        return stripped_text
    recovered = _recover_unfenced_code(stripped_text)
    if recovered is None:
        raise SourceExtractionError(
            "Model response did not contain recoverable single-file source code."
        )
    return recovered


def _recover_unfenced_code(text: str) -> str | None:
    lines = text.splitlines()
    code_spans: list[tuple[int, int]] = []
    span_start: int | None = None

    for index, line in enumerate(lines):
        if _looks_like_code(line):
            if span_start is None:
                span_start = index
            continue

        if span_start is not None:
            code_spans.append((span_start, index - 1))
            span_start = None

    if span_start is not None:
        code_spans.append((span_start, len(lines) - 1))

    if not code_spans:
        return None

    if len(code_spans) == 1:
        start, end = code_spans[0]
    elif _spans_are_separated_only_by_blank_lines(lines, code_spans):
        start = code_spans[0][0]
        end = code_spans[-1][1]
    else:
        span_lengths = [end - start + 1 for start, end in code_spans]
        longest_length = max(span_lengths)
        if longest_length < 2:
            return None
        longest_spans = [
            span
            for span, length in zip(code_spans, span_lengths)
            if length == longest_length
        ]
        if len(longest_spans) != 1:
            return None
        start, end = longest_spans[0]

    candidate = "\n".join(lines[start : end + 1]).strip("\n")
    if not candidate.strip():
        return None
    return candidate


def _spans_are_separated_only_by_blank_lines(
    lines: list[str], code_spans: list[tuple[int, int]]
) -> bool:
    for index in range(len(code_spans) - 1):
        left_end = code_spans[index][1]
        right_start = code_spans[index + 1][0]
        between = lines[left_end + 1 : right_start]
        if any(line.strip() for line in between):
            return False
    return True


def _looks_like_code(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False

    code_markers = (
        "#include",
        "import ",
        "from ",
        "def ",
        "class ",
        "public ",
        "private ",
        "protected ",
        "int ",
        "long ",
        "double ",
        "float ",
        "for ",
        "while ",
        "if ",
        "else",
        "return",
    )
    if any(stripped.startswith(marker) for marker in code_markers):
        return True
    return any(
        token in stripped for token in (";", "{", "}", "(", ")", "=", "->", "::")
    )
