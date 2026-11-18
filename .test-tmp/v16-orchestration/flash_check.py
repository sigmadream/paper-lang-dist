"""오프라인 검증 명령의 원출력·종료코드·해시를 보존합니다."""

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

root = Path.cwd()
output = root / "artifacts-rtt-v1.6/live-ds41f-20261118"
label = sys.argv[1]
command = sys.argv[2:]
started = datetime.now(timezone.utc).isoformat()
with (output / (label + ".log")).open("wb") as stream:
    result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT)
log = output / (label + ".log")
(output / (label + ".exitcode")).write_text(
    str(result.returncode) + "\n", encoding="utf-8"
)
record = {
    "command": command,
    "started_at": started,
    "finished_at": datetime.now(timezone.utc).isoformat(),
    "exitcode": result.returncode,
    "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest(),
}
(output / (label + ".json")).write_text(
    json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(record, ensure_ascii=False))
print(log.read_text(encoding="utf-8", errors="replace")[-6000:])
raise SystemExit(result.returncode)
