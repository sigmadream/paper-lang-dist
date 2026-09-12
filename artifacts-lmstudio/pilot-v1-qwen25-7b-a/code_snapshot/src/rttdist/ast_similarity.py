"""Identifier-abstracted, ordered C++ AST edit similarity, isolated by process."""
import importlib.metadata
import multiprocessing as mp
import time

REPRESENTATION_VERSION = "cpp-named-identifiers-abstract-operators-literals-v1"
IDENTIFIERS = {"identifier", "field_identifier", "type_identifier", "namespace_identifier", "statement_identifier"}
VALUES = {"number_literal", "char_literal", "string_literal", "raw_string_literal", "system_lib_string", "primitive_type", "true", "false", "null", "nullptr"}
OPERATORS = set("+ - * / % == != < > <= >= && || ! ~ & | ^ << >> = += -= *= /= %= &= |= ^= <<= >>= ++ -- -> ->* .* ? : sizeof alignof new delete co_await and or not xor bitand bitor compl and_eq or_eq xor_eq not_eq".split())


def parser_smoke():
    from tree_sitter import Language, Parser
    import tree_sitter_cpp
    parser = Parser(Language(tree_sitter_cpp.language()))
    assert not parser.parse(b"int main(){return 0;}").root_node.has_error
    return {p: importlib.metadata.version(p) for p in ("tree-sitter", "tree-sitter-cpp", "apted")}


def _calculate(a, b, limit):
    from tree_sitter import Language, Parser
    import tree_sitter_cpp
    from apted import APTED
    from apted.helpers import Tree
    parser = Parser(Language(tree_sitter_cpp.language()))
    roots, counts, errors, missing = [], [], [], []
    for source in (a, b):
        raw = source.encode("utf-8")
        root = parser.parse(raw).root_node
        stack, e, m = [root], 0, 0
        while stack:
            node = stack.pop()
            e += node.type == "ERROR"
            m += node.is_missing
            stack.extend(node.children)
        errors.append(e)
        missing.append(m)
        count = [0]

        def convert(node):
            if node.type == "comment":
                return None
            if not node.is_named and node.type not in OPERATORS:
                return None
            count[0] += 1
            if count[0] > limit:
                raise OverflowError("tree_too_large")
            label = node.type
            if node.type in IDENTIFIERS:
                return Tree(label)
            if node.type in VALUES or not node.is_named:
                return Tree(label + ":" + raw[node.start_byte:node.end_byte].decode("utf-8"))
            children = [converted for child in node.children if (converted := convert(child)) is not None]
            return Tree(label, *children)

        roots.append(convert(root))
        counts.append(count[0])
    result = {"node_counts": counts, "error_counts": errors, "missing_counts": missing}
    if any(errors + missing):
        return {**result, "status": "unavailable", "value": None, "reason": "parse_invalid"}
    ted = APTED(*roots).compute_edit_distance()
    return {**result, "status": "measured", "value": max(0, 1-ted/max(counts)), "ted": ted, "reason": None}


def _worker(conn, a, b, limit):
    start = time.perf_counter()
    try:
        result = _calculate(a, b, limit)
    except ImportError:
        result = {"status": "unavailable", "value": None, "reason": "parser_not_installed"}
    except (MemoryError, OverflowError, RecursionError) as exc:
        result = {"status": "unavailable", "value": None, "reason": "tree_too_large" if isinstance(exc, (OverflowError, RecursionError)) else "memory_limit"}
    import psutil
    mem = psutil.Process().memory_info()
    result.update(process_seconds=time.perf_counter()-start, peak_memory_bytes=getattr(mem, "peak_wset", mem.rss))
    conn.send(result)
    conn.close()


def ast_similarity(a, b, *, node_limit=5000, timeout=30, memory_mb=512):
    import psutil
    start = time.perf_counter()
    context = mp.get_context("spawn")
    receiver, sender = context.Pipe(duplex=False)
    process = context.Process(target=_worker, args=(sender, a, b, node_limit))
    process.start()
    sender.close()
    result = None
    peak = 0
    while process.is_alive():
        if receiver.poll(0.02):
            result = receiver.recv()
            break
        try:
            peak = max(peak, psutil.Process(process.pid).memory_info().rss)
        except psutil.NoSuchProcess:
            pass
        reason = "ast_timeout" if time.perf_counter()-start > timeout else "memory_limit" if peak > memory_mb*1024**2 else None
        if reason:
            result = {"status": "unavailable", "value": None, "reason": reason}
            process.terminate()
            break
    process.join(2)
    if process.is_alive():
        process.kill()
        process.join()
    if result is None and receiver.poll():
        try:
            result = receiver.recv()
        except EOFError:
            pass
    receiver.close()
    result = result or {"status": "unavailable", "value": None, "reason": "worker_failed"}
    return {"metric": "ast_tsed", "representation_version": REPRESENTATION_VERSION,
            "cost_config": {"insert": 1, "delete": 1, "rename": 1},
            "parser_versions": parser_smoke(), "wall_seconds": time.perf_counter()-start,
            "sampled_peak_memory_bytes": peak, **result}
