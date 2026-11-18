#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;

    vector<int> s(N);
    for (int i = 0; i < N; ++i) cin >> s[i];

    vector<int> dp(N + 1, 0);
    if (N >= 1) dp[1] = s[0];
    if (N >= 2) dp[2] = s[0] + s[1];

    for (int i = 3; i <= N; ++i) {
        dp[i] = max(dp[i - 2], dp[i - 3] + s[i - 2]) + s[i - 1];
    }

    cout << dp[N] << '\n';
    return 0;
}