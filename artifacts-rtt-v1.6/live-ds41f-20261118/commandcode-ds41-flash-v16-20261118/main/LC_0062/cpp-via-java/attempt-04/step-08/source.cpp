#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long m, n;
    if (!(cin >> m >> n)) return 0;

    vector<long long> dp(n, 1);

    for (int i = 1; i < m; ++i) {
        for (int j = 1; j < n; ++j) {
            dp[j] += dp[j - 1];
        }
    }

    cout << dp[n - 1] << '\n';
    return 0;
}