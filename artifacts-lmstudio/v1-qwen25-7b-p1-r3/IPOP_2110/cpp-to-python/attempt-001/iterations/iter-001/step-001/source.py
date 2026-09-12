def main():
    import sys
    input = sys.stdin.read
    data = input().split()

    n = int(data[0])
    c = int(data[1])
    a = [int(data[i]) for i in range(2, 2 + n)]

    a.sort()

    left = 1
    right = a[-1] - a[0]
    ans = 0

    while left <= right:
        mid = left + (right - left) // 2
        count = 1
        prev = a[0]

        for i in range(1, n):
            if a[i] - prev >= mid:
                count += 1
                prev = a[i]

        if count >= c:
            ans = mid
            left = mid + 1
        else:
            right = mid - 1

    print(ans)

if __name__ == "__main__":
    main()
