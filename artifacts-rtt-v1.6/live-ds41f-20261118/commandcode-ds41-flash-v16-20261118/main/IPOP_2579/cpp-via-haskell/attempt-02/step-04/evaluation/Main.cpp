#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<int> scores(n);
    for (int i = 0; i < n; ++i) cin >> scores[i];

    vector<int> dp(n + 1, 0);

    if (n >= 1) dp[1] = scores[0];
    if (n >= 2) dp[2] = scores[0] + scores[1];

    for (int i = 3; i <= n; ++i) {
        dp[i] = max(dp[i - 2], dp[i - 3] + scores[i - 2]) + scores[i - 1];
    }

    cout << dp[n] << '\n';
    return 0;
}