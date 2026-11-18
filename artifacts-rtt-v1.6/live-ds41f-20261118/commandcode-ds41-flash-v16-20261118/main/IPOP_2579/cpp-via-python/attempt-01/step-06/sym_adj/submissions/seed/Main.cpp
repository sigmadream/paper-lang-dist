#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> data;
    int x;
    while (std::cin >> x) {
        data.push_back(x);
    }

    if (data.empty()) {
        return 0;
    }

    int n = data[0];

    std::vector<long long> score(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        score[i] = data[i];
    }

    std::vector<long long> dp(n + 1, 0);

    if (n >= 1) {
        dp[1] = score[1];
    }
    if (n >= 2) {
        dp[2] = score[1] + score[2];
    }

    for (int i = 3; i <= n; ++i) {
        dp[i] = std::max(dp[i - 2], dp[i - 3] + score[i - 1]) + score[i];
    }

    std::cout << dp[n] << '\n';

    return 0;
}