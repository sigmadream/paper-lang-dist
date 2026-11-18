"""승인된 유료 래퍼 한 번을 실행하고 단계 근거를 조정자께 전달합니다."""

import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
OUTPUT = ROOT / "artifacts-rtt-v1.6/live-ds41f-20261118"
ORCA = "C:/Users/sigma/AppData/Local/Programs/orca/resources/bin/orca.exe"
COMMAND = [
    "uv",
    "run",
    "--env-file",
    "C:/Users/sigma/works/paper-lang-dist/.env",
    "--no-sync",
    "python",
    "scripts/run_deepseek_v41_flash_20261118.py",
    "--run",
    "--review-evidence",
    "artifacts-rtt-v1.6/live-ds41f-20261118/independent-review.json",
]


def now():
    return datetime.now(timezone.utc).isoformat()


def save(path, value):
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def relay(event):
    kind = event["event"]
    title = {
        "preflight_complete": "Flash 독립 사전 점검 통과",
        "pilot_complete": "Flash 파일럿 12슬롯 완료",
        "freeze_complete": "Flash 본 실험 동결 완료",
        "main_milestone": "Flash 본 실험 슬롯 이정표",
        "report_complete": "Flash 공식 보고·재현 완료",
        "execution_blocked": "Flash 실행 중지·감사 진행",
    }[kind]
    body = (
        "실제 래퍼 단계 기록입니다. 근거 루트는 artifacts-rtt-v1.6/live-ds41f-20261118이며 progress.jsonl·run.log 및 해당 단계의 원장·감사를 보존합니다. "
        + json.dumps(event, ensure_ascii=False)
    )
    result = subprocess.run(
        [
            ORCA,
            "orchestration",
            "send",
            "--from",
            "orca_session_id:c31b6f22-31ba-4537-96bb-7e5799e46a0f",
            "--type",
            "status",
            "--subject",
            title,
            "--body",
            body,
            "--task-id",
            "task_ba60a9c8ef8c",
            "--dispatch-id",
            "ctx_a080aff0e43a",
        ],
        capture_output=True,
        timeout=45,
    )
    record = {
        "at": now(),
        "event": event,
        "relay_exitcode": result.returncode,
        "stdout": result.stdout.decode("utf-8", errors="replace"),
        "stderr": result.stderr.decode("utf-8", errors="replace"),
    }
    with (OUTPUT / "조정자-단계보고.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(json.dumps(record, ensure_ascii=False), flush=True)


assert not (OUTPUT / "execution-session.json").exists(), "자동 재시작을 금지합니다"
assert not (OUTPUT / "run.log").exists(), "기존 실행 로그를 덮어쓰지 않습니다"
session = {
    "started_at": now(),
    "command": COMMAND,
    "paid_wrapper_launches": 1,
    "automatic_restarts": 0,
}
save(OUTPUT / "execution-session.json", session)
position = (OUTPUT / "progress.jsonl").stat().st_size
with (OUTPUT / "run.log").open("xb") as log:
    child = subprocess.Popen(COMMAND, stdout=log, stderr=subprocess.STDOUT)
    session["uv_pid"] = child.pid
    save(OUTPUT / "execution-session.json", session)
    print(json.dumps(session, ensure_ascii=False), flush=True)
    heartbeat = time.monotonic()
    while True:
        try:
            with (OUTPUT / "progress.jsonl").open("r", encoding="utf-8") as stream:
                stream.seek(position)
                lines = stream.readlines()
                position = stream.tell()
            for line in lines:
                event = json.loads(line)
                if event["event"] in {
                    "preflight_complete",
                    "pilot_complete",
                    "freeze_complete",
                    "main_milestone",
                    "report_complete",
                    "execution_blocked",
                }:
                    relay(event)
            if time.monotonic() - heartbeat >= 50:
                status = json.loads(
                    (OUTPUT / "status.json").read_text(encoding="utf-8")
                )
                print(
                    json.dumps(
                        {"at": now(), "supervised_pid": child.pid, "status": status},
                        ensure_ascii=False,
                    ),
                    flush=True,
                )
                heartbeat = time.monotonic()
        except Exception as exc:
            print(
                json.dumps(
                    {"at": now(), "monitor_exception_type": type(exc).__name__},
                    ensure_ascii=False,
                ),
                flush=True,
            )
        if child.poll() is not None:
            break
        time.sleep(1)
exitcode = child.wait()
(OUTPUT / "run.exitcode").write_text(str(exitcode) + "\n", encoding="utf-8")
session.update({"finished_at": now(), "wrapper_exitcode": exitcode})
save(OUTPUT / "execution-session.json", session)
print(json.dumps(session, ensure_ascii=False), flush=True)
raise SystemExit(exitcode)
