import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    score = [0] * (n + 1)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        score[i] = int(data[i])

    if n >= 1:
        dp[1] = score[1]
    if n >= 2:
        dp[2] = score[1] + score[2]
    for i in range(3, n + 1):
        dp[i] = max(dp[i - 2], dp[i - 3] + score[i - 1]) + score[i]

    sys.stdout.write(str(dp[n]) + '\n')

if __name__ == "__main__":
    main()
