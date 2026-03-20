def main():
    import sys
    input = sys.stdin.read
    data = input().split()

    n = int(data[0])
    scores = [0] + list(map(int, data[1:]))

    dp = [0] * (n + 1)
    if n >= 1:
        dp[1] = scores[1]
    if n >= 2:
        dp[2] = scores[1] + scores[2]
    for index in range(3, n + 1):
        dp[index] = max(dp[index - 2], dp[index - 3] + scores[index - 1]) + scores[index]

    print(dp[n])

if __name__ == "__main__":
    main()
