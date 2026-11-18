"""유료 호출 없이 전용 래퍼의 실제 관문과 보존 해시를 확인합니다."""

import hashlib
import json
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts import run_deepseek_v16_20261118 as runner


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    output = runner.OUTPUT
    with (
        runner.clean_execution_environment(),
        patch("socket.getaddrinfo", side_effect=RuntimeError("오프라인 검증입니다")),
        patch("socket.socket.connect", side_effect=RuntimeError("오프라인 검증입니다")),
        runner.file_lock(output / "execution.lock", blocking=False),
    ):
        runner.assert_live_date()
        manifest = runner.assert_sources()
        review = runner.require_review(output / "independent-review.json")
        runner.assert_no_unknown_requests()
        config = runner.load_config()
        actual_hash = file_hash(output / "source-manifest.json")
        if actual_hash != review["prepared_manifest_sha256"]:
            raise ValueError("준비 manifest의 실제 파일 해시가 검토 근거와 다릅니다")
        if (output / runner.CAMPAIGN_ID).exists():
            raise ValueError("아직 시작하지 않은 새 캠페인이라는 전제와 다릅니다")
        result = {
            "at": runner.timestamp(),
            "passed": True,
            "설명": "인증값을 읽지 않고 네트워크를 차단한 상태에서 실제 실행 관문을 통과하였습니다.",
            "gates": [
                "assert_sources",
                "require_review",
                "assert_live_date",
                "assert_no_unknown_requests",
                "load_config",
                "execution.lock",
                "prepared_manifest_sha256",
            ],
            "prepared_manifest_sha256": actual_hash,
            "source_files": len(manifest["files"]),
            "legacy_files": len(manifest["legacy_hashes"]),
            "legacy_hashes": manifest["legacy_hashes"],
            "review_sha256": file_hash(output / "independent-review.json"),
            "review_report_sha256": review["report_sha256"],
            "campaign_id": config["campaign_id"],
            "phase_budget_policy": runner.PHASES,
            "campaign_absent_before_run": True,
            "network_calls": 0,
        }
        runner.write_json(output / "실행전-관문검증.json", result)
    print(
        json.dumps(
            {
                "passed": True,
                "source_files": result["source_files"],
                "legacy_files": result["legacy_files"],
                "manifest_sha256": actual_hash,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
