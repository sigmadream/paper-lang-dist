"""75개 기준 구현의 975개 평가와 독립 계산 근거를 보존합니다."""

import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import time

import yaml

from rttdist.experiment_io import timestamp, write_json
from rttdist.fps_execution import canonical_output, evaluate, process

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))
from prepare_v16_corpus import (
    LANGUAGES,
    PROBLEM_IDS,
    check_fixtures,
    file_hashes,
    load_selection,
    sha256,
)


def oracle_module(group):
    path = ROOT / f"problem/metadata/{group}/tools/oracles.py"
    spec = importlib.util.spec_from_file_location(f"v16_{group}_oracles", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, path


def independent_checks(corpus):
    """기준 코드를 호출하지 않는 기존 이중 계산기를 다시 실행합니다."""
    ipop, ipop_path = oracle_module("ipop19")
    leetcode, lc_path = oracle_module("leetcode21")
    results = []
    methods = {
        "LC_0053": "Kadane 및 누적합 최솟값/소형 전구간",
        "LC_0062": "격자 점화식 및 이항계수",
        "LC_0242": "빈도 집계 및 정렬",
        "LC_0283": "제자리 교환 및 필터/0 채우기",
        "LC_0338": "비트 점화식 및 반복 나눗셈",
    }
    for pid in PROBLEM_IDS:
        for inp in sorted((corpus / pid / "evaluation").glob("*.inp")):
            start = time.monotonic()
            record = {"problem_id": pid, "case": inp.stem, "input_sha256": sha256(inp)}
            try:
                text = inp.read_text(encoding="utf-8")
                if pid.startswith("IPOP_"):
                    number = pid.split("_")[1]
                    first, second = ipop.solve(number, text)
                    record["methods"] = list(ipop.METHODS[number])
                    if number == "11729":
                        n = int(text)
                        record.update(
                            {
                                "n": n,
                                "minimum_moves": 2**n - 1,
                                "output_bytes": len(first.encode("utf-8")),
                                "legality_checked": True,
                            }
                        )
                    if number == "9663":
                        record.update({"n": int(text), "solution_count": int(first)})
                else:
                    number = int(pid.split("_")[1])
                    words = text.split()
                    values = list(map(int, words)) if number != 242 else words
                    args = (
                        [values[1:]]
                        if number in (53, 283)
                        else values if number in (62, 242) else [values[0]]
                    )
                    first, second = leetcode.solve(number, args)

                    def output(value):
                        return (
                            " ".join(map(str, value))
                            if isinstance(value, list)
                            else (
                                str(int(value))
                                if isinstance(value, bool)
                                else str(value)
                            )
                        )

                    first, second = output(first), output(second)
                    record["methods"] = methods[pid]
                expected = inp.with_suffix(".out").read_text(encoding="utf-8")
                record.update(
                    {
                        "passed": canonical_output(first)
                        == canonical_output(second)
                        == canonical_output(expected),
                        "computed_sha256": hashlib.sha256(
                            canonical_output(first).encode()
                        ).hexdigest(),
                        "expected_sha256": sha256(inp.with_suffix(".out")),
                    }
                )
            except (
                OSError,
                ValueError,
                AssertionError,
                KeyError,
                IndexError,
                RecursionError,
            ) as exc:
                record.update({"passed": False, "error": str(exc)})
            record["seconds"] = time.monotonic() - start
            results.append(record)
    return {
        "source_hashes": {
            str(path.relative_to(ROOT).as_posix()): sha256(path)
            for path in (ipop_path, lc_path)
        },
        "results": results,
        "passed": len(results) == 195 and all(record["passed"] for record in results),
    }


def preflight(corpus, cfg):
    errors = []
    if cfg.get("problem_ids") != PROBLEM_IDS:
        errors.append("설정 문제 목록이 고정한 15문제와 일치하지 않습니다")
    runtime = cfg.get("runtime", {})
    if runtime.get("fixture_timeout") != 5 or runtime.get("compile_timeout") != 180:
        errors.append("평가 5초·컴파일 180초 제한이 일치하지 않습니다")
    try:
        selection = load_selection(corpus / "selection.json")
        manifest = json.loads((corpus / "manifest.json").read_text(encoding="utf-8"))
        expected = dict(manifest["file_hashes"])
        expected["manifest.json"] = sha256(corpus / "manifest.json")
        if file_hashes(corpus) != expected:
            errors.append("동결 매니페스트와 코퍼스 파일 해시가 일치하지 않습니다")
        if manifest.get("selection_sha256") != sha256(corpus / "selection.json"):
            errors.append("선택 목록 해시가 일치하지 않습니다")
        if manifest.get("problem_ids") != PROBLEM_IDS or manifest.get(
            "reference_languages"
        ) != list(LANGUAGES):
            errors.append("매니페스트의 고정 문제·언어 목록이 일치하지 않습니다")
        if cfg.get("selection") and sha256(cfg["selection"]) != sha256(
            corpus / "selection.json"
        ):
            errors.append("설정의 선택 목록과 준비한 코퍼스가 다릅니다")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f"선택 목록/매니페스트 오류: {exc}")
    for pid in PROBLEM_IDS:
        try:
            check_fixtures(corpus / pid)
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
        for name in [
            "statement.md",
            *[f"reference.{ext}" for ext in LANGUAGES.values()],
        ]:
            if not (corpus / pid / name).is_file():
                errors.append(f"필수 파일이 없습니다: {pid}/{name}")
    return errors


def validate_corpus(cfg):
    corpus = Path(cfg["corpus_root"]).resolve()
    validation_path = Path(cfg["validation"]).resolve()
    if validation_path.is_relative_to(corpus):
        raise ValueError("검증 결과는 동결 코퍼스 바깥에 저장해야 합니다")
    runtime = deepcopy(cfg.get("runtime", {}))
    errors = preflight(corpus, cfg)
    versions = {}
    tools = runtime.get("tools", {})
    missing = {}
    for language in LANGUAGES:
        tool = tools.get(language)
        if not tool or not shutil.which(str(tool)):
            missing[language] = f"실행 도구를 찾을 수 없습니다: {language}={tool}"
            errors.append(missing[language])
            versions[language] = {"available": False, "error": missing[language]}
            continue
        try:
            version = process([str(tool), "--version"], ROOT, 30)
            versions[language] = {
                "available": not version["timed_out"] and version["exit_code"] == 0,
                **version,
            }
            if not versions[language]["available"]:
                missing[language] = f"도구 실행 확인에 실패했습니다: {language}"
                errors.append(missing[language])
            if language == "java":
                java = str(
                    Path(shutil.which(str(tool))).with_name("java" + Path(tool).suffix)
                )
                versions["java_runtime"] = process([java, "--version"], ROOT, 30)
                if (
                    versions["java_runtime"]["exit_code"] != 0
                    or versions["java_runtime"]["timed_out"]
                ):
                    missing[language] = "Java 실행 도구 확인에 실패했습니다"
                    errors.append(missing[language])
        except OSError as exc:
            missing[language] = f"도구 실행 오류: {language}: {exc}"
            versions[language] = {"available": False, "error": str(exc)}
            errors.append(missing[language])
    structural_errors = preflight(corpus, cfg)
    results = []
    for pid in PROBLEM_IDS:
        for language, extension in LANGUAGES.items():
            folder = validation_path.parent / "references" / pid / language
            result = {
                "problem_id": pid,
                "language": language,
                "status": "unavailable",
                "case_count": 0,
                "expected_cases": 13,
                "passed_cases": 0,
                "evaluation_path": str(folder / "evaluation.json"),
            }
            if structural_errors or language in missing:
                result["error"] = (
                    "코퍼스 사전 점검 실패" if structural_errors else missing[language]
                )
            else:
                try:
                    source = (corpus / pid / f"reference.{extension}").read_text(
                        encoding="utf-8"
                    )
                    value = evaluate(source, language, corpus / pid, folder, runtime)
                    result.update(
                        {
                            "status": value["status"],
                            "case_count": len(value["cases"]),
                            "passed_cases": sum(
                                case["status"] == "success" for case in value["cases"]
                            ),
                            "max_case_seconds": max(
                                (case["seconds"] for case in value["cases"]),
                                default=None,
                            ),
                            "compile_seconds": value["compile"]["seconds"],
                        }
                    )
                except (OSError, ValueError, KeyError) as exc:
                    result.update({"status": "infrastructure_error", "error": str(exc)})
            results.append(result)
            print(
                f"{pid} {language}: {result['status']} ({result['passed_cases']}/13)",
                flush=True,
            )
    independent = (
        independent_checks(corpus)
        if not structural_errors
        else {"passed": False, "results": [], "error": "코퍼스 사전 점검 실패"}
    )
    executed = sum(result["case_count"] for result in results)
    passed_cases = sum(result["passed_cases"] for result in results)
    reference_count = sum(
        result["status"] == "success" and result["case_count"] == 13
        for result in results
    )
    content_hashes = file_hashes(corpus)
    manifest_hash = content_hashes.get("manifest.json")
    value = {
        "schema_version": 1,
        "corpus_version": "rtt-v1.6",
        "created_at": timestamp(),
        "runtime": runtime,
        "tool_versions": versions,
        "reference_languages": list(LANGUAGES),
        "problem_ids": PROBLEM_IDS,
        "expected_references": 75,
        "expected_cases": 975,
        "reference_count": reference_count,
        "evaluation_count": passed_cases,
        "executed_cases": executed,
        "passed_cases": passed_cases,
        "results": results,
        "file_hashes": content_hashes,
        "manifest_sha256": manifest_hash,
        "independent_checks": independent,
        "validator_source_hashes": {
            f"scripts/{name}": sha256(ROOT / "scripts" / name)
            for name in ("prepare_v16_corpus.py", "validate_v16_corpus.py")
        },
        "errors": errors,
        "passed": not errors
        and reference_count == 75
        and executed == passed_cases == 975
        and independent["passed"],
    }
    write_json(validation_path, value)
    return value


def load_config(path):
    path = Path(path).resolve()
    cfg = yaml.safe_load(path.read_text(encoding="utf-8"))
    for key in ("corpus_root", "selection", "validation"):
        if cfg.get(key):
            value = Path(cfg[key])
            cfg[key] = str(
                value if value.is_absolute() else (path.parent / value).resolve()
            )
    return cfg


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config", type=Path, default=ROOT / "configs/v1.6/experiment.yaml"
    )
    args = parser.parse_args()
    result = validate_corpus(load_config(args.config))
    print(
        f"검증 {'통과' if result['passed'] else '실패'}: {result['reference_count']}/75개 구현, {result['passed_cases']}/975개 평가"
    )
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
