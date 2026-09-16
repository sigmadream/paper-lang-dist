# IPOP_10988: 팰린드롬인지 확인하기

소문자 문자열 하나를 읽고 팰린드롬이면 1, 아니면 0을 출력한다.

[기존 문제 명세](../../IPOP_10988.md) · [원문](https://www.acmicpc.net/problem/10988)

입력은 이 평가 묶음에서 자체 생성했다. GitHub 저장소의 공식 테스트를 수집한 것이 아니다.
기존 입력 파일 전체와 문제 본문의 입력 예제를 공백 정규화 후 제외했다. 모든 정답은 아래 두 방식으로 교차 검증했다.

- 기준 계산: 문자열 역순 비교
- 독립 검증: 대칭 위치 전수 비교

추가 대응 풀이: [problems/valid_palindrome/solution.js](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/valid_palindrome/solution.js). 소문자 영문 입력에 한정하고 boolean을 0/1로 변환.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 최소 길이 | [입력](case01.inp) | [정답](case01.out) |
| case02 | 길이 2 대칭 | [입력](case02.inp) | [정답](case02.out) |
| case03 | 길이 2 비대칭 | [입력](case03.inp) | [정답](case03.out) |
| case04 | 홀수 대칭 | [입력](case04.inp) | [정답](case04.out) |
| case05 | 짝수 대칭 | [입력](case05.inp) | [정답](case05.out) |
| case06 | 중앙 근처 불일치 | [입력](case06.inp) | [정답](case06.out) |
| case07 | 같은 문자 반복 | [입력](case07.inp) | [정답](case07.out) |
| case08 | 최대 길이 대칭 | [입력](case08.inp) | [정답](case08.out) |
| case09 | 최대 길이 끝 불일치 | [입력](case09.inp) | [정답](case09.out) |
| case10 | 긴 짝수 대칭 | [입력](case10.inp) | [정답](case10.out) |

정답 파일은 평가 전용이며 번역 프롬프트에 넣지 않는다. 검증 결과와 파일 해시는 상위 manifest 및 validation_report에 기록한다.
