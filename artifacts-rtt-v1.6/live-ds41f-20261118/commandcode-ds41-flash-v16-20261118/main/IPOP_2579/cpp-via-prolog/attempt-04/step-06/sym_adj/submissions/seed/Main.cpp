#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;

    vector<int> a(N + 1);
    for (int i = 1; i <= N; ++i) {
        cin >> a[i];
    }

    if (N == 1) {
        cout << a[1] << '\n';
        return 0;
    }

    if (N == 2) {
        cout << a[1] + a[2] << '\n';
        return 0;
    }

    vector<int> dp(N + 1, 0);
    dp[1] = a[1];
    dp[2] = a[1] + a[2];

    for (int i = 3; i <= N; ++i) {
        dp[i] = max(dp[i - 2] + a[i],
                    dp[i - 3] + a[i - 1] + a[i]);
    }

    cout << dp[N] << '\n';
    return 0;
}