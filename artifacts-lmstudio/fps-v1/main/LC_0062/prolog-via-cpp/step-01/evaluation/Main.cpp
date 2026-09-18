#include <iostream>
#include <vector>

int main() {
    int M, N;
    std::cin >> M >> N;

    std::vector<std::vector<int>> dp(M, std::vector<int>(N, 0));
    for (int i = 0; i < M; ++i) {
        dp[i][0] = 1;
    }
    for (int j = 0; j < N; ++j) {
        dp[0][j] = 1;
    }

    for (int i = 1; i < M; ++i) {
        for (int j = 1; j < N; ++j) {
            dp[i][j] = dp[i-1][j] + dp[i][j-1];
        }
    }

    std::cout << dp[M-1][N-1] << std::endl;
    return 0;
}