# problem_v1.5 다국어 해답지 (Solutions)

본 디렉토리는 problem_v1.5의 5개 문제에 대해 7개 언어(C++, C, Python, Java, Haskell, Erlang, OCaml)로 작성된 해답지를 별도로 보관하는 공간입니다.

## 1. 구성 문제 목록

1. LC_0338: Counting Bits (수치 연산 및 비트 점화식)
2. IPOP_9012: 괄호 (상태 머신 및 순차 파싱)
3. LC_0283: Move Zeroes (배열 제자리 이동 및 필터링)
4. LC_0053: Maximum Subarray (동적 계획법 및 카데인 알고리즘)
5. LC_0547: Number of Provinces (무방향 그래프 탐색 및 연결 성분 개수)

## 2. 지원 언어 및 파일 매핑

각 문제 디렉토리마다 아래의 7개 언어 정답 소스 코드가 포함되어 있습니다.

- C++: solution.cpp
- C: solution.c
- Python: solution.py
- Java: Main.java
- Haskell: solution.hs
- Erlang: solution.erl
- OCaml: solution.ml

## 3. 디렉토리 구조

- [LC_0338](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0338)
  - [solution.cpp](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0338/solution.cpp)
  - [solution.c](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0338/solution.c)
  - [solution.py](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0338/solution.py)
  - [Main.java](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0338/Main.java)
  - [solution.hs](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0338/solution.hs)
  - [solution.erl](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0338/solution.erl)
  - [solution.ml](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0338/solution.ml)

- [IPOP_9012](file:///D:/works/paper-lang-dist/solutions_v1.5/IPOP_9012)
  - [solution.cpp](file:///D:/works/paper-lang-dist/solutions_v1.5/IPOP_9012/solution.cpp)
  - [solution.c](file:///D:/works/paper-lang-dist/solutions_v1.5/IPOP_9012/solution.c)
  - [solution.py](file:///D:/works/paper-lang-dist/solutions_v1.5/IPOP_9012/solution.py)
  - [Main.java](file:///D:/works/paper-lang-dist/solutions_v1.5/IPOP_9012/Main.java)
  - [solution.hs](file:///D:/works/paper-lang-dist/solutions_v1.5/IPOP_9012/solution.hs)
  - [solution.erl](file:///D:/works/paper-lang-dist/solutions_v1.5/IPOP_9012/solution.erl)
  - [solution.ml](file:///D:/works/paper-lang-dist/solutions_v1.5/IPOP_9012/solution.ml)

- [LC_0283](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0283)
  - [solution.cpp](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0283/solution.cpp)
  - [solution.c](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0283/solution.c)
  - [solution.py](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0283/solution.py)
  - [Main.java](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0283/Main.java)
  - [solution.hs](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0283/solution.hs)
  - [solution.erl](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0283/solution.erl)
  - [solution.ml](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0283/solution.ml)

- [LC_0053](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0053)
  - [solution.cpp](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0053/solution.cpp)
  - [solution.c](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0053/solution.c)
  - [solution.py](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0053/solution.py)
  - [Main.java](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0053/Main.java)
  - [solution.hs](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0053/solution.hs)
  - [solution.erl](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0053/solution.erl)
  - [solution.ml](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0053/solution.ml)

- [LC_0547](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0547)
  - [solution.cpp](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0547/solution.cpp)
  - [solution.c](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0547/solution.c)
  - [solution.py](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0547/solution.py)
  - [Main.java](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0547/Main.java)
  - [solution.hs](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0547/solution.hs)
  - [solution.erl](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0547/solution.erl)
  - [solution.ml](file:///D:/works/paper-lang-dist/solutions_v1.5/LC_0547/solution.ml)

## 4. 컴파일 및 실행 방법

1. C++
   - 컴파일: clang++ -O2 solution.cpp -o solution.exe
   - 실행: ./solution.exe < input.txt

2. C
   - 컴파일: clang -O2 solution.c -o solution.exe
   - 실행: ./solution.exe < input.txt

3. Python
   - 실행: python solution.py < input.txt

4. Java
   - 컴파일: javac -encoding UTF-8 Main.java
   - 실행: java Main < input.txt

5. Haskell
   - 컴파일: ghc -O2 solution.hs -o solution.exe
   - 실행: ./solution.exe < input.txt 또는 runghc solution.hs < input.txt

6. Erlang
   - 실행: escript solution.erl < input.txt

7. OCaml
   - 실행: ocaml solution.ml < input.txt
