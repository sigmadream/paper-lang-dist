#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int M, N;
    if (!(cin >> M >> N)) return 0;

    vector<long long> dp(N, 1);

    for (int i = 1; i < M; ++i) {
        for (int j = 1; j < N; ++j) {
            dp[j] += dp[j - 1];
        }
    }

    cout << dp[N - 1] << '\n';
    return 0;
}