#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<int> vals;
    int x;
    while (cin >> x) vals.push_back(x);

    if (vals.empty()) return 0;

    int n = vals[0];

    if (n == 0) {
        cout << 0 << '\n';
        return 0;
    }

    vector<int> s(n + 1, 0);
    for (int i = 1; i <= n && i < (int)vals.size(); ++i) {
        s[i] = vals[i];
    }

    vector<int> dp(n + 1, 0);

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