# IPOP_5567: 결혼식

무방향 친구 관계에서 1번 사람과 거리가 1 또는 2인 사람의 수를 출력한다.

[기존 문제 명세](statement.md) · [원문](https://www.acmicpc.net/problem/5567)

입력은 이 평가 묶음에서 자체 생성했다. GitHub 저장소의 공식 테스트를 수집한 것이 아니다.
기존 입력 파일 전체와 문제 본문의 입력 예제를 공백 정규화 후 제외했다. 모든 정답은 아래 두 방식으로 교차 검증했다.

- 기준 계산: 깊이 2 BFS
- 독립 검증: 길이 1·2 경로 직접 검사

이 묶음에서 채택한 LeetCode 대응 풀이는 없다. 로컬 명세와 독립 검증기를 사용한다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 본인 고립 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 직접 친구 한 명 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 거리 2 포함 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 거리 3 이상 제외 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 삼각형 중복 경로 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 별 모양 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 완전 그래프 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 중복 도달 및 분리 성분 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 사이클과 고립점 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 정점 번호 상한 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |
| case11 | 고정 seed 기능 입력 1 | [입력](evaluation/case11.inp) | [정답](evaluation/case11.out) |
| case12 | 고정 seed 기능 입력 2 | [입력](evaluation/case12.inp) | [정답](evaluation/case12.out) |
| case13 | 규모·수치 경계 입력 | [입력](evaluation/case13.inp) | [정답](evaluation/case13.out) |

정답 파일은 평가 전용이며 번역 프롬프트에 넣지 않는다. 검증 결과와 파일 해시는 [manifest](../metadata/ipop19/manifest.json) 및 [validation_report](../metadata/ipop19/validation_report.json)에 기록한다.
