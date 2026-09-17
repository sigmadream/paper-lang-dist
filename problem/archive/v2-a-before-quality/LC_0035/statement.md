# LC_0035: Search Insert Position

정렬 배열에서 target의 위치 또는 정렬을 유지할 삽입 위치를 0-based로 출력한다.

## 제약

1<=N<=10000; 원소,target은 -10000..10000; 배열은 중복 없이 오름차순이다. 요구 시간 O(log N).

## 표준입출력 계약

첫 줄 N target, 다음 줄 N개 정수.
출력은 정수 하나 또는 공백으로 구분한 정수 배열이다. 참/거짓은 각각 1/0으로 출력한다. 인덱스는 0부터 시작한다.

## 공개 예제

```text
4 5
1 3 5 6
```

출력:

```text
2
```

[공식 명세](https://leetcode.com/problems/search-insert-position/)
