#include <cstdio>

int main() {
    int n;
    if (std::scanf("%d", &n) != 1) return 0;

    int score[301] = {0};
    int dp[301] = {0};

    for (int index = 1; index <= n; ++index) {
        std::scanf("%d", &score[index]);
    }

    if (n >= 1) {
        dp[1] = score[1];
    }
    if (n >= 2) {
        dp[2] = score[1] + score[2];
    }
    for (int index = 3; index <= n; ++index) {
        int a = dp[index - 2];
        int b = dp[index - 3] + score[index - 1];
        dp[index] = (a > b ? a : b) + score[index];
    }

    std::printf("%d\n", dp[n]);
    return 0;
}
