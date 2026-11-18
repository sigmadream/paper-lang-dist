import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); c = int(data[1])
    a = sorted(map(int, data[2:2+n]))
    ans = 0
    left, right = 1, a[-1] - a[0]
    while left <= right:
        mid = (left + right) // 2
        count = 1
        prev = a[0]
        for x in a[1:]:
            if x - prev >= mid:
                count += 1
                prev = x
        if count >= c:
            ans = mid
            left = mid + 1
        else:
            right = mid - 1
    print(ans)

main()