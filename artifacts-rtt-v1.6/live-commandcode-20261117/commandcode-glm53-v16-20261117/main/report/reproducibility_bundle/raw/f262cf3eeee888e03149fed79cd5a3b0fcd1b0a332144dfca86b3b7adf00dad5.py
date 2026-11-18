import sys

def main():
    m, n = map(int, sys.stdin.read().split())
    dp = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]
    print(dp[-1])

main()