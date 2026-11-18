"""동결 설정을 사용하는 검사에 현재 체크아웃의 출력 경로를 연결합니다."""

from importlib import import_module
from pathlib import Path, PureWindowsPath

import pytest

CAMPAIGN_RUNNERS = {
    "test_deepseek_flash_runner.py": "scripts.run_deepseek_v41_flash_20261118",
    "test_deepseek_restart_runner.py": "scripts.run_deepseek_v16_20261118",
}


@pytest.fixture(autouse=True)
def use_checkout_output_for_archived_campaign(request, monkeypatch):
    """캠페인 계약 검사에서 과거 호스트 경로만 현재 체크아웃에 맞춥니다."""
    module = CAMPAIGN_RUNNERS.get(request.node.path.name)
    if module is None or request.node.name != (
        "test_new_campaign_keeps_problem_protocol_and_uses_api_provider"
    ):
        return

    runner = import_module(module)
    campaign_config, _ = runner.config_paths()
    load_config = runner.core.load_hops_config

    def load_for_test(config, *args, **kwargs):
        loaded = load_config(config, *args, **kwargs)
        if Path(config).resolve() == campaign_config.resolve():
            archived_output = PureWindowsPath(loaded["output_root"])
            assert archived_output.parts[-2:] == runner.OUTPUT.parts[-2:]
            loaded["output_root"] = str(runner.OUTPUT)
        return loaded

    monkeypatch.setattr(runner.core, "load_hops_config", load_for_test)
