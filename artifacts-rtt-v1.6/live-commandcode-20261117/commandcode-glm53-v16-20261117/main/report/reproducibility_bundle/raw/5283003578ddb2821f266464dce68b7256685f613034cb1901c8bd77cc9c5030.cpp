#include <iostream>
#include <vector>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long m, n;
    if (!(cin >> m >> n)) return 0;

    vector<long long> dp(n, 1);
    for (long long row = 2; row <= m; ++row) {
        for (long long col = 1; col < n; ++col) {
            dp[col] += dp[col - 1];
        }
    }

    cout << dp[n - 1] << '\n';
    return 0;
}