"""기존 파일을 변경하지 않고 Flash 전용 파일만 작성합니다."""

from pathlib import Path

import yaml

root = Path.cwd()
old_name = "commandcode_deepseek_v4_pro_20261118.yaml"
new_name = "commandcode_deepseek_v41_flash_20261118.yaml"
script = (root / "scripts/run_deepseek_v16_20261118.py").read_text(encoding="utf-8")
for old, new in (
    ("live-deepseek-20261118", "live-ds41f-20261118"),
    ("commandcode-deepseek_v4_pro-v16-20261118", "commandcode-ds41-flash-v16-20261118"),
    ("deepseek/deepseek-v4-pro", "deepseek/deepseek-v4.1-flash"),
    ("commandcode_deepseek_v4_pro_20261118", "commandcode_deepseek_v41_flash_20261118"),
    ("run_deepseek_v16_20261118", "run_deepseek_v41_flash_20261118"),
    ("test_deepseek_restart_runner", "test_deepseek_flash_runner"),
    ("0.24", "0.23"),
    ("49.62", "49.28"),
    ("49.32", "48.62"),
    ("32768 * 1.32 + 16384 * 3.96", "32768 * 0.30 + 16384 * 1.20"),
):
    script = script.replace(old, new)
(root / "scripts/run_deepseek_v41_flash_20261118.py").write_text(
    script, encoding="utf-8"
)

provider = yaml.safe_load(
    (root / "configs/v1.6/providers" / old_name).read_text(encoding="utf-8")
)
provider["model"] = "deepseek/deepseek-v4.1-flash"
provider["generation_profile"]["name"] = "commandcode-ds41-flash-v16-low-16384"
provider["cost_cap_usd"] = 48.62
provider["pricing"] = {
    "input_per_million": 0.30,
    "output_per_million": 1.20,
    "cached_input_per_million": 0.006,
}
(root / "configs/v1.6/providers" / new_name).write_text(
    "# Flash 전용 설정이며 피크 상계 단가를 사용합니다.\n"
    "# temperature는 추론 모드 미지원, top_p는 지원되나 기존 조건 유지로 생략합니다.\n"
    "# seed는 추가하지 않으며 미보고 실효 설정은 null로 유지합니다.\n"
    + yaml.safe_dump(provider, allow_unicode=True, sort_keys=False),
    encoding="utf-8",
)
campaign = yaml.safe_load(
    (root / "configs/v1.6/campaigns" / old_name).read_text(encoding="utf-8")
)
campaign["output_root"] = str(root / "artifacts-rtt-v1.6/live-ds41f-20261118")
campaign["campaign_id"] = "commandcode-ds41-flash-v16-20261118"
campaign["profile_id"] = "commandcode-ds41-flash-v16-low-16384"
campaign["provider_config"] = str(root / "configs/v1.6/providers" / new_name)
campaign["budget"]["cost_cap_usd"] = 48.62
campaign["execution_wrapper"]["path"] = "scripts/run_deepseek_v41_flash_20261118.py"
campaign["execution_wrapper"]["sha256"] = "최종 서식 이후 기록합니다"
for phase, cap in {"preflight": 0.23, "pilot": 49.28, "main": 48.62}.items():
    campaign["phase_budget_policy"][phase]["cost_cap_usd"] = cap
(root / "configs/v1.6/campaigns" / new_name).write_text(
    "# 독립 Flash 캠페인이며 기존 Pro·GLM 결과를 가져오지 않습니다.\n"
    + yaml.safe_dump(campaign, allow_unicode=True, sort_keys=False),
    encoding="utf-8",
)
