#include <iostream>
#include <vector>

int main() {
    long long M, N;
    if (!(std::cin >> M >> N)) return 0;

    std::vector<long long> dp(static_cast<size_t>(N), 1);

    for (long long i = 1; i < M; ++i) {
        for (long long j = 1; j < N; ++j) {
            dp[static_cast<size_t>(j)] += dp[static_cast<size_t>(j - 1)];
        }
    }

    std::cout << dp[static_cast<size_t>(N - 1)] << '\n';
    return 0;
}