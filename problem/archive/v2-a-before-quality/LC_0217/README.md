# LC_0217: Contains Duplicate

배열에 같은 값이 두 번 이상 등장하면 1, 아니면 0을 출력한다.

- 유형: 배열·해시
- [문제 명세와 입출력](statement.md)
- [C++17 기준 풀이](reference.cpp)
- [저장소 대응 풀이](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/contains_duplicate/solution.js)
- [공식 문제](https://leetcode.com/problems/contains-duplicate/)
- 정답 교차 검증: 집합 크기 비교 / 정렬 후 인접 값 검사

공개 입력 예제 전체는 [public_examples.json](public_examples.json)에 기록하고 평가 입력에서 제외했다. 프롬프트에 사용할 수 있는 파일은 statement.md와 prompt_examples뿐이다.
아래 입력은 자체 생성한 평가용 자료이며 공식 비공개 테스트가 아니다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 최소 크기 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 같은 두 값 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 다른 두 값 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 음수 중복 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 0 중복 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 값 양끝 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 마지막 원소 중복 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 모두 동일 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 정렬 역순 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 반복 없는 혼합 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |

이 README, evaluation, manifest, 검증 보고서를 번역 프롬프트에 넣지 않는다.
