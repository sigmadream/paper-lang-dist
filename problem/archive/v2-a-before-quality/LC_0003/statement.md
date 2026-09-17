# LC_0003: Longest Substring Without Repeating Characters

문자가 중복되지 않는 연속 부분문자열의 최대 길이를 구한다. 빈 문자열의 답은 0이다.

## 제약

길이 0..100000; 영문자, 숫자, 기호, 공백. 이 묶음은 인쇄 가능한 ASCII를 사용한다.

## 표준입출력 계약

첫 줄 전체가 문자열이다. 공백도 문자로 보존하며 LC_0003은 빈 줄을 허용한다.
출력은 정수 하나 또는 공백으로 구분한 정수 배열이다. 참/거짓은 각각 1/0으로 출력한다. 인덱스는 0부터 시작한다.

## 공개 예제

```text
abcabcbb
```

출력:

```text
3
```

[공식 명세](https://leetcode.com/problems/longest-substring-without-repeating-characters/)
