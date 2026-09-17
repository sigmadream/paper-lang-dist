# IPOP_11729: 하노이 탑 이동 순서

N개 원판을 1번에서 3번 막대로 옮기는 최소 이동 횟수와 이동 목록을 출력한다.

[기존 문제 명세](statement.md) · [원문](https://www.acmicpc.net/problem/11729)

입력은 이 평가 묶음에서 자체 생성했다. GitHub 저장소의 공식 테스트를 수집한 것이 아니다.
기존 입력 파일 전체와 문제 본문의 입력 예제를 공백 정규화 후 제외했다. 모든 정답은 아래 두 방식으로 교차 검증했다.

- 기준 계산: 재귀 이동열 생성
- 독립 검증: 모든 이동의 합법성·최종 상태·2^N-1 최소 이동 수 검사

이 묶음에서 채택한 LeetCode 대응 풀이는 없다. 로컬 명세와 독립 검증기를 사용한다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | N=1, 최소 크기 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | N=2, 홀수/짝수 재귀 이동 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | N=4, 홀수/짝수 재귀 이동 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | N=5, 홀수/짝수 재귀 이동 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | N=6, 홀수/짝수 재귀 이동 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | N=7, 홀수/짝수 재귀 이동 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | N=8, 홀수/짝수 재귀 이동 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | N=9, 홀수/짝수 재귀 이동 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | N=10, 홀수/짝수 재귀 이동 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | N=11, 홀수/짝수 재귀 이동 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |

정답 파일은 평가 전용이며 번역 프롬프트에 넣지 않는다. 검증 결과와 파일 해시는 [manifest](../metadata/ipop19/manifest.json) 및 [validation_report](../metadata/ipop19/validation_report.json)에 기록한다.
