"""Execution smoke tests, AST response fixtures and final experiment audit."""
from dataclasses import asdict
from pathlib import Path
import sys

from rttdist.ast_similarity import ast_similarity
from rttdist.config import load_experiment_config
from rttdist.corpus import FixturePair, ProblemCorpusEntry
from rttdist.exec.adapters import evaluate_source
from rttdist.experiment_io import digest, environment, read_json, write_json
from rttdist.similarity import token_deltas
from rttdist.normalize import hash_normalized_cpp_tokens
from rttdist.extract import extract_single_file_source_text, SourceExtractionError


def prepare():
    root = Path("artifacts-lmstudio/preflight-v1").resolve()
    root.mkdir(parents=True, exist_ok=True)
    (root / "1.inp").write_text("7\n", encoding="utf-8")
    (root / "1.out").write_text("14\n", encoding="utf-8")
    sources = {
        "cpp": '#include <iostream>\nint main(){int n;std::cin>>n;std::cout<<n*2<<"\\n";}\n',
        "c": '#include <stdio.h>\nint main(){int n;scanf("%d",&n);printf("%d\\n",n*2);}\n',
        "java": 'import java.util.*; public class Main {public static void main(String[] args){Scanner s=new Scanner(System.in);System.out.println(s.nextInt()*2);}}\n',
        "python": 'print(int(input())*2)\n'}
    entry = ProblemCorpusEntry("smoke", root / "statement.md", root,
        (FixturePair(root / "1.inp", root / "1.out"),), root / "source.cpp")
    results = {}
    for language, source in sources.items():
        path = root / ("source." + {"python": "py"}.get(language, language))
        path.write_text(source, encoding="utf-8")
        evaluation = evaluate_source(language=language, source_path=path, problem=entry, workspace_root=root, timeout_seconds=30)
        assert evaluation.status.value == "success", (language, evaluation)
        results[language] = asdict(evaluation)
    write_json(root / "smoke.json", {"environment": environment(), "results": results})
    a = 'int f(int a){int b=a+1; int c=a+2; return b+c;}'
    variants = {
        "identical": a,
        "rename": 'int g(int x){int y=x+1; int z=x+2; return y+z;}',
        "reorder_distinct": 'int f(int a){int c=a+2; int b=a+1; return b+c;}',
        "operator": a.replace('a+1', 'a-1'), "literal": a.replace('a+1', 'a+3'),
        "for": 'int f(int a){int s=0;for(int i=0;i<a;i++)s+=i;return s;}',
        "while": 'int f(int a){int s=0;int i=0;while(i<a){s+=i;i++;}return s;}',
        "alternative": 'int f(int a){return 2*a+3;}',
    }
    fixture = Path("tests/fixtures/similarity")
    fixture.mkdir(parents=True, exist_ok=True)
    for name, source in variants.items():
        (fixture / (name+".cpp")).write_text(source+"\n", encoding="utf-8")
    responses = {}
    for name, source in variants.items():
        responses[name] = {"token_deltas": token_deltas(a, source), "ast_similarity": ast_similarity(a, source)}
    # Structurally indistinguishable renamed statements intentionally collapse after abstraction.
    responses["reorder_abstract_equal"] = {"token_deltas": token_deltas('int f(){a();b();}', 'int f(){b();a();}'), "ast_similarity": ast_similarity('int f(){a();b();}', 'int f(){b();a();}')}
    responses["for_to_while"] = {"token_deltas": token_deltas(variants["for"], variants["while"]), "ast_similarity": ast_similarity(variants["for"], variants["while"])}
    write_json(root / "similarity_variants.json", responses)
    assert responses["rename"]["ast_similarity"]["value"] == 1
    assert responses["operator"]["ast_similarity"]["value"] < 1
    assert responses["literal"]["ast_similarity"]["value"] < 1
    original_stats = {}
    for path in sorted(Path("corpus/solutions").glob("*/reference.cpp")):
        source = path.read_text(encoding="utf-8")
        original_stats[path.parent.name] = ast_similarity(source, source)
    write_json(root / "original_ast.json", original_stats)


def audit(summary_path, allow_partial=False):
    s = read_json(summary_path)
    rows, meta = s["observations"], s["run_metadata"]
    output_root = Path(summary_path).resolve().parent.parent
    for metadata in meta:
        condition_keys = ("experiment_version", "problem_ids", "target_languages", "runtime", "lmstudio", "server",
                          "decoding", "validation_hash", "code", "ast", "recovery", "execution_schedule")
        conditions = {key: metadata[key] for key in condition_keys if key in metadata}
        assert digest(conditions) == metadata["condition_hash"]
        assert digest(metadata["code"]["file_hashes"]) == metadata["code"]["source_hash"]
        for relative, checksum in metadata["code"]["file_hashes"].items():
            assert digest((output_root / metadata["run_id"] / "code_snapshot" / relative).read_bytes()) == checksum
        validation = dict(metadata["validation_snapshot"])
        validation_hash = validation.pop("validation_hash")
        assert digest(validation) == validation_hash == metadata["validation_hash"]
        for problem in metadata["problem_ids"]:
            assert validation["problems"][problem]["status"] == "success"
            for filename, checksum in validation["content_hashes"][problem].items():
                assert digest(Path(filename).read_bytes()) == checksum
    expected = len(meta[0]["problem_ids"])*len(meta[0]["target_languages"])*len(meta)
    assert len(rows) <= expected if allow_partial else len(rows) == expected
    if not allow_partial:
        assert not s["exclusions"]
    keys = {(r["problem_id"], r["run_id"], r["route"]) for r in rows}
    assert len(keys) == len(rows)
    for row in rows:
        successes = list(row["success"].values())
        assert successes == sorted(successes, reverse=True)
        if row["success"]["5"]:
            assert len(row["iterations"]) == row["tau"] + 5
            assert all(it["all_steps_passed"] for it in row["iterations"])
        assert row["status"] not in ("api_error", "running")
        manifest_path = Path(row["manifest_path"])
        manifest = read_json(manifest_path)
        index = read_json(manifest_path.parent.parent / "attempts.json")
        assert index["selected_attempt_id"] == manifest["attempt_id"] == row["attempt_id"]
        assert manifest["condition_hash"] == meta[0]["condition_hash"]
        assert manifest["validation_hash"] == meta[0]["validation_hash"]
        hashes = [hash_normalized_cpp_tokens((manifest_path.parent / "seed.cpp").read_text(encoding="utf-8"))]
        candidate_passed = True
        candidate = None
        held = 0
        for it in manifest["iterations"]:
            t = it["iteration_index"]
            folder = manifest_path.parent / "iterations" / f"iter-{t:03d}"
            durable = read_json(folder / "iteration.json")
            assert durable == it
            for step in it["steps"]:
                step_folder = folder / f"step-{step['step_index']:03d}"
                assert read_json(step_folder / "step.json") == step
                req = read_json(step_folder / "llm-request.json")
                response = read_json(step_folder / "llm-response.json")
                assert req["model"] == meta[0]["lmstudio"]["model"]
                assert req["max_tokens"] == meta[0]["lmstudio"]["max_tokens"]
                assert req["temperature"] == 0
                for key, value in meta[0]["decoding"].items():
                    assert req[key] == value
                assert step["truncated"] == any(ch.get("finish_reason") == "length" for ch in response.get("choices", []))
                if step.get("source_path"):
                    extracted = extract_single_file_source_text(response["choices"][0]["message"]["content"])
                    translated_source = Path(step["source_path"]).read_text(encoding="utf-8")
                    assert translated_source.rstrip() == extracted.rstrip()
                    prepared_filename = {"cpp": "Main.cpp", "c": "Main.c", "java": "Main.java", "python": "main.py"}[step["target_language"]]
                    prepared = Path(step["execution"]["work_directory"]) / prepared_filename
                    assert prepared.read_text(encoding="utf-8") == translated_source
                elif step["status"] == "parse_error":
                    try:
                        extract_single_file_source_text(response["choices"][0]["message"]["content"])
                    except (SourceExtractionError, KeyError, IndexError, TypeError):
                        pass
                    else:
                        raise AssertionError("A recorded parse_error is extractable with the pinned extractor")
                if step["status"] == "success":
                    execution = step["execution"]
                    expected_fixtures = len(meta[0]["validation_snapshot"]["problems"][row["problem_id"]]["fixture_results"])
                    assert len(execution["fixture_results"]) == expected_fixtures
                    assert all(f["status"] == "success" for f in execution["fixture_results"])
                    if execution["compile_result"]:
                        assert execution["compile_result"]["exit_code"] == 0
                        assert not execution["compile_result"]["timed_out"]
            if it["roundtrip_hash"]:
                actual = hash_normalized_cpp_tokens((folder / "roundtrip.cpp").read_text(encoding="utf-8"))
                assert actual == it["roundtrip_hash"]
                hashes.append(actual)
            passed = len(it["steps"]) == 2 and all(step["status"] == "success" for step in it["steps"])
            assert it["all_steps_passed"] == passed
            if candidate is None:
                candidate_passed = candidate_passed and passed
                if passed and len(hashes) >= 2 and hashes[-1] == hashes[-2]:
                    candidate = t
            else:
                assert it["confirmation_index"] == t-candidate
                if passed and hashes[-1] == hashes[candidate]:
                    held += 1
        assert hashes == manifest["hash_history"]
        for c in range(6):
            assert row["success"][str(c)] == (candidate is not None and candidate_passed and held >= c)
        assert candidate == row["tau"]
        if candidate:
            seed = (manifest_path.parent / "seed.cpp").read_text(encoding="utf-8")
            candidate_source = Path(manifest["candidate_source_path"]).read_text(encoding="utf-8")
            expected_deltas = token_deltas(seed, candidate_source)
            assert all(row["distance_metrics"]["delta_0"][k]["value"] == v["value"] for k,v in expected_deltas.items())
    for agg in s["rtt_route_aggregates"].values():
        assert sum(v["count"] for v in agg["failures"]["categories"].values()) == agg["evaluable_count"]-agg["by_confirmation"]["5"]["success_count"]
        for c in ("1", "5"):
            cond = agg["conditional"][c]
            for metric in cond["delta_0"].values():
                assert metric["n"]+sum(metric["excluded_by_reason"].values()) == cond["success_count"]
    result = {"passed": True, "scope": "completed_observations_only" if allow_partial else "complete_experiment",
              "expected": expected, "observed": len(rows), "run_count": len(meta),
              "problem_count": len(meta[0]["problem_ids"]), "condition_hash": meta[0]["condition_hash"]}
    write_json(Path(summary_path).parent / ("partial_audit.json" if allow_partial else "completion_audit.json"), result)
    print(result)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        audit(sys.argv[1], allow_partial="--partial" in sys.argv)
    else:
        prepare()
