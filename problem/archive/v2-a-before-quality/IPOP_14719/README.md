# IPOP_14719: 빗물

높이 H, 너비 W와 각 열의 높이를 읽고 갇히는 빗물의 총량을 출력한다.

[기존 문제 명세](statement.md) · [원문](https://www.acmicpc.net/problem/14719)

입력은 이 평가 묶음에서 자체 생성했다. GitHub 저장소의 공식 테스트를 수집한 것이 아니다.
기존 입력 파일 전체와 문제 본문의 입력 예제를 공백 정규화 후 제외했다. 모든 정답은 아래 두 방식으로 교차 검증했다.

- 기준 계산: 열별 좌우 최대 높이
- 독립 검증: 높이별 수평 빈칸 계수

이 묶음에서 채택한 LeetCode 대응 풀이는 없다. 로컬 명세와 독립 검증기를 사용한다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 최소 너비 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 최소 높이 물 고임 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 벽 없음 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 단조 증가 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 단조 감소 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 깊은 단일 분지 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 여러 분지 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 평탄한 벽 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 양끝 낮음 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 높이 상한 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |

정답 파일은 평가 전용이며 번역 프롬프트에 넣지 않는다. 검증 결과와 파일 해시는 [manifest](../metadata/ipop19/manifest.json) 및 [validation_report](../metadata/ipop19/validation_report.json)에 기록한다.
