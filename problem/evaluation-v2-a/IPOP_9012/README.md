# IPOP_9012: 괄호

T개 소괄호 문자열마다 올바른 괄호열이면 YES, 아니면 NO를 출력한다.

[기존 문제 명세](../../IPOP_9012.md) · [원문](https://www.acmicpc.net/problem/9012)

입력은 이 평가 묶음에서 자체 생성했다. GitHub 저장소의 공식 테스트를 수집한 것이 아니다.
기존 입력 파일 전체와 문제 본문의 입력 예제를 공백 정규화 후 제외했다. 모든 정답은 아래 두 방식으로 교차 검증했다.

- 기준 계산: 접두 합과 최종 균형
- 독립 검증: 인접 괄호 쌍 반복 제거

추가 대응 풀이: [problems/valid_parentheses/solution.js](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/valid_parentheses/solution.js). 소괄호 입력에 한정하고 각 문자열의 boolean을 YES/NO로 변환.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 최소 올바른 괄호 | [입력](case01.inp) | [정답](case01.out) |
| case02 | 최소 잘못된 접두사 | [입력](case02.inp) | [정답](case02.out) |
| case03 | 중첩 | [입력](case03.inp) | [정답](case03.out) |
| case04 | 연속 쌍 | [입력](case04.inp) | [정답](case04.out) |
| case05 | 닫는 괄호 부족 | [입력](case05.inp) | [정답](case05.out) |
| case06 | 여는 괄호 부족 | [입력](case06.inp) | [정답](case06.out) |
| case07 | 길이 상한 중첩 | [입력](case07.inp) | [정답](case07.out) |
| case08 | 균형만 맞고 접두사 오류 | [입력](case08.inp) | [정답](case08.out) |
| case09 | 길이 상한 반복 | [입력](case09.inp) | [정답](case09.out) |
| case10 | 여러 질의 혼합 | [입력](case10.inp) | [정답](case10.out) |

정답 파일은 평가 전용이며 번역 프롬프트에 넣지 않는다. 검증 결과와 파일 해시는 상위 manifest 및 validation_report에 기록한다.
