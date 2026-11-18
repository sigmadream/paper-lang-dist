"""Flash 준비의 실제 관문·잠금·경로·기존 불변을 오프라인 검증합니다."""

import hashlib
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path.cwd() / "src"))

from scripts import run_deepseek_v41_flash_20261118 as runner


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


output = runner.OUTPUT
baseline = runner.read_json(output / "기존-보존기준.json")


def check(item):
    name, expected = item
    path = runner.ROOT / name
    return name if not path.is_file() or sha(path) != expected else None


with ThreadPoolExecutor(max_workers=12) as pool:
    differences = [p for p in pool.map(check, baseline["hashes"].items()) if p]
assert not differences, differences
runner.write_json(
    output / "기존-불변검증.json",
    {
        "at": runner.timestamp(),
        "baseline_sha256": sha(output / "기존-보존기준.json"),
        "checked_files": len(baseline["hashes"]),
        "differences": differences,
        "passed": not differences,
    },
)

with (
    runner.clean_execution_environment(),
    patch("socket.getaddrinfo", side_effect=AssertionError("DNS 금지")),
    patch("socket.socket.connect", side_effect=AssertionError("네트워크 금지")),
):
    manifest = runner.assert_sources()
    cfg = runner.load_config()
    runner.assert_live_date()
    runner.assert_no_unknown_requests()
    contract = runner.core.build_run_contract(
        cfg,
        runner.core._validated_inputs(cfg, runner.read_json(cfg["validation"])),
        runner.core.collect_hops_environment(cfg),
    )
    assert contract["contract_hash"] == manifest["proposed_contract_hash"]
    assert len(runner.core.build_hops_schedule(cfg, "pilot")) == 12
    assert len(runner.core.build_hops_schedule(cfg, "main")) == 300
    for previous in (
        runner.ROOT
        / "artifacts-rtt-v1.6/live-deepseek-20261118/independent-review.json",
        None,
    ):
        try:
            runner.require_review(previous)
        except ValueError:
            pass
        else:
            raise AssertionError("신규 실제 독립 검토 없이 관문을 통과하였습니다")
    lock = output / "execution.lock"
    code = (
        "from rttdist.providers import file_lock, UnknownRequestState\n"
        "from pathlib import Path\n"
        "import sys\n"
        "try:\n"
        "    with file_lock(Path(sys.argv[1]), blocking=False):\n"
        "        raise SystemExit(9)\n"
        "except UnknownRequestState:\n"
        "    print('단일 잠금이 중복 프로세스를 차단하였습니다')\n"
    )
    with runner.file_lock(lock, blocking=False):
        child = subprocess.run(
            [sys.executable, "-c", code, str(lock)],
            capture_output=True,
            timeout=30,
            env={**__import__("os").environ, "PYTHONPATH": str(runner.ROOT / "src")},
        )
        assert child.returncode == 0, child.stderr.decode(errors="replace")

    campaign = output / runner.CAMPAIGN_ID
    assert not campaign.exists()
    longest_call_lock = (
        campaign / "preflight/provider_ledger.jsonl.calls" / ("f" * 64 + ".lock")
    )
    assert len(str(longest_call_lock)) < 260
    with runner.file_lock(longest_call_lock, blocking=False):
        assert longest_call_lock.is_file()
    longest_call_lock.unlink()
    for directory in (
        longest_call_lock.parent,
        longest_call_lock.parent.parent,
        campaign,
    ):
        directory.rmdir()

    remapped = []
    for name in baseline["hashes"]:
        for prior_root, prior_campaign in (
            ("live-commandcode-20261117", "commandcode-glm53-v16-20261117"),
            ("live-deepseek-20261118", "commandcode-deepseek_v4_pro-v16-20261118"),
        ):
            prefix = "artifacts-rtt-v1.6/" + prior_root + "/" + prior_campaign + "/"
            if name.startswith(prefix):
                remapped.append(campaign / name.removeprefix(prefix))
    longest = max(remapped, key=lambda p: len(str(p)))
    assert len(str(longest)) < 260, str(longest)

result = {
    "at": runner.timestamp(),
    "passed": True,
    "live_api_calls": 0,
    "credentials_read": False,
    "source_files": len(manifest["files"]),
    "legacy_protected_files": len(manifest["legacy_hashes"]),
    "baseline_files_unchanged": len(baseline["hashes"]),
    "prepared_manifest_sha256": sha(output / "source-manifest.json"),
    "proposed_contract_hash": contract["contract_hash"],
    "prior_review_rejected": True,
    "missing_review_rejected": True,
    "separate_process_lock_blocked": True,
    "lock_child_stdout": child.stdout.decode("utf-8", errors="replace"),
    "lock_child_exitcode": child.returncode,
    "actual_call_lock_path_length": len(str(longest_call_lock)),
    "longest_remapped_collected_or_report_path_length": len(str(longest)),
    "longest_remapped_path": str(longest),
    "windows_260_character_bound_passed": True,
    "live_campaign_directory_exists": campaign.exists(),
    "new_independent_review_received": False,
    "budget": runner.prior_budget_evidence(),
}
runner.write_json(output / "오프라인-관문검증.json", result)
print(json.dumps(result, ensure_ascii=False))
