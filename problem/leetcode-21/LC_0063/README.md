# LC_0063: Unique Paths Ii

0은 통과 가능, 1은 장애물이다. 좌상단에서 우하단까지 오른쪽·아래로만 이동하는 경로 수를 구한다.

- 유형: 동적 계획법·격자
- [문제 명세와 입출력](statement.md)
- [C++17 기준 풀이](reference.cpp)
- [저장소 대응 풀이](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/unique_paths_ii/solution.js)
- [공식 문제](https://leetcode.com/problems/unique-paths-ii/)
- 정답 교차 검증: 격자 DP / 모든 합법 경로 재귀 탐색

공개 입력 예제 전체는 [public_examples.json](public_examples.json)에 기록하고 평가 입력에서 제외했다. 프롬프트에 사용할 수 있는 파일은 statement.md와 prompt_examples뿐이다.
아래 입력은 자체 생성한 평가용 자료이며 공식 비공개 테스트가 아니다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 최소 통과 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 최소 차단 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 한 행 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 한 열 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 출발점 차단 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 도착점 차단 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 장애물 없음 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 우회 통로 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 가로 장벽 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 여러 우회 경로 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |

이 README, evaluation, manifest, 검증 보고서를 번역 프롬프트에 넣지 않는다.
