#include <iostream>
#include <vector>

int main() {
    int m, n;
    if (!(std::cin >> m >> n)) return 0;

    std::vector<long long> dp(n, 1);

    for (int i = 1; i < m; ++i) {
        for (int j = 1; j < n; ++j) {
            dp[j] += dp[j - 1];
        }
    }

    std::cout << dp[n - 1] << '\n';
    return 0;
}