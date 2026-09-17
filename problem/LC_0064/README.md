# LC_0064: Minimum Path Sum

오른쪽·아래로만 이동할 때 좌상단에서 우하단까지 방문한 칸의 값의 합을 최소화한다.

- 유형: 동적 계획법·격자
- [문제 명세와 입출력](statement.md)
- [C++17 기준 풀이](reference.cpp)
- [저장소 대응 풀이](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/minimum_path_sum/solution.js)
- [공식 문제](https://leetcode.com/problems/minimum-path-sum/)
- 정답 교차 검증: 최소 누적합 DP / 메모이제이션을 사용한 도착점 기준 재귀 비용 계산

공개 입력 예제 전체는 [public_examples.json](public_examples.json)에 기록하고 평가 입력에서 제외했다. 프롬프트에 사용할 수 있는 파일은 statement.md와 prompt_examples뿐이다.
아래 입력은 자체 생성한 평가용 자료이며 공식 비공개 테스트가 아니다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 최소 값 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 칸 값 상한 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 한 행 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 한 열 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 모든 값 0 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 아래 우선 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 오른쪽 우선 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 내부 꺾임 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 최대 값 반복 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 직사각형 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |
| case11 | 고정 seed 기능 입력 1 | [입력](evaluation/case11.inp) | [정답](evaluation/case11.out) |
| case12 | 고정 seed 기능 입력 2 | [입력](evaluation/case12.inp) | [정답](evaluation/case12.out) |
| case13 | 규모·수치 경계 입력 | [입력](evaluation/case13.inp) | [정답](evaluation/case13.out) |

이 README, evaluation, manifest, 검증 보고서를 번역 프롬프트에 넣지 않는다.
