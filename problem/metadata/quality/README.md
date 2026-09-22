# 논문용 데이터 품질 점검

현재 코퍼스 버전은 `v2-a-quality-1`이다. 40문제의 기존 평가 400쌍을 보존하고 문제당 3쌍을 추가하여 총 520쌍을 사용한다. 생성 seed는 `20260917`이며 문제 번호를 더해 문제별 난수열을 고정했다. 스칼라 입력 영역이 작은 문제는 고정된 미사용 값을 사용했다. 모델 출력이나 모델별 통과 여부를 기준으로 입력을 선별하지 않았다.

| 산출물 | 내용 |
|---|---|
| [논문 반영용 검토 보고서](../../../docs/DATASET_QUALITY_v2.md) | 적합 범위, 발견 사항, 개선 내역, 난이도 해석과 남은 한계 |
| [audit_report.json](audit_report.json) | 문제별 규모, 예제 실행, 원본 보존, 오류 코드 검출 결과와 파일 해시 |
| [problem_profile.csv](problem_profile.csv) | 40문제의 알고리즘 구조, 유사 문제군, 입력 크기, 설명·프롬프트 길이 |
| [prompt_previews](prompt_previews/) | 각 문제의 C++→C/Java/Python 첫 번역 요청 120개와 해시 |
| [진단 오류 코드](tools/mutants.py) | 의도적으로 잘못 작성한 8개 구현. 전체 오류 분포의 대표 표본은 아님 |
| [변경 전 자료](../../archive/v2-a-before-quality/) | 기존 40문제·400쌍, 명세, 메타데이터, 설정과 P1 템플릿 |

## 재검증

프로젝트 루트에서 실행한다. C++17 컴파일러와 Node.js, 기존 고정 커밋의 외부 JavaScript 소스가 필요하다. 아래 명령은 모델 API를 호출하지 않는다.

```powershell
python problem/metadata/ipop19/tools/validate_dataset.py
python problem/metadata/leetcode21/tools/validate_dataset.py
python problem/metadata/quality/tools/audit_dataset.py
```

첫 두 검증기는 입력 제약, 공개 예제와 중복, 독립 계산, C++ 및 대응 JavaScript 출력을 검사한다. 품질 감사기는 기존 평가 파일·기준 코드·첫 예제의 바이트 보존, 40개 기준 코드의 컴파일과 예제 실행, 프롬프트 스냅샷, 진단 오류 코드 검출 결과를 기록한다. 동일한 예제 쌍은 한 번 실행하고 해당 중복 파일들의 결과에 연결한다.

작은 입력은 기존 완전탐색을 유지하며, 큰 입력은 다른 알고리즘·수학적 상한·공개 계수로 교차 확인한다. 구체적인 방식은 각 문제의 README와 manifest에 있다. N-Queen의 N=12..14는 비트마스크 계산과 [OEIS A000170의 공개 계수](https://oeis.org/A000170/b000170.txt)를 대조한다. IPOP_2110의 큰 입력은 균등 간격 좌표이며 배치의 상한 공식을 사용한다. 이를 임의의 큰 입력에 대한 검증으로 확대 해석하지 않는다.

## 재생성

생성기는 활성 자료를 덮어쓴다. 버전 변경과 재검증을 함께 수행할 때만 다음 순서로 실행한다.

```powershell
python problem/metadata/quality/tools/prepare_statements.py
python problem/metadata/ipop19/tools/build_dataset.py
python problem/metadata/leetcode21/tools/build_dataset.py
python problem/metadata/quality/tools/refresh_index.py
```

이후 위 재검증 명령을 실행한다. `refresh_index.py`는 생성된 평가 파일의 해시를 검사한 다음 색인의 개수와 manifest 해시를 갱신한다. IPOP 공개 예제 제외 검사는 보관한 변경 전 명세까지 포함하므로 `archive/v2-a-before-quality`는 재현에 필요하다.

## 프롬프트 조건

`lmstudio_v2.yaml`은 `prompt_template_version: rtt.prompts.v2`를 사용한다. P2는 모든 유효 입력에 대한 동작 보존, 표준입출력, 문자열 공백, 수치 범위, 인덱스와 출력 순서를 명시한다. Java에는 실행기와 맞는 `Main` 진입점을 명시한다. 빈 예제와 공백을 제거하지 않는다. 명세에는 공개 예제를 중복 삽입하지 않으며 별도 예제 구역에 동일한 첫 예제 한 쌍을 제공한다.

버전을 생략한 설정은 P1인 `rtt.prompts.v1`을 유지한다. P1/P2는 서로 다른 실험 조건이며 결과를 같은 조건으로 합치지 않는다. 역방향 요청은 모델이 만든 중간 코드에 의존하므로 미리 만든 예시에 포함하지 않았다.
