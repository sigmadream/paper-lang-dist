from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from importlib import import_module
from typing import Any, Final, Literal

SupportedASTLanguage = Literal["c", "cpp", "java", "python"]
ParseStatus = Literal["ok", "parser_failure"]

SUPPORTED_AST_LANGUAGES: Final[frozenset[str]] = frozenset(
    {"c", "cpp", "java", "python"}
)

_LANGUAGE_MODULE_NAMES: Final[dict[str, str]] = {
    "c": "tree_sitter_c",
    "cpp": "tree_sitter_cpp",
    "java": "tree_sitter_java",
    "python": "tree_sitter_python",
}

_NODE_KIND_MAP: Final[dict[str, dict[str, str]]] = {
    "common": {
        "function_definition": "function_def",
        "method_declaration": "function_def",
        "constructor_declaration": "function_def",
        "for_statement": "for_loop",
        "enhanced_for_statement": "for_loop",
        "while_statement": "while_loop",
        "if_statement": "if_stmt",
        "else_clause": "else_clause",
        "return_statement": "return_stmt",
        "expression_statement": "expr_stmt",
        "declaration": "declaration",
        "local_variable_declaration": "declaration",
        "assignment_expression": "assignment",
        "assignment": "assignment",
        "call_expression": "call_expr",
        "method_invocation": "call_expr",
        "call": "call_expr",
        "subscript_expression": "subscript_expr",
        "array_access": "subscript_expr",
        "subscript": "subscript_expr",
        "binary_expression": "binary_expr",
        "comparison_operator": "binary_expr",
        "update_expression": "update_expr",
        "argument_list": "arg_list",
        "parameter_list": "parameters",
        "formal_parameters": "parameters",
        "parameters": "parameters",
        "compound_statement": "block",
        "block": "block",
    },
    "java": {
        "program": "root",
    },
    "python": {
        "module": "root",
    },
    "c": {
        "translation_unit": "root",
    },
    "cpp": {
        "translation_unit": "root",
    },
}

_TRANSPARENT_NODE_TYPES: Final[frozenset[str]] = frozenset(
    {
        "translation_unit",
        "program",
        "module",
        "class_declaration",
        "class_body",
        "modifiers",
        "primitive_type",
        "integral_type",
        "array_type",
        "dimensions",
        "pointer_declarator",
        "parameter_declaration",
        "formal_parameter",
        "function_declarator",
        "init_declarator",
        "variable_declarator",
        "parenthesized_expression",
        "field_access",
        "identifier",
        "number_literal",
        "decimal_integer_literal",
        "integer",
        "string_literal",
    }
)


class AstIRError(ValueError):
    pass


@dataclass(frozen=True)
class ASTParseResult:
    status: ParseStatus
    tree: "IRNode | None"
    message: str | None = None

    def to_dict(self) -> dict[str, str | dict[str, object] | None]:
        return {
            "status": self.status,
            "tree": None if self.tree is None else self.tree.to_dict(),
            "message": self.message,
        }


@dataclass(frozen=True)
class IRNode:
    kind: str
    children: tuple["IRNode", ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "kind": self.kind,
            "children": [child.to_dict() for child in self.children],
        }


def parse_to_ir(language: str, source: str) -> IRNode:
    normalized_language = _normalize_language(language)
    validated_source = _validate_source(source)
    parser = _get_parser(normalized_language)
    tree = parser.parse(validated_source.encode("utf-8"))
    root = tree.root_node

    if _has_parse_error(root):
        raise AstIRError(
            f"Failed to parse `{normalized_language}` source into AST IR due to syntax errors."
        )

    normalized_nodes = _normalize_node(normalized_language, root)
    if len(normalized_nodes) == 1:
        return normalized_nodes[0]
    return IRNode(kind="root", children=tuple(normalized_nodes))


def try_parse_to_ir(language: str, source: str) -> ASTParseResult:
    try:
        return ASTParseResult(status="ok", tree=parse_to_ir(language, source))
    except AstIRError as exc:
        return ASTParseResult(status="parser_failure", tree=None, message=str(exc))


def ir_to_sexpr(node: IRNode) -> str:
    if not node.children:
        return f"({node.kind})"
    child_repr = " ".join(ir_to_sexpr(child) for child in node.children)
    return f"({node.kind} {child_repr})"


def _normalize_language(language: str) -> SupportedASTLanguage:
    if not isinstance(language, str) or not language.strip():
        raise AstIRError("`language` must be a non-empty string.")

    normalized = language.strip().lower()
    if normalized not in SUPPORTED_AST_LANGUAGES:
        supported = ", ".join(sorted(SUPPORTED_AST_LANGUAGES))
        raise AstIRError(
            f"Unsupported AST language `{language}`. Supported: {supported}."
        )
    return normalized  # type: ignore[return-value]


def _validate_source(source: str) -> str:
    if not isinstance(source, str) or not source.strip():
        raise AstIRError("`source` must be a non-empty string.")
    return source


@lru_cache(maxsize=None)
def _get_parser(language: SupportedASTLanguage):
    ts_module = import_module("tree_sitter")
    language_module = import_module(_LANGUAGE_MODULE_NAMES[language])
    parser_class = getattr(ts_module, "Parser")
    language_class = getattr(ts_module, "Language")
    capsule = language_module.language()
    return parser_class(language_class(capsule))


def _has_parse_error(node: Any) -> bool:
    node_obj = node
    is_error = bool(getattr(node_obj, "is_error"))
    is_missing = bool(getattr(node_obj, "is_missing"))
    children = tuple(getattr(node_obj, "children"))

    if is_error or is_missing:
        return True
    for child in children:
        if _has_parse_error(child):
            return True
    return False


def _normalize_node(language: SupportedASTLanguage, node: Any) -> list[IRNode]:
    node_obj = node
    if not bool(getattr(node_obj, "is_named")):
        return []

    node_type = str(getattr(node_obj, "type"))
    if node_type == "if_statement":
        return [_normalize_if_statement(language, node_obj)]

    children: list[IRNode] = []
    for child in tuple(getattr(node_obj, "named_children")):
        children.extend(_normalize_node(language, child))

    if node_type in _TRANSPARENT_NODE_TYPES:
        return children

    mapped_kind = _map_node_kind(language, node_type)
    if mapped_kind is None:
        return children

    return [IRNode(kind=mapped_kind, children=tuple(children))]


def _normalize_if_statement(language: SupportedASTLanguage, node: Any) -> IRNode:
    node_obj = node
    children: list[IRNode] = []
    condition = node_obj.child_by_field_name("condition")
    consequence = node_obj.child_by_field_name("consequence")
    alternative = node_obj.child_by_field_name("alternative")

    if condition is not None:
        children.extend(_normalize_node(language, condition))
    if consequence is not None:
        children.extend(_normalize_node(language, consequence))
    if alternative is not None:
        alt_nodes = _normalize_node(language, alternative)
        if len(alt_nodes) == 1 and alt_nodes[0].kind == "else_clause":
            children.append(alt_nodes[0])
        else:
            children.append(IRNode(kind="else_clause", children=tuple(alt_nodes)))

    if not children:
        for child in tuple(getattr(node_obj, "named_children")):
            children.extend(_normalize_node(language, child))

    return IRNode(kind="if_stmt", children=tuple(children))


def _map_node_kind(language: SupportedASTLanguage, node_type: str) -> str | None:
    language_map = _NODE_KIND_MAP.get(language, {})
    if node_type in language_map:
        return language_map[node_type]

    common_map = _NODE_KIND_MAP["common"]
    if node_type in common_map:
        return common_map[node_type]

    if node_type.endswith("statement"):
        return "statement"
    if node_type.endswith("expression"):
        return "expression"
    return None
