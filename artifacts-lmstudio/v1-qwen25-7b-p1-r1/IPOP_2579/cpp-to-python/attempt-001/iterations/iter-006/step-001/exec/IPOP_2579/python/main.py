def main():
    import sys
    input = sys.stdin.read
    data = input().split()

    n = int(data[0])
    score = [0] * (n + 1)
    dp = [0] * (n + 1)

    for index in range(1, n + 1):
        score[index] = int(data[index])

    if n >= 1:
        dp[1] = score[1]
    if n >= 2:
        dp[2] = score[1] + score[2]
    for index in range(3, n + 1):
        dp[index] = max(dp[index - 2], dp[index - 3] + score[index - 1]) + score[index]

    print(dp[n])

if __name__ == "__main__":
    main()
