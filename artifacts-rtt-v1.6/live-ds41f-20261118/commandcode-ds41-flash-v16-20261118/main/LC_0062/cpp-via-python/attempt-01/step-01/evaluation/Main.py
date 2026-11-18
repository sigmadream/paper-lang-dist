import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    m, n = map(int, data[:2])
    dp = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]
    print(dp[-1])

if __name__ == "__main__":
    main()