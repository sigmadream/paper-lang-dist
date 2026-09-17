# IPOP_1992: 쿼드트리

이진 정사각 영상을 동일 값이면 압축하고 아니면 네 사분면을 재귀 인코딩한다.

[기존 문제 명세](statement.md) · [원문](https://www.acmicpc.net/problem/1992)

입력은 이 평가 묶음에서 자체 생성했다. GitHub 저장소의 공식 테스트를 수집한 것이 아니다.
기존 입력 파일 전체와 문제 본문의 입력 예제를 공백 정규화 후 제외했다. 모든 정답은 아래 두 방식으로 교차 검증했다.

- 기준 계산: 영역 재귀 분할
- 독립 검증: 단일 픽셀에서 2x2 상향 병합

추가 대응 풀이: [problems/construct_quad_tree/solution.js](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/construct_quad_tree/solution.js). Node 객체를 제공하고 TL/TR/BL/BR 순서의 BOJ 문자열로 직렬화.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 최소 흰색 픽셀 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 최소 검정 픽셀 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 동일 영역 0 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 동일 영역 1 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 체커보드 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 상하 분할 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 모두 분할 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 한 픽셀만 다름 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 불균일 깊이 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 최대 변 길이 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |

정답 파일은 평가 전용이며 번역 프롬프트에 넣지 않는다. 검증 결과와 파일 해시는 [manifest](../metadata/ipop19/manifest.json) 및 [validation_report](../metadata/ipop19/validation_report.json)에 기록한다.
