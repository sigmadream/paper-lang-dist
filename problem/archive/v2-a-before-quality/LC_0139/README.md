# LC_0139: Word Break

문자열을 사전 단어들의 연결로 만들 수 있으면 1을 출력한다. 같은 단어를 여러 번 쓸 수 있다.

- 유형: 동적 계획법·문자열
- [문제 명세와 입출력](statement.md)
- [C++17 기준 풀이](reference.cpp)
- [저장소 대응 풀이](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/word_break/solution.js)
- [공식 문제](https://leetcode.com/problems/word-break/)
- 정답 교차 검증: 접두사 DP / 모든 분할 위치 완전탐색

공개 입력 예제 전체는 [public_examples.json](public_examples.json)에 기록하고 평가 입력에서 제외했다. 프롬프트에 사용할 수 있는 파일은 statement.md와 prompt_examples뿐이다.
아래 입력은 자체 생성한 평가용 자료이며 공식 비공개 테스트가 아니다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 최소 성공 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 최소 실패 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 단어 재사용 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 두 단어 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 탐욕적 접두 선택 함정 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 끝부분 실패 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 긴 접두 후 실패 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 같은 단어 두 번 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 전체 단어도 허용 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 여러 분할 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |

이 README, evaluation, manifest, 검증 보고서를 번역 프롬프트에 넣지 않는다.
