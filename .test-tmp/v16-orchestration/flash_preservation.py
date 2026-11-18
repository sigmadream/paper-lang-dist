"""조정자의 main 반영을 위한 실제 보존 파일·해시 목록을 작성합니다."""

import hashlib
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
OUTPUT = ROOT / "artifacts-rtt-v1.6/live-ds41f-20261118"
assert (OUTPUT / "run.exitcode").is_file(), "실행 종료 후에만 보존 목록을 작성합니다"


def entry(path):
    return path.relative_to(ROOT).as_posix(), {
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
    }


def save(name, data):
    (OUTPUT / name).write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


auxiliary = ROOT / ".test-tmp/v16-orchestration"
required = set(auxiliary.glob("restart-review-*"))
required.update(auxiliary.glob("flash_*.py"))
required.update(auxiliary.glob("test_flash_safety.py"))
required.update((auxiliary / "flash-independent-211fed").rglob("*"))
required.update(
    auxiliary / name
    for name in (
        "deepseek-restart-final-review.md",
        "deepseek-v41-flash-task-20261118.txt",
        "deepseek-v41-flash-review-task-20261118.txt",
        "deepseek-live-resume-task-20261118.txt",
    )
)
required = sorted(p for p in required if p.is_file() and "__pycache__" not in p.parts)
records = dict(entry(p) for p in required)
save(
    "보존필수-검토참조.json",
    {
        "at": datetime.now(timezone.utc).isoformat(),
        "설명": "현재 실제 존재하는 .test-tmp 검토·검사·보조 기록의 정확한 보존 목록입니다. 실행 소스와 원자료는 변경하지 않습니다.",
        "runtime_guard_required": [
            ".test-tmp/v16-orchestration/deepseek-restart-final-review.md"
        ],
        "files": records,
        "file_count": len(records),
    },
)
exclusions = {"데이터-보존목록.json", "최종-기계검증.json"}
paths = sorted(p for p in OUTPUT.rglob("*") if p.is_file() and p.name not in exclusions)
with ThreadPoolExecutor(max_workers=12) as pool:
    records = dict(pool.map(entry, paths))
save(
    "데이터-보존목록.json",
    {
        "at": datetime.now(timezone.utc).isoformat(),
        "설명": "유료 실행·보고·재현·종료 감사 후의 신규 Flash 산출물 목록입니다. 이 목록 파일과 이를 검증하는 최종 기계검증 JSON 자체는 제외합니다.",
        "files": records,
        "file_count": len(records),
        "total_bytes": sum(v["bytes"] for v in records.values()),
        "largest_file": max(records, key=lambda n: records[n]["bytes"]),
    },
)
print(
    json.dumps(
        {
            "new_output_files": len(records),
            "new_output_bytes": sum(v["bytes"] for v in records.values()),
            "auxiliary_files": len(required),
        },
        ensure_ascii=False,
    )
)
