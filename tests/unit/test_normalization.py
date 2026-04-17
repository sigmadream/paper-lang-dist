from __future__ import annotations

import pytest

from rttdist.normalize import (
    NormalizationError,
    cpp_token_sorensen_dice_similarity,
    hash_normalized_cpp_tokens,
    normalize_source,
    normalize_tokens,
)


@pytest.mark.parametrize("language", ["c", "cpp", "java"])
def test_c_like_normalization_removes_comments_and_collapses_whitespace(
    language: str,
) -> None:
    noisy = """
    // leading comment
    int main() {   /* inline block */
        return  0; // trailing comment
    }
    """
    compact = "int main(){return 0;}"

    assert normalize_tokens(language, noisy) == normalize_tokens(language, compact)
    assert normalize_source(language, noisy) == "int main ( ) { return 0 ; }"


def test_python_normalization_removes_comments_and_ignores_layout_noise() -> None:
    noisy = """
def solve():  # keep behavior
    value = 666
    print(value)  # trailing comment
"""
    compact = "def solve():\n    value = 666\n    print(value)\n"

    assert normalize_tokens("python", noisy) == normalize_tokens("python", compact)
    assert normalize_source("python", noisy) == (
        "def solve ( ) : value = 666 print ( value )"
    )


def test_normalized_cpp_hash_is_stable_across_comment_and_whitespace_noise() -> None:
    left = """
    #include <iostream>
    int main() {
        // comment
        std::cout << 666 << "\\n";
    }
    """
    right = '#include <iostream>\nint main(){std::cout<<666<<"\\n";}'

    assert hash_normalized_cpp_tokens(left) == hash_normalized_cpp_tokens(right)


def test_cpp_token_similarity_uses_multiset_sorensen_dice() -> None:
    seed = "int main(){return 1 + 2;}"
    candidate = "int main(){return 1 + 3;}"

    assert cpp_token_sorensen_dice_similarity(seed, candidate) == pytest.approx(10 / 11)


def test_normalize_tokens_rejects_unknown_language() -> None:
    with pytest.raises(NormalizationError) as excinfo:
        normalize_tokens("rust", "fn main() {}")

    assert "Unsupported normalization language" in str(excinfo.value)
