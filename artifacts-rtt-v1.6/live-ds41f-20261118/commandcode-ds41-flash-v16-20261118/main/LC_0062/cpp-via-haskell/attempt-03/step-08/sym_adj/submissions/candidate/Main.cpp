#include <iostream>
#include <vector>

long long uniquePaths(int m, int n) {
    std::vector<long long> dp(n, 1);
    for (int i = 1; i < m; ++i) {
        for (int j = 1; j < n; ++j) {
            dp[j] += dp[j - 1];
        }
    }
    return dp[n - 1];
}

int main() {
    int m, n;
    if (std::cin >> m >> n) {
        std::cout << uniquePaths(m, n) << '\n';
    }
    return 0;
}