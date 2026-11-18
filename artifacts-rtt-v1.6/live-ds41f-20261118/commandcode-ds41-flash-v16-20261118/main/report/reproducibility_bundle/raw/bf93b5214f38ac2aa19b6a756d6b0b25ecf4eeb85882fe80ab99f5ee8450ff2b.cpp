#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;

    vector<int> score(N + 1);
    for (int i = 1; i <= N; ++i) {
        cin >> score[i];
    }

    long long ans = 0;

    if (N == 1) {
        ans = score[1];
    } else if (N == 2) {
        ans = score[1] + score[2];
    } else {
        vector<long long> dp(N + 1, 0);
        dp[1] = score[1];
        dp[2] = score[1] + score[2];

        for (int i = 3; i <= N; ++i) {
            dp[i] = max(dp[i - 2] + score[i],
                        dp[i - 3] + score[i - 1] + score[i]);
        }

        ans = dp[N];
    }

    cout << ans << '\n';
    return 0;
}