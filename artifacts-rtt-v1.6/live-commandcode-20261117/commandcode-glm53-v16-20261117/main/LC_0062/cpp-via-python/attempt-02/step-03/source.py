import sys

def main():
    data = sys.stdin.read().split()
    if len(data) < 2:
        return
    m, n = int(data[0]), int(data[1])
    dp = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]
    print(dp[n - 1])

main()