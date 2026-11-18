#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int m, n;
    if (!(std::cin >> m >> n)) return 0;

    std::vector<std::vector<long long>> dp(m, std::vector<long long>(n, 0));
    dp[0][0] = 1;

    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            if (i == 0 && j == 0) continue;
            long long fromUp = (i > 0) ? dp[i - 1][j] : 0;
            long long fromLeft = (j > 0) ? dp[i][j - 1] : 0;
            dp[i][j] = fromUp + fromLeft;
        }
    }

    std::cout << dp[m - 1][n - 1] << '\n';
    return 0;
}