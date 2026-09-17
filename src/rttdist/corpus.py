from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

from rttdist.config import ExperimentConfig, reference_filename_for_language


class CorpusValidationError(ValueError):
    pass


@dataclass(frozen=True)
class FixturePair:
    input_path: Path
    output_path: Path


@dataclass(frozen=True)
class ProblemCorpusEntry:
    problem_id: str
    statement_path: Path
    fixture_directory: Path
    fixture_pairs: tuple[FixturePair, ...]
    seed_path: Path
    prompt_examples: tuple[FixturePair, ...] | None = None

    @property
    def prompt_sample(self) -> FixturePair:
        # Entries created by legacy callers use their original sample fixtures.
        examples = self.fixture_pairs if self.prompt_examples is None else self.prompt_examples
        if not examples:
            raise CorpusValidationError(f"Missing prompt examples for problem `{self.problem_id}`")
        return examples[0]


def validate_corpus(config: ExperimentConfig) -> tuple[ProblemCorpusEntry, ...]:
    if config.dataset_index is not None:
        return _load_indexed_corpus(config)
    entries: list[ProblemCorpusEntry] = []
    for problem_id in config.problem_ids:
        statement_path = config.problem_root / f"{problem_id}.md"
        if not statement_path.is_file():
            raise CorpusValidationError(
                f"Missing statement file for problem `{problem_id}`: {statement_path}"
            )

        fixture_directory = config.problem_root / problem_id
        if not fixture_directory.is_dir():
            raise CorpusValidationError(
                "Missing fixture directory for problem "
                f"`{problem_id}`: {fixture_directory}"
            )

        fixture_pairs = _discover_fixture_pairs(problem_id, fixture_directory)

        seed_filename = reference_filename_for_language(config.seed_language)
        seed_path = config.corpus_root / problem_id / seed_filename
        if not seed_path.is_file():
            raise CorpusValidationError(
                f"Missing seed {seed_filename} for problem `{problem_id}`: {seed_path}"
            )

        entries.append(
            ProblemCorpusEntry(
                problem_id=problem_id,
                statement_path=statement_path,
                fixture_directory=fixture_directory,
                fixture_pairs=fixture_pairs,
                seed_path=seed_path,
            )
        )

    return tuple(entries)


def _load_indexed_corpus(config: ExperimentConfig) -> tuple[ProblemCorpusEntry, ...]:
    """Load separate prompt and evaluation inputs from a versioned dataset index."""
    index_path = config.dataset_index
    assert index_path is not None
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
        schema_version = index["schema_version"]
        if schema_version not in (1, 2):
            raise ValueError("Unsupported dataset index schema")
        directories: dict[str, Path] = {}
        normalizations: dict[str, str] = {}
        for dataset in index["datasets"]:
            manifest_path = index_path.parent / dataset["manifest"]
            if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != dataset["manifest_sha256"]:
                raise ValueError(f"Dataset manifest hash mismatch: {manifest_path}")
            for item in dataset["problems"]:
                problem_id = item["id"]
                if problem_id in directories:
                    raise ValueError(f"Duplicate problem ID: {problem_id}")
                directories[problem_id] = (index_path.parent / item["directory"]).resolve()
                normalization = item.get("input_normalization", "tokens")
                if normalization not in ("tokens", "line"):
                    raise ValueError(f"Unsupported input normalization: {normalization}")
                normalizations[problem_id] = normalization
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise CorpusValidationError(f"Invalid dataset index {index_path}: {exc}") from exc

    entries = []
    for problem_id in config.problem_ids:
        if problem_id not in directories:
            raise CorpusValidationError(f"Problem `{problem_id}` missing from dataset index {index_path}")
        directory = directories[problem_id]
        seed_filename = reference_filename_for_language(config.seed_language)
        if schema_version == 2:
            statement = directory / "statement.md"
            examples_dir = directory / "prompt_examples"
            evaluation_dir = directory / "evaluation"
            seed = directory / seed_filename
        elif problem_id.startswith("IPOP_"):
            statement = config.problem_root / f"{problem_id}.md"
            examples_dir = config.problem_root / problem_id
            evaluation_dir = directory
            seed = config.corpus_root / problem_id / seed_filename
        elif problem_id.startswith("LC_"):
            statement = directory / "statement.md"
            examples_dir = directory / "prompt_examples"
            evaluation_dir = directory / "evaluation"
            seed = directory / seed_filename
        else:
            raise CorpusValidationError(f"Unsupported dataset layout for problem `{problem_id}`")
        for label, path in (("statement file", statement), (f"seed {seed_filename}", seed)):
            if not path.is_file():
                raise CorpusValidationError(f"Missing {label} for problem `{problem_id}`: {path}")
        examples = _discover_fixture_pairs(problem_id, examples_dir)
        evaluation = _discover_fixture_pairs(problem_id, evaluation_dir)
        def input_key(path):
            value = path.read_text(encoding="utf-8")
            return value.removesuffix("\n") if normalizations[problem_id] == "line" else tuple(value.split())

        example_inputs = {input_key(pair.input_path) for pair in examples}
        if any(input_key(pair.input_path) in example_inputs for pair in evaluation):
            raise CorpusValidationError(f"Evaluation input overlaps prompt examples for problem `{problem_id}`")
        entries.append(ProblemCorpusEntry(
            problem_id=problem_id, statement_path=statement,
            fixture_directory=evaluation_dir, fixture_pairs=evaluation,
            seed_path=seed, prompt_examples=examples,
        ))
    return tuple(entries)


def _discover_fixture_pairs(
    problem_id: str,
    fixture_directory: Path,
) -> tuple[FixturePair, ...]:
    input_paths = sorted(fixture_directory.glob("*.inp"))
    output_paths = sorted(fixture_directory.glob("*.out"))

    input_stems = {path.stem for path in input_paths}
    output_stems = {path.stem for path in output_paths}

    if not input_stems and not output_stems:
        raise CorpusValidationError(
            "Missing fixture pair for problem "
            f"`{problem_id}` in directory: {fixture_directory}"
        )

    if input_stems and not output_stems:
        missing_stem = sorted(input_stems)[0]
        raise CorpusValidationError(
            "Missing fixture pair for problem "
            f"`{problem_id}`: expected output file `{missing_stem}.out` "
            f"in {fixture_directory}"
        )

    if output_stems and not input_stems:
        missing_stem = sorted(output_stems)[0]
        raise CorpusValidationError(
            "Missing fixture pair for problem "
            f"`{problem_id}`: expected input file `{missing_stem}.inp` "
            f"in {fixture_directory}"
        )

    missing_outputs = sorted(input_stems - output_stems)
    if missing_outputs:
        missing_stem = missing_outputs[0]
        raise CorpusValidationError(
            "Missing fixture pair for problem "
            f"`{problem_id}`: expected output file `{missing_stem}.out` "
            f"in {fixture_directory}"
        )

    missing_inputs = sorted(output_stems - input_stems)
    if missing_inputs:
        missing_stem = missing_inputs[0]
        raise CorpusValidationError(
            "Missing fixture pair for problem "
            f"`{problem_id}`: expected input file `{missing_stem}.inp` "
            f"in {fixture_directory}"
        )

    paired_stems = sorted(input_stems)
    if not paired_stems:
        raise CorpusValidationError(
            "Missing fixture pair for problem "
            f"`{problem_id}` in directory: {fixture_directory}"
        )

    return tuple(
        FixturePair(
            input_path=fixture_directory / f"{stem}.inp",
            output_path=fixture_directory / f"{stem}.out",
        )
        for stem in paired_stems
    )
