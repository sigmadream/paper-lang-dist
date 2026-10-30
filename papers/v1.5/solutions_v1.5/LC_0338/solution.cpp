#include <iostream>
#include <vector>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) {
        return 0;
    }

    vector<int> dp(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        dp[i] = dp[i >> 1] + (i & 1);
    }

    for (int i = 0; i <= n; ++i) {
        cout << (i > 0 ? " " : "") << dp[i];
    }
    cout << "\n";

    return 0;
}
