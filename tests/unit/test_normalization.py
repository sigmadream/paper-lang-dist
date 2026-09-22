import pytest

from rttdist.normalize import NormalizationError, hash_normalized_cpp_tokens, normalize_source, normalize_tokens


def test_c_like_normalization_ignores_layout_and_comments() -> None:
    noisy = "int main(){ // hi\n return 0; }"
    compact = "int main(){return 0;}"
    assert normalize_tokens("cpp", noisy) == normalize_tokens("cpp", compact)
    assert normalize_source("cpp", noisy) == "int main ( ) { return 0 ; }"


def test_python_normalization_ignores_layout_comments() -> None:
    noisy = "def solve():\n    # hi\n    return 1\n"
    compact = "def solve():\n return 1\n"
    assert normalize_tokens("python", noisy) == normalize_tokens("python", compact)


def test_hash_normalized_cpp_tokens_is_layout_stable() -> None:
    assert hash_normalized_cpp_tokens("int main(){return 0;}") == hash_normalized_cpp_tokens("int main ( ) { return 0 ; }")


def test_normalize_tokens_rejects_unknown_language() -> None:
    with pytest.raises(NormalizationError):
        normalize_tokens("rust", "fn main() {}")
