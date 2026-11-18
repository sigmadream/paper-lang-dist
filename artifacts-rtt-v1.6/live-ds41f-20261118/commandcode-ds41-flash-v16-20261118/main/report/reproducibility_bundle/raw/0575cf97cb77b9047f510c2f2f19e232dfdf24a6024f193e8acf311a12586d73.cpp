#include <iostream>
#include <vector>
using namespace std;

int main() {
    int M, N;
    if (!(cin >> M >> N)) return 0;

    vector<vector<long long>> dp(M, vector<long long>(N, 1));

    for (int i = 1; i < M; ++i) {
        for (int j = 1; j < N; ++j) {
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
        }
    }

    cout << dp[M - 1][N - 1] << '\n';
    return 0;
}