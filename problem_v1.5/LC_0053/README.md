# LC_0053: Maximum Subarray

비어 있지 않은 연속 부분배열의 합 중 최댓값을 구한다.

- 유형: 동적 계획법
- [문제 명세와 입출력](statement.md)
- [C++17 기준 풀이](reference.cpp)
- [저장소 대응 풀이](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/maximum_subarray/solution.js)
- [공식 문제](https://leetcode.com/problems/maximum-subarray/)
- 정답 교차 검증: Kadane DP / 소형 구간 전수 검사 / 대형 누적합과 최소 접두합

공개 입력 예제 전체는 [public_examples.json](public_examples.json)에 기록하고 평가 입력에서 제외했다. 프롬프트에 사용할 수 있는 파일은 statement.md와 prompt_examples뿐이다.
아래 입력은 자체 생성한 평가용 자료이며 공식 비공개 테스트가 아니다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 음수 하나 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 0 하나 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 양수 하나 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 모두 음수 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 모두 양수 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 내부 최대 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 마지막 최대 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 첫 부분 최대 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 0 포함 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 큰 양수 연결 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |
| case11 | 고정 seed 기능 입력 1 | [입력](evaluation/case11.inp) | [정답](evaluation/case11.out) |
| case12 | 고정 seed 기능 입력 2 | [입력](evaluation/case12.inp) | [정답](evaluation/case12.out) |
| case13 | 규모·수치 경계 입력 | [입력](evaluation/case13.inp) | [정답](evaluation/case13.out) |

이 README, evaluation, manifest, 검증 보고서를 번역 프롬프트에 넣지 않는다.
