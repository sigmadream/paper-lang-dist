#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) {
        return 0;
    }

    int *dp = (int *)malloc((size_t)(n + 1) * sizeof(int));
    if (!dp) {
        return 1;
    }

    dp[0] = 0;
    for (int i = 1; i <= n; ++i) {
        dp[i] = dp[i >> 1] + (i & 1);
    }

    for (int i = 0; i <= n; ++i) {
        if (i > 0) {
            putchar(' ');
        }
        printf("%d", dp[i]);
    }
    putchar('\n');

    free(dp);
    return 0;
}
