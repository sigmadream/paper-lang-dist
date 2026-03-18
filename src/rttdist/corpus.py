from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from rttdist.config import ExperimentConfig


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


def validate_corpus(config: ExperimentConfig) -> tuple[ProblemCorpusEntry, ...]:
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

        seed_path = config.corpus_root / problem_id / "reference.cpp"
        if not seed_path.is_file():
            raise CorpusValidationError(
                f"Missing seed reference.cpp for problem `{problem_id}`: {seed_path}"
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
