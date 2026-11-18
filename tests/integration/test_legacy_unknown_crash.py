import io
import json
import socket
import subprocess
import sys
from urllib.error import HTTPError, URLError

import pytest

from rttdist.experiment_io import read_json, write_json
from rttdist.providers import UnknownRequestState, create_provider


def legacy_config():
    return {
        "provider": "openai_compatible",
        "endpoint": "https://example.test/v1",
        "model": "test",
        "generation": {},
        "request_timeout": 1,
        "retries": 2,
        "pricing": {"input_per_million": 1, "output_per_million": 2},
    }


CRASH_PROCESS = """
import io
import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from rttdist import providers
from rttdist.experiment_io import read_json
root, mode, failure = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
def send(req, timeout):
    with (root / 'transports.txt').open('a', encoding='utf-8') as stream:
        stream.write('sent\\n')
    if mode == 'first':
        if failure == 'transport_crash':
            raise KeyboardInterrupt('전송 뒤 결과 저장 전 충돌')
        if failure == 'timeout':
            raise TimeoutError('fake-private-timeout')
        if failure == 'url_timeout':
            raise URLError(TimeoutError('fake-private-url-timeout'))
        if failure == 'reset':
            raise ConnectionResetError('fake-private-reset')
    raise HTTPError(req.full_url, 524, 'fake-private-reason', {}, io.BytesIO(b'fake-private-body'))
providers.request.urlopen = send
real_write = providers.write_json
def crash(path, value):
    result = real_write(path, value)
    if mode == 'first' and path.name == 'api_errors.json':
        raise KeyboardInterrupt('오류 기록 저장 직후 충돌')
    return result
providers.write_json = crash
try:
    providers.create_provider(read_json(root / 'config.json'), root / 'ledger.jsonl').complete({}, root / 'call')
except KeyboardInterrupt:
    print(json.dumps({'status': 'interrupted'}))
except providers.UnknownRequestState:
    print(json.dumps({'status': 'unknown'}))
else:
    raise AssertionError('불명 요청이 완료되어서는 안 됩니다.')
"""


@pytest.mark.parametrize(
    "failure", ["http524", "timeout", "url_timeout", "reset", "transport_crash"]
)
def test_legacy_incomplete_transport_survives_crash_and_new_processes(
    tmp_path, failure
):
    write_json(tmp_path / "config.json", legacy_config())

    def run(mode):
        result = subprocess.run(
            [sys.executable, "-c", CRASH_PROCESS, str(tmp_path), mode, failure],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
        )
        assert result.returncode == 0, result.stderr
        return json.loads(result.stdout)

    assert run("first") == {"status": "interrupted"}
    counter = tmp_path / "transports.txt"
    assert len(counter.read_text(encoding="utf-8").splitlines()) == 1
    assert not (tmp_path / "call/unknown_request.json").exists()
    if failure != "transport_crash":
        assert (tmp_path / "call/api_errors.json").is_file()
    for _ in range(2):
        assert run("resume") == {"status": "unknown"}
        assert len(counter.read_text(encoding="utf-8").splitlines()) == 1
    assert read_json(tmp_path / "call/transport_state.json")["status"] in (
        "inflight",
        "unknown",
    )
    for path in (tmp_path / "call").rglob("*"):
        if path.is_file():
            assert b"fake-private-" not in path.read_bytes()


@pytest.mark.parametrize("http_status", [408, 500, 503, 504, 520, 524, 599])
def test_existing_ambiguous_http_error_blocks_legacy_resume_without_new_markers(
    tmp_path, monkeypatch, http_status
):
    write_json(
        tmp_path / "api_errors.json", [{"attempt": 1, "http_status": http_status}]
    )
    monkeypatch.setattr(
        "rttdist.providers.request.urlopen",
        lambda *a, **k: pytest.fail("기존 불명 오류를 재전송하지 않습니다."),
    )
    for _ in range(2):
        with pytest.raises(UnknownRequestState):
            create_provider(legacy_config()).complete({}, tmp_path)


@pytest.mark.parametrize(
    "error_type", ["TimeoutError", "URLError", "ConnectionResetError", "OSError"]
)
def test_existing_unclassified_communication_error_blocks_legacy_resume(
    tmp_path, monkeypatch, error_type
):
    write_json(tmp_path / "api_errors.json", [{"attempt": 1, "type": error_type}])
    monkeypatch.setattr(
        "rttdist.providers.request.urlopen",
        lambda *a, **k: pytest.fail("불명 통신 오류를 재전송하지 않습니다."),
    )
    with pytest.raises(UnknownRequestState):
        create_provider(legacy_config()).complete({}, tmp_path)


@pytest.mark.parametrize("cached", ["normalized", "raw"])
def test_completed_legacy_cache_precedes_inflight_and_old_unknown_errors(
    tmp_path, monkeypatch, cached
):
    calls = []
    body = {
        "model": "test",
        "choices": [],
        "usage": {"prompt_tokens": 10, "completion_tokens": 2},
    }

    def send(*args, **kwargs):
        calls.append(1)
        return io.BytesIO(json.dumps(body).encode())

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    ledger = tmp_path / "ledger.jsonl"
    folder = tmp_path / "call"
    first = create_provider(legacy_config(), ledger).complete({}, folder)
    saved_ledger = ledger.read_bytes()
    raw = (folder / "response_body.txt").read_bytes()
    write_json(folder / "transport_state.json", {"status": "inflight"})
    write_json(folder / "unknown_request.json", {"reason": "request_outcome_unknown"})
    write_json(folder / "api_errors.json", [{"http_status": 524}])
    if cached == "raw":
        (folder / "response.json").unlink()
    for _ in range(2):
        replay = create_provider(legacy_config(), ledger).complete({}, folder)
        assert replay["cost_usd"] == first["cost_usd"]
        assert replay["body"] == body
        assert len(calls) == 1
        assert ledger.read_bytes() == saved_ledger
        assert (folder / "response_body.txt").read_bytes() == raw


@pytest.mark.parametrize("failure", ["429", "dns", "refused"])
def test_legacy_proven_pre_send_failures_still_retry_within_limit(
    tmp_path, monkeypatch, failure
):
    calls, delays = [], []

    def send(req, timeout):
        calls.append(1)
        if len(calls) < 3:
            if failure == "429":
                raise HTTPError(req.full_url, 429, "withheld", {}, None)
            raise URLError(
                socket.gaierror("fake DNS")
                if failure == "dns"
                else ConnectionRefusedError("fake refusal")
            )
        return io.BytesIO(b'{"model":"test","choices":[]}')

    monkeypatch.setattr("rttdist.providers.request.urlopen", send)
    monkeypatch.setattr("rttdist.providers.time.sleep", delays.append)
    result = create_provider(legacy_config()).complete({}, tmp_path)
    assert result["actual_model"] == "test" and len(calls) == 3
    assert delays == [1, 2]
    assert create_provider(legacy_config()).complete({}, tmp_path) == result
    assert len(calls) == 3
