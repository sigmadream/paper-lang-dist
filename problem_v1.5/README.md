# problem_v1: 프로그래밍 언어 간 의미 거리 측정을 위한 5대 선별 문제 세트

## 1. 개요 및 선별 배경

본 문제 세트는 C++을 기준(reference) 언어로 설정하고, 6개 대상 언어(C, Java, Python, Haskell, OCaml, Elixir) 간의 의미 거리를 왕복 번역(Round-Trip Translation, RTT)을 통해 측정하기 위해 구성된 5개 문제 축소 코퍼스입니다.

다양한 언어 패러다임(절차형, 클래스 기반 객체지향, 동적 스크립트, 순수 함수형, 강타입 함수형, 액터/동시성 함수형)과 다수의 LLM(Qwen 3, GLM-5 및 향후 대형 모델)을 조합할 때 발생하는 기하급수적인 토큰 소모와 실행 비용을 통제하면서도, 언어 간 계산 모델의 본질적 차이를 극명하게 포착할 수 있도록 5개의 상호 직교하는(orthogonal) 계산 축에서 1문제씩 엄선하였습니다.

모든 문제는 기존 [problem](file:///D:/works/paper-lang-dist/problem) 데이터셋에서 검증된 표준 입출력 계약(stdin/stdout)과 13쌍의 정밀 평가 케이스(총 65개 평가 케이스)를 완전히 계승합니다.

---

## 2. 5대 선별 문제 요약

| 문제 ID | 문제명 | 계산 및 패러다임 축 | C++ 기준 구현 방식 | 언어 간 핵심 대조 포인트 | 상세 경로 |
|---|---|---|---|---|---|
| LC_0338 | Counting Bits | 수치 연산 및 비트 점화식 | 비트 시프트 연산, 1차원 점화식 | 재귀적 비트 분해 vs 점화식 매핑 | [LC_0338](file:///D:/works/paper-lang-dist/problem_v1/LC_0338/statement.md) |
| IPOP_9012 | 괄호 | 상태 머신 및 순차 파싱 | 루프, 가변 균형 카운터, 조기 종료 | 가변 루프 카운터 vs 불변 꼬리 재귀 누적기 | [IPOP_9012](file:///D:/works/paper-lang-dist/problem_v1/IPOP_9012/statement.md) |
| LC_0283 | Move Zeroes | 가변 메모리 조작 vs 불변 필터링 | 투 포인터 제자리 swap | 제자리 메모리 변경 vs 불변 스트림 필터링 | [LC_0283](file:///D:/works/paper-lang-dist/problem_v1/LC_0283/statement.md) |
| LC_0053 | Maximum Subarray | 동적 계획법 및 누적 최적화 | 카데인(Kadane) 알고리즘, 스칼라 갱신 | 명령형 상태 갱신 vs 고차 함수 foldl/reduce | [LC_0053](file:///D:/works/paper-lang-dist/problem_v1/LC_0053/statement.md) |
| LC_0547 | Number of Provinces | 관계형 그래프 탐색 및 도달성 | 인접행렬, 가변 boolean 방문 배열 DFS | 가변 방문 배열 vs 불변 Set 전달 재귀 | [LC_0547](file:///D:/works/paper-lang-dist/problem_v1/LC_0547/statement.md) |

---

## 3. 문제별 상세 분석 및 언어별 대조 포인트

### 문제 1. LC_0338: Counting Bits
- 공식 명세: [LC_0338/statement.md](file:///D:/works/paper-lang-dist/problem_v1/LC_0338/statement.md)
- C++ 기준 코드: [LC_0338/reference.cpp](file:///D:/works/paper-lang-dist/problem_v1/LC_0338/reference.cpp)
- 문제 설명: 0부터 N까지 각 정수의 2진수 표현에 포함된 1의 개수를 순서대로 배열로 출력합니다.
- 입출력 계약: 입력은 첫 줄 정수 N(0 <= N <= 100,000), 출력은 공백으로 구분된 N+1개 정수.
- C++ 기준 구현 특성:
  - vector<int> counts(n+1, 0) 버퍼를 할당하고, counts[i] = counts[i/2] + i%2 점화식을 통해 O(N)으로 해결합니다.
- 언어별 관용적 패턴 및 거리 유발 요인:
  - C: 정적/동적 int 배열 할당, 비트 연산자 (i >> 1) + (i & 1) 사용. C++과 구조적 거리가 가장 가깝습니다.
  - Java: int[] 배열 및 for 루프 또는 Integer.bitCount() 호출.
  - Python: [bin(x).count('1') for x in range(n+1)] 형태의 리스트 컴프리헨션 또는 DP 루프.
  - Haskell: ones n = n `mod` 2 + ones (n `div` 2) 순수 재귀 함수와 map (show . ones) [0..n] 파이프라인. 점화식 배열 생성 대신 지연 리스트 스트림 생성을 선호합니다.
  - OCaml: Array.init (n+1) (fun i -> ...) 또는 List.init을 사용한 재귀적 비트 카운팅.
  - Elixir: 0..n |> Enum.map(&popcount/1) 형태의 파이프라인과 비트 패턴 매칭.
- LLM(Qwen 3, GLM-5) 관찰 포인트:
  - 함수형 언어 변환 시 C 스타일 DP 배열을 그대로 흉내 내려고 가변 배열을 무리하게 도입하는지, 아니면 언어 고유의 map/스트림 재귀로 재구성하는지 평가합니다.

### 문제 2. IPOP_9012: 괄호
- 공식 명세: [IPOP_9012/statement.md](file:///D:/works/paper-lang-dist/problem_v1/IPOP_9012/statement.md)
- C++ 기준 코드: [IPOP_9012/reference.cpp](file:///D:/works/paper-lang-dist/problem_v1/IPOP_9012/reference.cpp)
- 문제 설명: T개의 괄호 문자열이 주어질 때, 열린 괄호와 닫힌 괄호의 짝이 올바르게 닫힌 VPS(Valid PS)인지 판별하여 YES 또는 NO를 출력합니다.
- 입출력 계약: 첫 줄 테스트케이스 수 T, 이후 T개 줄에 괄호 문자열. 각 줄마다 YES/NO 출력.
- C++ 기준 구현 특성:
  - 문자열을 순회하며 int bal 변수를 증감시키고, 중간에 bal < 0이 되면 조기 탈출(break)합니다.
- 언어별 관용적 패턴 및 거리 유발 요인:
  - C: char 포인터 순회 및 정수형 누적 변수.
  - Java: String.charAt() 순회 또는 Stack<Character> 클래스 활용.
  - Python: for char in s 루프 또는 괄호 치환 replace('()', '') 방식.
  - Haskell: balanced [] depth = depth == 0 및 패턴 매칭 balanced (c:cs) depth 형태의 꼬리 재귀. 조기 탈출을 가드 조건(depth < 0 = False)으로 처리합니다.
  - OCaml: match cs with '('::tl -> ... | ')'::tl -> ... 패턴 매칭과 재귀 함수.
  - Elixir: def balanced([?( | rest], depth)와 같이 문자 코드 매칭을 활용한 다중 함수 정의.
- LLM(Qwen 3, GLM-5) 관찰 포인트:
  - C++의 break 구문과 명령형 플래그(valid = false)가 함수형 언어로 옮겨갈 때 꼬리 재귀(tail recursion) 상태 전이 함수로 올바르게 추상화되는지 측정합니다.

### 문제 3. LC_0283: Move Zeroes
- 공식 명세: [LC_0283/statement.md](file:///D:/works/paper-lang-dist/problem_v1/LC_0283/statement.md)
- C++ 기준 코드: [LC_0283/reference.cpp](file:///D:/works/paper-lang-dist/problem_v1/LC_0283/reference.cpp)
- 문제 설명: 배열에서 0이 아닌 원소들의 상대적인 순서를 보존하면서 모든 0을 배열의 뒷부분으로 이동시킵니다.
- 입출력 계약: 첫 줄 배열 크기 N, 둘째 줄 N개 정수. 수정된 배열 전체를 공백 구분으로 출력.
- C++ 기준 구현 특성:
  - write 포인터와 read 포인터를 사용하여 swap(a[write++], a[read])을 수행하는 제자리(in-place) 가변 조작입니다.
- 언어별 관용적 패턴 및 거리 유발 요인:
  - C: 포인터 조작을 통한 제자리 swap. C++과 동일한 메모리 변경 모델.
  - Java: int write 포인터를 이용한 제자리 값 덮어쓰기.
  - Python: a = [x for x in a if x != 0] + [0] * a.count(0) 또는 투 포인터 제자리 swap.
  - Haskell: 불변 데이터 구조 특성상 제자리 조작이 불가능합니다. nonzero = filter (/=0) xs 및 nonzero ++ replicate (n - length nonzero) 0 형태로 리스트 분할/결합을 수행합니다.
  - OCaml: List.filter 기반의 불변 리스트 처리 또는 Array 모듈을 통한 가변 제자리 swap.
  - Elixir: Enum.filter(nums, &(&1 != 0)) ++ List.duplicate(0, count) 불변 리스트 합성.
- LLM(Qwen 3, GLM-5) 관찰 포인트:
  - 명령형 언어의 핵심인 제자리 메모리 변경(in-place mutation)이 순수 함수형 언어로 번역될 때, 그리고 다시 C++로 역번역될 때 원본의 투 포인터 swap 구조가 유지되는지 혹은 vector 재할당 구조로 변질되는지 관찰하는 핵심 문제입니다.

### 문제 4. LC_0053: Maximum Subarray
- 공식 명세: [LC_0053/statement.md](file:///D:/works/paper-lang-dist/problem_v1/LC_0053/statement.md)
- C++ 기준 코드: [LC_0053/reference.cpp](file:///D:/works/paper-lang-dist/problem_v1/LC_0053/reference.cpp)
- 문제 설명: 연속된 부분 배열의 합 중 최댓값을 구합니다.
- 입출력 계약: 첫 줄 배열 크기 N, 둘째 줄 N개 정수. 최댓값 정수 하나 출력.
- C++ 기준 구현 특성:
  - 카데인(Kadane) 알고리즘을 사용하여 단일 루프에서 cur = max(a[i], cur + a[i])와 best = max(best, cur) 두 변수를 갱신합니다.
- 언어별 관용적 패턴 및 거리 유발 요인:
  - C / Java: 2개의 스칼라 변수를 루프에서 갱신하는 정석적인 카데인 알고리즘.
  - Python: max() 함수 기반의 루프 또는 functools.reduce.
  - Haskell: foldl' step (head xs, head xs) (tail xs) 고차 함수 활용. 누적 상태를 튜플 (ending, best)로 묶어 전달합니다.
  - OCaml: List.fold_left를 사용하여 상태 쌍 (acc_cur, acc_max)를 넘기는 불변 누적.
  - Elixir: Enum.reduce(tail, {head, head}, fn x, {cur, best} -> ... end) 튜플 축약.
- LLM(Qwen 3, GLM-5) 관찰 포인트:
  - 루프 내부의 가변 변수 2개가 함수형 고차 축약 함수(fold/reduce)의 어큐뮬레이터 튜플로 매핑되는 과정에서 수렴성과 안정성을 평가합니다.

### 문제 5. LC_0547: Number of Provinces
- 공식 명세: [LC_0547/statement.md](file:///D:/works/paper-lang-dist/problem_v1/LC_0547/statement.md)
- C++ 기준 코드: [LC_0547/reference.cpp](file:///D:/works/paper-lang-dist/problem_v1/LC_0547/reference.cpp)
- 문제 설명: N x N 인접 행렬로 표현된 무방향 연결 그래프에서 서로 연결된 독립적인 연결 요소(컴포넌트)의 총개수를 구합니다.
- 입출력 계약: 첫 줄 정수 N(1 <= N <= 200), 이후 N개 줄에 N개의 0 또는 1. 컴포넌트 수 정수 하나 출력.
- C++ 기준 구현 특성:
  - vector<vector<int>> g 인접행렬과 vector<bool> seen 방문 배열을 사용하며, 명시적 스택(stack)을 이용한 비재귀 DFS로 미방문 노드를 탐색합니다.
- 언어별 관용적 패턴 및 거리 유발 요인:
  - C: 2차원 배열과 int visited[] 배열을 사용하는 DFS/BFS 함수.
  - Java: 재귀 DFS 또는 Disjoint Set Union(유니온 파인드) 클래스 구현.
  - Python: set 자료형을 방문 집합으로 유지하며 재귀 DFS 또는 큐 기반 BFS.
  - Haskell: Data.IntSet을 방문 집합으로 삼아 visit 함수에 seen을 인자로 넘기고 새로운 seen을 반환받는 불변 상태 스레딩.
  - OCaml: Set 모듈을 통한 불변 집합 누적 또는 bool 배열 기반의 명령형 순회.
  - Elixir: MapSet.put 및 MapSet.member를 활용한 꼬리 재귀 그래프 순회.
- LLM(Qwen 3, GLM-5) 관찰 포인트:
  - 복잡한 관계형 데이터 구조(그래프)와 전역 상태(방문 목록)를 다룰 때, 객체지향/명령형의 가변 참조 vs 함수형의 불변 Set 상태 전달이 가장 큰 의미 거리를 만들어내는 벤치마크입니다.

---

## 4. 디렉토리 구조

```text
problem_v1/
  dataset-index.json             # 5개 문제 메타데이터 및 설정 파일
  README.md                      # 코퍼스 선정 배경 및 상세 분석 보고서
  LC_0338/                       # 문제 1: 수치/비트 점화식
    statement.md
    reference.cpp
    README.md
    public_examples.json
    prompt_examples/
    evaluation/                  # case01..13.inp, case01..13.out
  IPOP_9012/                     # 문제 2: 상태 머신/순차 파싱
    statement.md
    reference.cpp
    README.md
    prompt_examples/
    evaluation/                  # case01..13.inp, case01..13.out
  LC_0283/                       # 문제 3: 가변 배열 조작 vs 불변 필터링
    statement.md
    reference.cpp
    README.md
    public_examples.json
    prompt_examples/
    evaluation/                  # case01..13.inp, case01..13.out
  LC_0053/                       # 문제 4: 동적 계획법/카데인 최적화
    statement.md
    reference.cpp
    README.md
    public_examples.json
    prompt_examples/
    evaluation/                  # case01..13.inp, case01..13.out
  LC_0547/                       # 문제 5: 관계형 그래프 탐색
    statement.md
    reference.cpp
    README.md
    public_examples.json
    prompt_examples/
    evaluation/                  # case01..13.inp, case01..13.out
```

---

## 5. 실험 설정 및 실행 예시

rttdist 실행 설정 YAML 파일(예: `config_v1.yaml`)에서 다음과 같이 `problem_root`와 `problem_ids`를 지정하여 실험을 수행할 수 있습니다.

```yaml
problem_root: problem_v1
problem_ids:
  - LC_0338
  - IPOP_9012
  - LC_0283
  - LC_0053
  - LC_0547
seed_language: cpp
target_languages:
  - c
  - java
  - python
  - haskell
  - ocaml
  - elixir
```

5개 문제를 통해 총 6개 언어 경로(C++, C, Java, Python, Haskell, OCaml, Elixir)와 2개 모델(Qwen 3, GLM-5) 간의 의미 거리를 효율적이고 정밀하게 측정할 수 있습니다.
