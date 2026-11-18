"""승인한 v1.6 목록을 원본 변경 없이 독립 코퍼스로 준비합니다."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = {
    "cpp": "cpp",
    "python": "py",
    "java": "java",
    "haskell": "hs",
    "prolog": "pl",
}
PROBLEM_IDS = [
    "IPOP_11729",
    "IPOP_2110",
    "IPOP_1992",
    "IPOP_2579",
    "IPOP_5567",
    "IPOP_10988",
    "IPOP_1929",
    "IPOP_2609",
    "IPOP_9012",
    "LC_0053",
    "LC_0062",
    "IPOP_9663",
    "LC_0242",
    "LC_0283",
    "LC_0338",
]
REPLACEMENTS = {
    "IPOP_1436": "IPOP_11729",
    "IPOP_2217": "IPOP_1992",
    "LC_0217": "IPOP_9663",
}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def file_hashes(directory):
    return {
        path.relative_to(directory).as_posix(): sha256(path)
        for path in sorted(Path(directory).rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def load_selection(path):
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if value.get("corpus_version") != "rtt-v1.6" or value.get("schema_version") != 1:
        raise ValueError("v1.6 선택 목록 스키마가 일치하지 않습니다")
    if [item["problem_id"] for item in value["problems"]] != PROBLEM_IDS:
        raise ValueError("설계에서 고정한 15문제와 순서가 일치하지 않습니다")
    if (
        value.get("languages") != list(LANGUAGES)
        or value.get("replacements") != REPLACEMENTS
    ):
        raise ValueError("고정 언어 또는 문제 교체 대응이 일치하지 않습니다")
    recursive = set(REPLACEMENTS.values())
    for item in value["problems"]:
        expected = item["problem_id"] in recursive
        if item.get("recursive") is not expected or item.get("group") != (
            "recursive" if expected else "comparison"
        ):
            raise ValueError("재귀 구현군은 신규 3문제만 포함해야 합니다")
        if item.get("evaluation_cases") != 13:
            raise ValueError("문제별 평가 수는 13개여야 합니다")
    gcd = next(item for item in value["problems"] if item["problem_id"] == "IPOP_2609")
    if gcd.get("recursion_kind") != "iterative_euclid":
        raise ValueError("기존 C++ 최대공약수는 반복형으로 분류해야 합니다")
    return value


def fixture_pairs(directory, expected=None):
    directory = Path(directory)
    inputs = {path.stem: path for path in directory.glob("*.inp")}
    outputs = {path.stem: path for path in directory.glob("*.out")}
    if not inputs or inputs.keys() != outputs.keys():
        raise ValueError(f"완전한 입력·정답 쌍이 필요합니다: {directory}")
    if expected is not None and len(inputs) != expected:
        raise ValueError(f"평가 입력은 정확히 {expected}개여야 합니다: {directory}")
    return [(inputs[stem], outputs[stem]) for stem in sorted(inputs)]


def check_fixtures(directory):
    evaluation = fixture_pairs(directory / "evaluation", 13)
    examples = fixture_pairs(directory / "prompt_examples")
    public = {tuple(inp.read_text(encoding="utf-8").split()) for inp, _ in examples}
    held_out = [tuple(inp.read_text(encoding="utf-8").split()) for inp, _ in evaluation]
    if public.intersection(held_out):
        raise ValueError(f"공개 예시와 평가 입력이 중복됩니다: {directory.name}")
    if len(set(held_out)) != 13:
        raise ValueError(f"평가 입력끼리 중복됩니다: {directory.name}")
    return len(examples)


def prepare_corpus(selection_path, source_root, destination):
    selection_path = Path(selection_path).resolve()
    source_root, destination = Path(source_root).resolve(), Path(destination).resolve()
    if (
        destination == source_root
        or destination.is_relative_to(source_root)
        or source_root.is_relative_to(destination)
    ):
        raise ValueError("원본 자료와 생성 코퍼스 경로가 겹칩니다")
    selection = load_selection(selection_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix="v16-corpus-", dir=destination.parent
    ) as temporary:
        stage = Path(temporary) / "corpus"
        stage.mkdir()
        records = []
        for item in selection["problems"]:
            pid = item["problem_id"]
            source, target = source_root / pid, stage / pid
            target.mkdir()
            for name in ("statement.md", "reference.cpp"):
                shutil.copy2(source / name, target / name)
            for name in ("evaluation", "prompt_examples"):
                shutil.copytree(source / name, target / name)
            provenance = {
                "cpp": {
                    "source": f"problem/{pid}/reference.cpp",
                    "sha256": sha256(source / "reference.cpp"),
                    "method": "원본 바이트 보존",
                }
            }
            for language, extension in LANGUAGES.items():
                if language == "cpp":
                    continue
                reference = (
                    selection_path.parent
                    / "references"
                    / pid
                    / f"reference.{extension}"
                )
                shutil.copy2(reference, target / reference.name)
                provenance[language] = {
                    "source": reference.relative_to(selection_path.parent).as_posix(),
                    "sha256": sha256(reference),
                    "method": "외부 모델 API 없이 로컬 작성, 기존 13개 평가 및 독립 계산과 대조",
                }
            example_count = check_fixtures(target)
            records.append(
                {
                    "problem_id": pid,
                    "source": f"problem/{pid}",
                    "reference_provenance": provenance,
                    "evaluation_cases": 13,
                    "prompt_example_cases": example_count,
                }
            )
        shutil.copy2(selection_path, stage / "selection.json")
        manifest = {
            "schema_version": 1,
            "corpus_version": "rtt-v1.6",
            "selection_sha256": sha256(selection_path),
            "reference_languages": list(LANGUAGES),
            "problem_ids": PROBLEM_IDS,
            "problems": records,
            "file_hashes": file_hashes(stage),
        }
        (stage / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        if destination.exists():
            if file_hashes(destination) != file_hashes(stage):
                raise ValueError(
                    "기존 동결 코퍼스와 내용이 다릅니다. 별도 경로에 준비하고 해시를 다시 동결해 주십시오"
                )
        else:
            shutil.move(str(stage), destination)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--selection", type=Path, default=ROOT / "papers/v1.6/data/selection.json"
    )
    parser.add_argument("--source-root", type=Path, default=ROOT / "problem")
    parser.add_argument("--destination", type=Path, default=ROOT / "data/rtt-v1.6")
    args = parser.parse_args()
    result = prepare_corpus(args.selection, args.source_root, args.destination)
    print(
        f"{len(result['problem_ids'])}문제·75개 기준 구현을 준비하였습니다: {args.destination}"
    )


if __name__ == "__main__":
    main()
