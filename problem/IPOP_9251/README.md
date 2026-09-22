# IPOP_9251: LCS

두 대문자 문자열의 최장 공통 부분수열 길이를 출력한다.

[기존 문제 명세](statement.md) · [원문](https://www.acmicpc.net/problem/9251)

입력은 이 평가 묶음에서 자체 생성했다. GitHub 저장소의 공식 테스트를 수집한 것이 아니다.
기존 입력 파일 전체와 문제 본문의 입력 예제를 공백 정규화 후 제외했다. 모든 정답은 아래 두 방식으로 교차 검증했다.

- 기준 계산: 행 단위 LCS DP
- 독립 검증: 소형 부분수열 전수 탐색 / 대형 비트셋 LCS

이 묶음에서 채택한 LeetCode 대응 풀이는 없다. 로컬 명세와 독립 검증기를 사용한다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 최소 일치 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 공통 문자 없음 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 전체 동일 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 역순 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 반복 문자 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 부분수열과 부분문자열 구분 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 여러 최적해 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 교대 반복 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 분리 알파벳 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 한쪽 길이 상한 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |
| case11 | 고정 seed 기능 입력 1 | [입력](evaluation/case11.inp) | [정답](evaluation/case11.out) |
| case12 | 고정 seed 기능 입력 2 | [입력](evaluation/case12.inp) | [정답](evaluation/case12.out) |
| case13 | 규모·수치 경계 입력 | [입력](evaluation/case13.inp) | [정답](evaluation/case13.out) |

정답 파일은 평가 전용이며 번역 프롬프트에 넣지 않는다. 검증 결과와 파일 해시는 [manifest](../metadata/ipop19/manifest.json) 및 [validation_report](../metadata/ipop19/validation_report.json)에 기록한다.
