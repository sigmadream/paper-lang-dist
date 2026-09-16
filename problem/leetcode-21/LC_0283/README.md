# LC_0283: Move Zeroes

0이 아닌 원소의 상대 순서를 유지하면서 모든 0을 뒤로 옮긴 배열을 출력한다.

- 유형: 배열·재배치
- [문제 명세와 입출력](statement.md)
- [C++17 기준 풀이](reference.cpp)
- [저장소 대응 풀이](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/move_zeroes/solution.js)
- [공식 문제](https://leetcode.com/problems/move-zeroes/)
- 정답 교차 검증: 두 포인터 in-place 이동 / 0 제외 목록과 0 개수 결합

공개 입력 예제 전체는 [public_examples.json](public_examples.json)에 기록하고 평가 입력에서 제외했다. 프롬프트에 사용할 수 있는 파일은 statement.md와 prompt_examples뿐이다.
아래 입력은 자체 생성한 평가용 자료이며 공식 비공개 테스트가 아니다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 0 없는 한 원소 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 0만 반복 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 0 없음 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 맨 앞 0 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 맨 뒤 0 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 0 교대 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 연속 0 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 음수와 0 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 정수 하한 상한 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 중복 비영 원소 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |

이 README, evaluation, manifest, 검증 보고서를 번역 프롬프트에 넣지 않는다.
