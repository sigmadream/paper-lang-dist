from __future__ import annotations

from pathlib import Path
import subprocess

from pytest import MonkeyPatch

from rttdist.moss import measure_pair_similarity


class _FakeResponse:
    def __init__(self, html: str) -> None:
        self._html: str = html

    def __enter__(self) -> _FakeResponse:
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        del exc_type
        del exc
        del tb

    def read(self) -> bytes:
        return self._html.encode("utf-8")


def test_measure_pair_similarity_returns_zero_when_moss_reports_no_matches(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    script_path = tmp_path / "moss.pl"
    _ = script_path.write_text("#!/usr/bin/env perl\n", encoding="utf-8")

    html = """<HTML>
<HEAD><TITLE>Moss Results</TITLE></HEAD>
<BODY>
<TABLE>
<TR><TH>File 1<TH>File 2<TH>Lines Matched
</TABLE>
No matches were found in your submission.<p></BODY>
</HTML>
"""

    def _fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        del args
        del kwargs
        return subprocess.CompletedProcess(
            args=["perl", script_path.as_posix()],
            returncode=0,
            stdout="http://moss.stanford.edu/results/2/5083218440796\n",
            stderr="",
        )

    def _fake_urlopen(*args: object, **kwargs: object) -> _FakeResponse:
        del args
        del kwargs
        return _FakeResponse(html)

    monkeypatch.setattr("rttdist.moss.subprocess.run", _fake_run)
    monkeypatch.setattr("rttdist.moss.urlopen", _fake_urlopen)

    parsed = measure_pair_similarity(
        "int main() { return 0; }",
        "int main() { return 1; }",
        script_path=script_path,
        label="rttdist:test",
    )

    assert parsed.report_url == "http://moss.stanford.edu/results/2/5083218440796"
    assert parsed.match_url is None
    assert parsed.seed_percentage == 0
    assert parsed.roundtrip_percentage == 0


def test_measure_pair_similarity_parses_rows_without_closing_tr_tags(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    script_path = tmp_path / "moss.pl"
    _ = script_path.write_text("#!/usr/bin/env perl\n", encoding="utf-8")

    html = """<HTML>
<HEAD><TITLE>Moss Results</TITLE></HEAD>
<BODY>
<TABLE>
<TR><TH>File 1<TH>File 2<TH>Lines Matched
<TR><TD><A HREF="http://moss.stanford.edu/results/2/1589505654733/match0.html">/tmp/seed.cpp (70%)</A>
    <TD><A HREF="http://moss.stanford.edu/results/2/1589505654733/match0.html">/tmp/roundtrip.cpp (76%)</A>
<TD ALIGN=right>16
</TABLE>
</BODY>
</HTML>
"""

    def _fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        del args
        del kwargs
        return subprocess.CompletedProcess(
            args=["perl", script_path.as_posix()],
            returncode=0,
            stdout="http://moss.stanford.edu/results/2/1589505654733\n",
            stderr="",
        )

    def _fake_urlopen(*args: object, **kwargs: object) -> _FakeResponse:
        del args
        del kwargs
        return _FakeResponse(html)

    monkeypatch.setattr("rttdist.moss.subprocess.run", _fake_run)
    monkeypatch.setattr("rttdist.moss.urlopen", _fake_urlopen)

    parsed = measure_pair_similarity(
        "int main() { return 0; }",
        "int main() { return 1; }",
        script_path=script_path,
        label="rttdist:test",
    )

    assert parsed.report_url == "http://moss.stanford.edu/results/2/1589505654733"
    assert (
        parsed.match_url
        == "http://moss.stanford.edu/results/2/1589505654733/match0.html"
    )
    assert parsed.seed_percentage == 70
    assert parsed.roundtrip_percentage == 76
