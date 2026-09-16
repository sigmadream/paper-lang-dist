# LC_0496: Next Greater Element I

nums1의 각 원소가 nums2에서 처음 만나는 오른쪽의 더 큰 값을 출력한다. 없으면 -1이다.

- 유형: 스택
- [문제 명세와 입출력](statement.md)
- [C++17 기준 풀이](reference.cpp)
- [저장소 대응 풀이](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/next_greater_element_i/solution.js)
- [공식 문제](https://leetcode.com/problems/next-greater-element-i/)
- 정답 교차 검증: 단조 스택 사전 / 질의별 오른쪽 직접 탐색

공개 입력 예제 전체는 [public_examples.json](public_examples.json)에 기록하고 평가 입력에서 제외했다. 프롬프트에 사용할 수 있는 파일은 statement.md와 prompt_examples뿐이다.
아래 입력은 자체 생성한 평가용 자료이며 공식 비공개 테스트가 아니다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 최소 배열 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 값 양끝 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 마지막 질의 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 감소 배열 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 증가 배열 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 질의 순서 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 멀리 있는 큰 값 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 다른 거리 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 조회 순서 뒤집기 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 내부 질의 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |

이 README, evaluation, manifest, 검증 보고서를 번역 프롬프트에 넣지 않는다.
