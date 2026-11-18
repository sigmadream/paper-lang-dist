#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<int> scores(n);
    for (int i = 0; i < n; ++i) cin >> scores[i];

    auto s = [&](int i) -> int {
        return scores[i - 1];
    };

    int ans;
    if (n <= 0) {
        ans = 0;
    } else if (n == 1) {
        ans = scores[0];
    } else if (n == 2) {
        ans = scores[0] + scores[1];
    } else {
        int dp1 = s(1);
        int dp2 = dp1 + s(2);

        int prev1 = dp2;
        int prev2 = dp1;
        int prev3 = 0;

        for (int i = 3; i <= n; ++i) {
            int next = max(prev2, prev3 + s(i - 1)) + s(i);
            prev3 = prev2;
            prev2 = prev1;
            prev1 = next;
        }

        ans = prev1;
    }

    cout << ans << '\n';
    return 0;
}