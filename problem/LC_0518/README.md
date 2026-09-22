# LC_0518: Coin Change Ii

동전을 무제한 사용해 amount를 만드는 조합 수를 구한다. 동전 순서는 구별하지 않는다.

- 유형: 동적 계획법·수치
- [문제 명세와 입출력](statement.md)
- [C++17 기준 풀이](reference.cpp)
- [저장소 대응 풀이](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/coin_change_ii/solution.js)
- [공식 문제](https://leetcode.com/problems/coin-change-ii/)
- 정답 교차 검증: 동전별 조합 DP / 메모이제이션 액면가별 개수 탐색 / 최대공약수 도달 불가 증명

공개 입력 예제 전체는 [public_examples.json](public_examples.json)에 기록하고 평가 입력에서 제외했다. 프롬프트에 사용할 수 있는 파일은 statement.md와 prompt_examples뿐이다.
아래 입력은 자체 생성한 평가용 자료이며 공식 비공개 테스트가 아니다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 0원 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 최소 액면가 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 도달 불가 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 조합과 순열 구분 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 서로소 액면가 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 짝수 액면가 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 홀수 도달 불가 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 정렬되지 않은 동전 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 다양한 조합 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 금액과 액면가 상한 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |
| case11 | 고정 seed 기능 입력 1 | [입력](evaluation/case11.inp) | [정답](evaluation/case11.out) |
| case12 | 고정 seed 기능 입력 2 | [입력](evaluation/case12.inp) | [정답](evaluation/case12.out) |
| case13 | 규모·수치 경계 입력 | [입력](evaluation/case13.inp) | [정답](evaluation/case13.out) |

이 README, evaluation, manifest, 검증 보고서를 번역 프롬프트에 넣지 않는다.
