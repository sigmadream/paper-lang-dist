#include <iostream>
#include <vector>

int main() {
    int m, n;
    std::cin >> m >> n;

    std::vector<long long> dp(n, 1);

    for (int i = 1; i < m; ++i) {
        long long acc = 1;
        for (int j = 1; j < n; ++j) {
            acc += dp[j - 1];
            dp[j] = acc;
        }
        dp[0] = 1;
    }

    std::cout << dp[n - 1] << '\n';
    return 0;
}