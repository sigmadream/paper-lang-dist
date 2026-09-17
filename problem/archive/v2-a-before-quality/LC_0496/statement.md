# LC_0496: Next Greater Element I

nums1의 각 원소가 nums2에서 처음 만나는 오른쪽의 더 큰 값을 출력한다. 없으면 -1이다.

## 제약

1<=N1<=N2<=1000; 값 0..10000; 각 배열은 중복이 없고 nums1은 nums2의 부분집합이다.

## 표준입출력 계약

첫 줄 N1 N2, 둘째 줄 nums1, 셋째 줄 nums2.
출력은 정수 하나 또는 공백으로 구분한 정수 배열이다. 참/거짓은 각각 1/0으로 출력한다. 인덱스는 0부터 시작한다.

## 공개 예제

```text
3 4
4 1 2
1 3 4 2
```

출력:

```text
-1 3 -1
```

[공식 명세](https://leetcode.com/problems/next-greater-element-i/)
