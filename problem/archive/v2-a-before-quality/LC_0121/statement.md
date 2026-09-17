# LC_0121: Best Time To Buy And Sell Stock

먼저 하루에 매수하고 이후 하루에 매도할 때 최대 이익을 구한다. 거래하지 않을 때 이익은 0이다.

## 제약

1<=N<=100000; 0<=가격<=10000.

## 표준입출력 계약

첫 줄 N, 다음 줄 N개 정수.
출력은 정수 하나 또는 공백으로 구분한 정수 배열이다. 참/거짓은 각각 1/0으로 출력한다. 인덱스는 0부터 시작한다.

## 공개 예제

```text
6
7 1 5 3 6 4
```

출력:

```text
5
```

[공식 명세](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)
