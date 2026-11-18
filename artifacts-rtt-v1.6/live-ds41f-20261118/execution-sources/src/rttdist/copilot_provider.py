"""공식 Copilot Python SDK의 격리된 단일 번역 턴 어댑터입니다."""

import asyncio
from importlib import metadata, util
import json
import os
from pathlib import Path
import shutil
import tempfile
import time
import uuid

from rttdist.experiment_io import timestamp, write_json
from rttdist.providers import (
    APIProvider,
    ProviderError,
    UnknownRequestState,
    atomic_text,
)

SDK_VERSION = "0.1.32"


def sdk_available():
    return util.find_spec("copilot") is not None


def sdk_version():
    try:
        return metadata.version("github-copilot-sdk")
    except metadata.PackageNotFoundError:
        return None


def load_sdk():
    if not sdk_available():
        raise ProviderError("github-copilot-sdk==0.1.32 선택 의존성을 설치해 주세요")
    if sdk_version() != SDK_VERSION:
        raise ProviderError("검증한 SDK 버전은 github-copilot-sdk==0.1.32입니다")
    from copilot import CopilotClient
    from copilot.types import PermissionRequestResult

    return CopilotClient, PermissionRequestResult


def field(value, name, default=None):
    return (
        value.get(name, default)
        if isinstance(value, dict)
        else getattr(value, name, default)
    )


class CopilotProvider(APIProvider):
    def __init__(self, config, ledger=None):
        config = {**config, "protocol": "copilot_sdk"}
        if set(config.get("generation", {})) - {"reasoning_effort"}:
            raise ValueError(
                "Unsupported generation options for Copilot SDK; 별도 SDK 프로파일이 필요합니다"
            )
        super().__init__(config, ledger)

    async def _sdk_turn(self, wire, folder, call_id, token):
        client_factory, permission_result = load_sdk()
        cli_path = self.config.get("cli_path") or shutil.which("copilot")
        if not cli_path:
            raise ProviderError(
                "공식 Copilot CLI를 찾지 못했습니다. cli_path 또는 PATH를 확인해 주세요"
            )
        with tempfile.TemporaryDirectory(prefix="rttdist-copilot-") as isolated:
            root = Path(isolated)
            work = root / "work"
            settings = root / "config"
            home = root / "home"
            for path in (work, settings, home):
                path.mkdir()
            # 인증은 명시한 토큰만 사용하며 사용자 설정·로그인 저장소를 상속하지 않습니다.
            child_env = {
                name: os.environ[name]
                for name in (
                    "PATH",
                    "SystemRoot",
                    "WINDIR",
                    "COMSPEC",
                    "PATHEXT",
                    "TEMP",
                    "TMP",
                )
                if name in os.environ
            }
            child_env.update(
                {
                    "HOME": str(home),
                    "USERPROFILE": str(home),
                    "XDG_CONFIG_HOME": str(settings),
                    "APPDATA": str(settings),
                    "LOCALAPPDATA": str(settings),
                    "COPILOT_HOME": str(settings),
                    "COPILOT_TELEMETRY_DISABLED": "true",
                }
            )
            client = client_factory(
                {
                    "cli_path": cli_path,
                    "cwd": str(work),
                    "env": child_env,
                    "github_token": token,
                    "use_logged_in_user": False,
                    "auto_restart": False,
                    "log_level": "error",
                }
            )
            session = None
            try:
                await client.start()
                status = await client.get_status()
                auth = await client.get_auth_status()
                if not field(auth, "isAuthenticated", False):
                    raise ProviderError("Copilot SDK 인증이 확인되지 않았습니다")
                models = await client.list_models()
                model_info = next(
                    (model for model in models if field(model, "id") == wire["model"]),
                    None,
                )
                if model_info is None:
                    raise ProviderError(
                        "지정한 모델에 대한 Copilot SDK 접근을 확인하지 못했습니다"
                    )
                if "reasoning_effort" in wire:
                    capabilities = field(model_info, "capabilities", {})
                    if not field(
                        field(capabilities, "supports", {}), "reasoning_effort", False
                    ):
                        raise ProviderError(
                            "Copilot 모델이 요청한 reasoning_effort를 지원하지 않습니다"
                        )

                def deny_permission(*args):
                    return permission_result(kind="denied-by-rules")

                def deny_tool(*args):
                    return {
                        "permissionDecision": "deny",
                        "permissionDecisionReason": "이 실험에서는 도구를 사용할 수 없습니다",
                    }

                messages = wire.get("messages", [])
                instructions = "\n\n".join(
                    item["content"]
                    for item in messages
                    if item.get("role") in ("system", "developer")
                )
                prompt = "\n\n".join(
                    item["content"] for item in messages if item.get("role") == "user"
                )
                if any(
                    item.get("role") not in ("system", "developer", "user")
                    or not isinstance(item.get("content"), str)
                    for item in messages
                ):
                    raise ProviderError(
                        "Copilot 단일 턴은 문자열 지침과 사용자 요청만 허용합니다"
                    )
                session_config = {
                    "model": wire["model"],
                    "session_id": "rttdist-" + uuid.uuid4().hex,
                    "client_name": "rttdist-v1.6",
                    "working_directory": str(work),
                    "config_dir": str(settings),
                    "available_tools": [],
                    "tools": [],
                    "mcp_servers": {},
                    "custom_agents": [],
                    "skill_directories": [],
                    "disabled_skills": ["*"],
                    "infinite_sessions": {"enabled": False},
                    "system_message": {
                        "mode": "replace",
                        "content": instructions
                        or "제공된 텍스트만 번역하고 코드만 출력해 주세요.",
                    },
                    "on_permission_request": deny_permission,
                    "hooks": {"on_pre_tool_use": deny_tool},
                    "streaming": False,
                }
                if "reasoning_effort" in wire:
                    session_config["reasoning_effort"] = wire["reasoning_effort"]
                session = await client.create_session(session_config)
                usages = []
                actual_models = []

                def observe(event):
                    kind = field(field(event, "type"), "value", field(event, "type"))
                    data = field(event, "data", {})
                    if kind == "assistant.usage":
                        observed = {
                            "prompt_tokens": field(data, "input_tokens"),
                            "completion_tokens": field(data, "output_tokens"),
                        }
                        usages.append(observed)
                        model = field(data, "model")
                        if model:
                            actual_models.append(model)

                session.on(observe)
                self._sdk_send_started = True
                response = await session.send_and_wait(
                    {"prompt": prompt}, timeout=self.timeout
                )
                actual = field(field(response, "data", {}), "model")
                if actual:
                    actual_models.append(actual)
                if len(set(actual_models)) > 1:
                    raise ProviderError(
                        "Copilot SDK가 한 번역 턴에 여러 모델 ID를 보고했습니다"
                    )
                usage = None
                if usages and all(
                    all(isinstance(value, (int, float)) for value in entry.values())
                    for entry in usages
                ):
                    usage = {
                        key: sum(entry[key] for entry in usages)
                        for key in ("prompt_tokens", "completion_tokens")
                    }
                raw = {
                    "id": field(field(response, "data", {}), "message_id"),
                    "model": actual_models[-1] if actual_models else None,
                    "text": field(field(response, "data", {}), "content", "") or "",
                    "finish_reason": "stop",
                    "usage": usage,
                    "sdk_metadata": {
                        "sdk_version": sdk_version(),
                        "cli_version": field(status, "version"),
                        "protocol_version": field(status, "protocolVersion"),
                        "session_id": field(session, "session_id"),
                        "sdk_turns": 1,
                        "internal_model_calls": None,
                        "context_control": "새 빈 작업·설정·홈 폴더와 도구 차단을 적용했으나 내부 컨텍스트는 검증하지 못했습니다",
                    },
                }
                atomic_text(
                    folder / "response_body.txt",
                    json.dumps(self.redact(raw), ensure_ascii=False),
                )
                return raw
            finally:
                # 종료 오류가 수신 응답의 보존을 가로막지 않게 합니다.
                if session is not None:
                    try:
                        await asyncio.wait_for(session.disconnect(), timeout=5)
                    except Exception:
                        pass
                try:
                    await asyncio.wait_for(client.stop(), timeout=5)
                except Exception:
                    pass

    def _receive(self, wire, folder, call_id, headers):
        unsupported = set(wire) - {"model", "messages", "reasoning_effort"}
        if unsupported:
            raise ValueError("Unsupported generation options for Copilot SDK")
        if not self.key_env or not os.environ.get(self.key_env):
            raise ProviderError(
                "Copilot SDK에는 auth.api_key_env로 명시한 인증 토큰이 필요합니다"
            )
        # SDK를 시작하기 전에 의존성과 CLI 존재만 확인합니다. 자동 설치는 하지 않습니다.
        load_sdk()
        if not (self.config.get("cli_path") or shutil.which("copilot")):
            raise ProviderError("공식 Copilot CLI를 찾지 못했습니다")
        attempt = {
            "attempt_id": uuid.uuid4().hex,
            "attempt": 1,
            "at": timestamp(),
            "status": "inflight",
            "unit": "sdk_turn",
        }
        self.record_transport_attempt(call_id, attempt["attempt_id"], attempt)
        write_json(folder / "transport_attempts.json", [attempt])
        self._sdk_send_started = False
        started = time.monotonic()
        try:
            raw = asyncio.run(
                self._sdk_turn(wire, folder, call_id, os.environ[self.key_env])
            )
            atomic_text(
                folder / "response_body.txt",
                json.dumps(self.redact(raw), ensure_ascii=False),
            )
            attempt["status"] = "received"
            write_json(folder / "transport_attempts.json", [attempt])
            self.record_transport_attempt(call_id, attempt["attempt_id"], attempt)
            write_json(
                folder / "receipt.json",
                {
                    "latency_seconds": time.monotonic() - started,
                    "received_at": timestamp(),
                },
            )
        except Exception:
            unknown = self._sdk_send_started
            attempt["status"] = "unknown" if unknown else "failed"
            write_json(folder / "transport_attempts.json", [attempt])
            self.record_transport_attempt(call_id, attempt["attempt_id"], attempt)
            self._mark(call_id, attempt["status"])
            if unknown:
                raise UnknownRequestState(
                    "Copilot request state unknown; automatic regeneration blocked"
                ) from None
            raise ProviderError(
                "Copilot SDK 연결·인증·모델 접근 점검 실패; 상세 예외는 비밀정보 보호를 위해 저장하지 않습니다"
            ) from None
