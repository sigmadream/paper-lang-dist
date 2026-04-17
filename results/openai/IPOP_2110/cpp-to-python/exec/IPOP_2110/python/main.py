import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    c = int(data[1])
    a = list(map(int, data[2:2 + n]))
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

    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    main()
