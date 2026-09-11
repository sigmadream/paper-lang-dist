"""Regenerate numeric tables for RESULT_v1.1.md from frozen experiment artifacts."""
from pathlib import Path
import sys

from rttdist.experiment_io import read_json


def number(x, digits=3):
    return "NA" if x is None else f"{x:.{digits}f}"


def percent(x):
    return "NA" if x is None else f"{100*x:.1f}%"


def ci(x):
    return "NA" if x is None else f"[{percent(x[0])}, {percent(x[1])}]"


def stat(x):
    if x["n"] == 0:
        return "NA (n=0)"
    return f"{number(x['median'])} [{number(x['q1'])}, {number(x['q3'])}], n={x['n']}"


def write(summary_path, output):
    s = read_json(summary_path)
    metas = s["run_metadata"]
    m = metas[0]
    agg = s["rtt_route_aggregates"]
    p = len(m["problem_ids"])
    cmax = m["runtime"]["confirmation_cycles"]
    lines = ["# 1차 실험 결과 v1.1", "", "## 실험 범위와 방법", "",
             f"실험 단위는 (문제, 경로, run-id)이다. 원본 검증을 통과한 {p}문제, C/Java/Python 3경로, {len(metas)}회 반복으로 총 {len(s['observations'])}개 관측을 수집했다. 예비 실행은 본 실험에 합산하지 않았다.", "",
             "SF(Stabilized and Functional)는 후보 안정화가 존재하고, 후보까지 모든 중간/복원 단계가 fixture를 통과하며, 추가 확인 왕복에서도 동일한 정규화 토큰 해시와 기능 통과가 유지된 경우다. 후보 탐색 상한 K=10, 확인 왕복 상한 c_max=5이다. 첫 왕복은 t=1이고 tau는 확인 왕복을 제외한 후보 시점이다. parse_error는 분모에 포함한다.", "",
             f"모델: {m['server']['model']}, 양자화 {m['server']['quantization']['name']}, 로드 컨텍스트 {m['server']['config']['context_length']}, LM Studio {m['server']['lmstudio_version']}. temperature=0, max_tokens={m['lmstudio']['max_tokens']}. 컴파일/fixture당 시간 제한 {m['runtime']['timeout_seconds']}초. 요청의 나머지 디코딩 설정은 `{m['decoding']}`이다.", "",
             f"실험 버전 `{m['experiment_version']}`, 조건 해시 `{m['condition_hash']}`, 검증 해시 `{m['validation_hash']}`. 실행 코드 커밋 `{m['code']['commit']}`, lock SHA256 `{m['code']['lock_hash']}`. Python과 도구 버전, 파일별 해시 및 실제 소스 스냅샷은 각 run의 run_metadata.json과 code_snapshot에 보존한다.", "",
             "문제 집합: " + ", ".join(m["problem_ids"]) + ".", "",
             "## 표 1. 안정화와 기능 보존의 성공률 및 실패 거리", "",
             "통합 비율의 95% 구간은 문제 단위 percentile bootstrap 2,000회(seed=20260911)로 계산했다. 같은 문제의 모든 경로와 반복을 함께 재표집한다. 세 반복은 독립 문제 수를 늘리지 않는다.", "",
             "| 경로 | c | 성공/평가 | p_SF (95% CI) | d_SF (95% CI) | CI 상태 |",
             "|---|---:|---:|---|---|---|"]
    for route, a in agg.items():
        for c in ("1", "5"):
            v = a["by_confirmation"][c]
            lines.append(f"| {route} | {c} | {v['success_count']}/{a['evaluable_count']} | {percent(v['p_sf'])} {ci(v['p_sf_ci95'])} | {percent(v['d_sf'])} {ci(v['d_sf_ci95'])} | {v['ci_status']} |")
    lines += ["", "## 표 2. 성공 조건부 후보 시점과 코드 변화", "", "c=5 성공 집합만 사용한다. 값은 중앙값 [Q1, Q3], 유효 n이다. Delta_0는 원본 C++와 후보 C++ 사이의 1-유사도이다.", "",
              "| 경로 | tau | Delta_0 Dice | Delta_0 sequence | Delta_0 AST | AST 측정률 |", "|---|---|---|---|---|---|"]
    for route, a in agg.items():
        v = a["conditional"]["5"]
        d = v["delta_0"]
        lines.append(f"| {route} | {stat(v['tau'])} | {stat(d['token_multiset_dice'])} | {stat(d['token_sequence_ratio'])} | {stat(d['ast_tsed'])} | {percent(d['ast_tsed']['measurement_rate'])} |")
    lines += ["", "AST는 tree-sitter의 named 노드를 순서대로 사용하며 식별자는 추상화하고 연산자·리터럴 값은 보존한다. 삽입/삭제/변경 비용은 1/1/1이다. 이는 이번 실험의 TSED 정의이며 구문 구조 비교에 해당한다. AST 결측은 SF 결과를 바꾸지 않는다.", "",
              "## 표 3. 실패 이유", "", "c=5 기준이며 비율의 분모는 각 경로의 전체 평가 가능 관측 수다. 범주 비율의 합은 d_SF이다.", "",
              "| 경로 | 기능 오류 | 순환 | K 도달 | 확인 해시 변경 | 출력 형식 오류 |", "|---|---|---|---|---|---|"]
    for route, a in agg.items():
        cats = a["failures"]["categories"]
        cells = [f"{cats[k]['count']} ({percent(cats[k]['rate'])})" for k in ("functionality_error", "oscillation", "max_iterations", "confirmation_failed", "format_error")]
        lines.append("| " + route + " | " + " | ".join(cells) + " |")
    lines += ["", "## 확인 횟수에 따른 변화", "", "| 경로 | c=0 | c=1 | c=2 | c=3 | c=4 | c=5 |", "|---|---|---|---|---|---|---|"]
    for route, a in agg.items():
        lines.append("| " + route + " | " + " | ".join(percent(a["by_confirmation"][str(c)]["p_sf"]) for c in range(6)) + " |")
    lines += ["", "## 그림", "",
              "![확인 횟수별 성공률](presentation/v1/results-v1.1/sf_confirmation.png)", "",
              "![실패 거리와 문제 단위 신뢰구간](presentation/v1/results-v1.1/sf_distance.png)", "",
              "![성공 조건부 후보 시점](presentation/v1/results-v1.1/tau.png)", "",
              "![성공 조건부 코드 변화](presentation/v1/results-v1.1/delta_0.png)", "",
              "![토큰 Dice와 AST TSED의 관계](presentation/v1/results-v1.1/dice_tsed.png)", ""]
    lines += ["", "## 부록: c=1 조건부 결과", "", "| 경로 | tau | Delta_0 Dice | Delta_0 sequence | Delta_0 AST |", "|---|---|---|---|---|"]
    for route, a in agg.items():
        v = a["conditional"]["1"]
        lines.append("| " + route + " | " + " | ".join([stat(v["tau"])] + [stat(v["delta_0"][k]) for k in ("token_multiset_dice", "token_sequence_ratio", "ast_tsed")]) + " |")
    lines += ["", "## 부록: 반복별 성공률", "", "| 경로 | run | c=1 | c=5 | c=5 Wilson 95% CI |", "|---|---|---|---|---|"]
    for route, a in agg.items():
        for run, v in a["per_run"].items():
            b = v["by_confirmation"]
            lines.append(f"| {route} | {run} | {percent(b['1']['p_sf'])} | {percent(b['5']['p_sf'])} | {ci(b['5']['p_sf_wilson_ci95'])} |")
    lines += ["", "반복 해시 비교: " + str(s["hash_repeatability"]) + ".", "",
              "## 부록: 출력 형식 오류 제외 민감도", "", "| 경로 | c | 기본 p_SF | 형식 오류 제외 p_SF | 제외 후 분모 | 제외된 성공 수 |", "|---|---:|---|---|---:|---:|"]
    for route, a in agg.items():
        for c in range(6):
            b = a["by_confirmation"][str(c)]
            lines.append(f"| {route} | {c} | {percent(b['p_sf'])} | {percent(b['p_sf_excluding_parse_error'])} | {b['sensitivity_evaluable_count']} | {b['sensitivity_excluded_success_count']} |")
    lines += ["", "## 불확실성과 해석 한계", "",
              "단일 모델·단일 프롬프트와 선정 문제 집합의 탐색적 결과다. 언어 자체의 고유 거리로 일반화할 수 없다. SF는 관찰한 확인 횟수와 fixture에 대한 결과이며 영구 고정점이나 모든 입력의 실행 동치를 증명하지 않는다. 성공 조건부 tau와 Delta_0에는 선택 효과가 있으므로 실패 관측을 0이나 K로 대체하지 않는다.", "",
              "부트스트랩 CI가 degenerate이면 구간이 퇴화한 것이며 불확실성이 없다는 뜻이 아니다. 중앙값 CI는 유효 재표집이 95% 미만이면 unavailable로 기록한다. 상세 구간과 AST 결측 사유는 summary.json에 보존한다.", "",
              "## 재생성", "", "```powershell", "$env:UV_CACHE_DIR = 'D:/works/paper-lang-dist/.uv-cache'",
              "uv run rttdist report --config lmstudio_v1.yaml --runs " + ",".join(mm["run_id"] for mm in metas),
              "uv run python scripts/v1_checks.py artifacts-lmstudio/v1-combined/summary.json",
              ".tools/R/bin/x64/Rscript.exe --vanilla graph/v1/drawFigures.r artifacts-lmstudio/v1-combined/summary.json presentation/v1/results-v1.1",
              "uv run python scripts/write_result_v1.py artifacts-lmstudio/v1-combined/summary.json RESULT_v1.1.md", "```", ""]
    lines += ["## 부록: 조건부 중앙값 신뢰구간과 AST 결측", "",
              "| 경로 | c | 지표 | 중앙값 95% CI | 유효 재표집 | CI 상태 | 결측 사유별 수 |",
              "|---|---:|---|---|---:|---|---|"]
    for route, a in agg.items():
        for c in ("1", "5"):
            conditional = a["conditional"][c]
            for name, v in {"tau": conditional["tau"], **conditional["delta_0"]}.items():
                bounds = v["median_ci95"]
                formatted = "NA" if bounds is None else f"[{number(bounds[0])}, {number(bounds[1])}]"
                lines.append(f"| {route} | {c} | {name} | {formatted} | {v['valid_resamples']}/2000 | {v['ci_status']} | {v.get('excluded_by_reason', {})} |")
    lines.append("")
    notes = Path("docs/RESULT_v1.1_interpretation.md")
    if notes.exists():
        lines.extend([notes.read_text(encoding="utf-8"), ""])
    Path(output).write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    write(sys.argv[1], sys.argv[2])
