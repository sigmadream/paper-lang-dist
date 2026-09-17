# LC_0035: Search Insert Position

정렬 배열에서 target의 위치 또는 정렬을 유지할 삽입 위치를 0-based로 출력한다.

- 유형: 이분탐색
- [문제 명세와 입출력](statement.md)
- [C++17 기준 풀이](reference.cpp)
- [저장소 대응 풀이](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/search_insert_position/solution.js)
- [공식 문제](https://leetcode.com/problems/search-insert-position/)
- 정답 교차 검증: lower-bound 이분탐색 / target보다 작은 원소 개수

공개 입력 예제 전체는 [public_examples.json](public_examples.json)에 기록하고 평가 입력에서 제외했다. 프롬프트에 사용할 수 있는 파일은 statement.md와 prompt_examples뿐이다.
아래 입력은 자체 생성한 평가용 자료이며 공식 비공개 테스트가 아니다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 최소 크기 존재 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 최솟값보다 작음 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 최댓값보다 큼 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 첫 원소 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 마지막 원소 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 내부 원소 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 중간 빈 위치 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 큰 양수 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 큰 음수 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 홀수 길이의 부재 값 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |
| case11 | 고정 seed 기능 입력 1 | [입력](evaluation/case11.inp) | [정답](evaluation/case11.out) |
| case12 | 고정 seed 기능 입력 2 | [입력](evaluation/case12.inp) | [정답](evaluation/case12.out) |
| case13 | 규모·수치 경계 입력 | [입력](evaluation/case13.inp) | [정답](evaluation/case13.out) |

이 README, evaluation, manifest, 검증 보고서를 번역 프롬프트에 넣지 않는다.
