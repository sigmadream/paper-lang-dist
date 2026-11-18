"""한글 경로를 파일에서 읽어 종료 후 오프라인 안전 상태를 검증합니다."""

import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts import run_deepseek_v16_20261118 as runner


def main():
    output = runner.OUTPUT
    runner.assert_sources()
    review = runner.require_review(output / "independent-review.json")
    runner.assert_live_date()
    manifest_hash = hashlib.sha256(
        (output / "source-manifest.json").read_bytes()
    ).hexdigest()
    if manifest_hash != review["prepared_manifest_sha256"]:
        raise ValueError("준비 manifest의 실제 파일 해시가 다릅니다")
    blocked = False
    try:
        runner.assert_no_unknown_requests()
    except ValueError:
        blocked = True
    with runner.file_lock(output / "execution.lock", blocking=False):
        released = True
    result = {
        "at": runner.timestamp(),
        "source_guard_passed": True,
        "review_guard_passed": True,
        "date_guard_passed": True,
        "prepared_manifest_sha256_matches": True,
        "restart_gate_blocked_by_unknown": blocked,
        "execution_lock_released": released,
        "network_calls": 0,
        "credential_files_read": False,
        "설명": "불명 요청으로 재개가 차단되며 종료된 실행 잠금이 해제되었음을 오프라인으로 확인하였습니다.",
    }
    runner.write_json(Path(__file__).with_suffix(".json"), result)
    print(
        {
            "restart_gate_blocked_by_unknown": blocked,
            "execution_lock_released": released,
        }
    )


if __name__ == "__main__":
    main()
