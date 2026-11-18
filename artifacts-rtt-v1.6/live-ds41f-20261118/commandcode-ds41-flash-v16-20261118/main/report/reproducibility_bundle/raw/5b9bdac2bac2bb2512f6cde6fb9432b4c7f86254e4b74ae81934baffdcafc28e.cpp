#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    cin >> N;

    vector<int> score(N + 1);
    for (int i = 1; i <= N; ++i) {
        cin >> score[i];
    }

    if (N == 1) {
        cout << score[1] << '\n';
        return 0;
    }

    if (N == 2) {
        cout << score[1] + score[2] << '\n';
        return 0;
    }

    vector<int> dp(N + 1, 0);
    dp[1] = score[1];
    dp[2] = score[1] + score[2];

    for (int i = 3; i <= N; ++i) {
        dp[i] = max(dp[i - 2], dp[i - 3] + score[i - 1]) + score[i];
    }

    cout << dp[N] << '\n';

    return 0;
}