#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;

    vector<long long> score(N + 1);
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

    vector<long long> dp(N + 1, 0);
    dp[1] = score[1];
    dp[2] = score[1] + score[2];

    for (int i = 3; i <= N; ++i) {
        long long takeTwo = dp[i - 2] + score[i];
        long long takeOne = dp[i - 3] + score[i - 1] + score[i];
        dp[i] = max(takeTwo, takeOne);
    }

    cout << dp[N] << '\n';
    return 0;
}