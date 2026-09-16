# LC_0338: Counting Bits

0부터 N까지 각 정수의 이진 표현에서 1의 개수를 순서대로 출력한다.

- 유형: 비트·수치
- [문제 명세와 입출력](statement.md)
- [C++17 기준 풀이](reference.cpp)
- [저장소 대응 풀이](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/counting_bits/solution.js)
- [공식 문제](https://leetcode.com/problems/counting-bits/)
- 정답 교차 검증: 절반 값 기반 DP / 각 수를 2로 나누며 나머지 합산

공개 입력 예제 전체는 [public_examples.json](public_examples.json)에 기록하고 평가 입력에서 제외했다. 프롬프트에 사용할 수 있는 파일은 statement.md와 prompt_examples뿐이다.
아래 입력은 자체 생성한 평가용 자료이며 공식 비공개 테스트가 아니다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | N=0: 0 및 2의 거듭제곱 경계 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | N=1: 0 및 2의 거듭제곱 경계 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | N=3: 0 및 2의 거듭제곱 경계 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | N=4: 0 및 2의 거듭제곱 경계 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | N=7: 0 및 2의 거듭제곱 경계 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | N=8: 0 및 2의 거듭제곱 경계 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | N=15: 0 및 2의 거듭제곱 경계 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | N=16: 0 및 2의 거듭제곱 경계 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | N=31: 0 및 2의 거듭제곱 경계 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | N=100000: 입력 상한 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |

이 README, evaluation, manifest, 검증 보고서를 번역 프롬프트에 넣지 않는다.
