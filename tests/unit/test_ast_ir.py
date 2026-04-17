from __future__ import annotations

import pytest

from rttdist.ast_ir import ir_to_sexpr, parse_to_ir, try_parse_to_ir


LANGUAGE_SAMPLES = {
    "c": "int f(int* a, int n){ for(int i=0;i<n;i++){ if(a[i]>0){ foo(a[i]); } else { return 0; } } return a[0]; }",
    "cpp": "int f(int* a, int n){ for(int i=0;i<n;i++){ if(a[i]>0){ foo(a[i]); } else { return 0; } } return a[0]; }",
    "java": "class Main { static int f(int[] a){ for(int i=0;i<a.length;i++){ if(a[i]>0){ foo(a[i]); } else { return 0; } } return a[0]; } }",
    "python": "def f(a):\n    for i in range(len(a)):\n        if a[i] > 0:\n            foo(a[i])\n        else:\n            return 0\n    return a[0]\n",
}

EXPECTED_GOLDEN = {
    "c": "(function_def (parameters) (block (for_loop (declaration) (binary_expr) (update_expr) (block (if_stmt (binary_expr (subscript_expr)) (block (expr_stmt (call_expr (arg_list (subscript_expr))))) (else_clause (block (return_stmt)))))) (return_stmt (subscript_expr))))",
    "cpp": "(function_def (parameters) (block (for_loop (declaration) (binary_expr) (update_expr) (block (if_stmt (binary_expr (subscript_expr)) (block (expr_stmt (call_expr (arg_list (subscript_expr))))) (else_clause (block (return_stmt)))))) (return_stmt (subscript_expr))))",
    "java": "(function_def (parameters) (block (for_loop (declaration) (binary_expr) (update_expr) (block (if_stmt (binary_expr (subscript_expr)) (block (expr_stmt (call_expr (arg_list (subscript_expr))))) (else_clause (block (return_stmt)))))) (return_stmt (subscript_expr))))",
    "python": "(function_def (parameters) (block (for_loop (call_expr (arg_list (call_expr (arg_list)))) (block (if_stmt (binary_expr (subscript_expr)) (block (expr_stmt (call_expr (arg_list (subscript_expr))))) (else_clause (block (return_stmt)))))) (return_stmt (subscript_expr))))",
}


@pytest.mark.parametrize("language", ["c", "cpp", "java", "python"])
def test_constructs_normalize_with_stable_golden_shape(language: str) -> None:
    tree = parse_to_ir(language, LANGUAGE_SAMPLES[language])
    assert ir_to_sexpr(tree) == EXPECTED_GOLDEN[language]


@pytest.mark.parametrize("language", ["c", "cpp", "java", "python"])
def test_loop_branch_call_array_return_constructs_exist(language: str) -> None:
    tree = parse_to_ir(language, LANGUAGE_SAMPLES[language])
    text = ir_to_sexpr(tree)

    for required in (
        "for_loop",
        "if_stmt",
        "call_expr",
        "subscript_expr",
        "return_stmt",
    ):
        assert f"({required}" in text


def test_try_parse_to_ir_returns_parser_failure_instead_of_raising() -> None:
    invalid_python = "def f(:\n  return 1\n"
    result = try_parse_to_ir("python", invalid_python)

    assert result.status == "parser_failure"
    assert result.tree is None
    assert result.message is not None
    assert "Failed to parse `python` source" in result.message
