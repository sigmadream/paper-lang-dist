#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<int> scores(n + 1);
    for (int i = 1; i <= n; ++i) {
        cin >> scores[i];
    }

    if (n == 1) {
        cout << scores[1] << '\n';
        return 0;
    }

    vector<int> dp(n + 1, 0);
    dp[1] = scores[1];
    dp[2] = scores[1] + scores[2];

    for (int i = 3; i <= n; ++i) {
        dp[i] = max(dp[i - 2], dp[i - 3] + scores[i - 1]) + scores[i];
    }

    cout << dp[n] << '\n';
    return 0;
}