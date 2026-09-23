# v1 문제 데이터

> 논문에 사용될 기초 평가 문제 40문제이다.

## 형식

```text
problem/
  IPOP_<id>/ 또는 LC_<id>/
    statement.md              # 문제 요약, 제약, 입출력 계약
    prompt_examples/          # 공개 예제, 첫 쌍만 프롬프트에 전달
    evaluation/               # case01..13.inp, `.out`
    reference.cpp             # 번역 원본 및 C++17 검증 기준
    README.md                 # 사례 목적과 정답 검증 설명
    public_examples.json      # LeetCode 공개 예제 전체의 제외 근거
  metadata/
    ipop19/                   # 19문제(247쌍) manifest, 검증 결과, 도구
    leetcode21/               # 21문제(273쌍) manifest, 검증 결과, 도구
    quality/                  # 감사 보고서, CSV, 프롬프트 스냅샷, 도구
  leetcode-source/            # 외부 소스, 공개 예제의 수집 기록
  dataset-index.json
  README.md
```

## 선정 문제

| ID | 문제 | 명세 | 프롬프트 예제 | 평가 입력, 설명 |
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

```powershell
uv run problem/metadata/ipop19/tools/validate_dataset.py
uv run problem/metadata/leetcode21/tools/validate_dataset.py
uv run problem/metadata/quality/tools/audit_dataset.py
uv run rttdist validate-corpus --config lmstudio_v2.yaml --execute
```
