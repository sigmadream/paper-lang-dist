import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    scores = [0] + data[1:1 + n]

    dp = [0] * (n + 1)

    if n >= 1:
        dp[1] = scores[1]
    if n >= 2:
        dp[2] = scores[1] + scores[2]

    for i in range(3, n + 1):
        dp[i] = max(dp[i - 2], dp[i - 3] + scores[i - 1]) + scores[i]

    print(dp[n])

if __name__ == "__main__":
    main()