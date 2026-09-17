# LC_0121: Best Time To Buy And Sell Stock

먼저 하루에 매수하고 이후 하루에 매도할 때 최대 이익을 구한다. 거래하지 않을 때 이익은 0이다.

- 유형: 배열·최적화
- [문제 명세와 입출력](statement.md)
- [C++17 기준 풀이](reference.cpp)
- [저장소 대응 풀이](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/best_time_to_buy_and_sell_stock/solution.js)
- [공식 문제](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)
- 정답 교차 검증: 최저 매수가 순회 / 모든 매수·매도 쌍 검사

공개 입력 예제 전체는 [public_examples.json](public_examples.json)에 기록하고 평가 입력에서 제외했다. 프롬프트에 사용할 수 있는 파일은 statement.md와 prompt_examples뿐이다.
아래 입력은 자체 생성한 평가용 자료이며 공식 비공개 테스트가 아니다.

| 사례 | 목적 | 입력 | 정답 |
|---|---|---|---|
| case01 | 하루만 존재 | [입력](evaluation/case01.inp) | [정답](evaluation/case01.out) |
| case02 | 최대 가격 하루 | [입력](evaluation/case02.inp) | [정답](evaluation/case02.out) |
| case03 | 오름차순 | [입력](evaluation/case03.inp) | [정답](evaluation/case03.out) |
| case04 | 내림차순 | [입력](evaluation/case04.inp) | [정답](evaluation/case04.out) |
| case05 | 가격 동일 | [입력](evaluation/case05.inp) | [정답](evaluation/case05.out) |
| case06 | 가격 양끝 | [입력](evaluation/case06.inp) | [정답](evaluation/case06.out) |
| case07 | 가격 양끝 역순 | [입력](evaluation/case07.inp) | [정답](evaluation/case07.out) |
| case08 | 늦은 최저점 | [입력](evaluation/case08.inp) | [정답](evaluation/case08.out) |
| case09 | 앞선 최고점 | [입력](evaluation/case09.inp) | [정답](evaluation/case09.out) |
| case10 | 여러 저점 | [입력](evaluation/case10.inp) | [정답](evaluation/case10.out) |

이 README, evaluation, manifest, 검증 보고서를 번역 프롬프트에 넣지 않는다.
