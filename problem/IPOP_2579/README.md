# IPOP_2579: 계단 오르기

1칸 또는 2칸씩 이동하고 세 계단 연속 방문을 금지하며 마지막 계단까지 점수를 최대화한다.

[기존 문제 명세](statement.md) · [원문](https://www.acmicpc.net/problem/2579)

입력은 이 평가 묶음에서 자체 생성했다. GitHub 저장소의 공식 테스트를 수집한 것이 아니다.
기존 입력 파일 전체와 문제 본문의 입력 예제를 공백 정규화 후 제외했다. 모든 정답은 아래 두 방식으로 교차 검증했다.

- 기준 계산: 점화식 DP
- 독립 검증: 메모이제이션을 사용한 합법 이동 상태 탐색

이 묶음에서 채택한 LeetCode 대응 풀이는 없다. 로컬 명세와 독립 검증기를 사용한다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 최소 계단과 점수 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 점수 상한 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 두 계단 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 세 계단 연속 금지 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 양끝 고득점 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 동일 점수 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 증가 점수 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 감소 점수 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 번갈아 고득점 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 홀수 길이 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |
| case11 | 고정 seed 기능 입력 1 | [입력](evaluation/case11.inp) | [정답](evaluation/case11.out) |
| case12 | 고정 seed 기능 입력 2 | [입력](evaluation/case12.inp) | [정답](evaluation/case12.out) |
| case13 | 규모·수치 경계 입력 | [입력](evaluation/case13.inp) | [정답](evaluation/case13.out) |

정답 파일은 평가 전용이며 번역 프롬프트에 넣지 않는다. 검증 결과와 파일 해시는 [manifest](../metadata/ipop19/manifest.json) 및 [validation_report](../metadata/ipop19/validation_report.json)에 기록한다.
