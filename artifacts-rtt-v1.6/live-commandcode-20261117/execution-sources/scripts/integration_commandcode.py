"""두 모델의 제한된 실접속·왕복 번역을 본 실험과 분리해 점검합니다."""

import argparse
from contextlib import contextmanager
from copy import deepcopy
import json
import os
from pathlib import Path
import sys
from urllib import request

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rttdist.experiment_io import digest, read_json, timestamp, write_json
from rttdist.extract import extract_single_file_source_text, SourceExtractionError
from rttdist.fps_execution import evaluate, EXTENSIONS
from rttdist.fps_experiment import SYSTEM
from rttdist.providers import (
    create_provider,
    ProviderError,
    UnknownRequestState,
    file_lock,
)

MODEL_IDS = {"zai-org/GLM-5.3", "deepseek/deepseek-v4-pro"}
DEFAULT_CONFIGS = [
    ROOT / "configs/v1.6/providers/commandcode_glm53.yaml",
    ROOT / "configs/v1.6/providers/commandcode_deepseek_v4_pro.yaml",
]
CATALOG_URL = "https://api.commandcode.ai/provider/v1/models"


def validate_smoke_config(config):
    if config.get("model") not in MODEL_IDS:
        raise ValueError("승인한 두 모델의 정확한 ID만 허용합니다")
    if (
        config.get("base_url") != "https://api.commandcode.ai/provider/v1"
        or config.get("protocol") != "chat_completions"
    ):
        raise ValueError("공식 Command Code Chat Completions 주소만 허용합니다")
    if (
        config.get("retries") != 0
        or not 1 <= config.get("max_calls", 0) <= 6
        or not 1 <= config.get("max_transport_attempts", 0) <= 6
    ):
        raise ValueError("모델당 최대 6회, 재시도 0회만 허용합니다")
    if (
        not 0 < config.get("cost_cap_usd", 0) <= 1
        or not 0 < config.get("max_request_cost_usd", 0) <= 0.15
    ):
        raise ValueError("모델당 1달러와 요청당 0.15달러 예약 상한이 필요합니다")
    if config.get("generation", {}).get("max_tokens", 0) > 4096:
        raise ValueError("연동 점검의 출력 상한은 4096입니다")
    create_provider(config)


@contextmanager
def evaluation_environment():
    """생성 프로그램과 컴파일러에 인증값을 상속하지 않습니다."""
    original = dict(os.environ)
    allowed = {
        "PATH",
        "SYSTEMROOT",
        "WINDIR",
        "COMSPEC",
        "PATHEXT",
        "TEMP",
        "TMP",
        "HOME",
        "USERPROFILE",
        "APPDATA",
        "LOCALAPPDATA",
        "LANG",
        "LC_ALL",
        "PYTHONUTF8",
        "GHCUP_INSTALL_BASE_PREFIX",
    }
    isolated = {
        name: value for name, value in original.items() if name.upper() in allowed
    }
    os.environ.clear()
    os.environ.update(isolated)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(original)


def prompt(problem, source, source_language, target_language):
    samples = []
    for path in sorted((problem / "prompt_examples").glob("*.inp"))[:2]:
        samples.append(
            {
                "input": path.read_text(encoding="utf-8"),
                "output": path.with_suffix(".out").read_text(encoding="utf-8"),
            }
        )
    content = (
        f"Source language: {source_language}\nTarget language: {target_language}\nSpecification:\n"
        + (problem / "statement.md").read_text(encoding="utf-8")
        + "\nPublic examples:\n"
        + json.dumps(samples, ensure_ascii=False)
        + "\nSource code:\n"
        + source
    )
    return [{"role": "system", "content": SYSTEM}, {"role": "user", "content": content}]


def call(provider, payload, folder, token):
    # 토큰은 지정된 하위 프로세스 메모리에만 유지하고 실제 호출 동안만 환경에 둡니다.
    if "CMD_API_KEY" in os.environ:
        raise ValueError("호출 전 인증 환경 격리가 필요합니다")
    os.environ["CMD_API_KEY"] = token
    try:
        return provider.complete(payload, folder)
    finally:
        os.environ.pop("CMD_API_KEY", None)


def error_record(exc, folder):
    errors = (
        read_json(folder / "api_errors.json")
        if (folder / "api_errors.json").exists()
        else []
    )
    return {
        "status": (
            "unknown" if isinstance(exc, UnknownRequestState) else "provider_error"
        ),
        "exception_type": type(exc).__name__,
        "reason": str(exc),
        "http_status": errors[-1].get("http_status") if errors else None,
        "automatic_retry_allowed": False,
        "regeneration_performed": False,
    }


def run_model(config, folder, experiment, corpus_root, token):
    validate_smoke_config(config)
    folder = Path(folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)
    provider = create_provider(config, ledger=folder / "provider_ledger.jsonl")
    runtime = experiment["runtime"]
    report = {
        "model": config["model"],
        "phase": "integration_smoke",
        "main_reusable": False,
        "routes": [],
        "passed": False,
        "generation": config["generation"],
        "generation_profile": config["generation_profile"],
    }
    preflight_folder = folder / "preflight"
    payload = {
        "messages": [
            {"role": "user", "content": "Return exactly OK, with no additional text."}
        ],
        "generation": {"max_tokens": 1024},
        "logical_request": {
            "campaign": "commandcode-integration-20261117",
            "phase": "integration_smoke",
            "problem": "authentication",
            "route": "preflight",
            "repeat": 1,
            "step": 0,
        },
    }
    try:
        response = call(provider, payload, preflight_folder, token)
        report["preflight"] = {
            key: response.get(key)
            for key in (
                "requested_model",
                "actual_model",
                "model_evidence",
                "finish_reason",
                "usage",
                "usage_raw",
                "cost_usd",
                "cost_source",
                "request_id",
                "requested_generation",
                "sent_generation",
                "effective_generation",
                "raw_response_path",
            )
        }
        report["preflight"]["ok"] = response["text"].strip() == "OK"
        write_json(folder / "result.json", report)
        print(
            json.dumps(
                {
                    "model": config["model"],
                    "stage": "preflight",
                    "ok": report["preflight"]["ok"],
                    "actual_model": response.get("actual_model"),
                    "model_evidence": response.get("model_evidence"),
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
        if not report["preflight"]["ok"]:
            report["reason"] = "인증 응답은 수신했으나 OK 형식을 충족하지 못했습니다"
            return report
    except (ProviderError, ValueError) as exc:
        report["preflight"] = error_record(exc, preflight_folder)
        write_json(folder / "result.json", report)
        print(
            json.dumps(
                {"model": config["model"], "stage": "preflight", **report["preflight"]},
                ensure_ascii=False,
            ),
            flush=True,
        )
        return report
    for problem_id, language in (("LC_0053", "python"), ("IPOP_1992", "haskell")):
        problem = Path(corpus_root) / problem_id
        current = (problem / "reference.cpp").read_text(encoding="utf-8")
        route = {
            "problem_id": problem_id,
            "route": "cpp-via-" + language,
            "passed": False,
            "steps": [],
        }
        for number, target_language in ((1, language), (2, "cpp")):
            step_folder = folder / problem_id / f"step-{number:02}"
            source_language = "cpp" if number == 1 else language
            payload = {
                "messages": prompt(problem, current, source_language, target_language),
                "logical_request": {
                    "campaign": "commandcode-integration-20261117",
                    "phase": "integration_smoke",
                    "problem": problem_id,
                    "route": route["route"],
                    "repeat": 1,
                    "step": number,
                },
            }
            try:
                response = call(provider, payload, step_folder, token)
                if response.get("finish_reason") in (
                    "length",
                    "max_tokens",
                    "max_output_tokens",
                ):
                    raise SourceExtractionError("출력이 잘렸습니다")
                source = extract_single_file_source_text(
                    response["text"], preserve_unfenced=True
                )
                source_path = step_folder / ("source." + EXTENSIONS[target_language])
                source_path.parent.mkdir(parents=True, exist_ok=True)
                source_path.write_text(source, encoding="utf-8", newline="")
                with evaluation_environment():
                    evaluation = evaluate(
                        source,
                        target_language,
                        problem,
                        step_folder / "evaluation",
                        runtime,
                    )
                step = {
                    key: response.get(key)
                    for key in (
                        "requested_model",
                        "actual_model",
                        "model_evidence",
                        "finish_reason",
                        "usage",
                        "usage_raw",
                        "cost_usd",
                        "cost_source",
                        "request_id",
                        "requested_generation",
                        "sent_generation",
                        "effective_generation",
                        "raw_response_path",
                        "latency_seconds",
                    )
                }
                step.update(
                    {
                        "step": number,
                        "language": target_language,
                        "source_path": str(source_path),
                        "source_sha256": digest(source.encode("utf-8")),
                        "evaluation_status": evaluation["status"],
                        "passed_cases": sum(
                            case["status"] == "success" for case in evaluation["cases"]
                        ),
                        "case_count": len(evaluation["cases"]),
                        "evaluation_path": str(
                            step_folder / "evaluation" / "evaluation.json"
                        ),
                    }
                )
                route["steps"].append(step)
                print(
                    json.dumps(
                        {
                            "model": config["model"],
                            "problem": problem_id,
                            "language": target_language,
                            "status": step["evaluation_status"],
                            "passed_cases": step["passed_cases"],
                            "case_count": step["case_count"],
                        },
                        ensure_ascii=False,
                    ),
                    flush=True,
                )
                if evaluation["status"] != "success" or step["passed_cases"] != 13:
                    route["reason"] = "생성물의 13개 기능 평가를 통과하지 못했습니다"
                    break
                current = source
                if number == 2:
                    route["passed"] = True
            except (ProviderError, ValueError, SourceExtractionError) as exc:
                route["steps"].append(
                    {
                        "step": number,
                        "language": target_language,
                        **error_record(exc, step_folder),
                    }
                )
                route["reason"] = "추가 생성 없이 해당 왕복 점검을 중단했습니다"
                break
        report["routes"].append(route)
        write_json(folder / "result.json", report)
    report["passed"] = len(report["routes"]) == 2 and all(
        route["passed"] for route in report["routes"]
    )
    write_json(folder / "result.json", report)
    return report


def fetch_catalog(folder):
    query = request.Request(CATALOG_URL, headers={"User-Agent": "rttdist/2.0"})
    with request.urlopen(query, timeout=30) as response:
        catalog = json.loads(response.read())
    selected = [model for model in catalog["data"] if model.get("id") in MODEL_IDS]
    if {model["id"] for model in selected} != MODEL_IDS or any(
        "/chat/completions" not in model.get("supported_endpoints", [])
        for model in selected
    ):
        raise ValueError(
            "공식 모델 목록에서 두 모델과 Chat Completions를 확인하지 못했습니다"
        )
    write_json(
        folder / "catalog.json",
        {"source": CATALOG_URL, "checked_at": timestamp(), "models": selected},
    )
    return selected


def summarize(root, results):
    summary = {
        "phase": "integration_smoke",
        "main_reusable": False,
        "models": results,
        "known_cost_usd": 0,
        "logical_requests": 0,
        "transport_attempts": 0,
        "unknown_cost_requests": 0,
        "passed": all(result["passed"] for result in results) and len(results) == 2,
    }
    for state_path in root.glob("*/provider_ledger.jsonl.state.json"):
        state = read_json(state_path)
        summary["logical_requests"] += len(state["requests"])
        summary["transport_attempts"] += len(state["attempts"])
        summary["known_cost_usd"] += sum(
            item.get("cost_usd") or 0 for item in state["requests"].values()
        )
        summary["unknown_cost_requests"] += sum(
            item.get("cost_usd") is None for item in state["requests"].values()
        )
    write_json(root / "summary.json", summary)
    return summary


def secret_audit(root, token):
    """토큰보다 작은 잠금 파일은 읽지 않고 저장 파일의 토큰 유출을 검사합니다."""
    encoded = token.encode()
    for path in Path(root).rglob("*"):
        if not path.is_file() or path.stat().st_size < len(encoded):
            continue
        if encoded in path.read_bytes():
            return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description="모델별 최대 6회의 별도 실제 연동 점검"
    )
    parser.add_argument("--config", default=str(ROOT / "configs/v1.6/experiment.yaml"))
    parser.add_argument(
        "--output", default=str(ROOT / "artifacts-rtt-v1.6/integration-commandcode")
    )
    parser.add_argument(
        "--model", choices=["glm53", "deepseek_v4_pro", "all"], default="all"
    )
    args = parser.parse_args()
    root = Path(args.output).resolve()
    root.mkdir(parents=True, exist_ok=True)
    token = os.environ.pop("CMD_API_KEY", None)
    if not token:
        raise SystemExit("지정한 하위 프로세스에 CMD_API_KEY가 필요합니다")
    experiment = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    corpus_root = (
        Path(args.config).resolve().parent / experiment["corpus_root"]
    ).resolve()
    config_paths = (
        DEFAULT_CONFIGS
        if args.model == "all"
        else [DEFAULT_CONFIGS[0 if args.model == "glm53" else 1]]
    )
    configs = [
        yaml.safe_load(path.read_text(encoding="utf-8")) for path in config_paths
    ]
    for config in configs:
        validate_smoke_config(config)
    if (
        sum(
            yaml.safe_load(path.read_text(encoding="utf-8"))["cost_cap_usd"]
            for path in DEFAULT_CONFIGS
        )
        > 2
    ):
        raise SystemExit("두 모델 합계 2달러 상한을 초과했습니다")
    fetch_catalog(root)
    with file_lock(root / "integration.lock", blocking=False):
        for config in configs:
            model_folder = root / (
                "glm53" if config["model"] == "zai-org/GLM-5.3" else "deepseek_v4_pro"
            )
            contract_path = model_folder / "smoke_contract.json"
            contract = {
                "phase": "integration_smoke",
                "main_reusable": False,
                "provider": config,
                "runtime": experiment["runtime"],
                "problems": ["LC_0053", "IPOP_1992"],
                "routes": ["cpp-via-python", "cpp-via-haskell"],
                "maximum_logical_requests": 6,
                "maximum_transport_attempts": 6,
            }
            if contract_path.exists() and read_json(contract_path) != contract:
                raise SystemExit(
                    "저장된 연동 점검 계약이 다릅니다. 기존 요청을 재생성하지 않습니다"
                )
            write_json(contract_path, contract)
            run_model(config, model_folder, experiment, corpus_root, token)
        results = [read_json(path) for path in sorted(root.glob("*/result.json"))]
        summary = summarize(root, results)
        summary["secret_audit_passed"] = secret_audit(root, token)
        write_json(root / "summary.json", summary)
        print(
            json.dumps(
                {
                    key: summary[key]
                    for key in (
                        "phase",
                        "passed",
                        "logical_requests",
                        "transport_attempts",
                        "known_cost_usd",
                        "unknown_cost_requests",
                        "secret_audit_passed",
                    )
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
    return 0 if summary["passed"] and summary["secret_audit_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
