# LC_0387: First Unique Character In A String

한 번만 등장하는 첫 문자의 0-based 인덱스를 출력하고 없으면 -1을 출력한다.

- 유형: 문자열
- [문제 명세와 입출력](statement.md)
- [C++17 기준 풀이](reference.cpp)
- [저장소 대응 풀이](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/first_unique_character_in_a_string/solution.js)
- [공식 문제](https://leetcode.com/problems/first-unique-character-in-a-string/)
- 정답 교차 검증: 빈도표와 첫 위치 / 각 위치의 다른 위치 전수 대조

공개 입력 예제 전체는 [public_examples.json](public_examples.json)에 기록하고 평가 입력에서 제외했다. 프롬프트에 사용할 수 있는 파일은 statement.md와 prompt_examples뿐이다.
아래 입력은 자체 생성한 평가용 자료이며 공식 비공개 테스트가 아니다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 최소 문자열 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 고유 문자 없음 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 마지막 고유 문자 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 첫 고유 문자 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 중간 고유 문자 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 여러 고유 문자 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 모든 문자 반복 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 모든 문자 두 번 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 모든 문자 고유 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 긴 반복 안의 고유 문자 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |

이 README, evaluation, manifest, 검증 보고서를 번역 프롬프트에 넣지 않는다.
