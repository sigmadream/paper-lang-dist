#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    long long m, n;
    if (!(std::cin >> m >> n)) return 0;

    std::vector<long long> dp(n, 1);

    for (long long i = 1; i < m; ++i) {
        for (long long j = 1; j < n; ++j) {
            dp[j] += dp[j - 1];
        }
    }

    std::cout << dp[n - 1] << '\n';
    return 0;
}