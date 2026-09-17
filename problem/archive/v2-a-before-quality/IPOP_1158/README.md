# IPOP_1158: 요세푸스 문제

N명 중 K번째 사람을 반복 제거한 순서를 꺾쇠와 쉼표 형식으로 출력한다.

[기존 문제 명세](statement.md) · [원문](https://www.acmicpc.net/problem/1158)

입력은 이 평가 묶음에서 자체 생성했다. GitHub 저장소의 공식 테스트를 수집한 것이 아니다.
기존 입력 파일 전체와 문제 본문의 입력 예제를 공백 정규화 후 제외했다. 모든 정답은 아래 두 방식으로 교차 검증했다.

- 기준 계산: 리스트 인덱스 제거
- 독립 검증: deque 회전 시뮬레이션

이 묶음에서 채택한 LeetCode 대응 풀이는 없다. 로컬 명세와 독립 검증기를 사용한다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 최소 N | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | K=1 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | K=N | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 순서 그대로 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 모든 인원 수만큼 순환 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 공약수 있는 N,K | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 서로소 N,K | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 홀수 인원 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 큰 K | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 여러 차례 순환 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |

정답 파일은 평가 전용이며 번역 프롬프트에 넣지 않는다. 검증 결과와 파일 해시는 [manifest](../metadata/ipop19/manifest.json) 및 [validation_report](../metadata/ipop19/validation_report.json)에 기록한다.
