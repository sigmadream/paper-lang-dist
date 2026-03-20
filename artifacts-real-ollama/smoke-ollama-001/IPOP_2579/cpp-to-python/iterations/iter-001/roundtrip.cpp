#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    std::cin >> n;

    std::vector<int> scores(n + 1);
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
    for (int index = 3; index <= n; ++index) {
        dp[index] = std::max(dp[index - 2], dp[index - 3] + scores[index - 1]) + scores[index];
    }

    std::cout << dp[n] << std::endl;

    return 0;
}
