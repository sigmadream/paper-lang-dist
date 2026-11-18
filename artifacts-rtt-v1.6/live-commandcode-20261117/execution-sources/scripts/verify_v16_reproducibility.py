"""외부 호출을 차단하고 v1.6 보고 수치의 재현성을 검증합니다."""

import argparse
from contextlib import contextmanager, ExitStack
import hashlib
import importlib.abc
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

from rttdist.hops_reporting import summarize_hops

if __package__:
    from scripts.report_v16 import load_bundle, load_report_inputs, write_v16_report
else:
    from report_v16 import load_bundle, load_report_inputs, write_v16_report


SDK_PREFIXES = (
    "copilot",
    "github_copilot",
    "openai",
    "anthropic",
    "litellm",
    "rttdist.copilot_provider",
    "rttdist.providers",
    "rttdist.provider_protocols",
)


class _BlockSdkImport(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if any(
            fullname == name or fullname.startswith(name + ".") for name in SDK_PREFIXES
        ):
            raise AssertionError(
                "보고서 재생성 중 SDK 가져오기를 차단했습니다: " + fullname
            )
        return None


@contextmanager
def offline_reporting():
    """소켓·HTTP·SDK·하위 프로세스를 보고 재생성 동안 차단합니다."""
    message = "보고서 재생성 중 외부 호출을 차단했습니다."
    guard = _BlockSdkImport()
    methods = (
        "start",
        "send",
        "send_and_wait",
        "create_session",
        "complete",
        "completion",
        "create",
        "request",
        "connect",
        "invoke",
    )
    with ExitStack() as stack:
        for target in (
            "socket.create_connection",
            "socket.socket.connect",
            "socket.socket.connect_ex",
            "socket.getaddrinfo",
            "urllib.request.urlopen",
            "http.client.HTTPConnection.connect",
            "http.client.HTTPSConnection.connect",
            "subprocess.Popen",
            "os.system",
            "os.popen",
            "asyncio.create_subprocess_exec",
            "asyncio.create_subprocess_shell",
        ):
            stack.enter_context(patch(target, side_effect=AssertionError(message)))
        for name, module in list(sys.modules.items()):
            if not any(
                name == prefix or name.startswith(prefix + ".")
                for prefix in SDK_PREFIXES
            ):
                continue
            for attr, item in list(vars(module).items()):
                if isinstance(item, type):
                    for method in methods:
                        if hasattr(item, method):
                            try:
                                stack.enter_context(
                                    patch.object(
                                        item,
                                        method,
                                        side_effect=AssertionError(message),
                                    )
                                )
                            except AttributeError, TypeError:
                                pass
                elif attr in methods and callable(item):
                    stack.enter_context(
                        patch.object(module, attr, side_effect=AssertionError(message))
                    )
        sys.meta_path.insert(0, guard)
        try:
            yield
        finally:
            sys.meta_path.remove(guard)


def _snapshot(folder):
    return {
        p.name: p.read_bytes()
        for p in sorted(folder.iterdir())
        if p.suffix in (".json", ".csv") and p.name != "reproducibility.json"
    }


def verify_v16_reproducibility(config, provider_config):
    """같은 원관측에서 수치 JSON·CSV·그림 입력이 두 번 동일한지 검사합니다."""
    data = load_report_inputs(config, provider_config)
    destination = Path(
        data.get("report_destination", "artifacts-rtt-v1.6/reproducibility")
    )
    # 글꼴 탐색 도구의 초기화를 보고서 실행 구간 전에 완료합니다.
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot

    with tempfile.TemporaryDirectory(prefix="rtt-v16-reproduction-") as temporary:
        with offline_reporting():
            folders = [Path(temporary) / "first", Path(temporary) / "second"]
            for folder in folders:
                summary = summarize_hops(
                    data["records"], data["manifest"], data["contract"]
                )
                write_v16_report(summary, folder)
            first, second = [_snapshot(folder) for folder in folders]
            different = sorted(
                name
                for name in set(first) | set(second)
                if first.get(name) != second.get(name)
            )
            if different:
                raise AssertionError(
                    "두 보고서의 수치가 다릅니다: " + ", ".join(different)
                )
            # 같은 차단 구간에서 최종 출력도 다시 생성합니다.
            final = summarize_hops(data["records"], data["manifest"], data["contract"])
            write_v16_report(final, destination)
            if _snapshot(destination) != first:
                raise AssertionError(
                    "최종 보고서의 수치가 검증된 재생성 결과와 다릅니다."
                )
    result = {
        "passed": True,
        "network_disabled": True,
        "sdk_disabled": True,
        "subprocess_disabled": True,
        "summary_exactly_equal": True,
        "csv_exactly_equal": True,
        "figure_inputs_exactly_equal": True,
        "compared_files": sorted(first),
        "sha256": {
            name: hashlib.sha256(content).hexdigest() for name, content in first.items()
        },
        "excluded_from_comparison": [
            "그림 렌더링 바이트와 PDF 비수치 메타데이터",
            "재현 검증 결과 파일 자체",
        ],
        "scope": "수치 재생성의 동일성 검증이며 자료 수집의 완전성·가설 지지와 별개입니다.",
        "complete_by_threshold": final["complete_by_threshold"],
    }
    (destination / "reproducibility.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/v1.6/experiment.yaml")
    parser.add_argument("--provider-config")
    parser.add_argument("--bundle")
    parser.add_argument("--destination")
    args = parser.parse_args()
    config = load_bundle(args.bundle) if args.bundle else args.config
    if args.destination:
        config = load_report_inputs(config, args.provider_config)
        config["report_destination"] = args.destination
    result = verify_v16_reproducibility(config, args.provider_config)
    print("외부 호출 없이 수치 재현성을 검증했습니다:", result["passed"])


if __name__ == "__main__":
    main()
