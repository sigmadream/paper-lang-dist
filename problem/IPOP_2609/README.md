# IPOP_2609: 최대공약수와 최소공배수

두 양의 정수의 최대공약수와 최소공배수를 순서대로 출력한다.

[기존 문제 명세](statement.md) · [원문](https://www.acmicpc.net/problem/2609)

입력은 이 평가 묶음에서 자체 생성했다. GitHub 저장소의 공식 테스트를 수집한 것이 아니다.
기존 입력 파일 전체와 문제 본문의 입력 예제를 공백 정규화 후 제외했다. 모든 정답은 아래 두 방식으로 교차 검증했다.

- 기준 계산: 유클리드 GCD와 곱/GCD
- 독립 검증: 약수·공배수 직접 순회

이 묶음에서 채택한 LeetCode 대응 풀이는 없다. 로컬 명세와 독립 검증기를 사용한다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 두 수의 하한 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 하한과 상한 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 동일 상한 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 서로 다른 소수 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 약수 관계 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 입력 순서 역전 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 공통 인수 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 서로소 거듭제곱 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 상한 근처 연속 수 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 비자명 공약수 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |
| case11 | 고정 seed 기능 입력 1 | [입력](evaluation/case11.inp) | [정답](evaluation/case11.out) |
| case12 | 고정 seed 기능 입력 2 | [입력](evaluation/case12.inp) | [정답](evaluation/case12.out) |
| case13 | 규모·수치 경계 입력 | [입력](evaluation/case13.inp) | [정답](evaluation/case13.out) |

정답 파일은 평가 전용이며 번역 프롬프트에 넣지 않는다. 검증 결과와 파일 해시는 [manifest](../metadata/ipop19/manifest.json) 및 [validation_report](../metadata/ipop19/validation_report.json)에 기록한다.
