# LC_0739: Daily Temperatures

각 날짜에서 더 높은 기온이 처음 나타날 때까지 일수를 출력한다. 없으면 0이다.

- 유형: 스택
- [문제 명세와 입출력](statement.md)
- [C++17 기준 풀이](reference.cpp)
- [저장소 대응 풀이](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/daily_temperatures/solution.js)
- [공식 문제](https://leetcode.com/problems/daily-temperatures/)
- 정답 교차 검증: 단조 스택 / 각 날짜의 미래 직접 탐색

공개 입력 예제 전체는 [public_examples.json](public_examples.json)에 기록하고 평가 입력에서 제외했다. 프롬프트에 사용할 수 있는 파일은 statement.md와 prompt_examples뿐이다.
아래 입력은 자체 생성한 평가용 자료이며 공식 비공개 테스트가 아니다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 기온 하한 하루 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 기온 상한 하루 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 모두 동일 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 증가 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 감소 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 동일 기온 뒤 상승 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 멀리 있는 최고점 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 기온 양끝 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 교대 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 여러 대기 길이 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |

이 README, evaluation, manifest, 검증 보고서를 번역 프롬프트에 넣지 않는다.
