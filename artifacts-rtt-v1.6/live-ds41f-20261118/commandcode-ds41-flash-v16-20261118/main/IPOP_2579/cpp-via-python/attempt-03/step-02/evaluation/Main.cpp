#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    std::vector<int> scores(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        std::cin >> scores[i];
    }

    std::vector<int> dp(n + 1, 0);

    if (n >= 1) {
        dp[1] = scores[1];
    }
    if (n >= 2) {
        dp[2] = scores[1] + scores[2];
    }

    for (int i = 3; i <= n; ++i) {
        dp[i] = std::max(dp[i - 2], dp[i - 3] + scores[i - 1]) + scores[i];
    }

    std::cout << dp[n] << '\n';

    return 0;
}