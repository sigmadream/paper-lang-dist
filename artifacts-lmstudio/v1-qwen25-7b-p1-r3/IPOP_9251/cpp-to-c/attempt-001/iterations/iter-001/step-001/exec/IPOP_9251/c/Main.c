#include <stdio.h>
#include <string.h>

int main() {
    char a[1001], b[1001];
    if (scanf("%s %s", a, b) != 2) return 0;
    
    int n = strlen(a);
    int m = strlen(b);
    int dp[1001][1001] = {0};
    
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (a[i - 1] == b[j - 1]) dp[i][j] = dp[i - 1][j - 1] + 1;
            else dp[i][j] = dp[i - 1][j] > dp[i][j - 1] ? dp[i - 1][j] : dp[i][j - 1];
        }
    }
    
    printf("%d\n", dp[n][m]);
    return 0;
}
