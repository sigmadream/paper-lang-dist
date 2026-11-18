#include <iostream>
#include <vector>

int main() {
    long long n;
    if (!(std::cin >> n)) {
        return 0;
    }

    std::vector<int> dp(static_cast<size_t>(n + 1), 0);
    for (long long i = 1; i <= n; ++i) {
        dp[static_cast<size_t>(i)] = dp[static_cast<size_t>(i / 2)] + static_cast<int>(i % 2);
    }

    for (long long i = 0; i <= n; ++i) {
        if (i > 0) std::cout << ' ';
        std::cout << dp[static_cast<size_t>(i)];
    }
    std::cout << '\n';

    return 0;
}