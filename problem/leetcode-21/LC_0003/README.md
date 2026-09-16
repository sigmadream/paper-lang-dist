# LC_0003: Longest Substring Without Repeating Characters

문자가 중복되지 않는 연속 부분문자열의 최대 길이를 구한다. 빈 문자열의 답은 0이다.

- 유형: 문자열·슬라이딩 윈도
- [문제 명세와 입출력](statement.md)
- [C++17 기준 풀이](reference.cpp)
- [저장소 대응 풀이](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/longest_substring_without_repeating_characters/solution.js)
- [공식 문제](https://leetcode.com/problems/longest-substring-without-repeating-characters/)
- 정답 교차 검증: 최근 등장 위치 기반 윈도 / 모든 부분문자열의 고유 문자 검사

공개 입력 예제 전체는 [public_examples.json](public_examples.json)에 기록하고 평가 입력에서 제외했다. 프롬프트에 사용할 수 있는 파일은 statement.md와 prompt_examples뿐이다.
아래 입력은 자체 생성한 평가용 자료이며 공식 비공개 테스트가 아니다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 빈 문자열 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 공백 하나 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 같은 문자 반복 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 모두 다름 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 왼쪽 경계 역행 방지 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 겹치는 후보 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 공백 포함 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 대소문자와 기호 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 중간 반복 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 숫자와 반복 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |

이 README, evaluation, manifest, 검증 보고서를 번역 프롬프트에 넣지 않는다.
