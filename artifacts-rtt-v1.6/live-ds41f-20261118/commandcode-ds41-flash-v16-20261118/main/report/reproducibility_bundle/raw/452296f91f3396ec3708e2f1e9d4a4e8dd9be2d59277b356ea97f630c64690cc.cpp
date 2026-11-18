#include <iostream>
#include <vector>

int main() {
    int n;
    if (!(std::cin >> n)) {
        return 0;
    }

    std::vector<int> dp(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        dp[i] = dp[i / 2] + (i % 2);
    }

    for (int i = 0; i <= n; ++i) {
        if (i > 0) {
            std::cout << ' ';
        }
        std::cout << dp[i];
    }
    std::cout << '\n';

    return 0;
}