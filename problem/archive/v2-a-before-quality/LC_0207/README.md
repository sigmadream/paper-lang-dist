# LC_0207: Course Schedule

선수과목 관계 [a,b]는 b를 먼저 이수해야 a를 들을 수 있다는 뜻이다. 모든 과목을 이수할 수 있으면 1이다.

- 유형: 그래프
- [문제 명세와 입출력](statement.md)
- [C++17 기준 풀이](reference.cpp)
- [저장소 대응 풀이](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/course_schedule/solution.js)
- [공식 문제](https://leetcode.com/problems/course-schedule/)
- 정답 교차 검증: Kahn 위상 정렬 / 모든 정점 순서의 선수 관계 검사

공개 입력 예제 전체는 [public_examples.json](public_examples.json)에 기록하고 평가 입력에서 제외했다. 프롬프트에 사용할 수 있는 파일은 statement.md와 prompt_examples뿐이다.
아래 입력은 자체 생성한 평가용 자료이며 공식 비공개 테스트가 아니다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 최소 과목 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 자기 순환 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 선수 관계 없음 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 선형 선수 관계 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 세 과목 순환 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 다이아몬드 DAG | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 분리된 순환 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 역순 나열 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 고립 과목 포함 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 긴 순환 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |

이 README, evaluation, manifest, 검증 보고서를 번역 프롬프트에 넣지 않는다.
