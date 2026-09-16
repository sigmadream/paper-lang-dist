# LC_0242: Valid Anagram

두 소문자 문자열의 문자별 개수가 모두 같으면 1, 아니면 0을 출력한다.

- 유형: 문자열
- [문제 명세와 입출력](statement.md)
- [C++17 기준 풀이](reference.cpp)
- [저장소 대응 풀이](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/valid_anagram/solution.js)
- [공식 문제](https://leetcode.com/problems/valid-anagram/)
- 정답 교차 검증: 문자 빈도표 / 문자 정렬 비교

공개 입력 예제 전체는 [public_examples.json](public_examples.json)에 기록하고 평가 입력에서 제외했다. 프롬프트에 사용할 수 있는 파일은 statement.md와 prompt_examples뿐이다.
아래 입력은 자체 생성한 평가용 자료이며 공식 비공개 테스트가 아니다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 최소 일치 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 최소 불일치 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 길이 다름 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 역순 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 중복 문자 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 빈도 차이 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 한 문자 차이 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 동일 문자 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 여러 빈도 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 알파벳 전체 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |

이 README, evaluation, manifest, 검증 보고서를 번역 프롬프트에 넣지 않는다.
