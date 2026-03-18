from __future__ import annotations

from collections import Counter
from io import StringIO
from typing import Final
import hashlib
import re
import token as token_types
import tokenize

SUPPORTED_NORMALIZATION_LANGUAGES: Final[frozenset[str]] = frozenset(
    {"c", "cpp", "java", "python"}
)

_C_LIKE_TOKEN_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"""(?:
    "(?:\\.|[^"\\])*"
    | '(?:\\.|[^'\\])*'
    | [A-Za-z_][A-Za-z0-9_]*
    | 0[xX][0-9A-Fa-f]+[A-Za-z0-9_]*
    | \d+(?:\.\d+)?(?:[eE][+-]?\d+)?[A-Za-z0-9_]*
    | ::|->\*|->|\+\+|--|<<=|>>=|==|!=|<=|>=|&&|\|\||<<|>>|\+=|-=|\*=|/=|%=|&=|\|=|\^=|\.\.\.
    | [#{}\[\]();,.:?~<>+\-*/%=!&|^\\]
    )""",
    re.VERBOSE,
)

_PYTHON_IGNORED_TOKENS: Final[set[int]] = {
    token_types.COMMENT,
    token_types.NL,
    token_types.NEWLINE,
    token_types.INDENT,
    token_types.DEDENT,
    token_types.ENDMARKER,
}


class NormalizationError(ValueError):
    pass


def normalize_source(language: str, source: str) -> str:
    return " ".join(normalize_tokens(language, source))


def normalize_tokens(language: str, source: str) -> tuple[str, ...]:
    normalized_language = _normalize_language(language)
    validated_source = _validate_source(source)

    if normalized_language == "python":
        return _normalize_python_tokens(validated_source)
    return _normalize_c_like_tokens(validated_source)


def normalize_cpp_tokens(source: str) -> tuple[str, ...]:
    return normalize_tokens("cpp", source)


def hash_normalized_cpp_tokens(source: str) -> str:
    token_bytes = "\x00".join(normalize_cpp_tokens(source)).encode("utf-8")
    return hashlib.sha256(token_bytes).hexdigest()


def cpp_token_sorensen_dice_similarity(
    seed_source: str, candidate_source: str
) -> float:
    """Compute Sorensen-Dice similarity over normalized C++ token multisets.

    This intentionally uses token multiplicity rather than set membership so repeated
    identifiers, literals, and operators continue to affect the residual score.
    """

    left_tokens = normalize_cpp_tokens(seed_source)
    right_tokens = normalize_cpp_tokens(candidate_source)

    if not left_tokens and not right_tokens:
        return 1.0

    left_counts = Counter(left_tokens)
    right_counts = Counter(right_tokens)
    overlap = sum(min(left_counts[token], right_counts[token]) for token in left_counts)
    return (2.0 * overlap) / (len(left_tokens) + len(right_tokens))


def _normalize_language(language: str) -> str:
    if not isinstance(language, str) or not language.strip():
        raise NormalizationError("`language` must be a non-empty string.")

    normalized = language.strip().lower()
    if normalized not in SUPPORTED_NORMALIZATION_LANGUAGES:
        supported = ", ".join(sorted(SUPPORTED_NORMALIZATION_LANGUAGES))
        raise NormalizationError(
            f"Unsupported normalization language `{language}`. Supported: {supported}."
        )
    return normalized


def _validate_source(source: str) -> str:
    if not isinstance(source, str) or not source.strip():
        raise NormalizationError("`source` must be a non-empty string.")
    return source


def _normalize_python_tokens(source: str) -> tuple[str, ...]:
    tokens: list[str] = []
    try:
        token_stream = tokenize.generate_tokens(StringIO(source).readline)
        for token_info in token_stream:
            if token_info.type in _PYTHON_IGNORED_TOKENS:
                continue
            tokens.append(token_info.string)
    except tokenize.TokenError as exc:
        raise NormalizationError("Failed to tokenize Python source.") from exc
    return tuple(tokens)


def _normalize_c_like_tokens(source: str) -> tuple[str, ...]:
    stripped = _strip_c_like_comments(source)
    return tuple(_C_LIKE_TOKEN_PATTERN.findall(stripped))


def _strip_c_like_comments(source: str) -> str:
    output: list[str] = []
    in_line_comment = False
    in_block_comment = False
    active_quote: str | None = None
    index = 0

    while index < len(source):
        current = source[index]
        next_char = source[index + 1] if index + 1 < len(source) else ""

        if in_line_comment:
            if current == "\n":
                output.append("\n")
                in_line_comment = False
            index += 1
            continue

        if in_block_comment:
            if current == "*" and next_char == "/":
                output.append(" ")
                in_block_comment = False
                index += 2
                continue
            if current == "\n":
                output.append("\n")
            index += 1
            continue

        if active_quote is not None:
            output.append(current)
            if current == "\\" and index + 1 < len(source):
                output.append(source[index + 1])
                index += 2
                continue
            if current == active_quote:
                active_quote = None
            index += 1
            continue

        if current in {'"', "'"}:
            active_quote = current
            output.append(current)
            index += 1
            continue

        if current == "/" and next_char == "/":
            in_line_comment = True
            index += 2
            continue

        if current == "/" and next_char == "*":
            in_block_comment = True
            index += 2
            continue

        output.append(current)
        index += 1

    return "".join(output)
