#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int n;
    std::cin >> n;
    std::vector<int> scores(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> scores[i];
    }

    std::vector<int> best(n + 1, 0);
    best[1] = scores[0];
    if (n > 1) {
        best[2] = scores[0] + scores[1];
    }
    for (int i = 3; i <= n; ++i) {
        best[i] = std::max(best[i - 2], best[i - 3] + scores[i - 1]) + scores[i - 1];
    }

    std::cout << best[n] << std::endl;
    return 0;
}