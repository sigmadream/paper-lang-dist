"""분할 저장한 v1.6 산출물을 SHA-256을 확인하여 원래 경로에 복원합니다."""

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile

PROJECT = Path(__file__).resolve().parents[1]
INVENTORY = PROJECT / "docs/superpowers/verification/2026-11-18-main-v16/inventory.json"


def within(root, relative):
    """저장 목록이 가리키는 상대 경로를 지정된 루트 안에서 확인합니다."""
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"허용되지 않는 경로입니다. {relative}")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError(f"저장 루트를 벗어난 경로입니다. {relative}")
    return resolved


def matches(path, expected):
    if path.stat().st_size != expected["크기"]:
        return False
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest() == expected["sha256"]


def restore(project, destination, relative, item):
    original = within(destination, relative)
    if original.exists():
        if matches(original, item["원본"]):
            return "이미 일치"
        raise ValueError(f"기존 파일의 바이트가 다릅니다. {relative}")

    original.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".v16-restore-", dir=original.parent
    ) as work:
        compressed = Path(work) / "joined.gz"
        reconstructed = Path(work) / "restored"
        with compressed.open("wb") as joined:
            for piece in item["조각"]:
                chunk = within(project, piece["경로"])
                if not matches(chunk, piece):
                    raise ValueError(
                        f"조각 해시 또는 크기 불일치입니다. {piece['경로']}"
                    )
                with chunk.open("rb") as source:
                    shutil.copyfileobj(source, joined)
        with gzip.open(compressed, "rb") as source, reconstructed.open("wb") as target:
            shutil.copyfileobj(source, target)
        if not matches(reconstructed, item["원본"]):
            raise ValueError(f"원본 해시 또는 크기 불일치입니다. {relative}")
        os.link(reconstructed, original)
    return "복원 완료"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths", nargs="*", help="생략하면 목록의 모든 산출물을 복원합니다."
    )
    parser.add_argument(
        "--destination", type=Path, default=PROJECT, help="복원 루트입니다."
    )
    args = parser.parse_args()

    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))["분할_보관"]
    for path in args.paths or sorted(inventory):
        if path not in inventory:
            parser.error(f"분할 저장 목록에 없는 경로입니다. {path}")
        print(restore(PROJECT, args.destination.resolve(), path, inventory[path]), path)


if __name__ == "__main__":
    main()
