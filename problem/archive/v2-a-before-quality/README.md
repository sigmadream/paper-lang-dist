# v2 문제 데이터

[lmstudio_v2.yaml](../lmstudio_v2.yaml)의 `problem_ids`에 지정된 IPOP 19개와 LeetCode 21개, 총 40문제를 문제별 폴더로 관리한다. 평가 입력·정답은 문제당 10쌍, 총 400쌍이다.

## 폴더 구성

```text
problem/
  dataset-index.json
  README.md
  IPOP_<id>/ 또는 LC_<id>/      # v2 선정 40문제
    statement.md                # 번역 프롬프트용 문제 명세
    prompt_examples/            # 프롬프트 예제
    evaluation/                 # 평가 전용 입력·정답 10쌍
    reference.cpp               # C++17 기준 풀이
    README.md                   # 사례 목적과 검증 설명
    public_examples.json        # LeetCode의 공개 예제 제외 근거
  metadata/
    ipop19/                     # IPOP manifest, 검증 보고서, 생성·검증 도구
    leetcode21/                 # LeetCode manifest, 검증 보고서, 생성·검증 도구
  leetcode-source/              # 출처와 공개 예제 수집 기록 및 수집 도구
  archive/
    v1/                         # 기존 IPOP 20문제의 명세와 입력·정답 원본
    layout-before/              # 정리 전 색인, manifest, 검증 보고서
    README.md
```

두 출처 모두 같은 구조로 읽는다. `statement.md`와 `prompt_examples`를 프롬프트에 사용하며 예제 중 파일명 순서상 첫 쌍을 전달한다. `reference.cpp`는 번역 원본과 실행 검증에 사용한다. `evaluation`, 사례 설명, 공개 예제 제외 근거, 검증 결과 및 실패 진단은 번역 프롬프트에 전달하지 않는다.

IPOP의 기존 예제 10쌍은 이름과 내용을 유지해 `prompt_examples`에 복사했다. IPOP 기준 코드도 기존 `corpus/solutions`의 C++ 파일을 내용 변경 없이 복사했다. v2에서는 각 문제 폴더의 파일이 기준이며, v1 원본은 보관 자료다. 평가 입력은 자체 생성한 자료로 공식 비공개 채점 데이터가 아니다.

## 색인과 경로

[dataset-index.json](dataset-index.json)의 `schema_version: 2`는 모든 문제에 동일한 파일 배치를 적용한다. 문제 ID나 파일 존재 여부로 예전 배치에 자동 대체하지 않는다. 각 `directory`는 이 폴더를 기준으로 해석하고, manifest 내부 파일 경로는 각 manifest 위치를 기준으로 해석한다. 색인에는 manifest의 SHA-256도 기록한다.

`lmstudio_v2.yaml`의 `problem_root`와 `corpus_root`는 모두 `./problem`이다. 구형 색인 schema 1도 실행기에서 계속 지원한다. `dataset_index`가 없는 v1 설정들은 `problem_root: ./problem/archive/v1`로 원래 20문제 자료를 읽는다. 제외 문제 `IPOP_1260`은 v2 색인에 없으며 과거 사전 검증용 설정에만 남아 있다.

## 선정 문제

아래 순서는 `lmstudio_v2.yaml`과 같다.

| 순서 | ID | 문제 | 명세 | 프롬프트 예제 | 평가 입력·설명 |
|---:|---|---|---|---|---|
| 1 | IPOP_10988 | 팰린드롬인지 확인하기 | [명세](IPOP_10988/statement.md) | [예제](IPOP_10988/prompt_examples/) | [평가 10쌍](IPOP_10988/README.md) |
| 2 | IPOP_1158 | 요세푸스 문제 | [명세](IPOP_1158/statement.md) | [예제](IPOP_1158/prompt_examples/) | [평가 10쌍](IPOP_1158/README.md) |
| 3 | IPOP_11729 | 하노이 탑 이동 순서 | [명세](IPOP_11729/statement.md) | [예제](IPOP_11729/prompt_examples/) | [평가 10쌍](IPOP_11729/README.md) |
| 4 | IPOP_1436 | 영화감독 숌 | [명세](IPOP_1436/statement.md) | [예제](IPOP_1436/prompt_examples/) | [평가 10쌍](IPOP_1436/README.md) |
| 5 | IPOP_14719 | 빗물 | [명세](IPOP_14719/statement.md) | [예제](IPOP_14719/prompt_examples/) | [평가 10쌍](IPOP_14719/README.md) |
| 6 | IPOP_1620 | 나는야 포켓몬 마스터 이다솜 | [명세](IPOP_1620/statement.md) | [예제](IPOP_1620/prompt_examples/) | [평가 10쌍](IPOP_1620/README.md) |
| 7 | IPOP_18870 | 좌표 압축 | [명세](IPOP_18870/statement.md) | [예제](IPOP_18870/prompt_examples/) | [평가 10쌍](IPOP_18870/README.md) |
| 8 | IPOP_1929 | 소수 구하기 | [명세](IPOP_1929/statement.md) | [예제](IPOP_1929/prompt_examples/) | [평가 10쌍](IPOP_1929/README.md) |
| 9 | IPOP_1992 | 쿼드트리 | [명세](IPOP_1992/statement.md) | [예제](IPOP_1992/prompt_examples/) | [평가 10쌍](IPOP_1992/README.md) |
| 10 | IPOP_2003 | 수들의 합 2 | [명세](IPOP_2003/statement.md) | [예제](IPOP_2003/prompt_examples/) | [평가 10쌍](IPOP_2003/README.md) |
| 11 | IPOP_2110 | 공유기 설치 | [명세](IPOP_2110/statement.md) | [예제](IPOP_2110/prompt_examples/) | [평가 10쌍](IPOP_2110/README.md) |
| 12 | IPOP_2217 | 로프 | [명세](IPOP_2217/statement.md) | [예제](IPOP_2217/prompt_examples/) | [평가 10쌍](IPOP_2217/README.md) |
| 13 | IPOP_2579 | 계단 오르기 | [명세](IPOP_2579/statement.md) | [예제](IPOP_2579/prompt_examples/) | [평가 10쌍](IPOP_2579/README.md) |
| 14 | IPOP_2609 | 최대공약수와 최소공배수 | [명세](IPOP_2609/statement.md) | [예제](IPOP_2609/prompt_examples/) | [평가 10쌍](IPOP_2609/README.md) |
| 15 | IPOP_5567 | 결혼식 | [명세](IPOP_5567/statement.md) | [예제](IPOP_5567/prompt_examples/) | [평가 10쌍](IPOP_5567/README.md) |
| 16 | IPOP_9012 | 괄호 | [명세](IPOP_9012/statement.md) | [예제](IPOP_9012/prompt_examples/) | [평가 10쌍](IPOP_9012/README.md) |
| 17 | IPOP_9251 | LCS | [명세](IPOP_9251/statement.md) | [예제](IPOP_9251/prompt_examples/) | [평가 10쌍](IPOP_9251/README.md) |
| 18 | IPOP_9663 | N-Queen | [명세](IPOP_9663/statement.md) | [예제](IPOP_9663/prompt_examples/) | [평가 10쌍](IPOP_9663/README.md) |
| 19 | IPOP_9935 | 문자열 폭발 | [명세](IPOP_9935/statement.md) | [예제](IPOP_9935/prompt_examples/) | [평가 10쌍](IPOP_9935/README.md) |
| 20 | LC_0001 | Two Sum | [명세](LC_0001/statement.md) | [예제](LC_0001/prompt_examples/) | [평가 10쌍](LC_0001/README.md) |
| 21 | LC_0121 | Best Time To Buy And Sell Stock | [명세](LC_0121/statement.md) | [예제](LC_0121/prompt_examples/) | [평가 10쌍](LC_0121/README.md) |
| 22 | LC_0217 | Contains Duplicate | [명세](LC_0217/statement.md) | [예제](LC_0217/prompt_examples/) | [평가 10쌍](LC_0217/README.md) |
| 23 | LC_0053 | Maximum Subarray | [명세](LC_0053/statement.md) | [예제](LC_0053/prompt_examples/) | [평가 10쌍](LC_0053/README.md) |
| 24 | LC_0704 | Binary Search | [명세](LC_0704/statement.md) | [예제](LC_0704/prompt_examples/) | [평가 10쌍](LC_0704/README.md) |
| 25 | LC_0035 | Search Insert Position | [명세](LC_0035/statement.md) | [예제](LC_0035/prompt_examples/) | [평가 10쌍](LC_0035/README.md) |
| 26 | LC_0283 | Move Zeroes | [명세](LC_0283/statement.md) | [예제](LC_0283/prompt_examples/) | [평가 10쌍](LC_0283/README.md) |
| 27 | LC_0242 | Valid Anagram | [명세](LC_0242/statement.md) | [예제](LC_0242/prompt_examples/) | [평가 10쌍](LC_0242/README.md) |
| 28 | LC_0387 | First Unique Character In A String | [명세](LC_0387/statement.md) | [예제](LC_0387/prompt_examples/) | [평가 10쌍](LC_0387/README.md) |
| 29 | LC_0003 | Longest Substring Without Repeating Characters | [명세](LC_0003/statement.md) | [예제](LC_0003/prompt_examples/) | [평가 10쌍](LC_0003/README.md) |
| 30 | LC_0139 | Word Break | [명세](LC_0139/statement.md) | [예제](LC_0139/prompt_examples/) | [평가 10쌍](LC_0139/README.md) |
| 31 | LC_0518 | Coin Change Ii | [명세](LC_0518/statement.md) | [예제](LC_0518/prompt_examples/) | [평가 10쌍](LC_0518/README.md) |
| 32 | LC_0062 | Unique Paths | [명세](LC_0062/statement.md) | [예제](LC_0062/prompt_examples/) | [평가 10쌍](LC_0062/README.md) |
| 33 | LC_0063 | Unique Paths Ii | [명세](LC_0063/statement.md) | [예제](LC_0063/prompt_examples/) | [평가 10쌍](LC_0063/README.md) |
| 34 | LC_0064 | Minimum Path Sum | [명세](LC_0064/statement.md) | [예제](LC_0064/prompt_examples/) | [평가 10쌍](LC_0064/README.md) |
| 35 | LC_0739 | Daily Temperatures | [명세](LC_0739/statement.md) | [예제](LC_0739/prompt_examples/) | [평가 10쌍](LC_0739/README.md) |
| 36 | LC_0496 | Next Greater Element I | [명세](LC_0496/statement.md) | [예제](LC_0496/prompt_examples/) | [평가 10쌍](LC_0496/README.md) |
| 37 | LC_0547 | Number Of Provinces | [명세](LC_0547/statement.md) | [예제](LC_0547/prompt_examples/) | [평가 10쌍](LC_0547/README.md) |
| 38 | LC_0207 | Course Schedule | [명세](LC_0207/statement.md) | [예제](LC_0207/prompt_examples/) | [평가 10쌍](LC_0207/README.md) |
| 39 | LC_0338 | Counting Bits | [명세](LC_0338/statement.md) | [예제](LC_0338/prompt_examples/) | [평가 10쌍](LC_0338/README.md) |
| 40 | LC_0912 | Sort An Array | [명세](LC_0912/statement.md) | [예제](LC_0912/prompt_examples/) | [평가 10쌍](LC_0912/README.md) |

## 검증과 실행

프로젝트 루트에서 실행한다. 데이터 자체 검증은 모델 API를 호출하지 않는다.

```powershell
python problem/metadata/ipop19/tools/validate_dataset.py
python problem/metadata/leetcode21/tools/validate_dataset.py
```

RTT 실행기를 통한 검증과 실험은 다음과 같다. 컴파일러 설정 등은 [프로젝트 안내](../README.md)를 참고한다.

```powershell
uv run rttdist validate-corpus --config lmstudio_v2.yaml --execute
uv run rttdist run --config lmstudio_v2.yaml --run-id v2-a-r1
```

결과는 `artifacts-lmstudio/v2-a`에 저장한다. 경로 정리 전의 검증·실행 기록에는 이전 경로가 포함되므로 새 구조에서는 다시 검증하고 새로운 run-id로 시작한다. 데이터 검증 보고서는 LLM 번역 실험 결과가 아니다.

| 검토 자료 | 내용 |
|---|---|
| [IPOP 안내](metadata/ipop19/README.md) | 19문제·190쌍의 생성·검증 방법 |
| [IPOP manifest](metadata/ipop19/manifest.json) | 사례 목적, 제외 예제, 파일 해시 |
| [IPOP 검증 보고서](metadata/ipop19/validation_report.json) | 독립 계산·C++ 190건과 대응 JavaScript 30건 |
| [LeetCode 안내](metadata/leetcode21/README.md) | 21문제·210쌍의 입출력 계약과 검증 방법 |
| [LeetCode manifest](metadata/leetcode21/manifest.json) | 출처, 공개 예제 제외 근거, 파일 해시 |
| [LeetCode 검증 보고서](metadata/leetcode21/validation_report.json) | 독립 계산·C++·JavaScript 각 210건과 공개 예제 21쌍 |
| [출처 수집 기록](leetcode-source/README.md) | 고정 커밋, 파일 목록, 공개 예제와 재수집 방법 |
| [보관 자료 안내](archive/README.md) | v1 원본, 제외 문제, 정리 전 검증 기록 |

생성기는 현재 문제 폴더의 평가 파일과 manifest를 덮어쓴다. 데이터 버전을 변경할 때만 사용하고, 재생성 후에는 데이터 검증과 색인의 manifest 해시 갱신이 필요하다.
