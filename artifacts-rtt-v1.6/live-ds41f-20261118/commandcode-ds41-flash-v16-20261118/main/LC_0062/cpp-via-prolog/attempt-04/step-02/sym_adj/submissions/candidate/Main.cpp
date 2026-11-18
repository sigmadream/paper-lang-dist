#include <bits/stdc++.h>
using namespace std;

int main() {
    long long M, N;
    if (!(cin >> M >> N)) return 0;
    vector<long long> dp(N, 1);
    for (long long k = 0; k < M - 1; ++k) {
        for (long long j = 1; j < N; ++j) {
            dp[j] += dp[j - 1];
        }
    }
    cout << dp[N - 1] << "\n";
    return 0;
}