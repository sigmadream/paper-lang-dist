"""Shared chat-completion transport; only transient infrastructure is retried.

Authentication values and headers never enter persisted requests or errors.
New non-compatible providers implement complete(payload, folder) with this
same persisted response contract and register in create_provider().

Cost accounting (v1/abs_EXPERIMENT.md 4장): when `pricing` is configured, every
newly received response adds usage x price to a JSON-lines ledger, and
`cost_cap_usd` refuses further network calls once the ledger total reaches it.
Cached responses are replayed without charge.
"""

import json
import os
from pathlib import Path
import re
import time
import math
import socket
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from copy import deepcopy
import uuid
from typing import Protocol
from urllib import request, error, parse

from rttdist.experiment_io import digest, read_json, write_json, timestamp


class ProviderError(RuntimeError):
    pass


class CostCapReached(ProviderError):
    pass


WIRE_OPTIONS = {
    "temperature",
    "top_p",
    "max_tokens",
    "seed",
    "thinking",
    "reasoning_effort",
}
# Values accepted by the commandcode.ai gateway (it rejects "none" and "minimal").
REASONING_EFFORTS = ("low", "medium", "high", "xhigh", "max")
ENV_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]{0,63}")
# Cloudflare-fronted gateways (e.g. commandcode.ai) reject urllib's default
# "Python-urllib/x.y" agent with error 1010, so every request names the client.
USER_AGENT = "rttdist/2.0"
# 520-524 are Cloudflare origin-connection errors: transient, no response was generated.
RETRYABLE_STATUS = (408, 429, 500, 502, 503, 504, 520, 521, 522, 523, 524)
ACCOUNTING_KEYS = ("pricing", "cost_cap_usd", "expected_model")


class Provider(Protocol):
    """Provider adapters return body, actual_model, usage and latency_seconds.

    The folder identifies a logical call, not a prompt hash. Implementations
    must replay a durable response there and must not persist credentials.
    """

    def complete(self, payload: dict, folder: Path) -> dict: ...


PROVIDER_FACTORIES = {}


def register_provider(name, factory):
    """Register an adapter factory(config, ledger=None) without editing runners."""
    if name in PROVIDER_FACTORIES:
        raise ValueError(f"Provider already registered: {name}")
    PROVIDER_FACTORIES[name] = factory


def usage_cost(usage, pricing):
    """USD for one response, or None when usage or pricing is unavailable."""
    if not usage or not pricing:
        return None
    if any(
        isinstance(usage.get(key), bool)
        or not isinstance(usage.get(key), (int, float))
        or not math.isfinite(usage[key])
        or usage[key] < 0
        for key in ("prompt_tokens", "completion_tokens")
    ):
        return None
    prompt = usage.get("prompt_tokens") or 0
    completion = usage.get("completion_tokens") or 0
    details = usage.get("prompt_tokens_details") or {}
    cached = min(details.get("cached_tokens") or 0, prompt)
    rate_in = float(pricing.get("input_per_million", 0))
    rate_out = float(pricing.get("output_per_million", 0))
    rate_cached = float(pricing.get("cached_input_per_million", rate_in))
    return (
        (prompt - cached) * rate_in + cached * rate_cached + completion * rate_out
    ) / 1e6


def model_matches(actual, expected, allowed_response_models=None, *, version="fps"):
    """과거 FPS 판정을 보존하며 v1.6은 정확한 ID와 명시적 별칭만 허용합니다."""
    if not isinstance(actual, str) or not actual.strip():
        return False
    if version == "fps" and allowed_response_models is None:
        actual_id = actual.strip().lower()
        expected_id = str(expected).strip().lower()
        return (
            actual_id == expected_id
            or expected_id in actual_id
            or actual_id in expected_id
        )
    return actual == expected or actual in (allowed_response_models or [])


class CompatibleProvider:
    def __init__(self, config, ledger=None):
        self.config = dict(config)
        self.wire = {k: v for k, v in self.config.items() if k not in ACCOUNTING_KEYS}
        endpoint = parse.urlsplit(config["endpoint"])
        if (
            endpoint.scheme not in ("http", "https")
            or not endpoint.netloc
            or endpoint.username
            or endpoint.password
            or endpoint.query
        ):
            raise ValueError(
                "Endpoint must be HTTP(S), without credentials or query parameters"
            )
        allowed = set(WIRE_OPTIONS)
        if config["provider"] == "lmstudio":
            allowed |= {"top_k", "repeat_penalty"}
        generation = config.get("generation", {})
        unknown = set(generation) - allowed
        if unknown:
            raise ValueError(f"Unsupported generation options: {sorted(unknown)}")
        thinking = generation.get("thinking")
        if thinking is not None and not (
            isinstance(thinking, dict)
            and thinking.get("type") in ("enabled", "disabled")
        ):
            raise ValueError(
                'thinking must be a mapping {"type": "enabled"|"disabled"}'
            )
        effort = generation.get("reasoning_effort")
        if effort is not None and effort not in REASONING_EFFORTS:
            raise ValueError(
                f"reasoning_effort must be one of {list(REASONING_EFFORTS)}"
            )
        key_env = config.get("api_key_env")
        if key_env is not None and not (
            isinstance(key_env, str) and ENV_NAME.fullmatch(key_env)
        ):
            # Never echo the value: a common mistake is pasting the secret itself here.
            raise ValueError(
                "api_key_env must be the NAME of an environment variable (e.g. CMD_API_KEY), not the key itself"
            )
        self.pricing = config.get("pricing")
        self.cost_cap = config.get("cost_cap_usd")
        if self.cost_cap is not None and not self.pricing:
            raise ValueError("cost_cap_usd requires pricing")
        if self.pricing and not {"input_per_million", "output_per_million"} <= set(
            self.pricing
        ):
            raise ValueError(
                "pricing requires input_per_million and output_per_million"
            )
        self.ledger = Path(ledger) if ledger else None
        self.total_cost = 0.0
        self.calls = 0
        self.charges = {}
        self.ledger_entries = []
        if self.ledger and self.ledger.exists():
            for line in self.ledger.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    entry = json.loads(line)
                    call_id = entry.get("call_id") or digest(
                        str(Path(entry["folder"]).resolve())
                    )
                    if call_id in self.charges:
                        continue
                    self.ledger_entries.append(entry)
                    self.charges[call_id] = entry["cost_usd"]
                    self.total_cost += entry["cost_usd"]
                    self.calls += 1

    @property
    def cap_reached(self):
        return self.cost_cap is not None and self.total_cost >= self.cost_cap

    def _record_cost(self, folder, result):
        call_id = digest(str(Path(folder).resolve()))
        if call_id in self.charges:
            result["cost_usd"] = self.charges[call_id]
            return
        cost = result.get("cost_usd")
        if cost is None:
            cost = usage_cost(result.get("usage"), self.pricing)
        result["cost_usd"] = cost
        if cost is None:
            return
        self.charges[call_id] = cost
        self.total_cost += cost
        self.calls += 1
        if self.ledger:
            self.ledger.parent.mkdir(parents=True, exist_ok=True)
            self.ledger_entries.append(
                {
                    "call_id": call_id,
                    "folder": str(folder),
                    "usage": result["usage"],
                    "cost_usd": cost,
                    "total_cost_usd": self.total_cost,
                    "at": timestamp(),
                }
            )
            temporary = self.ledger.with_suffix(".jsonl.tmp")
            temporary.write_text(
                "".join(
                    json.dumps(entry, ensure_ascii=False) + "\n"
                    for entry in self.ledger_entries
                ),
                encoding="utf-8",
            )
            os.replace(temporary, self.ledger)

    def complete(self, payload, folder):
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        contract = {"provider": self.wire, "payload": payload}
        reqpath = folder / "request.json"
        if reqpath.exists() and read_json(reqpath) != contract:
            raise ValueError("Stored model request changed; use a new run")
        write_json(reqpath, contract)
        target = folder / "response.json"
        if target.exists():
            result = read_json(target)
            before = dict(result)
            self._record_cost(folder, result)
            if result != before:
                write_json(target, result)
            return result
        if (folder / "response_body.txt").exists():
            # A crash after receiving a response must not cause another generation.
            raw = (folder / "response_body.txt").read_text(encoding="utf-8")
            try:
                body = json.loads(raw)
                if not isinstance(body, dict):
                    raise ValueError("Response must be an object")
            except ValueError:
                raise ProviderError(
                    "Malformed response preserved; no regeneration"
                ) from None
            result = {
                "body": body,
                "latency_seconds": None,
                "received_at": None,
                "actual_model": body.get("model"),
                "usage": body.get("usage"),
                "requested_generation": self.config.get("generation", {}),
                "applied_generation": None,
                "applied_generation_reason": "Recovered response; effective options not reported",
            }
            write_json(target, result)
            self._record_cost(folder, result)
            write_json(target, result)
            return result
        if self.cap_reached:
            raise CostCapReached(
                f"Cost cap {self.cost_cap} USD reached after {self.calls} calls ({self.total_cost:.4f} USD)"
            )
        headers = {"Content-Type": "application/json", "User-Agent": USER_AGENT}
        key_env = self.config.get("api_key_env")
        if key_env:
            key = os.environ.get(key_env)
            if not key:
                raise ProviderError(f"Missing API key environment variable {key_env}")
            headers["Authorization"] = "Bearer " + key
        errors_path = folder / "api_errors.json"
        errors = read_json(errors_path) if errors_path.exists() else []
        for attempt in range(self.config["retries"] + 1):
            start = time.monotonic()
            try:
                req = request.Request(
                    self.config["endpoint"].rstrip("/") + "/chat/completions",
                    data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                    headers=headers,
                )
                with request.urlopen(
                    req, timeout=self.config["request_timeout"]
                ) as stream:
                    raw = stream.read().decode("utf-8")
                # Preserve received bytes before parsing: malformed output is not regenerated.
                (folder / "response_body.txt").write_text(raw, encoding="utf-8")
                body = json.loads(raw)
                if not isinstance(body, dict):
                    raise ValueError("Response must be an object")
                result = {
                    "body": body,
                    "latency_seconds": time.monotonic() - start,
                    "received_at": timestamp(),
                    "actual_model": body.get("model"),
                    "usage": body.get("usage"),
                    "requested_generation": self.config.get("generation", {}),
                    "applied_generation": None,
                    "applied_generation_reason": "API does not echo effective decoding options",
                }
                write_json(target, result)
                self._record_cost(folder, result)
                write_json(target, result)
                return result
            except error.HTTPError as exc:
                code = exc.code
                errors.append(
                    {"attempt": len(errors) + 1, "http_status": code, "at": timestamp()}
                )
                write_json(errors_path, errors)
                if code not in RETRYABLE_STATUS or attempt == self.config["retries"]:
                    raise ProviderError(
                        f"HTTP {code}; response body withheld to avoid credential leakage"
                    ) from None
            except (error.URLError, TimeoutError) as exc:
                errors.append(
                    {
                        "attempt": len(errors) + 1,
                        "type": type(exc).__name__,
                        "at": timestamp(),
                    }
                )
                write_json(errors_path, errors)
                if attempt == self.config["retries"]:
                    raise ProviderError(type(exc).__name__) from None
            except (ValueError, KeyError) as exc:
                raise ProviderError(
                    "Malformed response preserved; no regeneration"
                ) from None
            time.sleep(min(2**attempt, 8))


def create_provider(config, ledger=None):
    factory = PROVIDER_FACTORIES.get(config["provider"])
    if factory is not None and factory not in (CompatibleProvider, APIProvider):
        return factory(config, ledger=ledger)
    if config.get("protocol") == "copilot_sdk" or config["provider"] == "copilot":
        from rttdist.copilot_provider import CopilotProvider

        return CopilotProvider(config, ledger=ledger)
    if config.get("protocol") or config.get("base_url"):
        return APIProvider(config, ledger=ledger)
    factory = PROVIDER_FACTORIES.get(config["provider"])
    if factory is None:
        raise ValueError(f"Unknown provider: {config['provider']}")
    return factory(config, ledger=ledger)


register_provider("lmstudio", CompatibleProvider)
register_provider("openai_compatible", CompatibleProvider)


class UnknownRequestState(ProviderError):
    """생성·과금 여부가 불명확하여 자동 재전송할 수 없습니다."""


_LEDGER_LOCKS = {}
_LOCKS_GUARD = threading.Lock()


@contextmanager
def file_lock(path, blocking=True):
    """스레드와 프로세스 사이에서 운영체제 잠금을 공유합니다."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with _LOCKS_GUARD:
        lock = _LEDGER_LOCKS.setdefault(str(path.resolve()), threading.RLock())
    if not lock.acquire(blocking=blocking):
        raise UnknownRequestState(
            "Request state unknown: another worker owns this request"
        )
    stream = None
    locked = False
    try:
        stream = path.open("a+b")
        stream.seek(0, 2)
        if stream.tell() == 0:
            stream.write(b"0")
            stream.flush()
        stream.seek(0)
        if os.name == "nt":
            import msvcrt

            while True:
                try:
                    msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                    break
                except OSError:
                    if not blocking:
                        raise UnknownRequestState(
                            "Request state unknown: another worker owns this request"
                        ) from None
                    time.sleep(0.01)
        else:
            import fcntl

            try:
                fcntl.flock(
                    stream.fileno(), fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB)
                )
            except BlockingIOError:
                raise UnknownRequestState(
                    "Request state unknown: another worker owns this request"
                ) from None
        locked = True
        yield
    finally:
        if stream is not None:
            if locked:
                stream.seek(0)
                if os.name == "nt":
                    import msvcrt

                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
            stream.close()
        lock.release()


def atomic_text(path, value):
    path = Path(path)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as stream:
        stream.write(value)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def endpoint_url(base_url, request_path, protocol):
    expected = "/responses" if protocol == "responses" else "/chat/completions"
    endpoint = parse.urlsplit(base_url)
    if (
        endpoint.scheme not in ("http", "https")
        or not endpoint.netloc
        or endpoint.username
        or endpoint.password
        or endpoint.query
        or endpoint.fragment
    ):
        raise ValueError(
            "base_url must be HTTP(S) without credentials, query or fragment"
        )
    path = request_path or expected
    if (
        not path.startswith("/")
        or "?" in path
        or "#" in path
        or "://" in path
        or ".." in path.split("/")
    ):
        raise ValueError("Invalid request_path")
    base = base_url.rstrip("/")
    if base.endswith(expected):
        if path != expected:
            raise ValueError("base_url and request_path conflict")
        return base
    if base.endswith("/responses") or base.endswith("/chat/completions"):
        raise ValueError("base_url protocol path conflict")
    return base + path


def retry_delay(header, attempt):
    if header:
        try:
            seconds = float(header)
            if math.isfinite(seconds):
                return max(0, seconds)
        except TypeError, ValueError:
            try:
                return max(
                    0,
                    (
                        parsedate_to_datetime(header) - datetime.now(timezone.utc)
                    ).total_seconds(),
                )
            except TypeError, ValueError, OverflowError:
                pass
    return min(2**attempt, 8)


class APIProvider:
    """v1.6 프로토콜 전송, 복구, 공유 예산을 관리합니다."""

    def __init__(self, config, ledger=None):
        from rttdist.provider_protocols import validate_generation

        self.config = deepcopy(config)
        self.protocol = config.get("protocol", "chat_completions")
        if self.protocol not in ("chat_completions", "responses", "copilot_sdk"):
            raise ValueError("Unsupported protocol")
        self.provider = config["provider"]
        if self.provider not in (
            "openai",
            "zai",
            "zai_coding",
            "opencode",
            "opencode_go",
            "compatible",
            "openai_compatible",
            "lmstudio",
            "copilot",
        ):
            raise ValueError("Unknown provider")
        self.profile = deepcopy(config.get("generation_profile") or {})
        if not isinstance(self.profile, dict):
            raise ValueError("generation_profile must be a mapping")
        validate_generation(self.profile, config.get("generation", {}))
        if (
            not isinstance(config.get("model"), str)
            or not config["model"].strip()
            or config["model"].startswith("<")
        ):
            raise ValueError("명시적인 model ID가 필요합니다")
        aliases = config.get("allowed_response_models", [])
        if not isinstance(aliases, list) or any(
            not isinstance(value, str) or not value for value in aliases
        ):
            raise ValueError("allowed_response_models must be an explicit list")
        self.url = None
        if self.protocol != "copilot_sdk":
            self.url = endpoint_url(
                config.get("base_url", config.get("endpoint", "")),
                config.get("request_path"),
                self.protocol,
            )
            hostpath = parse.urlsplit(self.url)
            if self.provider == "zai" and "/coding/" in hostpath.path:
                raise ValueError("Z.AI 일반 API와 Coding Plan 설정을 분리해 주세요")
            if self.provider == "zai_coding" and "/coding/" not in hostpath.path:
                raise ValueError("Coding Plan 전용 주소가 필요합니다")
        auth = config.get("auth") or {
            "type": "bearer",
            "api_key_env": config.get("api_key_env"),
        }
        if (
            not isinstance(auth, dict)
            or set(auth) - {"type", "api_key_env"}
            or auth.get("type", "bearer") not in ("bearer", "none", "sdk")
        ):
            raise ValueError("인증값 대신 auth 환경 변수 이름만 지정해 주세요")
        self.key_env = auth.get("api_key_env")
        if self.key_env is not None and (
            not isinstance(self.key_env, str) or not ENV_NAME.fullmatch(self.key_env)
        ):
            raise ValueError("api_key_env must be the NAME of an environment variable")
        self.retries = config.get("retries", 2)
        if (
            isinstance(self.retries, bool)
            or not isinstance(self.retries, int)
            or not 0 <= self.retries <= 2
        ):
            raise ValueError("retries must be between 0 and 2")
        self.timeout = config.get("request_timeout", 120)
        if (
            not isinstance(self.timeout, (int, float))
            or not math.isfinite(self.timeout)
            or self.timeout <= 0
        ):
            raise ValueError("request_timeout must be positive")
        self.pricing = config.get("pricing")
        if self.pricing is not None:
            if not isinstance(self.pricing, dict) or not {
                "input_per_million",
                "output_per_million",
            } <= set(self.pricing):
                raise ValueError(
                    "pricing requires input_per_million and output_per_million"
                )
            for value in self.pricing.values():
                if (
                    isinstance(value, bool)
                    or not isinstance(value, (int, float))
                    or not math.isfinite(value)
                    or value < 0
                ):
                    raise ValueError("pricing must contain nonnegative finite rates")
        for name in ("max_calls", "max_transport_attempts", "max_input_tokens"):
            value = config.get(name)
            if value is not None and (
                isinstance(value, bool) or not isinstance(value, int) or value <= 0
            ):
                raise ValueError(f"{name} must be a positive integer")
        self.cost_cap = config.get("cost_cap_usd")
        if config.get("max_calls") is None and self.cost_cap is None:
            raise ValueError("v1.6 실행에는 max_calls 또는 비용 상한이 필요합니다")
        for name in ("cost_cap_usd", "max_request_cost_usd"):
            value = config.get(name)
            if value is not None and (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
                or value <= 0
            ):
                raise ValueError(f"{name} must be positive and finite")
        if self.cost_cap is not None and self.maximum_request_cost() is None:
            raise ValueError(
                "cost_cap_usd requires pricing and maximum token estimate or max_request_cost_usd"
            )
        self.ledger = Path(ledger).resolve() if ledger else None
        self.total_cost = 0.0
        self.calls = 0
        self._secrets = []

    def maximum_request_cost(self, wire=None):
        explicit = self.config.get("max_request_cost_usd")
        if explicit is not None:
            return explicit
        generation = wire or self.config.get("generation", {})
        output = next(
            (
                generation[k]
                for k in ("max_tokens", "max_completion_tokens", "max_output_tokens")
                if k in generation
            ),
            None,
        )
        input_limit = self.config.get("max_input_tokens")
        if self.pricing and input_limit is not None and output is not None:
            input_rate = max(
                self.pricing["input_per_million"],
                self.pricing.get("cached_input_per_million", 0),
            )
            return (
                input_limit * input_rate + output * self.pricing["output_per_million"]
            ) / 1e6
        return None

    def redact(self, value):
        if isinstance(value, dict):
            return {
                key: (
                    "[REDACTED]"
                    if key.lower()
                    in (
                        "authorization",
                        "api_key",
                        "github_token",
                        "access_token",
                        "password",
                        "secret",
                        "token",
                    )
                    else self.redact(item)
                )
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [self.redact(item) for item in value]
        if isinstance(value, str):
            for secret in self._secrets:
                value = value.replace(secret, "[REDACTED]")
            value = re.sub(r"(?i)Bearer\s+[^\s\"']+", "Bearer [REDACTED]", value)
        return value

    @contextmanager
    def _state(self):
        if self.ledger is None:
            raise ValueError("공유 예산 장부 경로가 필요합니다")
        state_path = self.ledger.with_suffix(self.ledger.suffix + ".state.json")
        with file_lock(self.ledger.with_suffix(self.ledger.suffix + ".lock")):
            state = (
                read_json(state_path)
                if state_path.exists()
                else {"requests": {}, "attempts": []}
            )
            yield state
            write_json(state_path, self.redact(state))

    def _totals(self, state):
        entries = state["requests"].values()
        self.calls = len(state["requests"])
        self.total_cost = sum(entry.get("cost_usd") or 0 for entry in entries)
        return self.total_cost + sum(
            (entry.get("reserved_usd") or 0)
            + (entry.get("uncertain_reserved_usd") or 0)
            for entry in state["requests"].values()
        )

    @property
    def cap_reached(self):
        if self.ledger is None:
            return False
        with self._state() as state:
            reserved = self._totals(state)
            return (self.cost_cap is not None and reserved >= self.cost_cap) or (
                self.config.get("max_calls") is not None
                and self.calls >= self.config["max_calls"]
            )

    def reserve_request_budget(self, call_id, estimate):
        if estimate is not None and (
            not isinstance(estimate, (int, float))
            or not math.isfinite(estimate)
            or estimate < 0
        ):
            raise ValueError("Invalid request estimate")
        with self._state() as state:
            if call_id in state["requests"]:
                return deepcopy(state["requests"][call_id])
            reserved = self._totals(state)
            if (
                self.config.get("max_calls") is not None
                and self.calls >= self.config["max_calls"]
            ):
                raise CostCapReached("Logical call cap reached")
            if self.cost_cap is not None and (
                estimate is None or reserved + estimate > self.cost_cap + 1e-12
            ):
                raise CostCapReached("Cost cap including pending reservations reached")
            state["requests"][call_id] = {
                "status": "reserved",
                "reserved_usd": estimate,
                "cost_usd": None,
                "at": timestamp(),
            }
            return deepcopy(state["requests"][call_id])

    def record_transport_attempt(self, call_id, attempt_id, metadata):
        with self._state() as state:
            for entry in state["attempts"]:
                if entry["attempt_id"] == attempt_id:
                    entry.update(self.redact(metadata))
                    return
            maximum = self.config.get("max_transport_attempts")
            if maximum is not None and len(state["attempts"]) >= maximum:
                raise CostCapReached("Transport attempt cap reached")
            prior = [
                entry for entry in state["attempts"] if entry["call_id"] == call_id
            ]
            if (
                prior
                and prior[-1].get("status") == "http_error"
                and (
                    prior[-1].get("http_status", 0) >= 500
                    or prior[-1].get("http_status") == 408
                )
            ):
                # 서버 오류의 생성·과금 여부도 단정할 수 없으므로 재시도분을 추가 예약합니다.
                entry = state["requests"][call_id]
                extra = entry.get("reserved_usd")
                if self.cost_cap is not None and (
                    extra is None or self._totals(state) + extra > self.cost_cap + 1e-12
                ):
                    raise CostCapReached(
                        "Cost cap including uncertain transport charges reached"
                    )
                if extra is not None:
                    entry["uncertain_reserved_usd"] = (
                        entry.get("uncertain_reserved_usd") or 0
                    ) + extra
            state["attempts"].append(
                {"call_id": call_id, "attempt_id": attempt_id, **self.redact(metadata)}
            )
            state["requests"][call_id]["status"] = "inflight"

    def finalize_request(self, call_id, response):
        with self._state() as state:
            entry = state["requests"].setdefault(call_id, {})
            reserved = (
                entry.get("reserved_usd") if response.get("cost_usd") is None else None
            )
            entry.update(
                {
                    "status": "completed",
                    "cost_usd": response.get("cost_usd"),
                    "cost_source": response.get("cost_source"),
                    "usage": response.get("usage"),
                    "reserved_usd": reserved,
                    "at": entry.get("at", timestamp()),
                }
            )
            self._totals(state)
            # 상태 저장 전 장부를 먼저 원자적으로 재구성하여 충돌 시 중복 과금을 막습니다.
            records = [
                {
                    "call_id": key,
                    **{k: v for k, v in value.items() if k != "fingerprint"},
                }
                for key, value in state["requests"].items()
                if value.get("status") == "completed"
            ]
            atomic_text(
                self.ledger,
                "".join(
                    json.dumps(self.redact(item), ensure_ascii=False) + "\n"
                    for item in records
                ),
            )

    def _mark(self, call_id, status):
        with self._state() as state:
            state["requests"][call_id]["status"] = status
            uncertain = any(
                attempt["call_id"] == call_id
                and attempt.get("status") in ("unknown", "http_error")
                and (
                    attempt.get("status") == "unknown"
                    or attempt.get("http_status", 0) >= 500
                    or attempt.get("http_status") == 408
                )
                for attempt in state["attempts"]
            )
            if status == "failed" and not uncertain:
                state["requests"][call_id]["reserved_usd"] = None

    def _headers(self, call_id):
        headers = {"Content-Type": "application/json", "User-Agent": USER_AGENT}
        if self.key_env:
            secret = os.environ.get(self.key_env)
            if not secret:
                raise ProviderError(
                    f"Missing API key environment variable {self.key_env}"
                )
            self._secrets = [secret]
            headers["Authorization"] = "Bearer " + secret
        if self.provider in ("opencode", "opencode_go"):
            headers["x-opencode-session"] = "ses_" + call_id[:32]
        return headers

    def _receive(self, wire, folder, call_id, headers):
        attempts_path = folder / "transport_attempts.json"
        attempts = read_json(attempts_path) if attempts_path.exists() else []
        errors_path = folder / "api_errors.json"
        errors = read_json(errors_path) if errors_path.exists() else []
        for retry in range(len(attempts), self.retries + 1):
            attempt = {
                "attempt_id": uuid.uuid4().hex,
                "attempt": retry + 1,
                "status": "inflight",
                "at": timestamp(),
            }
            self.record_transport_attempt(call_id, attempt["attempt_id"], attempt)
            attempts.append(attempt)
            write_json(attempts_path, attempts)
            started = time.monotonic()
            try:
                req = request.Request(
                    self.url,
                    data=json.dumps(wire, ensure_ascii=False).encode("utf-8"),
                    headers=headers,
                )
                with request.urlopen(req, timeout=self.timeout) as stream:
                    raw_bytes = stream.read()
                # 수신 원문은 정규화나 장부 처리 전에 저장합니다. 비밀값은 저장 전 치환합니다.
                raw = self.redact(raw_bytes.decode("utf-8", errors="replace"))
                atomic_text(folder / "response_body.txt", raw)
                attempt.update(
                    {
                        "status": "received",
                        "latency_seconds": time.monotonic() - started,
                    }
                )
                write_json(attempts_path, attempts)
                self.record_transport_attempt(call_id, attempt["attempt_id"], attempt)
                write_json(
                    folder / "receipt.json",
                    {
                        "latency_seconds": attempt["latency_seconds"],
                        "received_at": timestamp(),
                    },
                )
                return
            except error.HTTPError as exc:
                attempt.update({"status": "http_error", "http_status": exc.code})
                delay = retry_delay(
                    exc.headers.get("Retry-After") if exc.headers else None, retry
                )
                transient = exc.code in RETRYABLE_STATUS
                message = f"HTTP {exc.code}; response body withheld"
            except (error.URLError, TimeoutError, ConnectionError, OSError) as exc:
                reason = exc.reason if isinstance(exc, error.URLError) else exc
                transient = isinstance(
                    reason, (ConnectionRefusedError, socket.gaierror)
                )
                attempt.update(
                    {
                        "status": "pre_send_failure" if transient else "unknown",
                        "type": type(exc).__name__,
                    }
                )
                delay = retry_delay(None, retry)
                message = (
                    "Connection failed before transmission"
                    if transient
                    else "Request state unknown; automatic regeneration blocked"
                )
            write_json(attempts_path, attempts)
            self.record_transport_attempt(call_id, attempt["attempt_id"], attempt)
            errors.append(
                {key: value for key, value in attempt.items() if key != "attempt_id"}
            )
            write_json(errors_path, errors)
            if attempt["status"] == "unknown":
                self._mark(call_id, "unknown")
                raise UnknownRequestState(message) from None
            if not transient or retry >= self.retries:
                self._mark(call_id, "failed")
                raise ProviderError(message) from None
            time.sleep(delay)
        raise ProviderError(
            "Transport retries exhausted; automatic regeneration blocked"
        )

    def _result(self, wire, folder, call_id, generation):
        from rttdist.provider_protocols import normalize_response

        target = folder / "response.json"
        if target.exists():
            result = read_json(target)
        else:
            try:
                raw = json.loads(
                    (folder / "response_body.txt").read_text(encoding="utf-8")
                )
                result = normalize_response(
                    self.protocol,
                    raw,
                    {
                        "model": self.config["model"],
                        "provider": self.provider,
                        "allowed_response_models": self.config.get(
                            "allowed_response_models", []
                        ),
                        "generation": generation,
                        "sent_generation": {
                            key: value
                            for key, value in wire.items()
                            if key not in ("model", "messages", "input", "instructions")
                        },
                        "raw_response_path": str(folder / "response_body.txt"),
                    },
                )
            except ValueError, KeyError, TypeError, AttributeError:
                self._mark(call_id, "unknown")
                raise ProviderError(
                    "Malformed response preserved; no regeneration"
                ) from None
            receipt = (
                read_json(folder / "receipt.json")
                if (folder / "receipt.json").exists()
                else {"latency_seconds": None, "received_at": None}
            )
            result.update(receipt)
            if result["cost_usd"] is None:
                result["cost_usd"] = usage_cost(result["usage"], self.pricing)
                result["cost_source"] = (
                    "estimated" if result["cost_usd"] is not None else None
                )
            result["logical_request_id"] = call_id
            if self.protocol == "copilot_sdk":
                result.update(
                    {
                        "execution_class": "sdk_exploratory",
                        "internal_model_calls": None,
                        "sdk_turns": 1,
                        "sdk_metadata": raw.get("sdk_metadata"),
                    }
                )
            else:
                result["execution_class"] = "direct_api"
            write_json(target, self.redact(result))
        self.finalize_request(call_id, result)
        evidence = result.get("model_evidence", {})
        if evidence.get("status") == "mismatch" or (
            evidence.get("status") == "missing" and self.protocol != "copilot_sdk"
        ):
            raise ProviderError(
                "Response model verification failed; response preserved"
            )
        return result

    def complete(self, payload, folder):
        from rttdist.provider_protocols import build_request, requested_generation

        folder = Path(folder).resolve()
        folder.mkdir(parents=True, exist_ok=True)
        if self.ledger is None:
            self.ledger = folder.parent / "provider_ledger.jsonl"
        request_data = {"model": self.config["model"], **deepcopy(payload)}
        if request_data["model"] != self.config["model"]:
            raise ValueError("payload model differs from configured model")
        generation = {
            **self.config.get("generation", {}),
            **requested_generation(payload),
        }
        request_data = {
            key: value
            for key, value in request_data.items()
            if key not in requested_generation(payload)
        }
        request_data["generation"] = generation
        wire = build_request(self.protocol, request_data, self.profile)
        input_limit = self.config.get("max_input_tokens")
        if input_limit is not None:
            # 바이트 기반 토큰화보다 보수적인 상한으로 입력 예산을 검사합니다.
            input_value = {
                key: wire[key]
                for key in ("messages", "input", "instructions")
                if key in wire
            }
            message_count = len(wire.get("messages", wire.get("input", [])))
            input_bound = len(
                json.dumps(input_value, ensure_ascii=False).encode("utf-8")
            ) + 64 * (message_count if isinstance(message_count, int) else 1)
            if input_bound > input_limit:
                raise ValueError("입력 input 예산의 보수적 토큰 상한을 초과했습니다")
        logical = payload.get("logical_request")
        if logical is not None and (
            not isinstance(logical, dict)
            or not {"campaign", "phase", "problem", "route", "repeat", "step"}
            <= set(logical)
        ):
            raise ValueError(
                "logical_request requires campaign/phase/problem/route/repeat/step"
            )
        call_id = digest(logical if logical is not None else str(folder))
        contract = {"provider": self.config, "payload": request_data}
        fingerprint = digest(contract)
        # 인증값은 요청 중에만 읽습니다. 재생 요청도 저장된 비밀값을 노출하지 않습니다.
        if self.key_env and os.environ.get(self.key_env):
            self._secrets = [os.environ[self.key_env]]
        call_lock = (
            self.ledger.parent / (self.ledger.name + ".calls") / (call_id + ".lock")
        )
        with file_lock(call_lock, blocking=False):
            with self._state() as state:
                previous = deepcopy(state["requests"].get(call_id))
                if previous and previous.get("fingerprint") not in (None, fingerprint):
                    raise ValueError("Stored model request changed; use a new run")
            canonical = (
                Path(previous["folder"])
                if previous and previous.get("folder")
                else folder
            )
            reqpath = canonical / "request.json"
            safe_contract = self.redact(contract)
            if reqpath.exists() and read_json(reqpath) != safe_contract:
                raise ValueError("Stored model request changed; use a new run")
            if not reqpath.exists():
                write_json(reqpath, safe_contract)
            response_exists = (canonical / "response.json").exists() or (
                canonical / "response_body.txt"
            ).exists()
            if (
                not response_exists
                and previous
                and previous.get("status") in ("inflight", "unknown", "completed")
            ):
                raise UnknownRequestState(
                    "Request state unknown; automatic regeneration blocked"
                )
            if not response_exists and previous and previous.get("status") == "failed":
                raise ProviderError(
                    "Previous transport failed; automatic regeneration blocked"
                )
            headers = None if response_exists else self._headers(call_id)
            estimate = self.maximum_request_cost(wire)
            self.reserve_request_budget(call_id, estimate)
            with self._state() as state:
                state["requests"][call_id].update(
                    {
                        "folder": str(canonical),
                        "fingerprint": fingerprint,
                        "logical_request": logical,
                    }
                )
            if not response_exists:
                self._receive(wire, canonical, call_id, headers)
            result = self._result(wire, canonical, call_id, generation)
            if canonical != folder:
                write_json(folder / "request.json", safe_contract)
                write_json(folder / "response.json", result)
            return result


for _provider_name in (
    "openai",
    "zai",
    "zai_coding",
    "opencode",
    "opencode_go",
    "compatible",
):
    register_provider(_provider_name, APIProvider)
