def max_score(n, scores):
    if n == 1:
        return scores[0]
    elif n == 2:
        return scores[0] + scores[1]

    dp = [0] * (n + 1)
    dp[1] = scores[0]
    dp[2] = scores[0] + scores[1]

    for index in range(3, n + 1):
        dp[index] = max(dp[index - 2], dp[index - 3] + scores[index - 1]) + scores[index]

    return dp[n]

# Input
n = int(input())
scores = [int(input()) for _ in range(n)]

# Output
print(max_score(n, scores))
