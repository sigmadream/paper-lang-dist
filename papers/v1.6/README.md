# v1.6 실험과 보고 재현 안내

이 판본은 승인된 [실험 설계](../../docs/superpowers/specs/2026-11-17-v1.6-experiment-design.md)를 구현합니다. `rtt-hops-v1.6` 관측만 사용하며 v1.5 원고와 과거 FPS 집계는 보존합니다. 저장소의 모의 테스트와 합성 보고는 라이브 실험 결과가 아닙니다.

## 작성한 논문 원고

2026-11-19에 v1.5 원고를 바탕으로 실험 해석을 확장한 [Word 원고](v1.6.docx)와 [Markdown 원고](manuscript.md)를 작성하였습니다. 경로별 실패 양상, 성공 조건부 홉 수, 확인 왕복의 유지율, 임계치 민감도, 재귀군 및 측정 한계를 중심으로 서술합니다. [작성·검증 기록](원고작성-검증기록.md)과 [표·그림 입력 및 원자료 해시](results/원고-해석근거.json)를 함께 확인해 주십시오.

## 실행 순서

저장소 루트에서 실행해 주십시오. Python 환경은 uv로 관리하며 그림에는 analysis 선택 의존성이 필요합니다. 공급자 설정의 모델·도구 경로·인증 환경변수·예산을 실행 전에 지정해 주십시오.

```powershell
uv sync --extra analysis
uv run python scripts/prepare_v16_corpus.py --selection papers/v1.6/data/selection.json --source-root problem --destination data/rtt-v1.6
uv run python scripts/validate_v16_corpus.py --config configs/v1.6/experiment.yaml
uv run python scripts/preflight_v16.py --config configs/v1.6/experiment.yaml --provider-config configs/v1.6/providers/openai.yaml --output artifacts-rtt-v1.6/preflight-static.json
```

기준 구현 검증은 15문제×5언어의 75개 구현과 975개 평가를 모두 통과해야 합니다. 정적 공급자 점검은 네트워크 호출 없이 설정만 검사합니다. 계정 인증·모델 접근을 확인할 때는 별도로 승인된 실행에서만 `--live`를 사용해 주십시오. 유료 호출과 본 실험은 아래 명령을 실제 실행할 때 발생하며 이 문서 작성 과정에서는 수행하지 않았습니다.

```powershell
uv run python scripts/preflight_v16.py --config configs/v1.6/experiment.yaml --provider-config configs/v1.6/providers/openai.yaml --live --output artifacts-rtt-v1.6/preflight-live.json
uv run rttdist hops --config configs/v1.6/experiment.yaml --provider-config configs/v1.6/providers/openai.yaml --phase pilot --action run
uv run python scripts/freeze_v16_design.py --config configs/v1.6/experiment.yaml --provider-config configs/v1.6/providers/openai.yaml --provider-preflight artifacts-rtt-v1.6/preflight-live.json
uv run rttdist hops --config configs/v1.6/experiment.yaml --provider-config configs/v1.6/providers/openai.yaml --phase main --action run
```

파일럿은 지정된 3문제×4경로×1회이며 본 실험 300슬롯과 분리합니다. 모델·코퍼스·프롬프트·도구·정지 규칙·생성 프로파일이 바뀌면 새 campaign을 사용해 주십시오. 중단한 실행은 저장된 응답과 같은 슬롯을 사용하여 재개합니다.

```powershell
uv run rttdist hops --config configs/v1.6/experiment.yaml --provider-config configs/v1.6/providers/openai.yaml --phase main --action resume
uv run python scripts/report_v16.py --config configs/v1.6/experiment.yaml --provider-config configs/v1.6/providers/openai.yaml --phase main
uv run python scripts/verify_v16_reproducibility.py --config configs/v1.6/experiment.yaml --provider-config configs/v1.6/providers/openai.yaml
```

보고서는 `output_root/campaign_id/main/report/`에 생성됩니다. 보고 경로를 바꾸려면 `--destination`을 지정해 주십시오. 관측 전용 계약과 구분하여 단계 루트의 `contract.json`을 읽습니다. 파일럿 보고는 `--phase pilot`으로 선택하며 확증 대상이 아닙니다.

## 통계 해석

| 항목 | 집계·판정 규칙 |
| --- | --- |
| P | 해당 임계치의 유효 시도 중 성공 비율 |
| H | 성공 reached_step의 평균, 편도 2·4·6·8·10홉 |
| D | 반올림 전 H/P; 성공 0이면 H·D 결측 |
| 완전성 | 임계치마다 경로당 75개 유효 슬롯 여부 |
| 주 임계치 | 0.85에서 문제 블록 10,000회 대응 재표집, 6쌍×3지표의 Bonferroni 18비교 구간 |
| 민감도 | 0.80·0.90의 미보정 95% 구간, 기술통계 한정 |
| 순위 지지 | Python–Java·Java–Haskell·Haskell–Prolog의 D 차이 보정 구간이 모두 예상 방향으로 0 제외 |
| 재표집 결측 | 성공 0인 표본 비율 공개, 해당 H·D 무조건부 구간과 전체 순위 산출 불가 |
| SDK 탐색 실행 | 확증에서 제외, 모델·컨텍스트 관측 한계를 별도 표시 |
| 재귀군 | 사전 지정 3문제와 비교군 12문제의 기술통계; 인과·패러다임 우월성 주장 금지 |

확인 실패는 이미 성공한 주 임계치 결과를 바꾸지 않습니다. 확인 유지율은 `passed/(passed+failed)`, 미확인 비율은 `unavailable/primary_successes`이며 분모 0은 결측입니다. invalid와 incomplete를 기능 실패나 hop_limit에 포함하지 않습니다. 방향별 단계 통과율은 탐색과 확인을 구분하고 판정 가능한 분모와 미확인 수를 공개합니다. 통신 재시도 자료가 관측에 없으면 호출 수를 추정해 0으로 채우지 않습니다.

합산 P와 문제별 P의 동일 가중 평균을 모두 공개합니다. D는 문제별 D의 평균이 아닙니다. 원본 대비 유사도는 주 성공 시도마다 도달 시점 값 한 개를 사용하며 실제 표본 수와 중앙값을 함께 보고합니다. 전체 단계 유사도에는 오래 진행한 시도의 가중 효과가 있습니다. JPlag 0은 설정된 매칭 기준에서의 값이며 의미 소멸의 증거가 아닙니다.

## 산출물과 근거

| 산출물 | 내용 |
| --- | --- |
| `summary.json` | 반올림 전 통계·원관측·계약·자료 해시의 단일 근거 |
| `observations.csv`, `problems.csv`, `thresholds.csv` | 관측·문제·임계치별 분모와 수치 |
| `failures.csv`, `confirmation.csv`, `stages.csv` | 임계치 분류·확인 분모·방향 및 단계별 통과율 |
| `comparisons.csv` | 구간 종류·비교 차이·재표집 결측 비율·산출 불가 사유 |
| `similarities.csv`, `recursive_groups.csv`, `call_usage.csv` | 유사도 표본 정의·군별 통계·호출 및 재시도 자료 |
| `code_annotations.csv` | Haskell 생성 코드 해시·근거 위치·재귀/누산기/리스트/상태 사용의 자동 결과와 검토 결과 |
| `model_metadata.json` | 모델 표시 설정·요청 ID·실제 응답 ID·별칭 근거·요청/전송/실효 설정 |
| `metrics.png/pdf`, `protocol.png/pdf`, `figure_inputs.csv` | 표준 matplotlib 그림·양방향 기능 검사와 확인 구간 흐름도·수치 입력 |
| `summary.md`, `evidence.json` | 한국어 수치 요약·summary 필드 경로·자료 해시·파생 비교식 |
| `reproducibility_bundle/`, `reproducibility.json` | 인증값 제외 입력·참조 원자료·환경·코드·의존성·해시 목록과 재생성 검증 |

코드 특성의 근거 위치는 검토자가 소스 파일과 행을 확인하여 채우며 자동 분석이 없으면 미확인으로 둡니다. 기능 통과를 코드 특성 확인으로 대체하지 않습니다. 숫자는 최종 표시에서만 반올림하며 배수와 %p 차이는 반올림 전 값으로 계산합니다.

재현 묶음의 `raw_sources.json`에서 참조된 원응답·생성 코드의 포함 여부와 원본/공개본 해시를 확인해 주십시오. 존재하지 않는 원자료를 포함한 것으로 표시하지 않습니다. 구조 감사는 실행 출력과 JPlag 원본을 다시 검증한 감사와 구분합니다. `reproducibility.json`의 통과는 수치 재생성의 동일성이며 자료 완전성이나 연구 가설의 지지를 뜻하지 않습니다.

고정 합성 자료만으로 다음 명령을 실행할 수 있습니다. 소켓·HTTP·SDK 가져오기 및 호출·하위 프로세스를 차단한 상태에서 JSON·CSV·그림 입력을 두 번 생성하여 정확히 비교합니다. 그림 렌더링 바이트와 PDF 비수치 메타데이터는 비교 대상에서 제외합니다.

```powershell
uv run python scripts/report_v16.py --bundle tests/fixtures/hops_v16 --destination <합성_보고_경로>
uv run python scripts/verify_v16_reproducibility.py --bundle tests/fixtures/hops_v16 --destination <합성_재현_경로>
```

## 판본 비교와 참고문헌 검토

v1.5와 v1.6은 3문제 교체 및 중단 규칙이 다르므로 직접 합산하거나 개선율로 주장하지 않습니다. 과거 하노이탑 결과 등은 원자료와 해당 판본의 실제 문제 목록을 확인한 뒤 인용해 주십시오. 과거 원자료가 없으면 재검증 미완료로 남깁니다. 원본 v1.5 원고는 수정하지 않습니다.

제출 전 아래 항목을 실제 원문과 대조해 주십시오. 이 구현은 문헌 검토를 완료했다고 표시하지 않습니다.

- 인용한 각 문헌의 저자·정확한 제목·연도·실제 판본·DOI 또는 공식 URL
- 본문 인용과 참고문헌 항목의 일대일 대응, 실제 인용 위치와 주장 범위
- JPlag 사용 버전·jar 해시·averageSimilarity·최소 매칭 토큰 9 설정의 기록
- MOSS를 실행했다는 서술의 부재 및 기능 검사와 전체 의미 동등성 증명의 구분
- [승인 설계의 제공자 문서 근거](../../docs/superpowers/specs/2026-11-17-v1.6-experiment-design.md), [JPlag 공식 저장소](https://github.com/jplag/JPlag), [matplotlib 공식 문서](https://matplotlib.org/stable/)
