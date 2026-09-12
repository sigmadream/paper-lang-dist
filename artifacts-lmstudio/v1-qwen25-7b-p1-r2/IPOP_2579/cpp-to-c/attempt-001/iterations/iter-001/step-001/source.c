#include <stdio.h>

int main() {
    int n;
    scanf("%d", &n);

    int score[n + 1];
    int dp[n + 1];
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
        dp[index] = (dp[index - 2] > dp[index - 3] + score[index - 1] ? dp[index - 2] : dp[index - 3] + score[index - 1]) + score[index];
    }

    printf("%d\n", dp[n]);
    return 0;
}
