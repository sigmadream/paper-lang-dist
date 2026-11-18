"""실제 종료 감사에서 한국어 최종 보고서를 작성합니다."""

import json
from decimal import Decimal
from pathlib import Path

ROOT = Path.cwd()
OUTPUT = ROOT / "artifacts-rtt-v1.6/live-ds41f-20261118"
data = json.loads((OUTPUT / "종료후-감사.json").read_text(encoding="utf-8"))
phases = data["phases"]
session = data["session"]


def money(value):
    return format(Decimal(value).quantize(Decimal("0.000000001")), "f")


lines = [
    "# DeepSeek V4.1 Flash 실행 보고서",
    "",
    f"지정한 단일 래퍼를 1회 실행하였고 종료 코드는 {data['wrapper_exitcode']}입니다. 독립 사전 점검 {phases['preflight']['saved_slots']}/1회, 파일럿 {phases['pilot']['saved_slots']}/12슬롯, 본 실험 {phases['main']['saved_slots']}/300슬롯을 저장하였습니다. 실행 완료 판정은 `{data['status']}`이며, 측정 불가 3슬롯으로 임계치별 분석 완전성은 모두 false인 점을 별도로 보존합니다.",
    "",
    "## 실행 범위와 근거",
    "",
    f"- 캠페인: `{data['campaign_id']}`",
    f"- 정확 모델: `{data['model_id']}`",
    "- 공급자: `https://api.commandcode.ai/provider/v1/chat/completions`",
    "- 생성 설정: `max_tokens=16384`, `reasoning_effort=low`",
    "- temperature·top_p·seed 미추가, 미보고 실효 설정 null",
    f"- 실행 시작: {session['started_at']}",
    f"- 실행 종료: {session['finished_at']}",
    "- 유료 래퍼 실행 1회, 자동 재시작 0회",
    f"- 실제 독립 검토자 세션: `{data['reviewer_session_id']}`",
    f"- 준비 manifest 파일 SHA-256: `{data['manifest_file_sha256']}`",
    f"- 실제 동결 계약: `{data['main_design']['contract_hash']}`",
    "",
    "실제 신규 Orca 독립 검토를 받은 뒤 현재 소스·보고서·manifest 해시를 확인하고 지정 uv 명령을 실행하였습니다. [실행 전 관문](실행전-관문검증.json), [실제 명령·프로세스·시각](execution-session.json), [독립 검토](independent-review.json), [원출력](run.log), [실제 종료 코드](run.exitcode), [종료 감사](종료후-감사.json)를 보존하였습니다. 실행 근거의 source_manifest_sha256은 기존 구조의 정규화 객체 해시이며, 위 준비 manifest 파일 바이트 해시와 구분하여 감사 JSON에 둘 다 기록하였습니다.",
    "",
    "## 단계별 실제 결과",
    "",
    "| 단계 | 실제 결과 | 근거 |",
    "|---|---|---|",
    "| 독립 사전 점검 | OK 응답 1회, 정확 모델 일치 | 캠페인 preflight.json |",
    "| 파일럿 | 12/12 저장, 구조·세 임계치 완전성 통과 | pilot/completion_audit.json |",
    "| 본 실험 동결 | 새 계약 동결, 제안 계약과 일치 | main_design.json |",
    f"| 본 실험 수집 | {phases['main']['saved_slots']}/300 저장, 미저장 {300-phases['main']['saved_slots']} | main/completion_audit.json |",
    f"| 공식 보고 | 생성 여부 {data['official_report_exists']} | main/report/summary.json 및 JSON·CSV·그림·재현 묶음 |",
    f"| 수치 재현 | 통과 여부 {(data['reproducibility'] or {}).get('passed')} | main/report/reproducibility.json |",
    "",
    "공식 보고와 재현은 단일 래퍼 내부 함수로 수행되므로 별도 CLI 종료 코드는 해당 없음(null)입니다. 재현 검증은 네트워크·SDK·하위 프로세스를 차단하고 두 번의 수치 재생성과 최종 출력의 JSON·CSV·그림 입력 동일성을 비교합니다. 그림 렌더링 바이트와 PDF 비수치 메타데이터는 비교 대상에서 제외합니다. 수치 재현 통과는 분석 완전성이나 가설 지지를 뜻하지 않습니다.",
    "",
    "사전 점검·파일럿·동결과 75·150·225·300슬롯 이정표 및 공식 보고·재현 결과를 조정자께 전달하였으며, 전달 근거는 조정자-단계보고.jsonl에 있습니다. 각 중간 감사의 시점과 현재 진행 예약은 종료 후 불명 예약 판정과 구분합니다.",
    "",
    "## 임계치 결과와 측정 제한",
    "",
    "| 단계 | 임계치 | 성공 | 기능 실패 | 홉 한도 | invalid | 미저장 |",
    "|---|---|---:|---:|---:|---:|---:|",
]
for phase, label, planned in (("pilot", "파일럿", 12), ("main", "본 실험", 300)):
    for threshold in ("0.80", "0.85", "0.90"):
        values = phases[phase]["outcomes_by_threshold"][threshold]
        lines.append(
            f"| {label} | {threshold} | {values.get('success',0)} | {values.get('functional_failure',0)} | {values.get('hop_limit',0)} | {values.get('invalid',0)} | {planned-phases[phase]['saved_slots']} |"
        )
lines.extend(
    [
        "",
        "300슬롯의 구조 감사는 passed=true·미저장 0·오류 목록 없음입니다. 다만 IPOP_2609의 Haskell 경유 반복 2·3·5는 기능 평가를 통과한 후 유사도 측정 불가로 중지되었습니다. JPlag 후보 토큰 수가 각각 6·7·7개로 고정 최소 길이 9보다 작아 도구 종료 코드 1과 유사도 null을 보존하였습니다. 세 임계치의 complete_by_threshold는 모두 false이며, 위 invalid를 기능 실패나 성공으로 바꾸지 않았습니다.",
        "",
        "[측정 불가 감사](측정불가-감사.json)에 생성 코드·원관측 경로와 SHA-256, 실제 오류 원문을 연결하였습니다. 해당 슬롯을 대체하거나 생성 요청·측정을 추가 실행하지 않았고, 문제·평가·프롬프트·시드 20261117·홉·확인·임계치·중단 규칙도 변경하지 않았습니다. 기존 GLM 및 두 Pro의 관측·공급자 응답을 새 결과와 합산하지 않았습니다.",
        "",
        "## 비용·토큰·요청·전송",
        "",
        "| 단계 | 논리 요청 | 전송 | 정상응답 | 입력 토큰 | 출력 토큰 | 입력 내 캐시 | 추정 USD | 종료 예약 USD |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
)
for phase, label in (
    ("preflight", "사전 점검"),
    ("pilot", "파일럿"),
    ("main", "본 실험"),
):
    p = phases[phase]
    lines.append(
        f"| {label} | {p['logical_requests']} | {p['transport_attempts']} | {p['responses']} | {p['prompt_tokens']} | {p['completion_tokens']} | {p['cached_tokens']} | {money(p['known_estimated_cost_usd'])} | {money(p['reserved_usd'])} |"
    )
glm = data["preserved_glm_campaign"]
lines.extend(
    [
        "",
        f"신규 전체 알려진 추정액은 {money(data['known_estimated_cost_usd'])}달러, 종료 시 예약은 {money(data['reserved_usd'])}달러입니다. 사전 점검·파일럿·본 실험의 상한 0.23/49.28/48.62달러와 논리·전송 한도를 모두 지켰는지 감사한 결과는 {data['all_phase_limits_passed']}입니다. 백만 토큰당 피크 입력 0.30·출력 1.20·캐시입력 0.006달러를 실행 시간대와 관계없이 보수적 추정에 사용하였습니다. 실제 청구액은 미확인(null)이며 출력 토큰에는 공급자가 보고한 추론 토큰이 포함됩니다.",
        "",
        "| 별도 보존 캠페인 | 논리 요청 | 전송 | 알려진 추정액+예약 USD |",
        "|---|---:|---:|---:|",
        f"| GLM 20261117 | {glm['logical_requests']} | {glm['transport_attempts']} | {money(glm['known_estimated_plus_reserved_usd'])} |",
        "| Pro 20261117 | 99 | 100 | 1.045928856 |",
        "| Pro 20261118 | 147 | 147 | 1.039800264 |",
        "",
        f"기존 전 캠페인과 신규의 알려진 추정액·예약 합계는 {money(data['all_campaigns_known_estimated_plus_reserved_usd'])}달러입니다. GLM의 미사용 한도까지 전부 보존한 보수적 신규 배정 계산은 100.25+1.045928856+1.039800264+98.13=200.465729120달러로 전체 200.50달러 이내입니다. 이전 사전 점검 두 번과 이번 독립 사전 점검 한 번을 별도로 공개하며, 논리·전송 한도는 독립 캠페인별로 적용합니다. 기존 미해결 예약은 해제하지 않았고 GLM도 재실행하지 않았습니다.",
        "",
        "## 모델·안전·불변 감사",
        "",
        f"신규 정상응답 {data['normal_responses']}건의 정확 모델 일치 여부는 {data['all_models_exact']}, 계획 생성 옵션·미보고 실효값의 일치 여부는 {data['all_generation_as_planned']}입니다. 소스·검토 관문은 종료 후에도 통과하였습니다. 실행 소스·설정 {data['source_files']}개와 동결 사본, 기존 중요 근거 {data['legacy_guard_files']}개의 해시를 대조하였습니다.",
        "",
        f"종료 후 불명 요청 관문 통과 여부는 {data['unknown_guard_passed']}이며, 새 요청의 unknown·inflight와 불명 예약은 종료 감사의 단계별 목록에 그대로 공개합니다. 유료 래퍼 잔존 프로세스는 {len(data['running_paid_wrapper_processes'])}개, 실행 잠금 해제 여부는 {data['execution_lock_released']}, 실제 비밀정보 감사 통과 여부는 {data['secret_audit']['passed']}입니다. 인증값을 출력·복사하지 않았으며 서버 처리·실제 청구를 추측하지 않습니다.",
        "",
        f"기존 Pro 두 실행·GLM·기존 소스·설정 등 {data['original_artifact_count']:,}개 파일을 최초 보존 기준과 다시 읽어 대조하였고 변경은 {len(data['original_artifact_hash_differences'])}개입니다. [최초 기준](기존-보존기준.json)과 [종료 후 불변 검사](종료후-기존불변.json)를 함께 보존합니다. 관련 회귀 150개와 별도 실제 독립 회귀 26개의 결과는 준비·검토 시점의 실제 검사이며 이번 종료 시 전체 회귀를 다시 실행했다고 표시하지 않습니다.",
        "",
        "## 조정자 인계와 기록 종료",
        "",
        "신규 래퍼·두 설정·통합 검사와 이 출력 루트 전체를 인계합니다. 공식 산출물은 캠페인 main/report이며 원관측·원응답·생성 코드·원장은 캠페인 아래에 보존합니다. 검토 참조의 정확한 .test-tmp 파일·해시는 보존필수-검토참조.json, 신규 출력 전체의 실제 파일·크기·해시는 데이터-보존목록.json, 최종 검증은 최종-기계검증.json에 기록합니다. 원자료 기록을 마감한 뒤 main 반영과 v1.6 브랜치 생성은 조정자가 담당합니다. 이 작업자는 git add·commit·체크아웃·push나 추가 작업자를 생성하지 않았습니다.",
    ]
)
report = "\n".join(lines) + "\n"
report = report.replace(
    "이전 사전 점검 두 번과 이번 독립 사전 점검 한 번",
    "이전 Pro 사전 점검 두 번·GLM 사전 점검 한 번과 이번 Flash 독립 사전 점검 한 번",
)
report = report.replace("True", "통과").replace("False", "미통과")
(OUTPUT / "최종-실행보고서.md").write_text(report, encoding="utf-8")
print("실제 종료 감사에서 최종 실행보고서를 작성하였습니다.")
