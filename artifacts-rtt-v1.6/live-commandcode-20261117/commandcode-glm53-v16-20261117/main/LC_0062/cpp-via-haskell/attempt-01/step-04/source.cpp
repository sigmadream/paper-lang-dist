#include <bits/stdc++.h>
using namespace std;

int main() {
    long long m, n;
    if (cin >> m >> n) {
        vector<long long> dp(n, 1);
        for (long long i = 1; i < m; ++i) {
            for (long long j = 1; j < n; ++j)
                dp[j] += dp[j - 1];
        }
        cout << dp[n - 1] << endl;
    }
    return 0;
}