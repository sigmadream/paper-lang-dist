#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<long long> score(n + 3, 0);
    for (int i = 1; i <= n; i++) scanf("%lld", &score[i]);
    if (n == 0) { printf("0\n"); return 0; }
    vector<long long> dp(n + 3, 0);
    dp[1] = score[1];
    if (n >= 2) dp[2] = score[1] + score[2];
    for (int i = 3; i <= n; i++)
        dp[i] = max(dp[i-2], dp[i-3] + score[i-1]) + score[i];
    printf("%lld\n", dp[n]);
    return 0;
}