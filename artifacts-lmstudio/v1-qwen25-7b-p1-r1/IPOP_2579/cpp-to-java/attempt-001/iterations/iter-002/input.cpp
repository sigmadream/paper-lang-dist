#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int n;
    std::cin >> n;

    std::vector<int> score(n + 1);
    std::vector<int> dp(n + 1);
    for (int index = 1; index <= n; ++index) {
        std::cin >> score[index];
    }

    if (n >= 1) {
        dp[1] = score[1];
    }
    if (n >= 2) {
        dp[2] = score[1] + score[2];
    }
    for (int index = 3; index <= n; ++index) {
        dp[index] = std::max(dp[index - 2], dp[index - 3] + score[index - 1]) + score[index];
    }

    std::cout << dp[n] << std::endl;
    return 0;
}
