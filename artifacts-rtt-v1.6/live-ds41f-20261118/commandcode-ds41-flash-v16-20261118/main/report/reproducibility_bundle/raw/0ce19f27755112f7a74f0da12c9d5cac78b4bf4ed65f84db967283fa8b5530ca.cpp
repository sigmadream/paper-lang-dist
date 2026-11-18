#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    if (n == 0) {
        cout << 0 << '\n';
        return 0;
    }

    vector<int> a(n + 1);
    for (int i = 1; i <= n; ++i) {
        cin >> a[i];
    }

    vector<int> dp(n + 1, 0);
    dp[0] = 0;

    if (n >= 1) dp[1] = a[1];
    if (n >= 2) dp[2] = a[1] + a[2];

    for (int i = 3; i <= n; ++i) {
        dp[i] = max(dp[i - 2], dp[i - 3] + a[i - 1]) + a[i];
    }

    cout << dp[n] << '\n';
    return 0;
}