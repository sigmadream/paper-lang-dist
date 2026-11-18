#include <iostream>
#include <vector>

int main() {
    int M, N;
    if (!(std::cin >> M >> N)) {
        return 0;
    }

    std::vector<long long> dp(N, 1);
    for (int i = 1; i < M; ++i) {
        for (int j = 1; j < N; ++j) {
            dp[j] += dp[j - 1];
        }
    }

    std::cout << dp[N - 1] << std::endl;
    return 0;
}