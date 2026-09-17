# 추가 LeetCode 21문제

기존 IPOP 19문제에 별도로 추가하는 21문제다. 전체 선정 문제는 40개이며, 평가 입력은 기존 190개와 신규 210개를 합쳐 400개다. IPOP_1260은 포함하지 않는다.

선정 기준은 저장소에 실제 풀이가 있고, 기존 19문제와 다른 과제이며, 표준입출력 변환과 독립 정답 검증이 가능한 문제다. 배열·문자열·탐색·동적 계획법·스택·그래프를 포함했다. 임의 추출한 대표 표본은 아니며, Unique Paths와 Unique Paths II처럼 같은 계열의 문제는 분석 시 문제군을 고려해야 한다.

## 문제 목록

각 문제에 평가 입력·정답 10쌍, 공개 프롬프트 예제 1쌍, 독립적으로 작성한 C++17 기준 풀이를 제공한다.

| ID | 문제 | 유형 | 평가 입력 |
|---|---|---|---:|
| [LC_0001](../../LC_0001/README.md) | Two Sum | 배열·해시 | 10 |
| [LC_0121](../../LC_0121/README.md) | Best Time to Buy and Sell Stock | 배열·최적화 | 10 |
| [LC_0217](../../LC_0217/README.md) | Contains Duplicate | 배열·해시 | 10 |
| [LC_0053](../../LC_0053/README.md) | Maximum Subarray | 동적 계획법 | 10 |
| [LC_0704](../../LC_0704/README.md) | Binary Search | 이분탐색 | 10 |
| [LC_0035](../../LC_0035/README.md) | Search Insert Position | 이분탐색 | 10 |
| [LC_0283](../../LC_0283/README.md) | Move Zeroes | 배열·재배치 | 10 |
| [LC_0242](../../LC_0242/README.md) | Valid Anagram | 문자열 | 10 |
| [LC_0387](../../LC_0387/README.md) | First Unique Character in a String | 문자열 | 10 |
| [LC_0003](../../LC_0003/README.md) | Longest Substring Without Repeating Characters | 슬라이딩 윈도 | 10 |
| [LC_0139](../../LC_0139/README.md) | Word Break | 동적 계획법·문자열 | 10 |
| [LC_0518](../../LC_0518/README.md) | Coin Change II | 동적 계획법·수치 | 10 |
| [LC_0062](../../LC_0062/README.md) | Unique Paths | 동적 계획법·격자 | 10 |
| [LC_0063](../../LC_0063/README.md) | Unique Paths II | 동적 계획법·격자 | 10 |
| [LC_0064](../../LC_0064/README.md) | Minimum Path Sum | 동적 계획법·격자 | 10 |
| [LC_0739](../../LC_0739/README.md) | Daily Temperatures | 스택 | 10 |
| [LC_0496](../../LC_0496/README.md) | Next Greater Element I | 스택 | 10 |
| [LC_0547](../../LC_0547/README.md) | Number of Provinces | 그래프 | 10 |
| [LC_0207](../../LC_0207/README.md) | Course Schedule | 그래프 | 10 |
| [LC_0338](../../LC_0338/README.md) | Counting Bits | 비트·수치 | 10 |
| [LC_0912](../../LC_0912/README.md) | Sort an Array | 정렬 | 10 |

## 출처와 입력 분리

출처 저장소는 [DhanushNehru/Leetcode](https://github.com/DhanushNehru/Leetcode)이며 기존 수집과 같은 커밋 `b9d7d2c234c39b3b3c67eded0c125e2841685b29`를 사용한다. 문제별 저장소 경로와 SHA-256은 [manifest.json](manifest.json)에 있다. 공식 LeetCode 명세·제약·공개 입력 예제는 2026-09-16에 대조했으며 문제별 statement.md에 출처를 연결했다.

평가 입력은 자체 생성했다. 공식 설명에서 확인한 공개 입력 예제 51개를 모두 기록하고 평가 집합에서 제외했다. 입력을 파싱한 인자 단위로 중복을 검사하며, 문자열 안의 공백은 보존하고 사전 단어·동전 종류·선수 관계의 순서 차이는 정규화한다. 난수 생성이나 풀이 실패에 따른 사례 선별은 사용하지 않았다.

| 문제별 파일 | 역할 | 프롬프트 전달 |
|---|---|---|
| statement.md | 문제 요약, 제약, 표준입출력 계약, 공개 예제 | 가능 |
| prompt_examples/example01.inp, .out | 공개 예제 1쌍 | 가능 |
| reference.cpp | 로컬에서 작성한 C++17 기준 코드 | 원본 코드로 가능 |
| evaluation/case01..10.inp, .out | 미제시 평가 입력과 독립 검증된 정답 | 제외 |
| public_examples.json | 제외 근거인 공개 예제 전체 | 제외 |
| README.md, manifest, validation_report | 사례 목적·정답 근거·감사 정보 | 제외 |

원래 LeetCode 문제는 함수 호출형이다. 이 묶음은 문제별로 문서화한 stdin/stdout 형식으로 변환했다. Move Zeroes는 수정된 배열을 출력하고, Two Sum은 두 인덱스를 오름차순으로 출력하며, boolean 결과는 1/0으로 표현한다. 예시·평가 입력·독립 구현·C++ 코드·저장소 JS 어댑터가 같은 계약을 사용한다.

## 검증 결과

[validation_report.json](validation_report.json)에 문제별 실행 결과를 기록했다.

- 신규 평가 입력의 독립 계산 두 방식 대조: 210/210 통과.
- 자체 작성 C++17 기준 풀이의 평가 입력 실행: 210/210 통과.
- 저장소 원본 JavaScript 풀이와의 결과 대조: 210/210 통과.
- 공개 프롬프트 예제 실행: C++ 21/21, JavaScript 21/21 통과.
- 문제별 평가 입력 중복 및 공개 예제 중복: 0건.

격자 문제는 DP와 경로 전수 탐색 또는 조합식을, 그래프 문제는 DFS와 서로소 집합 또는 위상 정렬과 정점 순열 전수 탐색을 비교했다. 배열·문자열 문제도 해시·스택·DP 계산을 직접 탐색 등과 대조했다. 구체적인 방법은 각 문제 README와 [oracles.py](tools/oracles.py)에 있다.

이 검증은 입력에 대한 기능적 정합성 검사다. 모든 최대 크기와 시간 복잡도를 검증한 것은 아니다. 특히 저장소의 Binary Search 풀이는 indexOf를 사용하므로 공식 명세의 O(log N) 요구를 만족하는 기준 구현으로 취급하지 않는다. 제공한 C++ 기준 코드는 이분탐색을 사용한다.

입력은 현재 문서화한 프롬프트 예제에 제시되지 않았다는 의미의 미제시 입력이며, 모델 학습 데이터와 중복되지 않는다는 보장은 아니다. 소규모 그래프·경로 사례는 완전탐색 검증을 위해 크기를 제한했다. 정수 상한, 빈 문자열, 값 반복, 장애물, 순환, 도달 불가 등 기능적 경계 조건을 포함한다.

## 재검증과 실험 연결

프로젝트 루트에서 실행한다. Python 표준 라이브러리, Node.js, C++17 컴파일러가 필요하다. assertion이 검증에 사용되므로 Python의 -O 옵션을 사용하지 않는다.

```powershell
python problem/metadata/leetcode21/tools/validate_dataset.py
```

기본 컴파일러는 `.tools/gcc/bin/g++.exe`, 소스 체크아웃은 `.tools/leetcode-source`다. 다른 경로를 사용하려면 다음과 같이 지정한다.

```powershell
python problem/metadata/leetcode21/tools/validate_dataset.py --compiler "C:/path/to/g++.exe" --upstream "C:/path/to/Leetcode"
```

검증기는 고정된 도구·문제 명세·예제·기준 코드·평가 파일과 외부 JS 소스의 해시를 확인한다. C++ 실행은 사례당 30초, JS 함수는 사례당 5초로 제한한다. 보고서는 재실행하면 갱신된다. 소스 재수집 방법은 [수집 기록](../../leetcode-source/README.md)을 참고한다.

생성기 [build_dataset.py](tools/build_dataset.py)는 입력·정답·문서·기준 코드·manifest를 덮어쓰므로 데이터 버전을 변경할 때만 사용한다. 평가 사례는 [cases.py](tools/cases.py), 공식 예제와 입출력 계약은 [catalog.py](tools/catalog.py)에 있다.

현재 [lmstudio_v2.yaml](../../../lmstudio_v2.yaml)은 [dataset-index.json](../../dataset-index.json)을 통해 이 묶음의 21문제를 읽는다. 실행기는 `problem/LC_*/`의 `statement.md`와 `prompt_examples`를 프롬프트에 사용하고, 각 문제 폴더의 `evaluation`에 있는 입력·정답 210쌍을 평가에만 사용한다. 이 메타데이터 폴더에는 manifest, 검증 보고서와 도구를 둔다. 평가 결과는 번역 프롬프트나 수정 재요청에 전달하지 않는다. 실행 방법은 [프로젝트 안내](../../../README.md)를 참고한다. 데이터 검증 기록은 LLM 번역 실험 결과와 구분한다.
