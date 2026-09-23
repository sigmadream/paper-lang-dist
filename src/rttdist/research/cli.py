"""CLI for research campaigns; existing commands remain compatible."""
from pathlib import Path
import json


def add_parser(subparsers):
    parser = subparsers.add_parser("research", help="Profile-driven multi-model RTT experiments")
    parser.add_argument("--extension", action="append", default=[], help="Import a trusted Python module that registers extensions")
    commands = parser.add_subparsers(dest="research_action", required=True)
    for name in ("validate", "run", "resume"):
        command = commands.add_parser(name)
        command.add_argument("--config", required=True)
        if name == "resume":
            command.add_argument("--new-attempt", action="store_true")
        command.set_defaults(func=execute)
    for name in ("analyze", "status", "replay"):
        command = commands.add_parser(name)
        command.add_argument("--experiment", required=True, help="Existing experiment directory")
        if name == "analyze":
            command.add_argument("--profile", help="Analysis YAML or full profile with unchanged execution")
            command.add_argument("--analysis-id")
        if name == "replay":
            command.add_argument("--replay-id")
        command.set_defaults(func=execute)
    commands.add_parser("profiles").set_defaults(func=execute)


def execute(args):
    try:
        import importlib
        for module in args.extension:
            importlib.import_module(module)
        if args.research_action == "profiles":
            from .profiles import PROFILES
            print(json.dumps(PROFILES, ensure_ascii=False, indent=2))
            return 0
        if args.research_action == "replay":
            from .replay import replay
            result = replay(args.experiment, replay_id=args.replay_id)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result["matches_original"] else 2
        if args.research_action in ("status", "analyze"):
            from .analysis import analyze, status
            result = status(args.experiment) if args.research_action == "status" else analyze(
                args.experiment, profile=args.profile, analysis_id=args.analysis_id)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        from .config import load_config
        from .engine import corpus_files, run_experiment, _metric_tools
        cfg = load_config(args.config)
        if args.research_action == "validate":
            corpus_files(cfg)
            _metric_tools(cfg["profile"])
            print(json.dumps(cfg, ensure_ascii=False, indent=2))
            return 0
        rows = run_experiment(cfg, resume=args.research_action == "resume", new_attempt=getattr(args, "new_attempt", False))
        print(f"Recorded {len(rows)} trials in {Path(cfg['output_root']) / cfg['id']}")
        return 2 if any(r["decision"]["category"] == "invalid" for r in rows) else 0
    except (ValueError, OSError, KeyError) as exc:
        # Configuration validation never includes credential values.
        print(f"Research experiment error: {exc}")
        return 1
