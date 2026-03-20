#include <stdio.h>

int max(int a, int b) {
    return a > b ? a : b;
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    int score[301] = {0};
    int dp[301] = {0};

    for (int index = 1; index <= n; ++index) {
        scanf("%d", &score[index]);
    }

    if (n >= 1) {
        dp[1] = score[1];
    }
    if (n >= 2) {
        dp[2] = score[1] + score[2];
    }
    for (int index = 3; index <= n; ++index) {
        dp[index] = max(dp[index - 2], dp[index - 3] + score[index - 1]) + score[index];
    }

    printf("%d\n", dp[n]);
    return 0;
}
