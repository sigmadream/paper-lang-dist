# v2 문제 데이터

[lmstudio_v2.yaml](../lmstudio_v2.yaml)의 40문제를 공통 구조로 관리한다. 현재 버전은 `v2-a-quality-1`, 평가 입력·정답은 문제당 13쌍, 총 520쌍이다. 기존 400쌍을 유지하고 고정 seed·경계 입력 120쌍을 추가했다.

[논문 적합성 검토 보고서](../docs/DATASET_QUALITY_v2.md)와 [재현·검증 안내](metadata/quality/README.md)에 난이도 해석, 검사 결과와 한계를 기록했다. [문제별 CSV](metadata/quality/problem_profile.csv)는 입력 크기와 설명·프롬프트 길이, 알고리즘 구조 분류를 제공한다.

```text
problem/
  IPOP_<id>/ 또는 LC_<id>/
    statement.md              # 문제 요약·제약·입출력 계약
    prompt_examples/          # 공개 예제, 첫 쌍만 프롬프트에 전달
    evaluation/               # case01..13.inp, .out
    reference.cpp             # 번역 원본 및 C++17 검증 기준
    README.md                 # 사례 목적과 정답 검증 설명
    public_examples.json      # LeetCode 공개 예제 전체의 제외 근거
  metadata/
    ipop19/                   # 19문제·247쌍: manifest, 검증 결과, 도구
    leetcode21/               # 21문제·273쌍: manifest, 검증 결과, 도구
    quality/                  # 감사 보고서, CSV, 프롬프트 스냅샷, 도구
  leetcode-source/            # 외부 소스·공개 예제의 수집 기록
  archive/v2-a-before-quality/# 개선 전 40문제·400쌍과 프롬프트 조건
  dataset-index.json
  README.md
```

색인 schema 2의 각 `directory`는 색인 위치를 기준으로 해석한다. manifest 내부 경로는 해당 manifest 위치를 기준으로 한다. `statement.md`, 고정된 첫 예제와 기준 코드만 번역 프롬프트에 제공하며 평가 입력·정답·사례 설명·실패 진단은 제공하지 않는다. LC_0003은 공백이 의미 있는 문자열 입력이므로 줄 단위 중복 검사를 사용한다.

현재 P2는 모든 유효 입력의 동작 보존을 요구하며 예제의 빈 줄과 공백을 그대로 유지한다. 원래 400쌍·기준 코드 40개·첫 예제는 내용 변경 없이 보존했다. 문제 설명과 프롬프트는 개선되어 과거 조건과 동일하지 않다. 오래된 설정의 실행에는 그 설정이 참조하는 별도 보관 자료가 필요하다.

## 선정 문제

| ID | 문제 | 명세 | 프롬프트 예제 | 평가 입력·설명 |
|---|---|---|---|---|
| IPOP_10988 | 팰린드롬인지 확인하기 | [명세](IPOP_10988/statement.md) | [예제](IPOP_10988/prompt_examples/) | [평가 13쌍](IPOP_10988/README.md) |
| IPOP_1158 | 요세푸스 문제 | [명세](IPOP_1158/statement.md) | [예제](IPOP_1158/prompt_examples/) | [평가 13쌍](IPOP_1158/README.md) |
| IPOP_11729 | 하노이 탑 이동 순서 | [명세](IPOP_11729/statement.md) | [예제](IPOP_11729/prompt_examples/) | [평가 13쌍](IPOP_11729/README.md) |
| IPOP_1436 | 영화감독 숌 | [명세](IPOP_1436/statement.md) | [예제](IPOP_1436/prompt_examples/) | [평가 13쌍](IPOP_1436/README.md) |
| IPOP_14719 | 빗물 | [명세](IPOP_14719/statement.md) | [예제](IPOP_14719/prompt_examples/) | [평가 13쌍](IPOP_14719/README.md) |
| IPOP_1620 | 나는야 포켓몬 마스터 이다솜 | [명세](IPOP_1620/statement.md) | [예제](IPOP_1620/prompt_examples/) | [평가 13쌍](IPOP_1620/README.md) |
| IPOP_18870 | 좌표 압축 | [명세](IPOP_18870/statement.md) | [예제](IPOP_18870/prompt_examples/) | [평가 13쌍](IPOP_18870/README.md) |
| IPOP_1929 | 소수 구하기 | [명세](IPOP_1929/statement.md) | [예제](IPOP_1929/prompt_examples/) | [평가 13쌍](IPOP_1929/README.md) |
| IPOP_1992 | 쿼드트리 | [명세](IPOP_1992/statement.md) | [예제](IPOP_1992/prompt_examples/) | [평가 13쌍](IPOP_1992/README.md) |
| IPOP_2003 | 수들의 합 2 | [명세](IPOP_2003/statement.md) | [예제](IPOP_2003/prompt_examples/) | [평가 13쌍](IPOP_2003/README.md) |
| IPOP_2110 | 공유기 설치 | [명세](IPOP_2110/statement.md) | [예제](IPOP_2110/prompt_examples/) | [평가 13쌍](IPOP_2110/README.md) |
| IPOP_2217 | 로프 | [명세](IPOP_2217/statement.md) | [예제](IPOP_2217/prompt_examples/) | [평가 13쌍](IPOP_2217/README.md) |
| IPOP_2579 | 계단 오르기 | [명세](IPOP_2579/statement.md) | [예제](IPOP_2579/prompt_examples/) | [평가 13쌍](IPOP_2579/README.md) |
| IPOP_2609 | 최대공약수와 최소공배수 | [명세](IPOP_2609/statement.md) | [예제](IPOP_2609/prompt_examples/) | [평가 13쌍](IPOP_2609/README.md) |
| IPOP_5567 | 결혼식 | [명세](IPOP_5567/statement.md) | [예제](IPOP_5567/prompt_examples/) | [평가 13쌍](IPOP_5567/README.md) |
| IPOP_9012 | 괄호 | [명세](IPOP_9012/statement.md) | [예제](IPOP_9012/prompt_examples/) | [평가 13쌍](IPOP_9012/README.md) |
| IPOP_9251 | LCS | [명세](IPOP_9251/statement.md) | [예제](IPOP_9251/prompt_examples/) | [평가 13쌍](IPOP_9251/README.md) |
| IPOP_9663 | N-Queen | [명세](IPOP_9663/statement.md) | [예제](IPOP_9663/prompt_examples/) | [평가 13쌍](IPOP_9663/README.md) |
| IPOP_9935 | 문자열 폭발 | [명세](IPOP_9935/statement.md) | [예제](IPOP_9935/prompt_examples/) | [평가 13쌍](IPOP_9935/README.md) |
| LC_0001 | Two Sum | [명세](LC_0001/statement.md) | [예제](LC_0001/prompt_examples/) | [평가 13쌍](LC_0001/README.md) |
| LC_0121 | Best Time To Buy And Sell Stock | [명세](LC_0121/statement.md) | [예제](LC_0121/prompt_examples/) | [평가 13쌍](LC_0121/README.md) |
| LC_0217 | Contains Duplicate | [명세](LC_0217/statement.md) | [예제](LC_0217/prompt_examples/) | [평가 13쌍](LC_0217/README.md) |
| LC_0053 | Maximum Subarray | [명세](LC_0053/statement.md) | [예제](LC_0053/prompt_examples/) | [평가 13쌍](LC_0053/README.md) |
| LC_0704 | Binary Search | [명세](LC_0704/statement.md) | [예제](LC_0704/prompt_examples/) | [평가 13쌍](LC_0704/README.md) |
| LC_0035 | Search Insert Position | [명세](LC_0035/statement.md) | [예제](LC_0035/prompt_examples/) | [평가 13쌍](LC_0035/README.md) |
| LC_0283 | Move Zeroes | [명세](LC_0283/statement.md) | [예제](LC_0283/prompt_examples/) | [평가 13쌍](LC_0283/README.md) |
| LC_0242 | Valid Anagram | [명세](LC_0242/statement.md) | [예제](LC_0242/prompt_examples/) | [평가 13쌍](LC_0242/README.md) |
| LC_0387 | First Unique Character In A String | [명세](LC_0387/statement.md) | [예제](LC_0387/prompt_examples/) | [평가 13쌍](LC_0387/README.md) |
| LC_0003 | Longest Substring Without Repeating Characters | [명세](LC_0003/statement.md) | [예제](LC_0003/prompt_examples/) | [평가 13쌍](LC_0003/README.md) |
| LC_0139 | Word Break | [명세](LC_0139/statement.md) | [예제](LC_0139/prompt_examples/) | [평가 13쌍](LC_0139/README.md) |
| LC_0518 | Coin Change Ii | [명세](LC_0518/statement.md) | [예제](LC_0518/prompt_examples/) | [평가 13쌍](LC_0518/README.md) |
| LC_0062 | Unique Paths | [명세](LC_0062/statement.md) | [예제](LC_0062/prompt_examples/) | [평가 13쌍](LC_0062/README.md) |
| LC_0063 | Unique Paths Ii | [명세](LC_0063/statement.md) | [예제](LC_0063/prompt_examples/) | [평가 13쌍](LC_0063/README.md) |
| LC_0064 | Minimum Path Sum | [명세](LC_0064/statement.md) | [예제](LC_0064/prompt_examples/) | [평가 13쌍](LC_0064/README.md) |
| LC_0739 | Daily Temperatures | [명세](LC_0739/statement.md) | [예제](LC_0739/prompt_examples/) | [평가 13쌍](LC_0739/README.md) |
| LC_0496 | Next Greater Element I | [명세](LC_0496/statement.md) | [예제](LC_0496/prompt_examples/) | [평가 13쌍](LC_0496/README.md) |
| LC_0547 | Number Of Provinces | [명세](LC_0547/statement.md) | [예제](LC_0547/prompt_examples/) | [평가 13쌍](LC_0547/README.md) |
| LC_0207 | Course Schedule | [명세](LC_0207/statement.md) | [예제](LC_0207/prompt_examples/) | [평가 13쌍](LC_0207/README.md) |
| LC_0338 | Counting Bits | [명세](LC_0338/statement.md) | [예제](LC_0338/prompt_examples/) | [평가 13쌍](LC_0338/README.md) |
| LC_0912 | Sort An Array | [명세](LC_0912/statement.md) | [예제](LC_0912/prompt_examples/) | [평가 13쌍](LC_0912/README.md) |

## 검증과 실행

프로젝트 루트에서 먼저 데이터와 프롬프트를 검증한다.

```powershell
python problem/metadata/ipop19/tools/validate_dataset.py
python problem/metadata/leetcode21/tools/validate_dataset.py
python problem/metadata/quality/tools/audit_dataset.py
uv run rttdist validate-corpus --config lmstudio_v2.yaml --execute
```

실험 결과 위치는 `artifacts-lmstudio/v2-a-quality-1`이다. 새 조건으로 검증한 뒤 새로운 run-id를 사용한다. 재생성과 논문에 쓸 수 있는 주장 범위는 [품질 점검 안내](metadata/quality/README.md)를 참고한다.
