from __future__ import annotations

import argparse
import logging
import os
import sys
from typing import TYPE_CHECKING
from collections.abc import Sequence
from pathlib import Path
import uuid

from rttdist import __version__
from rttdist.config import (
    ConfigValidationError,
    ExperimentConfig,
    load_experiment_config,
)
from rttdist.corpus import CorpusValidationError, ProblemCorpusEntry, validate_corpus
from rttdist.moss import MossSimilarityMatch, measure_pair_similarity
from rttdist.pipeline import run_pipeline_service
from rttdist.reporting import MossSimilarityFn, write_run_summary

if TYPE_CHECKING:
    from rttdist.pipeline import RTTRunResult

EXIT_SUCCESS = 0
EXIT_VALIDATION_ERROR = 1
EXIT_RUNTIME_ERROR = 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rttdist",
        description="Bootstrap CLI for RTT distance experiments.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # validate-corpus command
    validate_parser = subparsers.add_parser(
        "validate-corpus",
        help="Validate config and corpus without running experiments",
    )
    _add_config_arguments(validate_parser)
    validate_parser.set_defaults(func=_cmd_validate_corpus)

    # run command
    run_parser = subparsers.add_parser(
        "run",
        help="Execute the RTT pipeline from config",
    )
    _add_config_arguments(run_parser)
    _add_moss_arguments(run_parser)
    run_parser.add_argument(
        "--run-id",
        dest="run_id_option",
        default=None,
        help="Explicit run ID (auto-generated if not provided)",
    )
    run_parser.add_argument(
        "run_id",
        nargs="?",
        help="Optional positional run ID (deprecated in favor of --run-id)",
    )
    run_parser.set_defaults(func=_cmd_run)

    # resume command
    resume_parser = subparsers.add_parser(
        "resume",
        help="Resume a previous run using existing artifacts",
    )
    _add_config_arguments(resume_parser)
    _add_moss_arguments(resume_parser)
    resume_parser.add_argument(
        "--run-id",
        dest="run_id_option",
        default=None,
        help="Run ID to resume",
    )
    resume_parser.add_argument(
        "run_id",
        nargs="?",
        help="Optional positional run ID to resume",
    )
    resume_parser.set_defaults(func=_cmd_resume)

    # report command
    report_parser = subparsers.add_parser(
        "report",
        help="Generate summary report from existing run",
    )
    _add_config_arguments(report_parser)
    _add_moss_arguments(report_parser)
    report_parser.add_argument(
        "--run-id",
        dest="run_id_option",
        default=None,
        help="Run ID to generate report for",
    )
    report_parser.add_argument(
        "run_id",
        nargs="?",
        help="Optional positional run ID to generate report for",
    )
    report_parser.set_defaults(func=_cmd_report)

    return parser


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
    )


def _add_config_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--config",
        dest="config_option",
        default=None,
        help="Path to experiment config YAML file",
    )
    parser.add_argument(
        "config",
        nargs="?",
        help="Optional positional config path",
    )


def _add_moss_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--with-moss",
        action="store_true",
        help="Run opt-in MOSS similarity for seed vs final round-trip C++ during summary generation",
    )
    parser.add_argument(
        "--moss-script",
        default=None,
        help="Path to moss.pl (defaults to $RTTDIST_MOSS_SCRIPT or ./moss.pl when --with-moss is used)",
    )


def _load_config(config_path: str) -> ExperimentConfig:
    """Load and return experiment config, or exit with error."""
    try:
        return load_experiment_config(Path(config_path))
    except ConfigValidationError as exc:
        _error(f"Config validation failed: {exc}")
        sys.exit(EXIT_VALIDATION_ERROR)


def _resolve_required_argument(
    *,
    positional: str | None,
    option: str | None,
    field_name: str,
) -> str:
    positional_value = positional.strip() if isinstance(positional, str) else ""
    option_value = option.strip() if isinstance(option, str) else ""

    if positional_value and option_value and positional_value != option_value:
        _error(
            f"Conflicting {field_name} values provided; use either the positional argument or --{field_name.replace('_', '-')}."
        )
        sys.exit(EXIT_VALIDATION_ERROR)

    value = option_value or positional_value
    if not value:
        _error(
            f"Missing required {field_name}; provide it positionally or with --{field_name.replace('_', '-')}"
        )
        sys.exit(EXIT_VALIDATION_ERROR)
    return value


def _validate_corpus_entries(
    config: ExperimentConfig,
) -> tuple[ProblemCorpusEntry, ...]:
    """Validate corpus entries, or exit with error."""
    try:
        return validate_corpus(config)
    except CorpusValidationError as exc:
        _error(f"Corpus validation failed: {exc}")
        sys.exit(EXIT_VALIDATION_ERROR)


def _error(message: str) -> None:
    """Print error message to stderr."""
    print(message, file=sys.stderr)


def _cmd_validate_corpus(args: argparse.Namespace) -> int:
    """Validate config and corpus without running experiments."""
    config_path = _resolve_required_argument(
        positional=args.config,
        option=args.config_option,
        field_name="config",
    )
    config = _load_config(config_path)
    entries = _validate_corpus_entries(config)

    print(f"Config validated successfully.")
    print(f"Seed language: {config.seed_language}")
    print(f"Found {len(entries)} problem(s):")
    for entry in entries:
        print(f"  - {entry.problem_id}: {len(entry.fixture_pairs)} fixture pair(s)")

    return EXIT_SUCCESS


def _cmd_run(args: argparse.Namespace) -> int:
    """Execute the RTT pipeline from config."""
    config_path = _resolve_required_argument(
        positional=args.config,
        option=args.config_option,
        field_name="config",
    )
    config = _load_config(config_path)
    entries = _validate_corpus_entries(config)
    _validate_provider_runtime_or_exit(config)

    run_id = (
        _resolve_required_argument(
            positional=args.run_id,
            option=args.run_id_option,
            field_name="run_id",
        )
        if args.run_id or args.run_id_option
        else str(uuid.uuid4())
    )

    moss_similarity_fn = _build_moss_similarity_fn_or_exit(args)

    print(f"Starting run: {run_id}")
    print(f"Output root: {config.output_root}")

    try:
        results = run_pipeline_service(
            config=config,
            run_id=run_id,
            corpus_entries=entries,
        )
    except Exception as exc:
        _error(f"Pipeline execution failed: {exc}")
        return EXIT_RUNTIME_ERROR

    print(f"Run completed: {run_id}")
    print(f"Total experiments: {len(results)}")

    for result in results:
        status = result.final_record.status.value
        print(
            f"  - {result.problem_id}/{result.target_language}: {status}"
            f" ({result.final_record.message})"
        )
        error_detail = result.final_record.details.get("error")
        if isinstance(error_detail, str) and error_detail.strip():
            print(f"      detail: {error_detail.strip()}")

    _write_summary_or_exit(
        config=config,
        run_id=run_id,
        results=results,
        moss_similarity_fn=moss_similarity_fn,
    )

    return EXIT_SUCCESS


def _cmd_resume(args: argparse.Namespace) -> int:
    """Resume a previous run using existing artifacts."""
    config_path = _resolve_required_argument(
        positional=args.config,
        option=args.config_option,
        field_name="config",
    )
    config = _load_config(config_path)
    entries = _validate_corpus_entries(config)
    _validate_provider_runtime_or_exit(config)

    run_id = _resolve_required_argument(
        positional=args.run_id,
        option=args.run_id_option,
        field_name="run_id",
    )

    moss_similarity_fn = _build_moss_similarity_fn_or_exit(args)

    print(f"Resuming run: {run_id}")
    print(f"Output root: {config.output_root}")

    try:
        results = run_pipeline_service(
            config=config,
            run_id=run_id,
            corpus_entries=entries,
        )
    except Exception as exc:
        _error(f"Resume failed: {exc}")
        return EXIT_RUNTIME_ERROR

    print(f"Resume completed: {run_id}")
    print(f"Total experiments: {len(results)}")

    for result in results:
        status = result.final_record.status.value
        print(
            f"  - {result.problem_id}/{result.target_language}: {status}"
            f" ({result.final_record.message})"
        )
        error_detail = result.final_record.details.get("error")
        if isinstance(error_detail, str) and error_detail.strip():
            print(f"      detail: {error_detail.strip()}")

    _write_summary_or_exit(
        config=config,
        run_id=run_id,
        results=results,
        moss_similarity_fn=moss_similarity_fn,
    )

    return EXIT_SUCCESS


def _cmd_report(args: argparse.Namespace) -> int:
    """Generate summary report from existing run."""
    run_id = _resolve_required_argument(
        positional=args.run_id,
        option=args.run_id_option,
        field_name="run_id",
    )

    config_value = args.config.strip() if isinstance(args.config, str) else ""
    config_option_value = (
        args.config_option.strip() if isinstance(args.config_option, str) else ""
    )
    if config_value or config_option_value:
        config_path = _resolve_required_argument(
            positional=args.config,
            option=args.config_option,
            field_name="config",
        )
        output_root = _load_config(config_path).output_root
    else:
        output_root = Path("artifacts")

    moss_similarity_fn = _build_moss_similarity_fn_or_exit(args)

    print(f"Generating report for run: {run_id}")

    try:
        artifacts = write_run_summary(
            output_root=output_root,
            run_id=run_id,
            moss_similarity_fn=moss_similarity_fn,
        )
        print(f"Report generated successfully.")
        print(f"  - JSON: {artifacts.summary_json_path}")
        print(f"  - Markdown: {artifacts.summary_markdown_path}")
    except Exception as exc:
        _error(f"Report generation failed: {exc}")
        return EXIT_RUNTIME_ERROR

    return EXIT_SUCCESS


def _write_summary_or_exit(
    *,
    config: ExperimentConfig,
    run_id: str,
    results: tuple[RTTRunResult, ...],
    moss_similarity_fn: MossSimilarityFn | None,
) -> None:
    try:
        artifacts = write_run_summary(
            output_root=config.output_root,
            run_id=run_id,
            run_results=results,
            moss_similarity_fn=moss_similarity_fn,
        )
    except Exception as exc:
        _error(f"Report generation failed: {exc}")
        sys.exit(EXIT_RUNTIME_ERROR)

    print("Summary generated successfully.")
    print(f"  - JSON: {artifacts.summary_json_path}")
    print(f"  - Markdown: {artifacts.summary_markdown_path}")


def _build_moss_similarity_fn_or_exit(
    args: argparse.Namespace,
) -> MossSimilarityFn | None:
    if not getattr(args, "with_moss", False):
        return None

    raw_script_path = (
        args.moss_script.strip() if isinstance(args.moss_script, str) else ""
    )
    env_script_path = os.environ.get("RTTDIST_MOSS_SCRIPT", "").strip()
    selected_script_path = Path(raw_script_path or env_script_path or "moss.pl")
    resolved_script_path = selected_script_path.expanduser().resolve()
    if not resolved_script_path.is_file():
        _error(
            "MOSS requested but the script was not found. "
            "Provide --moss-script or set RTTDIST_MOSS_SCRIPT."
        )
        sys.exit(EXIT_VALIDATION_ERROR)

    def _measure(
        seed_cpp_source: str,
        roundtrip_cpp_source: str,
        label: str,
    ) -> MossSimilarityMatch:
        return measure_pair_similarity(
            seed_cpp_source,
            roundtrip_cpp_source,
            script_path=resolved_script_path,
            label=label,
        )

    return _measure


def _validate_provider_runtime_or_exit(config: ExperimentConfig) -> None:
    pass


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    parsed = parser.parse_args(list(argv) if argv is not None else None)

    _setup_logging(parsed.verbose)

    if hasattr(parsed, "func"):
        return parsed.func(parsed)

    parser.print_help()
    return EXIT_SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())
