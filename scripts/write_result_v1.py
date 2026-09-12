"""Regenerate numeric tables for RESULT_v1.1.md from frozen experiment artifacts."""
from pathlib import Path
from collections import Counter
from datetime import datetime
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
    if Path(output).name == "RESULT_v1.1.md":
        if not s["complete"] or len(metas) != 3 or any(x["phase"] != "main" for x in metas):
            raise ValueError("The final result requires all three completed main runs")
        audit = read_json(Path(summary_path).parent / "completion_audit.json")
        if not audit["passed"] or audit["observed"] != len(s["observations"]):
            raise ValueError("The final result requires the raw-artifact completion audit")
    labels = {"cpp-to-c": "C", "cpp-to-java": "Java", "cpp-to-python": "Python"}
    headline = ", ".join(f"{labels[route]} {percent(a['by_confirmation']['5']['p_sf'])} ({a['by_confirmation']['5']['success_count']}/{a['evaluable_count']})" for route, a in agg.items())
    lines = ["# 1차 실험 결과 v1.1", "", f"확인 왕복 5회 기준 통합 SF 성공률은 {headline}였다. 이 비율과 실패 거리 d_SF를 주 결과로 사용하며, 짧은 실패 종료를 가까운 거리로 해석하지 않는다.", "", "## 실험 범위와 방법", "",
             f"실험 단위는 (문제, 경로, run-id)이다. 원본 검증을 통과한 {p}문제, C/Java/Python 3경로, {len(metas)}회 반복으로 총 {len(s['observations'])}개 관측을 수집했다. 예비 실행은 본 실험에 합산하지 않았다.", "",
             "SF(Stabilized and Functional)는 후보 안정화가 존재하고, 후보까지 모든 중간/복원 단계가 fixture를 통과하며, 추가 확인 왕복에서도 동일한 정규화 토큰 해시와 기능 통과가 유지된 경우다. 후보 탐색 상한 K=10, 확인 왕복 상한 c_max=5이다. 첫 왕복은 t=1이고 tau는 확인 왕복을 제외한 후보 시점이다. parse_error는 분모에 포함한다.", "",
             f"모델: {m['server']['model']}, 양자화 {m['server']['quantization']['name']}, 로드 컨텍스트 {m['server']['config']['context_length']}, LM Studio {m['server']['lmstudio_version']}. temperature=0, max_tokens={m['lmstudio']['max_tokens']}. 컴파일/fixture당 시간 제한 {m['runtime']['timeout_seconds']}초. 요청의 나머지 디코딩 설정은 `{m['decoding']}`이다.", "",
             f"실행 스케줄은 `{m.get('execution_schedule', {'parallel_runs': 1, 'parallel_routes_per_run': 1})}`이다. 본 실험의 3개 run은 동시에 실행하며 각 run 내부의 문제·경로·번역 단계는 순차 실행한다. 병렬 부하도 실험 조건의 일부다.", "",
             f"실험 버전 `{m['experiment_version']}`, 조건 해시 `{m['condition_hash']}`, 검증 해시 `{m['validation_hash']}`. 실행 코드 커밋 `{m['code']['commit']}`, lock SHA256 `{m['code']['lock_hash']}`. Python과 도구 버전, 파일별 해시 및 실제 소스 스냅샷은 각 run의 run_metadata.json과 code_snapshot에 보존한다.", "",
             "문제 집합: " + ", ".join(m["problem_ids"]) + ".", "",
             "## 표 1. 안정화와 기능 보존의 성공률 및 실패 거리", "",
             "통합 비율의 95% 구간은 문제 단위 percentile bootstrap 2,000회(seed=20260911)로 계산했다. 같은 문제의 모든 경로와 반복을 함께 재표집한다. 세 반복은 독립 문제 수를 늘리지 않는다.", "",
             "| 경로 | c | 성공/평가 | p_SF (95% CI) | d_SF (95% CI) | CI 상태 |",
             "|---|---:|---:|---|---|---|"]
    environment = m["validation_snapshot"]["environment"]
    details = [f"실행 환경은 {environment['os']}, Python {environment['python_version']}이다. 생성 Python 코드도 `{environment['python_executable']}`로 실행했다.", "",
               "| 도구 | 기록된 버전 | 실행 경로 |", "|---|---|---|"]
    for tool, info in environment["toolchains"].items():
        details.append(f"| {tool} | {info['version'].splitlines()[0]} | `{info['path']}` |")
    details += ["", f"컴파일 옵션: `{environment['compile_options']}`. AST 패키지: `{environment['ast_packages']}`. AST 제한: `{m['ast']}`(노드 수, 초, MiB). 표와 상자그림의 사분위수는 선형 보간(R type=7)을 사용한다.", "",
                f"프롬프트 버전 `{m['prompt_template_version']}`, 실제 템플릿 SHA256 `{m['code']['prompt_template_hash']}`, 추출기 SHA256 `{m['code']['extractor_hash']}`. 실행 당시 코드와 보고서 출력 보완 이력은 `docs/EXPERIMENT_v1_log.md`에서 구분한다.", ""]
    position = lines.index("## 표 1. 안정화와 기능 보존의 성공률 및 실패 거리")
    lines[position:position] = details
    for route, a in agg.items():
        for c in ("1", "5"):
            v = a["by_confirmation"][c]
            lines.append(f"| {route} | {c} | {v['success_count']}/{a['evaluable_count']} | {percent(v['p_sf'])} {ci(v['p_sf_ci95'])} | {percent(v['d_sf'])} {ci(v['d_sf_ci95'])} | {v['ci_status']} |")
    lines += ["", "경로 차이 역시 같은 문제를 함께 재표집해 계산했다. 아래 구간이 0을 포함하면 이번 표본에서 차이의 방향이 명확하다고 판단하지 않는다.", "",
              "| 경로 차이 (앞-뒤) | c | p_SF 차이 | 대응 bootstrap 95% CI |", "|---|---:|---:|---|"]
    for pair, by_c in s["paired_route_differences"].items():
        left, right = pair.split(" minus ")
        for c in ("1", "5"):
            difference = agg[left]["by_confirmation"][c]["p_sf"]-agg[right]["by_confirmation"][c]["p_sf"]
            bounds = by_c[c]["p_sf_difference_ci95"]
            formatted = "NA" if bounds is None else f"[{100*bounds[0]:.1f}, {100*bounds[1]:.1f}]%p"
            lines.append(f"| {pair} | {c} | {100*difference:.1f}%p | {formatted} |")
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
    lines += ["", "기능 오류의 세부 상태는 다음과 같다. 각 셀은 건수이며 시간 초과는 실행 제한에 따른 결과다.", "",
              "| 경로 | 컴파일 오류 | 오답 | 실행 오류 | 실행 시간 초과 |", "|---|---:|---:|---:|---:|"]
    for route in agg:
        counts = Counter(row["status"] for row in s["observations"] if row["route"] == route)
        lines.append("| " + route + " | " + " | ".join(str(counts[k]) for k in ("compile_error", "wrong_answer", "runtime_error", "timeout")) + " |")
    lines += ["", "## 확인 횟수에 따른 변화", "", "| 경로 | c=0 | c=1 | c=2 | c=3 | c=4 | c=5 |", "|---|---|---|---|---|---|---|"]
    for route, a in agg.items():
        lines.append("| " + route + " | " + " | ".join(percent(a["by_confirmation"][str(c)]["p_sf"]) for c in range(6)) + " |")
    lost = sum(a["by_confirmation"]["0"]["success_count"]-a["by_confirmation"]["5"]["success_count"] for a in agg.values())
    lines += ["", f"c=0 후보·기능 조건을 만족한 뒤 c=5까지 유지하지 못한 관측은 {lost}건이다. 확인 횟수를 늘릴 때 p_SF가 낮아지는 정도는 후보 안정화와 관찰 기간 동안의 유지가 얼마나 다른지를 보여준다. 평탄한 구간이 나타나더라도 이 결과만으로 이후 모든 왕복의 영구 안정화를 보장하지 않는다.", ""]
    lines += ["", "## 그림", "",
              "![확인 횟수별 성공률](presentation/v1/results-v1.1/sf_confirmation.png)", "",
              "![실패 거리와 문제 단위 신뢰구간](presentation/v1/results-v1.1/sf_distance.png)", "",
              "![성공 조건부 후보 시점](presentation/v1/results-v1.1/tau.png)", "",
              "![성공 조건부 코드 변화](presentation/v1/results-v1.1/delta_0.png)", "",
              "![토큰 Dice와 AST TSED의 관계](presentation/v1/results-v1.1/dice_tsed.png)", ""]
    lines += ["## 실행 비용과 응답 감사", "",
              "API 시간은 호출별 경과 시간의 합이며, 병렬 실행의 실제 경과 시간과 다르다. 재시도는 실제 API 시도 수에서 논리 요청 수를 뺀 값이다.", "",
              "| run | 논리 요청 | API 시도 | API 시간 합(초) | 평균/최대(초) | 입력/출력 토큰 | API 오류 | 절단 | 형식 오류 |",
              "|---|---:|---:|---:|---|---|---:|---:|---:|"]
    finished = []
    for meta in metas:
        run_dir = Path(summary_path).parent.parent / meta["run_id"]
        diagnostic_path = run_dir / "diagnostics.json"
        if not diagnostic_path.exists():
            if Path(output).name == "RESULT_v1.1.md":
                raise ValueError(f"Missing response diagnostics: {diagnostic_path}")
            continue
        diagnostic = read_json(diagnostic_path)
        if Path(output).name == "RESULT_v1.1.md":
            step_glob = "IPOP_*/cpp-to-*/attempt-*/iterations/iter-*/step-*/"
            if diagnostic["logical_requests"] != len(list(run_dir.glob(step_glob + "llm-request.json"))) or diagnostic["api_attempt_count"] != len(list(run_dir.glob(step_glob + "api-attempt-*.json"))):
                raise ValueError(f"Response diagnostics must be refreshed: {diagnostic_path}")
        lines.append(f"| {meta['run_id']} | {diagnostic['logical_requests']} | {diagnostic['api_attempt_count']} | {number(diagnostic['call_seconds_total'], 1)} | {number(diagnostic['call_seconds_mean'])}/{number(diagnostic['call_seconds_max'])} | {diagnostic['prompt_tokens']}/{diagnostic['completion_tokens']} | {len(diagnostic['api_errors'])} | {len(diagnostic['truncations'])} | {len(diagnostic['parse_error_audit'])} |")
        for row in s["observations"]:
            if row["run_id"] == meta["run_id"]:
                manifest = read_json(run_dir / row["problem_id"] / row["route"] / row["attempt_id"] / "run.json")
                if manifest.get("finished_at"):
                    finished.append(datetime.fromisoformat(manifest["finished_at"]))
    if finished:
        start = min(datetime.fromisoformat(meta["started_at"]) for meta in metas)
        end = max(finished)
        lines += ["", f"실험 시작부터 마지막 관측 종료까지 {(end-start).total_seconds()/60:.2f}분이 걸렸다(UTC {start.isoformat()} ~ {end.isoformat()}). 이 경과 시간은 최종 AST 집계·그림·보고서 작성 시간을 포함하지 않는다."]
    lines.append("")
    lines += ["", "## 부록: c=1 조건부 결과", "", "| 경로 | tau | Delta_0 Dice | Delta_0 sequence | Delta_0 AST |", "|---|---|---|---|---|"]
    for route, a in agg.items():
        v = a["conditional"]["1"]
        lines.append("| " + route + " | " + " | ".join([stat(v["tau"])] + [stat(v["delta_0"][k]) for k in ("token_multiset_dice", "token_sequence_ratio", "ast_tsed")]) + " |")
    lines += ["", "## 부록: 반복별 성공률", "", "| 경로 | run | c=1 | c=5 | c=5 Wilson 95% CI |", "|---|---|---|---|---|"]
    for route, a in agg.items():
        for run, v in a["per_run"].items():
            b = v["by_confirmation"]
            lines.append(f"| {route} | {run} | {percent(b['1']['p_sf'])} | {percent(b['5']['p_sf'])} | {ci(b['5']['p_sf_wilson_ci95'])} |")
    lines += ["", "| 경로 | c | run별 p_SF 평균 | 최소 | 최대 |", "|---|---:|---:|---:|---:|"]
    for route, a in agg.items():
        for c in ("1", "5"):
            v = a["repeatability"]["by_confirmation"][c]
            lines.append(f"| {route} | {c} | {percent(v['p_sf_mean'])} | {percent(v['p_sf_min'])} | {percent(v['p_sf_max'])} |")
    repeatability = s["hash_repeatability"]
    if repeatability is not None:
        lines += ["", f"같은 문제·경로·왕복 번호에서 세 run의 복원 C++ 해시를 비교했다. 비교 가능한 {repeatability['comparable_positions']}개 위치 중 {repeatability['matched_positions']}개에서 모두 일치했다(일치율 {percent(repeatability['all_run_hash_match_rate'])}). 미도달 또는 실패로 비교할 수 없는 위치는 {repeatability['unreached_or_failed_positions']}개이며, 후보/확인 단계가 서로 다른 위치는 {repeatability['phase_mismatch_positions']}개다. 이 일치율은 관측 위치에 대한 기술 통계이며 독립 표본의 성공률로 해석하지 않는다."]
    lines += ["", "## 부록: 출력 형식 오류 제외 민감도", "", "| 경로 | c | 기본 p_SF | 형식 오류 제외 p_SF | 제외 후 분모 | 제외된 성공 수 |", "|---|---:|---|---|---:|---:|"]
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
