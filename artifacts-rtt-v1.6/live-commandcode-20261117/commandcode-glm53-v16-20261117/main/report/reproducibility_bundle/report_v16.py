"""단일 v1.6 집계 자료로 표·그림·한국어 요약을 작성합니다."""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil

from rttdist.hops_reporting import summarize_hops, public_data


def _json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
        + "\n",
        encoding="utf-8",
    )


def _read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _csv(path, rows, fields):
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    k: (
                        json.dumps(v, ensure_ascii=False, sort_keys=True)
                        if isinstance(v, (dict, list))
                        else v
                    )
                    for k, v in row.items()
                }
            )


def _leaves(value, prefix=""):
    if isinstance(value, dict):
        for key, item in value.items():
            escaped = str(key).replace("~", "~0").replace("/", "~1")
            yield from _leaves(item, prefix + "/" + escaped)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _leaves(item, prefix + "/" + str(index))
    else:
        yield prefix, value


def _display(value, digits=3):
    return "결측" if value is None else f"{value:.{digits}f}"


def _figures(summary, folder):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    available = {font.name for font in font_manager.fontManager.ttflist}
    korean_font = next(
        (
            name
            for name in (
                "Malgun Gothic",
                "AppleGothic",
                "Noto Sans CJK KR",
                "NanumGothic",
            )
            if name in available
        ),
        None,
    )
    if korean_font:
        plt.rcParams["font.family"] = korean_font
    plt.rcParams["axes.unicode_minus"] = False

    routes = list(summary["routes"])
    inputs = [
        {"route": r, **{m: summary["routes"][r][m] for m in ("P", "H", "D")}}
        for r in routes
    ]
    _csv(folder / "figure_inputs.csv", inputs, ["route", "P", "H", "D"])
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    labels = [r.split("-via-")[-1] for r in routes]
    for axis, metric in zip(axes, ("P", "H", "D")):
        values = [summary["routes"][r][metric] for r in routes]
        axis.bar(range(len(routes)), [float("nan") if v is None else v for v in values])
        axis.set_xticks(range(len(routes)), labels, rotation=25)
        axis.set_ylabel(metric)
        axis.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(folder / "metrics.png", dpi=180)
    fig.savefig(
        folder / "metrics.pdf", metadata={"CreationDate": None, "ModDate": None}
    )
    plt.close(fig)
    fig, axis = plt.subplots(figsize=(12, 3))
    axis.axis("off")
    stages = [
        "C++ 원본",
        "경유 언어 번역\n기능 검사",
        "C++ 복원\n기능 검사",
        "2홉 최초 비교\nJPlag 인접 유사도",
        "10홉 판정 완료\n임계치별 결과 동결",
        "다음 왕복 확인\n최대 12홉",
    ]
    for index, text in enumerate(stages):
        x = 0.085 + index * 0.166
        axis.text(
            x,
            0.5,
            text,
            ha="center",
            va="center",
            fontsize=8,
            bbox={"boxstyle": "round", "facecolor": "#edf3f9", "edgecolor": "#607d8b"},
            transform=axis.transAxes,
        )
        if index < len(stages) - 1:
            axis.annotate(
                "",
                xy=(x + 0.099, 0.5),
                xytext=(x + 0.068, 0.5),
                xycoords="axes fraction",
                arrowprops={"arrowstyle": "->"},
            )
    fig.tight_layout()
    fig.savefig(folder / "protocol.png", dpi=180)
    fig.savefig(
        folder / "protocol.pdf", metadata={"CreationDate": None, "ModDate": None}
    )
    plt.close(fig)


def _bundle(summary, destination):
    bundle = destination / "reproducibility_bundle"
    bundle.mkdir(exist_ok=True)
    _json(bundle / "observations.json", summary["observations"])
    _json(bundle / "contract.json", summary["contract"])
    _json(bundle / "manifest.json", summary["manifest"])
    _json(bundle / "environment.json", summary["contract"].get("environment", {}))
    references = []
    candidates = {}
    step_folders = set()
    for pointer, value in _leaves(summary["observations"]):
        if not isinstance(value, str) or not pointer.rsplit("/", 1)[-1] in {
            "source_path",
            "response_path",
            "raw_response_path",
            "evaluation_path",
        }:
            continue
        source = Path(value)
        candidates.setdefault(source, pointer)
        if pointer.endswith("/source_path") and source.is_file():
            step_folders.add(source.parent)
    suffixes = {
        ".json",
        ".jsonl",
        ".txt",
        ".csv",
        ".cpp",
        ".py",
        ".java",
        ".hs",
        ".pl",
        ".md",
        ".inp",
        ".out",
        ".zip",
    }
    for step_folder in sorted(step_folders):
        for source in sorted(step_folder.rglob("*")):
            if (
                source.is_file()
                and source.suffix.lower() in suffixes
                and not source.resolve().is_relative_to(destination.resolve())
            ):
                candidates.setdefault(source, "단계 원자료")
        for name in ("contract.json", "timing.json", "observation.json"):
            source = step_folder.parent / name
            if source.is_file():
                candidates.setdefault(source, "시도 원자료")
    cfg = summary["contract"].get("config", summary["contract"])
    if cfg.get("corpus_root") and Path(cfg["corpus_root"]).is_dir():
        for source in sorted(Path(cfg["corpus_root"]).rglob("*")):
            if (
                source.is_file()
                and source.suffix.lower() in suffixes
                and not source.resolve().is_relative_to(destination.resolve())
            ):
                candidates.setdefault(source, "동결 코퍼스 원자료")
    if cfg.get("output_root") and cfg.get("campaign_id"):
        campaign = Path(cfg["output_root"]) / cfg["campaign_id"]
        phases = {r.get("phase", "main") for r in summary["observations"]}
        for phase in sorted(phases):
            for source in sorted((campaign / phase).glob("*ledger*.jsonl")):
                candidates.setdefault(source, "공급자 원장")
    for source, pointer in candidates.items():
        value = str(source)
        if not source.is_file():
            references.append(
                {
                    "field": pointer,
                    "source": value,
                    "included": False,
                    "reason": "file_not_found",
                }
            )
            continue
        name = _sha(source) + source.suffix
        target = bundle / "raw" / name
        target.parent.mkdir(exist_ok=True)
        if source.suffix.lower() == ".json":
            _json(target, public_data(_read(source)))
        elif source.suffix.lower() == ".jsonl":
            entries = [
                public_data(json.loads(line))
                for line in source.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            target.write_text(
                "".join(
                    json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n"
                    for entry in entries
                ),
                encoding="utf-8",
            )
        else:
            shutil.copyfile(source, target)
        references.append(
            {
                "field": pointer,
                "source": value,
                "included": True,
                "bundle_path": "raw/" + name,
                "original_sha256": _sha(source),
                "exported_sha256": _sha(target),
            }
        )
    _json(bundle / "raw_sources.json", references)
    source_files = {
        "hops_reporting.py": Path(__file__).resolve().parents[1]
        / "src/rttdist/hops_reporting.py",
        "report_v16.py": Path(__file__),
        "verify_v16_reproducibility.py": Path(__file__).with_name(
            "verify_v16_reproducibility.py"
        ),
    }
    for name, path in source_files.items():
        shutil.copyfile(path, bundle / name)
    for name in ("pyproject.toml", "uv.lock"):
        path = Path(__file__).resolve().parents[1] / name
        if path.exists():
            shutil.copyfile(path, bundle / name)
    (bundle / "README.md").write_text(
        "# v1.6 재현 묶음\n\n인증값을 제외한 원관측·계약·문제 목록·환경·집계 코드를 보관합니다. 원응답과 생성 코드는 raw_sources.json의 포함 여부와 해시를 확인하십시오. 이 묶음만으로는 미포함 평가 출력의 정확성을 감사했다고 볼 수 없습니다.\n\n저장소의 uv 환경에서 실행하십시오.\n\n```powershell\nuv sync --extra analysis\nuv run python scripts/report_v16.py --bundle <이_묶음_경로> --destination <출력_경로>\nuv run python scripts/verify_v16_reproducibility.py --bundle <이_묶음_경로>\n```\n",
        encoding="utf-8",
    )
    hashes = {
        str(p.relative_to(bundle)).replace("\\", "/"): _sha(p)
        for p in sorted(bundle.rglob("*"))
        if p.is_file() and p.name != "sha256.json"
    }
    _json(bundle / "sha256.json", hashes)


def write_v16_report(summary, destination):
    """표·그림·수치 문장·근거를 전달된 summary만으로 작성합니다."""
    folder = Path(destination)
    folder.mkdir(parents=True, exist_ok=True)
    summary = public_data(summary)
    _json(folder / "summary.json", summary)
    _json(folder / "model_metadata.json", summary["metadata"])
    _json(folder / "completion_audit.json", summary["audit"])
    thresholds, problems, failures, confirmations, stages, comparisons = (
        [],
        [],
        [],
        [],
        [],
        [],
    )
    similarities, calls, recursive = [], [], []
    for threshold, block in summary["by_threshold"].items():
        for route, values in block["routes"].items():
            for scope, distribution in values["similarities"].items():
                if isinstance(distribution, dict):
                    similarities.append(
                        {
                            "threshold": threshold,
                            "route": route,
                            "scope": scope,
                            **distribution,
                        }
                    )
            thresholds.append(
                {
                    "threshold": threshold,
                    "route": route,
                    **{
                        key: values[key]
                        for key in (
                            "P",
                            "H",
                            "D",
                            "planned",
                            "recorded",
                            "valid",
                            "success",
                            "invalid",
                            "incomplete",
                            "P_problem_mean",
                        )
                    },
                    "complete": block["complete"],
                    "confirmatory_eligible": block["confirmatory_eligible"],
                    "interval_use": block["interval_use"],
                }
            )
            for problem, value in values["per_problem"].items():
                problems.append(
                    {
                        "threshold": threshold,
                        "route": route,
                        "problem_id": problem,
                        **value,
                    }
                )
            for category, count in values["categories"].items():
                failures.append(
                    {
                        "threshold": threshold,
                        "route": route,
                        "category": category,
                        "count": count,
                    }
                )
            if threshold == summary["primary_threshold"]:
                calls.extend(
                    {"route": route, "phase": kind, **counts}
                    for kind, counts in values["call_accounting"].items()
                )
                confirmations.append({"route": route, **values["confirmation"]})
                stages.extend({"route": route, **s} for s in values["stage_pass_rates"])
        comparisons.extend(
            {
                "threshold": threshold,
                "confirmatory_eligible": block["confirmatory_eligible"],
                **item,
            }
            for item in (block["bootstrap"] or {}).get("comparisons", [])
        )
    for group, data in summary["recursive_groups"]["groups"].items():
        for route, values in data["routes"].items():
            recursive.append(
                {
                    "group": group,
                    "problem_count": data["problem_count"],
                    "route": route,
                    **{
                        key: values[key]
                        for key in ("valid", "success", "P", "H", "D", "categories")
                    },
                }
            )
    _csv(
        folder / "similarities.csv",
        similarities,
        ["threshold", "route", "scope", "n", "mean", "median", "q1", "q3", "values"],
    )
    _csv(
        folder / "call_usage.csv",
        calls,
        [
            "route",
            "phase",
            "logical_requests",
            "transport_attempts",
            "known_transport_attempts",
            "transport_unknown_requests",
            "retries",
            "cost_usd",
            "known_cost_usd",
        ],
    )
    _csv(
        folder / "recursive_groups.csv",
        recursive,
        [
            "group",
            "problem_count",
            "route",
            "valid",
            "success",
            "P",
            "H",
            "D",
            "categories",
        ],
    )
    _csv(
        folder / "thresholds.csv",
        thresholds,
        [
            "threshold",
            "route",
            "P",
            "H",
            "D",
            "planned",
            "recorded",
            "valid",
            "success",
            "invalid",
            "incomplete",
            "P_problem_mean",
            "complete",
            "confirmatory_eligible",
            "interval_use",
        ],
    )
    _csv(
        folder / "problems.csv",
        problems,
        ["threshold", "route", "problem_id", "valid", "success", "P", "H", "D"],
    )
    _csv(folder / "failures.csv", failures, ["threshold", "route", "category", "count"])
    _csv(
        folder / "confirmation.csv",
        confirmations,
        [
            "route",
            "primary_successes",
            "passed",
            "failed",
            "unavailable",
            "assessable",
            "retention_rate",
            "unavailable_rate",
        ],
    )
    _csv(
        folder / "stages.csv",
        stages,
        [
            "route",
            "phase",
            "step",
            "direction",
            "attempts",
            "assessable",
            "unavailable",
            "passed",
            "pass_rate",
        ],
    )
    _csv(
        folder / "comparisons.csv",
        comparisons,
        [
            "threshold",
            "left",
            "right",
            "metric",
            "difference",
            "interval",
            "missing_fraction",
            "interval_reason",
            "interval_kind",
            "confidence_level",
            "confirmatory_eligible",
        ],
    )
    _csv(
        folder / "code_annotations.csv",
        summary["code_annotations"],
        [
            "problem_id",
            "route",
            "attempt",
            "step",
            "source_sha256",
            "source_path",
            "evidence_location",
            "recursive",
            "accumulator",
            "list_processing",
            "explicit_state",
            "automatic_result",
            "review_result",
        ],
    )
    observations = []
    for record in summary["observations"]:
        for threshold, outcome in record["outcomes"].items():
            observations.append(
                {
                    "problem_id": record["problem_id"],
                    "route": record["route"],
                    "attempt": record.get("attempt", record.get("repeat")),
                    "threshold": threshold,
                    **outcome,
                    "confirmation_status": record.get("confirmation_status"),
                    "terminal_status": record.get("terminal_status"),
                    "translation_steps": record.get("translation_steps"),
                }
            )
    _csv(
        folder / "observations.csv",
        observations,
        [
            "problem_id",
            "route",
            "attempt",
            "threshold",
            "success",
            "category",
            "reached_step",
            "reached_roundtrip",
            "unique_state_count_at_reach",
            "sym_adj",
            "sym_origin",
            "reason",
            "confirmation_status",
            "terminal_status",
            "translation_steps",
        ],
    )
    lines = [
        "# v1.6 홉 기반 결과",
        "",
        summary["interpretation"],
        "",
        "이 보고서는 저장된 관측을 재집계합니다. 보고서 생성 자체는 라이브 실험 수행이나 원자료의 실행 감사를 의미하지 않습니다.",
        "",
        f"모델 표시명: {summary['metadata']['model'].get('display_name') or summary['metadata']['model'].get('model') or '미확인'}; 요청 모델 ID: {summary['metadata']['model'].get('model') or '미확인'}; 실제 응답 ID: {', '.join(summary['metadata']['actual_models']) or '미확인'}. 별칭 허용 목록과 단계별 근거는 model_metadata.json을 확인하십시오.",
        "",
        "| 경로 | 성공/유효 | P | H | D |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for route, values in summary["routes"].items():
        lines.append(
            f"| {route} | {values['success']}/{values['valid']} | {_display(values['P'])} | {_display(values['H'])} | {_display(values['D'])} |"
        )
    lines.extend(
        [
            "",
            "H는 성공 시도의 reached_step 평균이고 P는 유효 시도 중 도달 비율이며 D=H/P입니다. 고유 상태 수와 전체 호출 수는 H에 사용하지 않습니다. 성공이 없으면 H·D는 결측입니다.",
            "",
            "각 표의 분모·임계치별 완전성은 thresholds.csv, 확인 분모는 confirmation.csv, 방향·탐색/확인 구분은 stages.csv를 확인하십시오.",
            "",
            "주 임계치에서 완전한 직접 API 실행만 15문제 블록 10,000회 재표집과 6쌍×3지표 Bonferroni 18비교 구간을 사용합니다. 0.80·0.90 구간은 미보정 기술통계이며 불완전 자료와 SDK 탐색 결과도 확증에서 제외합니다. 재표집 결측 비율이 양수이면 해당 무조건부 구간과 전체 순위를 산출하지 않습니다.",
            "",
            f"전체 예상 D 순위의 통계적 지지 여부: {summary['ranking']['full_order_supported']}. 불확실한 인접 쌍은 summary.json의 ranking.uncertain_adjacent_pairs를 확인하십시오.",
            "",
            "원본 대비 유사도 중앙값은 주 임계치 성공 시도마다 도달 시점 값 1개를 사용하며 결측을 제외한 실제 표본 수를 함께 공개합니다. 전체 단계 유사도는 오래 진행한 시도의 가중 효과가 있는 보조 기술통계입니다.",
            "",
            summary["recursive_groups"]["interpretation"],
        ]
    )
    baseline = summary["routes"].get("cpp-via-python")
    if baseline:
        for route, values in summary["routes"].items():
            if route == "cpp-via-python":
                continue
            if baseline["D"] and values["D"] is not None:
                lines.append(
                    f"\n{route}의 관측 D는 Python 경로 대비 {values['D'] / baseline['D']:.1f}배입니다."
                )
            if baseline["P"] is not None and values["P"] is not None:
                lines.append(
                    f"\n{route}의 도달률 차이는 Python 경로 대비 {(values['P'] - baseline['P']) * 100:+.1f}%p입니다."
                )
    lines.extend(
        [
            "",
            "v1.5와 v1.6은 코퍼스와 중단 규칙이 달라 합산하거나 직접 개선율로 해석하지 않습니다. 원자료 없는 과거 수치는 검증 완료로 표시하지 않습니다.",
            "",
            "수치 근거는 evidence.json의 summary 필드 경로와 자료 해시를 따릅니다. 코드 특성 CSV의 자동·검토 결과는 별도이며 검토 전에는 미확인으로 남깁니다.",
        ]
    )
    (folder / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    fields = {
        path: {"value": value, "data_hashes": summary["data_hashes"]}
        for path, value in _leaves(summary)
        if isinstance(value, (int, float)) and not isinstance(value, bool)
    }
    _json(
        folder / "evidence.json",
        {
            "summary_sha256": _sha(folder / "summary.json"),
            "fields": fields,
            "table_sources": {
                "thresholds.csv": "/by_threshold",
                "problems.csv": "/by_threshold/*/routes/*/per_problem",
                "failures.csv": "/by_threshold/*/routes/*/categories",
                "confirmation.csv": "/routes/*/confirmation",
                "stages.csv": "/routes/*/stage_pass_rates",
                "call_usage.csv": "/routes/*/call_accounting",
                "similarities.csv": "/by_threshold/*/routes/*/similarities",
                "recursive_groups.csv": "/recursive_groups/groups",
                "comparisons.csv": "/by_threshold/*/bootstrap/comparisons",
                "figure_inputs.csv": "/routes",
                "observations.csv": "/observations",
                "code_annotations.csv": "/code_annotations",
            },
            "prose_formulas": {
                "D_ratio": "/routes/{route}/D / /routes/cpp-via-python/D",
                "P_difference_pp": "100 * (/routes/{route}/P - /routes/cpp-via-python/P)",
            },
        },
    )
    _figures(summary, folder)
    _bundle(summary, folder)
    return {
        "destination": str(folder),
        "summary_sha256": _sha(folder / "summary.json"),
        "csv_sha256": {p.name: _sha(p) for p in sorted(folder.glob("*.csv"))},
    }


def load_report_inputs(config, provider_config=None, phase="main"):
    if isinstance(config, dict) and all(
        k in config for k in ("records", "manifest", "contract")
    ):
        return config
    from rttdist.hops_experiment import load_hops_config

    cfg = (
        config
        if isinstance(config, dict)
        else load_hops_config(config, provider_config)
    )
    root = Path(cfg["output_root"]) / cfg["campaign_id"] / phase
    candidates = [
        root / "run_contract.json",
        root / "contract.json",
        root.parent / "run_contract.json",
        root.parent / "contract.json",
    ]
    path = next((p for p in candidates if p.is_file()), None)
    if path is None:
        raise FileNotFoundError("동결 실행 계약을 찾을 수 없습니다: " + str(root))
    contract = _read(path)
    manifest = _read(cfg["selection"]) if cfg.get("selection") else contract["manifest"]
    records = [_read(p) for p in sorted(root.glob("**/observation.json"))]
    if phase == "pilot":
        contract = json.loads(json.dumps(contract))
        settings = contract.get("config", contract)
        settings["problem_ids"] = cfg["pilot_problem_ids"]
        settings["repeats"] = cfg.get("pilot_repeats", 1)
        contract.update(
            problem_ids=cfg["pilot_problem_ids"], repeats=cfg.get("pilot_repeats", 1)
        )
    return {
        "records": records,
        "manifest": manifest,
        "contract": contract,
        "report_destination": str(root / "report"),
    }


def load_bundle(path):
    root = Path(path)
    return {
        "records": _read(root / "observations.json"),
        "manifest": _read(root / "manifest.json"),
        "contract": _read(root / "contract.json"),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/v1.6/experiment.yaml")
    parser.add_argument("--provider-config")
    parser.add_argument("--phase", choices=["pilot", "main"], default="main")
    parser.add_argument("--destination")
    parser.add_argument("--bundle")
    args = parser.parse_args()
    data = (
        load_bundle(args.bundle)
        if args.bundle
        else load_report_inputs(args.config, args.provider_config, args.phase)
    )
    summary = summarize_hops(data["records"], data["manifest"], data["contract"])
    destination = args.destination or data.get(
        "report_destination", "artifacts-rtt-v1.6/rebuilt-report"
    )
    write_v16_report(summary, destination)
    print("v1.6 보고서를 작성했습니다:", destination)


if __name__ == "__main__":
    main()
