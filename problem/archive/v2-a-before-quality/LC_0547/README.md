# LC_0547: Number Of Provinces

대칭 인접행렬로 주어진 무방향 그래프의 연결 성분 수를 구한다.

- 유형: 그래프
- [문제 명세와 입출력](statement.md)
- [C++17 기준 풀이](reference.cpp)
- [저장소 대응 풀이](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/number_of_provinces/solution.js)
- [공식 문제](https://leetcode.com/problems/number-of-provinces/)
- 정답 교차 검증: DFS 연결 성분 / 서로소 집합 병합

공개 입력 예제 전체는 [public_examples.json](public_examples.json)에 기록하고 평가 입력에서 제외했다. 프롬프트에 사용할 수 있는 파일은 statement.md와 prompt_examples뿐이다.
아래 입력은 자체 생성한 평가용 자료이며 공식 비공개 테스트가 아니다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 한 정점 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 모두 고립 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 단일 연결 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 간접 연결 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 두 성분 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 긴 사슬 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 별 모양 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 연결 성분과 고립점 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 완전 그래프 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 세 성분 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |

이 README, evaluation, manifest, 검증 보고서를 번역 프롬프트에 넣지 않는다.
