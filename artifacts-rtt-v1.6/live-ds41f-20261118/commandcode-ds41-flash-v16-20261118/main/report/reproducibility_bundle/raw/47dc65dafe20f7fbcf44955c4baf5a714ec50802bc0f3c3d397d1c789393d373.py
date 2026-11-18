import sys


def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if len(data) < 2:
        return

    n, c = data[0], data[1]
    houses = data[2:2 + n]
    houses.sort()

    left = 1
    right = houses[-1] - houses[0]
    ans = 0

    while left <= right:
        mid = left + (right - left) // 2
        count = 1
        prev = houses[0]

        for i in range(1, n):
            if houses[i] - prev >= mid:
                count += 1
                prev = houses[i]

        if count >= c:
            ans = mid
            left = mid + 1
        else:
            right = mid - 1

    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    main()