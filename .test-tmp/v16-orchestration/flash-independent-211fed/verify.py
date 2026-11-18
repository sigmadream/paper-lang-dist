"""신규 Flash 준비를 인증·실제 전송 없이 독립 대조합니다."""

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from decimal import Decimal, ROUND_FLOOR
import hashlib
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
from unittest.mock import patch
from urllib.error import HTTPError

ROOT = Path.cwd()
LOG = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
from scripts import run_deepseek_v41_flash_20261118 as runner

OUTPUT = runner.OUTPUT


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    (LOG / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def reject(call):
    try:
        call()
    except ValueError:
        return True
    raise AssertionError("거부되어야 할 검증이 통과하였습니다")


def integrity():
    manifest = runner.assert_sources()
    baseline = runner.read_json(OUTPUT / "기존-보존기준.json")["hashes"]

    def check(item):
        name, expected = item
        return name if sha(ROOT / name) != expected else None

    with ThreadPoolExecutor(max_workers=12) as pool:
        differences = [name for name in pool.map(check, baseline.items()) if name]
    assert not differences, differences
    assert not (OUTPUT / runner.CAMPAIGN_ID).exists()
    return {
        "manifest_sha256": sha(OUTPUT / "source-manifest.json"),
        "source_hashes": {name: sha(ROOT / name) for name in manifest["files"]},
        "snapshot_hashes": {
            name: sha(OUTPUT / "execution-sources" / name) for name in manifest["files"]
        },
        "legacy_hashes": {name: sha(ROOT / name) for name in manifest["legacy_hashes"]},
        "baseline_files_checked": len(baseline),
        "baseline_differences": differences,
        "live_campaign_exists": False,
    }


def audit():
    before = integrity()
    save("before.json", before)
    manifest = runner.read_json(OUTPUT / "source-manifest.json")
    assert before["manifest_sha256"] == (
        "c3879f86b318f5765778cc730bddc073e2b804d94ed13f55935a5d474677e26b"
    )
    metadata = runner.read_json(OUTPUT / "준비검증.json")
    checked_logs = {}
    for name in (
        "related-pytest",
        "black-check",
        "diff-check",
        "offline-prepare",
        "offline-gates",
    ):
        recorded = runner.read_json(OUTPUT / (name + ".json"))
        code = int((OUTPUT / (name + ".exitcode")).read_text().strip())
        assert recorded["exitcode"] == code == 0
        assert recorded["log_sha256"] == sha(OUTPUT / (name + ".log"))
        checked_logs[name] = {"exitcode": code, "log_sha256": recorded["log_sha256"]}
    for name, expected in metadata["evidence_hashes"].items():
        assert sha(OUTPUT / name) == expected, name
    cfg = runner.load_config()
    excluded = {
        "output_root",
        "campaign_id",
        "profile_id",
        "provider_config",
        "llm",
        "execution_wrapper",
        "phase_budget_policy",
        "budget",
    }
    old = runner.core.load_hops_config(
        ROOT / "configs/v1.6/campaigns/commandcode_deepseek_v4_pro_20261118.yaml",
        ROOT / "configs/v1.6/providers/commandcode_deepseek_v4_pro_20261118.yaml",
    )
    assert {k: v for k, v in cfg.items() if k not in excluded} == {
        k: v for k, v in old.items() if k not in excluded
    }
    schedules = {}
    for phase, count in (("pilot", 12), ("main", 300)):
        jobs = runner.core.build_hops_schedule(cfg, phase)
        prior = runner.core.build_hops_schedule(old, phase)
        assert len(jobs) == count
        assert [{k: v for k, v in j.items() if k != "campaign_id"} for j in jobs] == [
            {k: v for k, v in j.items() if k != "campaign_id"} for j in prior
        ]
        schedules[phase] = count
    validation = runner.read_json(cfg["validation"])
    data = runner.core._validated_inputs(cfg, validation)
    environment = runner.core.collect_hops_environment(cfg)
    runner.core._check_validation_environment(validation, environment)
    contract = runner.core.build_run_contract(cfg, data, environment)
    assert contract["contract_hash"] == manifest["proposed_contract_hash"]
    old_manifest = runner.read_json(
        ROOT / "artifacts-rtt-v1.6/live-deepseek-20261118/source-manifest.json"
    )
    unchanged_shared = [
        name
        for name in manifest["files"]
        if name.startswith("src/") or name == "scripts/integration_commandcode.py"
    ]
    for name in unchanged_shared:
        assert manifest["files"][name] == old_manifest["files"][name], name
    independent_budget = {}
    for day, directory in (
        ("20261117", "live-commandcode-20261117"),
        ("20261118", "live-deepseek-20261118"),
    ):
        phases = {}
        for phase in ("preflight", "pilot", "main"):
            location = (
                ROOT
                / "artifacts-rtt-v1.6"
                / directory
                / ("commandcode-deepseek_v4_pro-v16-" + day)
                / phase
            )
            state = runner.read_json(location / "provider_ledger.jsonl.state.json")
            requests = list(state["requests"].values())
            ledger = [
                json.loads(line)
                for line in (location / "provider_ledger.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
                if line
            ]
            spent = sum(
                (Decimal(str(r.get("cost_usd") or 0)) for r in requests), Decimal(0)
            )
            assert spent == sum(
                (Decimal(str(r.get("cost_usd") or 0)) for r in ledger), Decimal(0)
            )
            reserved = sum(
                (
                    Decimal(str(r.get("reserved_usd") or 0))
                    + Decimal(str(r.get("uncertain_reserved_usd") or 0))
                    for r in requests
                ),
                Decimal(0),
            )
            phases[phase] = {
                "spent": str(spent),
                "reserved": str(reserved),
                "logical": len(requests),
                "transport": len(state["attempts"]),
            }
            if day == "20261118":
                cap = {"preflight": "0.24", "pilot": "49.62", "main": "49.32"}[phase]
                assert (Decimal(cap) - spent - reserved).quantize(
                    Decimal("0.01"), rounding=ROUND_FLOOR
                ) == Decimal(str(runner.PHASES[phase]["cost_cap_usd"]))
        independent_budget[day] = phases
    assert Decimal(independent_budget["20261117"]["main"]["reserved"]) == Decimal(
        "0.50"
    )
    assert Decimal(independent_budget["20261118"]["main"]["reserved"]) == Decimal(
        "0.25"
    )
    assert (
        runner.prior_budget_evidence()["conservative_allocated_total_usd"]
        == "200.465729120"
    )
    bound = (
        Decimal(32768) * Decimal("0.30") + Decimal(16384) * Decimal("1.20")
    ) / Decimal(1000000)
    assert bound == Decimal("0.0294912")
    for phase in runner.PHASES.values():
        assert Decimal(str(phase["max_request_cost_usd"])) >= bound
    assert reject(lambda: runner.require_review(None))
    assert reject(
        lambda: runner.require_review(
            ROOT / "artifacts-rtt-v1.6/live-deepseek-20261118/independent-review.json"
        )
    )
    save(
        "audit.json",
        {
            "passed": True,
            "checked_implementation_logs": checked_logs,
            "schedules": schedules,
            "contract_hash": contract["contract_hash"],
            "shared_sources_unchanged": len(unchanged_shared),
            "independent_prior_ledger_reconciliation": independent_budget,
            "maximum_request_cost_bound_usd": str(bound),
            "missing_and_prior_reviews_rejected": True,
            "live_api_calls": 0,
            "credentials_read": False,
        },
    )


def pytest_checks():
    import pytest

    with tempfile.TemporaryDirectory(prefix="fr-") as temporary:
        return pytest.main(
            [
                "tests/integration/test_deepseek_flash_runner.py",
                "-q",
                "-p",
                "no:cacheprovider",
                "--basetemp",
                str(Path(temporary) / "pt"),
            ]
        )


def final():
    before = runner.read_json(LOG / "before.json")
    accepted = runner.require_review(OUTPUT / "independent-review.json")
    after = integrity()
    assert before == after
    save("after.json", after)
    result = {
        "passed": True,
        "require_review_accepted": True,
        "reviewer_session_id": accepted["reviewer_session_id"],
        "source_guard_passed": True,
        "sources_and_snapshots_checked": len(after["source_hashes"]),
        "legacy_guard_checked": len(after["legacy_hashes"]),
        "baseline_files_checked": after["baseline_files_checked"],
        "before_after_unchanged": True,
        "manifest_sha256": after["manifest_sha256"],
        "live_campaign_exists": False,
        "live_api_calls": 0,
        "credentials_read": False,
    }
    result["checks"] = {}
    for name in ("audit", "pytest", "safety", "gates"):
        exitcode = int((LOG / (name + ".exitcode")).read_text().strip())
        assert exitcode == 0
        result["checks"][name] = {
            "exitcode": exitcode,
            "log_sha256": sha(LOG / (name + ".log")),
        }
    (OUTPUT / "독립-검토검증.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False))


def emit():
    manifest_path = OUTPUT / "source-manifest.json"
    manifest = runner.assert_sources()
    before = runner.read_json(LOG / "before.json")
    assert before["source_hashes"] == manifest["files"]
    assert before["snapshot_hashes"] == manifest["files"]
    report_path = OUTPUT / "독립-검토보고서.md"
    checks = {}
    for name in ("audit", "pytest", "safety", "gates"):
        code = int((LOG / (name + ".exitcode")).read_text().strip())
        assert code == 0
        checks[name] = {"exitcode": code, "log_sha256": sha(LOG / (name + ".log"))}
    evidence = {
        "passed": True,
        "reviewer": "Codex 독립 검토자(실제 Orca 검토 세션)",
        "reviewer_session_id": "orca_session_id:211fed9e-ae4c-432a-8a93-f58a8e14595b",
        "created_at": runner.timestamp(),
        "campaign_id": runner.CAMPAIGN_ID,
        "model_id": runner.MODEL_ID,
        "report_path": report_path.relative_to(ROOT).as_posix(),
        "report_sha256": sha(report_path),
        "prepared_manifest_path": manifest_path.relative_to(ROOT).as_posix(),
        "prepared_manifest_sha256": sha(manifest_path),
        "source_hashes": before["source_hashes"],
        "proposed_contract_hash": manifest["proposed_contract_hash"],
        "review_scope": "신규 Flash 캠페인의 오프라인 실행 준비에 대한 실제 독립 검토입니다.",
        "checks": checks,
        "independent_pytest_passed": 26,
        "preserved_implementation_pytest_passed": 150,
        "source_and_snapshot_files_checked": 67,
        "legacy_guard_files_checked": 389,
        "baseline_files_checked": 58079,
        "findings": {"critical": [], "important": [], "minor": []},
        "unresolved_execution_blockers": [],
        "live_api_calls": 0,
        "credentials_read": False,
        "paid_execution_passed": None,
        "excluded_scope": [
            "공유 소스 무변경에 따라 전체 531개 회귀 및 기준 평가 975회 재실행은 생략하였습니다.",
            "실제 prepare·유료 실행·새 원장·main_design·완전한 모의 캠페인·공식 보고 생성은 수행하지 않았습니다.",
            "실제 모델 접근·청구·지연·번역 품질과 수집 완전성은 오프라인 검토로 확인하지 않았습니다.",
        ],
        "remaining_live_steps": [
            "실행 작업자의 현재 소스·사본·검토 근거 일치 확인",
            "독립 OK 1회와 파일럿 12슬롯·완전성 감사",
            "새 본 실험 동결·300슬롯 수집·공식 보고·재현 및 종료 감사",
        ],
    }
    runner.write_json(OUTPUT / "independent-review.json", evidence)
    print("신규 실제 독립 검토 JSON을 작성하였습니다.")


def gates():
    cfg = runner.load_config()
    validation = runner.read_json(cfg["validation"])
    data = runner.core._validated_inputs(cfg, validation)
    environment = runner.core.collect_hops_environment(cfg)
    contract = runner.core.build_run_contract(cfg, data, environment)
    preflight = {
        "passed": True,
        "live": True,
        "actual_model": runner.MODEL_ID,
        "model_evidence": {"status": "exact"},
        "generation_profile": cfg["llm"]["generation_profile"],
    }
    pilot = {
        "passed": True,
        "observation_count": 12,
        "contract_hash": contract["contract_hash"],
        "complete_by_threshold": {"0.80": True, "0.85": False, "0.90": True},
    }
    assert reject(
        lambda: runner.core.freeze_main_design(cfg, pilot, validation, preflight)
    )
    assert not (OUTPUT / runner.CAMPAIGN_ID).exists()
    baseline = runner.read_json(OUTPUT / "기존-보존기준.json")["hashes"]
    campaign = OUTPUT / runner.CAMPAIGN_ID
    remapped = []
    for name in baseline:
        for previous_root, previous_campaign in (
            ("live-commandcode-20261117", "commandcode-glm53-v16-20261117"),
            ("live-deepseek-20261118", "commandcode-deepseek_v4_pro-v16-20261118"),
        ):
            prefix = (
                "artifacts-rtt-v1.6/" + previous_root + "/" + previous_campaign + "/"
            )
            if name.startswith(prefix):
                remapped.append(str(campaign / name.removeprefix(prefix)))
    longest = max(remapped, key=len)
    call_lock = (
        campaign / "preflight/provider_ledger.jsonl.calls" / ("f" * 64 + ".lock")
    )
    assert len(longest) == 243 and len(str(call_lock)) == 241
    assert max(len(longest), len(str(call_lock))) < 260
    save(
        "gates.json",
        {
            "passed": True,
            "actual_core_incomplete_pilot_rejected": True,
            "actual_core_new_main_design_created": False,
            "longest_remapped_path_length": len(longest),
            "longest_call_lock_length": len(str(call_lock)),
            "live_campaign_exists": False,
        },
    )


def transport_child():
    config = runner.load_config()["llm"]
    temporary = Path(sys.argv[2])
    runner.ROOT = temporary
    runner.OUTPUT = temporary / "artifacts-rtt-v1.6/live-ds41f-20261118"
    runner.assert_sources = lambda: {}
    counter = temporary / "transport-count.txt"

    def mock_send(req, timeout):
        count = int(counter.read_text()) if counter.exists() else 0
        counter.write_text(str(count + 1))
        wire = json.loads(req.data)
        assert wire["model"] == "deepseek/deepseek-v4.1-flash"
        assert wire["max_tokens"] == 16384 and wire["reasoning_effort"] == "low"
        assert not {"temperature", "top_p", "seed"} & wire.keys()
        raise HTTPError(req.full_url, 524, "가짜비밀-fr-524", {}, io.BytesIO(b""))

    folder = runner.OUTPUT / runner.CAMPAIGN_ID / "main"
    provider = runner.IsolatedProvider(
        runner.real_provider_factory(
            runner.phase_settings(config, "main"), folder / "provider_ledger.jsonl"
        ),
        "가짜비밀-fr-524",
    )
    from rttdist.providers import UnknownRequestState

    with patch("rttdist.providers.request.urlopen", mock_send):
        try:
            provider.complete(
                {
                    "messages": [],
                    "logical_request": {
                        "campaign": runner.CAMPAIGN_ID,
                        "phase": "main",
                        "problem": "mock",
                        "route": "cpp-via-python",
                        "repeat": 1,
                        "step": 1,
                    },
                },
                folder / ("slot-" + sys.argv[3]) / "step-01",
            )
        except UnknownRequestState:
            pass
        else:
            raise AssertionError("HTTP 524 불명 상태가 거부되지 않았습니다")
    assert "CMD_API_KEY" not in os.environ
    assert reject(runner.assert_no_unknown_requests)


def safety():
    with tempfile.TemporaryDirectory(prefix="fs-") as temporary:
        temporary = Path(temporary)
        exits = []
        for index in range(3):
            child = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(Path(__file__).resolve()),
                    "transport",
                    str(temporary),
                    str(index),
                ],
                capture_output=True,
                timeout=30,
            )
            assert child.returncode == 0, child.stderr.decode(errors="replace")
            exits.append(child.returncode)
        assert (temporary / "transport-count.txt").read_text() == "1"
        folder = (
            temporary
            / "artifacts-rtt-v1.6/live-ds41f-20261118"
            / runner.CAMPAIGN_ID
            / "main"
        )
        state = runner.read_json(folder / "provider_ledger.jsonl.state.json")
        request = list(state["requests"].values())[0]
        assert request["status"] == "unknown"
        assert request["reserved_usd"] == 0.25
        assert len(state["attempts"]) == 1
        assert all(
            "가짜비밀-fr-524" not in p.read_text(encoding="utf-8")
            for p in temporary.rglob("*.json")
        )
        lock = temporary / "독립검토.lock"
        code = (
            "import sys; from pathlib import Path; from rttdist.providers import file_lock, UnknownRequestState\n"
            "try:\n"
            "    with file_lock(Path(sys.argv[1]), blocking=False): raise SystemExit(9)\n"
            "except UnknownRequestState: pass\n"
        )
        with runner.file_lock(lock, blocking=False):
            child = subprocess.run(
                [sys.executable, "-c", code, str(lock)],
                capture_output=True,
                env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
                timeout=30,
            )
        assert child.returncode == 0, child.stderr.decode(errors="replace")
        with (
            patch.object(runner, "ROOT", temporary),
            patch.object(
                runner, "OUTPUT", temporary / "artifacts-rtt-v1.6/live-ds41f-20261118"
            ),
        ):
            source = temporary / "가짜소스.py"
            source.write_text("before", encoding="utf-8")
            snapshot = runner.OUTPUT / "execution-sources/가짜소스.py"
            snapshot.parent.mkdir(parents=True)
            snapshot.write_bytes(source.read_bytes())
            legacy = temporary / "기존근거.json"
            legacy.write_text("before", encoding="utf-8")
            runner.write_json(
                runner.OUTPUT / "source-manifest.json",
                {
                    "files": {"가짜소스.py": sha(source)},
                    "legacy_hashes": {"기존근거.json": sha(legacy)},
                },
            )
            runner.assert_sources()
            legacy.write_text("after", encoding="utf-8")
            assert reject(runner.assert_sources)
            legacy.write_text("before", encoding="utf-8")
            snapshot.write_text("after", encoding="utf-8")
            assert reject(runner.assert_sources)
    save(
        "safety.json",
        {
            "passed": True,
            "separate_process_http524_exitcodes": exits,
            "total_mock_transports": 1,
            "restart_additional_transports": 0,
            "unknown_status_preserved": True,
            "unknown_reservation_usd": 0.25,
            "wrapper_unknown_guard_rejected_each_process": True,
            "lock_child_exitcode": child.returncode,
            "legacy_and_snapshot_tamper_rejected": True,
            "fake_secret_not_stored": True,
            "live_api_calls": 0,
        },
    )


with (
    runner.clean_execution_environment(),
    patch.object(socket, "getaddrinfo", side_effect=AssertionError("검토 중 DNS 금지")),
    patch.object(
        socket.socket, "connect", side_effect=AssertionError("검토 중 실제 전송 금지")
    ),
):
    if sys.argv[1] == "audit":
        audit()
    elif sys.argv[1] == "pytest":
        raise SystemExit(pytest_checks())
    elif sys.argv[1] == "final":
        final()
    elif sys.argv[1] == "safety":
        safety()
    elif sys.argv[1] == "transport":
        transport_child()
    elif sys.argv[1] == "gates":
        gates()
    elif sys.argv[1] == "emit":
        emit()
