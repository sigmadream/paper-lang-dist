from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from apted import APTED
from apted.helpers import Tree

from rttdist.ast_ir import ASTParseResult, IRNode, ir_to_sexpr, try_parse_to_ir


@dataclass(frozen=True)
class ASTDistanceMetrics:
    status: str
    distance_to_seed_cpp: int | None
    distance_to_roundtrip_cpp: int | None
    parse_status: dict[str, str]
    parser_failures: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "distance_to_seed_cpp": self.distance_to_seed_cpp,
            "distance_to_roundtrip_cpp": self.distance_to_roundtrip_cpp,
            "parse_status": dict(self.parse_status),
            "parser_failures": dict(self.parser_failures),
        }


def compute_roundtrip_ast_distance_metrics(
    *,
    seed_cpp_source: str,
    target_language: str,
    target_source: str,
    roundtrip_cpp_source: str,
) -> ASTDistanceMetrics:
    parsed_nodes = {
        "seed_cpp": try_parse_to_ir("cpp", seed_cpp_source),
        "target": try_parse_to_ir(target_language, target_source),
        "roundtrip_cpp": try_parse_to_ir("cpp", roundtrip_cpp_source),
    }

    parse_status = {key: result.status for key, result in parsed_nodes.items()}
    parser_failures = {
        key: result.message or "unknown parser failure"
        for key, result in parsed_nodes.items()
        if result.status == "parser_failure"
    }

    if parser_failures:
        return ASTDistanceMetrics(
            status="parser_failure",
            distance_to_seed_cpp=None,
            distance_to_roundtrip_cpp=None,
            parse_status=parse_status,
            parser_failures=parser_failures,
        )

    target_tree = _require_tree(parsed_nodes["target"], key="target")
    seed_tree = _require_tree(parsed_nodes["seed_cpp"], key="seed_cpp")
    roundtrip_tree = _require_tree(parsed_nodes["roundtrip_cpp"], key="roundtrip_cpp")

    return ASTDistanceMetrics(
        status="ok",
        distance_to_seed_cpp=compute_apted_tree_distance(target_tree, seed_tree),
        distance_to_roundtrip_cpp=compute_apted_tree_distance(
            target_tree,
            roundtrip_tree,
        ),
        parse_status=parse_status,
        parser_failures={},
    )


def compute_apted_tree_distance(left: IRNode, right: IRNode) -> int:
    left_tree = _to_apted_tree(left)
    right_tree = _to_apted_tree(right)
    return int(APTED(left_tree, right_tree).compute_edit_distance())


def ir_preview(node: IRNode) -> str:
    return ir_to_sexpr(node)


def _to_apted_tree(node: IRNode) -> Tree:
    children = tuple(_to_apted_tree(child) for child in node.children)
    return Tree(node.kind, *children)


def _require_tree(result: ASTParseResult, *, key: str) -> IRNode:
    if result.tree is None:
        raise RuntimeError(
            f"Expected parsed AST IR tree for `{key}` but parser returned no tree."
        )
    return result.tree
