#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<int> data;
    int x;
    while (cin >> x) data.push_back(x);

    if (data.empty()) return 0;

    int n = data[0];
    vector<int> scores(n + 1, 0);
    for (int i = 1; i <= n && i < (int)data.size(); ++i) {
        scores[i] = data[i];
    }

    vector<long long> dp(n + 1, 0);

    if (n >= 1) dp[1] = scores[1];
    if (n >= 2) dp[2] = scores[1] + scores[2];

    for (int i = 3; i <= n; ++i) {
        dp[i] = max(dp[i - 2], dp[i - 3] + scores[i - 1]) + scores[i];
    }

    cout << dp[n] << '\n';
    return 0;
}