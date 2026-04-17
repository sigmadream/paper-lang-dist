from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
from tempfile import TemporaryDirectory
from urllib.parse import urljoin
from urllib.request import Request, urlopen

MOSS_REPORT_URL_RE = re.compile(r"https?://moss\.stanford\.edu/results/\d+/\d+/?")
MOSS_ROW_ENTRY_RE = re.compile(r"^(?P<name>.+?)\s*\((?P<pct>\d+)%\)$")
MOSS_NO_MATCHES_TEXT = "No matches were found in your submission."


class MossError(RuntimeError):
    pass


@dataclass(frozen=True)
class MossSimilarityMatch:
    report_url: str
    match_url: str | None
    seed_percentage: int
    roundtrip_percentage: int


def measure_pair_similarity(
    seed_cpp_source: str,
    roundtrip_cpp_source: str,
    *,
    script_path: Path,
    label: str,
    perl_command: str = "perl",
    timeout_seconds: int = 120,
) -> MossSimilarityMatch:
    normalized_script_path = Path(script_path).expanduser().resolve()
    if not normalized_script_path.is_file():
        raise MossError(f"MOSS script not found: {normalized_script_path}")

    with TemporaryDirectory(prefix="rttdist-moss-") as temp_dir:
        temp_root = Path(temp_dir)
        seed_path = temp_root / "seed.cpp"
        roundtrip_path = temp_root / "roundtrip.cpp"
        seed_path.write_text(f"{seed_cpp_source.rstrip()}\n", encoding="utf-8")
        roundtrip_path.write_text(
            f"{roundtrip_cpp_source.rstrip()}\n", encoding="utf-8"
        )

        completed = subprocess.run(
            [
                perl_command,
                normalized_script_path.as_posix(),
                "-l",
                "cc",
                "-c",
                label,
                seed_path.as_posix(),
                roundtrip_path.as_posix(),
            ],
            capture_output=True,
            check=False,
            text=True,
            timeout=timeout_seconds,
        )

    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()
    if completed.returncode != 0:
        raise MossError(
            "MOSS submission failed with non-zero exit status "
            f"{completed.returncode}: {stderr or stdout or 'no output'}"
        )

    report_url_match = MOSS_REPORT_URL_RE.search(f"{stdout}\n{stderr}")
    if report_url_match is None:
        raise MossError("MOSS did not return a parseable result URL.")

    report_url = report_url_match.group(0).rstrip("/")
    request = Request(report_url, headers={"User-Agent": "rttdist/0.1"})
    with urlopen(request, timeout=timeout_seconds) as response:
        report_html = response.read().decode("utf-8", errors="replace")

    parsed = _parse_report_index(
        report_url=report_url,
        html=report_html,
        expected_names=("seed.cpp", "roundtrip.cpp"),
    )
    if parsed is None:
        raise MossError("Unable to find the submitted pair in the MOSS report index.")

    return parsed


@dataclass
class _Anchor:
    href: str
    text: str


class _MossIndexParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[_Anchor]] = []
        self._current_row: list[_Anchor] | None = None
        self._current_href: str | None = None
        self._current_text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tr":
            if self._current_row:
                self.rows.append(self._current_row)
            self._current_row = []
            return

        if tag == "a" and self._current_row is not None:
            href = ""
            for key, value in attrs:
                if key == "href" and value is not None:
                    href = value
                    break
            self._current_href = href
            self._current_text_parts = []

    def handle_data(self, data: str) -> None:
        if self._current_href is not None:
            self._current_text_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if (
            tag == "a"
            and self._current_row is not None
            and self._current_href is not None
        ):
            text = " ".join(part.strip() for part in self._current_text_parts).strip()
            self._current_row.append(_Anchor(href=self._current_href, text=text))
            self._current_href = None
            self._current_text_parts = []
            return

        if tag == "tr" and self._current_row is not None:
            if self._current_row:
                self.rows.append(self._current_row)
            self._current_row = None

    def close(self) -> None:
        super().close()
        if self._current_row:
            self.rows.append(self._current_row)
            self._current_row = None


def _parse_report_index(
    *,
    report_url: str,
    html: str,
    expected_names: tuple[str, str],
) -> MossSimilarityMatch | None:
    parser = _MossIndexParser()
    parser.feed(html)
    parser.close()

    if MOSS_NO_MATCHES_TEXT in html:
        return MossSimilarityMatch(
            report_url=report_url,
            match_url=None,
            seed_percentage=0,
            roundtrip_percentage=0,
        )

    expected = {name.lower() for name in expected_names}
    fallback: MossSimilarityMatch | None = None

    for row in parser.rows:
        parsed_entries = [_parse_anchor(anchor) for anchor in row]
        parsed_entries = [item for item in parsed_entries if item is not None]
        if len(parsed_entries) < 2:
            continue

        first_name, first_pct, first_href = parsed_entries[0]
        second_name, second_pct, second_href = parsed_entries[1]
        names = {first_name.lower(), second_name.lower()}
        match_url = urljoin(f"{report_url}/", first_href or second_href)

        candidate = _build_similarity_match(
            report_url=report_url,
            match_url=match_url,
            first_name=first_name,
            first_pct=first_pct,
            second_name=second_name,
            second_pct=second_pct,
            expected_names=expected_names,
        )
        if candidate is None:
            continue
        if names == expected:
            return candidate
        if fallback is None:
            fallback = candidate

    return fallback


def _parse_anchor(anchor: _Anchor) -> tuple[str, int, str] | None:
    match = MOSS_ROW_ENTRY_RE.match(anchor.text.strip())
    if match is None:
        return None
    return (
        Path(match.group("name").strip()).name,
        int(match.group("pct")),
        anchor.href,
    )


def _build_similarity_match(
    *,
    report_url: str,
    match_url: str | None,
    first_name: str,
    first_pct: int,
    second_name: str,
    second_pct: int,
    expected_names: tuple[str, str],
) -> MossSimilarityMatch | None:
    seed_name, roundtrip_name = (name.lower() for name in expected_names)
    normalized_first = first_name.lower()
    normalized_second = second_name.lower()

    if normalized_first == seed_name and normalized_second == roundtrip_name:
        return MossSimilarityMatch(
            report_url=report_url,
            match_url=match_url,
            seed_percentage=first_pct,
            roundtrip_percentage=second_pct,
        )
    if normalized_first == roundtrip_name and normalized_second == seed_name:
        return MossSimilarityMatch(
            report_url=report_url,
            match_url=match_url,
            seed_percentage=second_pct,
            roundtrip_percentage=first_pct,
        )
    return None
