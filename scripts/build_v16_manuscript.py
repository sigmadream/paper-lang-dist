"""저장된 v1.6 자료에서 원고 표·그림·Word 문서와 검증 근거를 만듭니다."""

import argparse
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import re
from urllib.parse import unquote

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "papers/v1.6"
REPORTS = {
    "GLM": ROOT
    / "artifacts-rtt-v1.6/live-commandcode-20261117/commandcode-glm53-v16-20261117/main/report",
    "Flash": ROOT
    / "artifacts-rtt-v1.6/live-ds41f-20261118/commandcode-ds41-flash-v16-20261118/main/report",
}
ROUTES = ("python", "java", "haskell", "prolog")
NAMES = dict(zip(ROUTES, ("Python", "Java", "Haskell", "Prolog")))
SOURCES = {}


def remember(path):
    path = Path(path)
    data = path.read_bytes()
    SOURCES[path.relative_to(ROOT).as_posix()] = {
        "sha256": hashlib.sha256(data).hexdigest(),
        "바이트": len(data),
    }
    return data


def read_rows(path):
    remember(path)
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def read_json(path):
    return json.loads(remember(path).decode("utf-8-sig"))


def percent(value):
    return "—" if value in (None, "") else f"{100 * float(value):.1f}"


def number(value):
    return "—" if value in (None, "") else f"{float(value):.3f}"


def table(headers, rows):
    return "\n".join(
        [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
        ]
        + ["| " + " | ".join(map(str, row)) + " |" for row in rows]
    )


def collect():
    rows = read_rows(PAPER / "results/임계치별-경로-결과.csv")
    primary = [
        row for row in rows if row["집계"] == "공식 원관측" and row["임계치"] == "0.85"
    ]
    assert len(primary) == 8
    evidence = {"출처": SOURCES, "검증": {}, "표": {}, "도표입력": primary}
    inputs = {}
    for model, folder in REPORTS.items():
        inputs[model] = {
            name: read_rows(folder / (name + ".csv"))
            for name in (
                "observations",
                "thresholds",
                "failures",
                "confirmation",
                "stages",
                "recursive_groups",
                "problems",
                "similarities",
                "comparisons",
            )
        }
        audit = read_json(folder.parent / "completion_audit.json")
        reproduction = read_json(folder / "reproducibility.json")
        evidence["검증"][model] = {
            "수집": audit,
            "재현": reproduction,
        }
        remember(folder / "model_metadata.json")
        actual_rows = [
            r for r in inputs[model]["observations"] if r["threshold"] == "0.85"
        ]
        assert len(actual_rows) == 300
        for route in ROUTES:
            name = "cpp-via-" + route
            records = [r for r in actual_rows if r["route"] == name]
            assert len(records) == 75
            metric = next(
                r
                for r in primary
                if r["경로"] == name
                and (r["모델"].startswith("zai") == (model == "GLM"))
            )
            success = [r for r in records if r["category"] == "success"]
            valid = sum(r["category"] not in ("invalid", "incomplete") for r in records)
            assert len(success) == int(metric["성공"])
            assert valid == int(metric["유효분모"])
            assert math.isclose(float(metric["P"]), len(success) / valid)
            if success:
                mean_hops = sum(int(r["reached_step"]) for r in success) / len(success)
                assert math.isclose(float(metric["H"]), mean_hops)
                assert math.isclose(
                    float(metric["D"]), mean_hops / (len(success) / valid)
                )
            else:
                assert metric["H"] == metric["D"] == ""
            assert (
                sum(
                    int(metric[key])
                    for key in ("성공", "기능실패", "홉한도", "무효", "미완료")
                )
                == 75
            )
    audited_confirmation = read_rows(
        ROOT
        / "artifacts-rtt-v1.6/live-commandcode-20261117/glm53-audit-confirmation.csv"
    )
    evidence["GLM_감사후확인_원표"] = audited_confirmation
    remember(
        ROOT / "artifacts-rtt-v1.6/live-commandcode-20261117/glm53-failure-policy.json"
    )
    remember(ROOT / "artifacts-rtt-v1.6/live-ds41f-20261118/측정불가-감사.json")
    selection = read_json(PAPER / "data/selection.json")
    for path in (PAPER / "sources").glob("*.docx"):
        remember(path)

    def metrics(model, route, threshold="0.85", policy="공식 원관측"):
        return next(
            row
            for row in rows
            if row["모델"].startswith("zai") == (model == "GLM")
            and row["경로"] == "cpp-via-" + route
            and row["임계치"] == threshold
            and row["집계"] == policy
        )

    evidence["본문_보조근거"] = {}
    for model, data in inputs.items():
        failures = {}
        for route in ROUTES:
            failures[NAMES[route]] = dict(
                Counter(
                    row["reason"]
                    for row in data["observations"]
                    if row["threshold"] == "0.85"
                    and row["route"] == "cpp-via-" + route
                    and row["category"] == "functional_failure"
                )
            )
        comparisons = [
            row
            for row in data["comparisons"]
            if row["threshold"] == "0.85"
            and row["metric"] == "D"
            and row["left"] == "cpp-via-python"
            and row["right"] == "cpp-via-java"
        ]
        assert comparisons[0]["confirmatory_eligible"] == "False"
        assert comparisons[0]["interval_kind"] == "unadjusted_95"
        confirmation = (
            [r for r in audited_confirmation if r["version"] == "audit_derived"]
            if model == "GLM"
            else data["confirmation"]
        )
        passed = sum(int(row["passed"]) for row in confirmation)
        failed = sum(int(row["failed"]) for row in confirmation)
        unavailable = sum(int(row["unavailable"]) for row in confirmation)
        evidence["본문_보조근거"][model] = {
            "주임계치_기능실패사유": failures,
            "Python_Java_D_기술비교": comparisons,
            "확인": {
                "유지": passed,
                "실패": failed,
                "불가": unavailable,
                "판단가능": passed + failed,
                "유지율": passed / (passed + failed),
            },
            "재귀문제별": [
                r
                for r in data["problems"]
                if r["threshold"] == "0.85"
                and r["problem_id"] in ("IPOP_11729", "IPOP_1992", "IPOP_9663")
            ],
        }
    assert evidence["본문_보조근거"]["Flash"]["확인"]["유지"] == 75
    assert evidence["본문_보조근거"]["GLM"]["확인"]["판단가능"] == 120
    remember(ROOT / "configs/v1.6/providers/commandcode_glm53_experiment.yaml")
    remember(
        ROOT / "configs/v1.6/providers/commandcode_deepseek_v41_flash_20261118.yaml"
    )
    remember(ROOT / "artifacts-rtt-v1.6/validation/validation.json")
    remember(ROOT / "artifacts-rtt-v1.6/live-ds41f-20261118/최종-기계검증.json")
    labels = {
        "IPOP_11729": "다중 재귀·이동 순서 출력",
        "IPOP_2110": "반복 이분탐색·탐욕 배치",
        "IPOP_1992": "사분면 재귀·결과 결합",
        "IPOP_2579": "배열 기반 동적 계획법",
        "IPOP_5567": "깊이 제한 그래프 탐색",
        "IPOP_10988": "문자열 대칭 비교",
        "IPOP_1929": "반복·소수의 체",
        "IPOP_2609": "반복 유클리드 알고리즘",
        "IPOP_9012": "순차 괄호 균형 검사",
        "LC_0053": "반복·최대 부분배열 갱신",
        "LC_0062": "격자 경로 동적 계획법",
        "IPOP_9663": "재귀·되추적·가변 상태 복원",
        "LC_0242": "문자 빈도 집계",
        "LC_0283": "배열 원소 이동·상태 갱신",
        "LC_0338": "비트 수 동적 계획법",
    }
    tables = evidence["표"]
    tables["문제"] = table(
        ["문제", "내용", "기준 C++ 구현 특성"],
        [
            [r["problem_id"], r["display_name"], labels[r["problem_id"]]]
            for r in selection["problems"]
        ],
    )
    tables["주결과"] = table(
        ["모델", "경로", "성공/유효", "P(%)", "H(홉)", "D"],
        [
            [
                model,
                NAMES[route],
                f'{m["성공"]}/{m["유효분모"]}',
                percent(m["P"]),
                number(m["H"]),
                number(m["D"]),
            ]
            for model in REPORTS
            for route in ROUTES
            for m in [metrics(model, route)]
        ],
    )
    tables["분류"] = table(
        ["모델", "경로", "성공", "기능 실패", "홉 한도", "측정 불가 무효"],
        [
            [model, NAMES[route], m["성공"], m["기능실패"], m["홉한도"], m["무효"]]
            for model in REPORTS
            for route in ROUTES
            for m in [metrics(model, route)]
        ],
    )
    tables["첫왕복"] = table(
        ["모델", "경로", "정방향 기능 통과", "역방향 기능 통과(조건부)"],
        [
            [
                model,
                NAMES[route],
                f'{a["passed"]}/{a["assessable"]}',
                f'{b["passed"]}/{b["assessable"]}',
            ]
            for model in REPORTS
            for route in ROUTES
            for a in [
                next(
                    r
                    for r in inputs[model]["stages"]
                    if r["route"] == "cpp-via-" + route
                    and r["phase"] == "discovery"
                    and r["step"] == "1"
                )
            ]
            for b in [
                next(
                    r
                    for r in inputs[model]["stages"]
                    if r["route"] == "cpp-via-" + route
                    and r["phase"] == "discovery"
                    and r["step"] == "2"
                )
            ]
        ],
    )
    confirmation_rows = []
    for model in REPORTS:
        confirmation_input = (
            [r for r in audited_confirmation if r["version"] == "audit_derived"]
            if model == "GLM"
            else inputs[model]["confirmation"]
        )
        for row in confirmation_input:
            values = dict(row)
            confirmation_rows.append(
                [
                    model,
                    NAMES[row["route"].split("-via-")[1]],
                    values["primary_successes"],
                    values["passed"],
                    values["failed"],
                    values["unavailable"],
                    percent(values["retention_rate"]),
                ]
            )
    # 감사 원표에 5/9/1/14가 실제 존재하는지 확인합니다.
    assert any(
        r.get("route") == "cpp-via-haskell"
        and r.get("version") == "audit_derived"
        and r.get("passed") == "5"
        and r.get("failed") == "9"
        and r.get("unavailable") == "1"
        for r in audited_confirmation
    ), audited_confirmation
    tables["확인"] = table(
        ["모델", "경로", "최초 성공", "유지", "실패", "확인 불가", "유지율(%)"],
        confirmation_rows,
    )
    tables["민감도"] = table(
        ["모델", "경로", "P: 0.80→0.85→0.90(%)", "D: 0.80→0.85→0.90"],
        [
            [
                model,
                NAMES[route],
                " → ".join(percent(m["P"]) for m in values),
                " → ".join(number(m["D"]) for m in values),
            ]
            for model in REPORTS
            for route in ROUTES
            for values in [
                [
                    metrics(
                        model,
                        route,
                        t,
                        "HTTP 524 감사 후" if model == "GLM" else "공식 원관측",
                    )
                    for t in ("0.80", "0.85", "0.90")
                ]
            ]
        ],
    )
    tables["구조"] = table(
        ["모델", "경로", "성공 표본 n", "인접 유사도 중앙값", "원본 유사도 중앙값"],
        [
            [model, NAMES[route], a["n"], number(a["median"]), number(b["median"])]
            for model in REPORTS
            for route in ROUTES
            for a in [
                next(
                    r
                    for r in inputs[model]["similarities"]
                    if r["threshold"] == "0.85"
                    and r["route"] == "cpp-via-" + route
                    and r["scope"] == "adjacent_at_reach"
                )
            ]
            for b in [
                next(
                    r
                    for r in inputs[model]["similarities"]
                    if r["threshold"] == "0.85"
                    and r["route"] == "cpp-via-" + route
                    and r["scope"] == "origin_at_reach"
                )
            ]
        ],
    )
    tables["재귀"] = table(
        [
            "모델",
            "경로",
            "재귀 3문제: 성공/유효",
            "P(%)",
            "비교 12문제: 성공/유효",
            "P(%)",
        ],
        [
            [
                model,
                NAMES[route],
                f'{a["success"]}/{a["valid"]}',
                percent(a["P"]),
                f'{b["success"]}/{b["valid"]}',
                percent(b["P"]),
            ]
            for model in REPORTS
            for route in ROUTES
            for a in [
                next(
                    r
                    for r in inputs[model]["recursive_groups"]
                    if r["route"] == "cpp-via-" + route and r["group"] == "recursive"
                )
            ]
            for b in [
                next(
                    r
                    for r in inputs[model]["recursive_groups"]
                    if r["route"] == "cpp-via-" + route and r["group"] == "comparison"
                )
            ]
        ],
    )
    return evidence, inputs


def figures(evidence):
    folder = PAPER / "figures"
    folder.mkdir(exist_ok=True)
    plt.rcParams.update(
        {
            "font.family": "Malgun Gothic",
            "axes.unicode_minus": False,
            "font.size": 10,
            "pdf.fonttype": 42,
        }
    )
    colors = ("#2b607c", "#be603b")
    primary = evidence["도표입력"]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), layout="constrained")
    for index, (key, label) in enumerate(
        (("P", "도달률 P(%)"), ("H", "성공 조건부 평균 H(홉)"), ("D", "조작적 거리 D"))
    ):
        for model_index, model in enumerate(REPORTS):
            selected = [
                r for r in primary if r["모델"].startswith("zai") == (model == "GLM")
            ]
            values = [float(r[key]) if r[key] else np.nan for r in selected]
            if key == "P":
                values = [v * 100 for v in values]
            x = np.arange(4) + (model_index - 0.5) * 0.35
            axes[index].bar(
                x, values, width=0.34, label=model, color=colors[model_index]
            )
            for position, value in zip(x, values):
                if np.isnan(value):
                    axes[index].text(
                        position, 0.5, "결측", ha="center", fontsize=8, rotation=90
                    )
        axes[index].set_xticks(range(4), NAMES.values(), rotation=20)
        axes[index].set_ylabel(label)
        axes[index].spines[["top", "right"]].set_visible(False)
        if key == "P":
            axes[index].set_ylim(0, 100)
    axes[0].legend(frameon=False)
    save_figure(fig, folder / "fig2_primary_metrics")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.3), sharey=True)
    fig.subplots_adjust(left=0.075, right=0.99, top=0.87, bottom=0.25, wspace=0.06)
    categories = (
        ("성공", "성공", "#477d66"),
        ("기능실패", "기능 실패", "#b45b4b"),
        ("홉한도", "홉 한도", "#d5ad54"),
        ("무효", "측정 불가", "#8c8c8c"),
    )
    for axis, model in zip(axes, REPORTS):
        selected = [
            r for r in primary if r["모델"].startswith("zai") == (model == "GLM")
        ]
        base = np.zeros(4)
        for key, label, color in categories:
            values = np.array([int(r[key]) for r in selected])
            axis.bar(range(4), values, bottom=base, label=label, color=color)
            base += values
        axis.set_title(model)
        axis.set_xticks(range(4), NAMES.values(), rotation=20)
        axis.set_ylim(0, 80)
        axis.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("계획된 경로별 75슬롯의 분류")
    handles, labels = axes[1].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, fontsize=10, loc="lower center", ncol=4)
    save_figure(fig, folder / "fig3_outcomes")


def save_figure(fig, path):
    fig.savefig(path.with_suffix(".png"), dpi=220)
    fig.savefig(path.with_suffix(".pdf"), metadata={"Title": "v1.6 실험 원고 그림"})
    plt.close(fig)


def update_tables(evidence):
    path = PAPER / "manuscript.md"
    text = path.read_text(encoding="utf-8-sig")
    for name, content in evidence["표"].items():
        pattern = rf"<!-- 표:{name} -->.*?<!-- /표:{name} -->"
        replacement = f"<!-- 표:{name} -->\n{content}\n<!-- /표:{name} -->"
        text, count = re.subn(pattern, lambda _: replacement, text, flags=re.S)
        assert count == 1, name
    path.write_text(text, encoding="utf-8", newline="\n")
    return text


def plain_text(text):
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    return text.replace("`", "")


def add_linked_paragraph(document, text):
    paragraph = document.add_paragraph()
    offset = 0
    for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
        paragraph.add_run(text[offset : match.start()])
        relationship = document.part.relate_to(
            match.group(2), RELATIONSHIP_TYPE.HYPERLINK, is_external=True
        )
        link = OxmlElement("w:hyperlink")
        link.set(qn("r:id"), relationship)
        run = OxmlElement("w:r")
        properties = OxmlElement("w:rPr")
        font = OxmlElement("w:rFonts")
        font.set(qn("w:eastAsia"), "맑은 고딕")
        properties.append(font)
        run.append(properties)
        value = OxmlElement("w:t")
        value.text = match.group(1)
        run.append(value)
        link.append(run)
        paragraph._p.append(link)
        offset = match.end()
    paragraph.add_run(text[offset:])
    return paragraph


def export_word(text):
    document = Document()
    section = document.sections[0]
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    section.top_margin = section.bottom_margin = Cm(2)
    section.left_margin = section.right_margin = Cm(2)
    for name in ("Normal", "Title", "Heading 1", "Heading 2", "Heading 3", "Caption"):
        style = document.styles[name]
        style.font.name = "Malgun Gothic"
        style.element.get_or_add_rPr().rFonts.set(qn("w:eastAsia"), "맑은 고딕")
        style.font.size = Pt(10.5 if name == "Normal" else 12)
        style.font.bold = False
        style.font.italic = False
        style.font.color.rgb = RGBColor(0, 0, 0)
        style.paragraph_format.space_after = Pt(6)
        style.paragraph_format.line_spacing = 1.3
    document.styles["Title"].font.size = Pt(18)
    footer = section.footer.paragraphs[0]
    footer.alignment = 2
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    footer._p.append(field)
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        index += 1
        if not line.strip() or line.startswith("<!--"):
            continue
        if line.startswith("|"):
            block = [line]
            while index < len(lines) and lines[index].startswith("|"):
                block.append(lines[index])
                index += 1
            rows = [
                [plain_text(cell.strip()) for cell in row.strip("|").split("|")]
                for row in block
            ]
            rows = [
                row
                for row in rows
                if not all(re.fullmatch(r":?-+:?", cell) for cell in row)
            ]
            grid = document.add_table(rows=0, cols=len(rows[0]))
            grid.style = "Table Grid"
            for row in rows:
                cells = grid.add_row().cells
                for cell, value in zip(cells, row):
                    cell.text = value
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            run.font.size = Pt(8)
                            run.bold = run.italic = False
            header = OxmlElement("w:tblHeader")
            grid.rows[0]._tr.get_or_add_trPr().append(header)
            continue
        picture = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", line)
        if picture:
            path = (PAPER / picture.group(2)).resolve()
            document.add_picture(str(path), width=Cm(16.6))
            continue
        heading = re.match(r"^(#{1,4}) (.+)", line)
        if heading:
            level, title = len(heading.group(1)), plain_text(heading.group(2))
            if level == 1:
                document.add_paragraph(title, "Title")
            else:
                document.add_heading(title, level=level - 1)
        else:
            add_linked_paragraph(document, line)
    for paragraph in document.paragraphs:
        for run in paragraph.runs:
            run.bold = run.italic = False
    output = PAPER / "v1.6.docx"
    document.save(output)
    reopened = Document(output)
    assert len(reopened.tables) == 10
    assert "6.593" in " ".join(
        cell.text for grid in reopened.tables for row in grid.rows for cell in row.cells
    )
    return output


def verify_manuscript(text, evidence, docx_path):
    """원고 전체의 표·그림·인용·로컬 참조와 파생 수치를 대조합니다."""
    document = Document(docx_path)
    markdown_tables = []
    active = []
    for line in text.splitlines() + [""]:
        if line.startswith("|"):
            row = [plain_text(cell.strip()) for cell in line.strip("|").split("|")]
            if not all(re.fullmatch(r":?-+:?", value) for value in row):
                active.append(row)
        elif active:
            markdown_tables.append(active)
            active = []
    actual_tables = [
        [[cell.text for cell in row.cells] for row in grid.rows]
        for grid in document.tables
    ]
    assert actual_tables == markdown_tables
    assert len(actual_tables) == 10
    assert len(document.inline_shapes) == 2
    assert all(
        not run.bold and not run.italic for p in document.paragraphs for run in p.runs
    )
    missing = []
    local_links = 0
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if target.startswith(("https://", "http://")):
            continue
        local_links += 1
        if not (PAPER / unquote(target.split("#", 1)[0])).resolve().is_file():
            missing.append(target)
    assert not missing, missing
    before_bibliography, bibliography = text.split("## 참고문헌", 1)
    cited = {
        number
        for group in re.findall(r"\[([0-9]+(?:,[0-9]+)*)\]", before_bibliography)
        for number in group.split(",")
    }
    entries = set(re.findall(r"^\[(\d+)\]", bibliography, re.M))
    assert cited == entries == set(map(str, range(1, 8)))
    glm = evidence["본문_보조근거"]["GLM"]
    flash = evidence["본문_보조근거"]["Flash"]
    assert glm["확인"] == {
        "유지": 55,
        "실패": 65,
        "불가": 2,
        "판단가능": 120,
        "유지율": 55 / 120,
    }
    assert flash["확인"] == {
        "유지": 75,
        "실패": 93,
        "불가": 2,
        "판단가능": 168,
        "유지율": 75 / 168,
    }
    assert flash["주임계치_기능실패사유"]["Prolog"] == {
        "runtime_error": 33,
        "wrong_answer": 8,
        "timeout": 5,
        "compile_error": 2,
    }
    assert flash["주임계치_기능실패사유"]["Python"] == {"timeout": 3}
    body_start = text.index("## 3. 실험 결과 및 해석")
    body_end = text.index("## 5. 결론")
    record = {
        "통과": True,
        "전체표": len(actual_tables),
        "삽입그림": len(document.inline_shapes),
        "참고문헌": sorted(entries),
        "로컬참조": local_links,
        "누락참조": missing,
        "원고문자수": len(text),
        "결과해석_논의_문자수": body_end - body_start,
        "입력원자료": len(SOURCES),
        "입력원자료_변경": 0,
        "실제추가실험": False,
        "산출물": {},
    }
    for path in [
        PAPER / "manuscript.md",
        docx_path,
        Path(__file__),
        *(PAPER / "figures").glob("*.*"),
    ]:
        record["산출물"][path.relative_to(ROOT).as_posix()] = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
    (PAPER / "results/원고-검증결과.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--prepare-data",
        action="store_true",
        help="원고 작성 전 해석 자료만 준비합니다",
    )
    args = parser.parse_args()
    evidence, inputs = collect()
    figures(evidence)
    output = PAPER / "results/원고-해석근거.json"
    if not args.prepare_data:
        text = update_tables(evidence)
        docx_path = export_word(text)
        assert len(re.findall(r"^# ", text, re.M)) == 1
        assert not re.search(r"\*\*|__|(?<!\w)\*[^\n*]+\*", text)
        assert "{{" not in text
        validation = verify_manuscript(text, evidence, docx_path)
        evidence["원고검증"] = {
            "마크다운": (PAPER / "manuscript.md").relative_to(ROOT).as_posix(),
            "Word": docx_path.relative_to(ROOT).as_posix(),
            "자동생성표": len(evidence["표"]),
            "전체표": 10,
            "원고문자수": len(text),
            "중점": "경로별 도달률·조건부 홉·실패·확인·민감도·측정 한계의 해석",
            "검증결과": validation,
        }
    for relative, expected in SOURCES.items():
        assert (
            hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
            == expected["sha256"]
        ), relative
    evidence["원자료_변경"] = 0
    output.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "통과": True,
                "출처수": len(SOURCES),
                "표수": len(evidence["표"]),
                "원자료변경": 0,
                "원고": evidence.get("원고검증"),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
