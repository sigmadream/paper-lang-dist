#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<long long> s(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        cin >> s[i];
    }

    if (n == 0) {
        cout << 0 << '\n';
        return 0;
    }

    vector<long long> dp(n + 1, 0);
    dp[1] = s[1];

    if (n >= 2) {
        dp[2] = s[1] + s[2];
    }

    for (int i = 3; i <= n; ++i) {
        dp[i] = max(dp[i - 2], dp[i - 3] + s[i - 1]) + s[i];
    }

    cout << dp[n] << '\n';
    return 0;
}