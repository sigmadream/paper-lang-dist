from rttdist.fixed_point import classify_cpp_history, classify_hash_history


def test_classifies_adjacent_fixed_point() -> None:
    assert classify_hash_history(["a", "b", "b"]) == "fixed_point"


def test_classifies_two_cycle_oscillation() -> None:
    assert classify_hash_history(["a", "b", "a", "b"]) == "oscillation"


def test_classifies_cpp_fixed_point_by_normalized_hash() -> None:
    source = "int main(){return 0;}"
    assert classify_cpp_history([source, "int main ( ) { return 0 ; }"]) == "fixed_point"
