#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    std::vector<int> scores(n + 1);
    for (int i = 1; i <= n; ++i) {
        std::cin >> scores[i];
    }

    if (n <= 0) {
        std::cout << 0 << '\n';
        return 0;
    }
    if (n == 1) {
        std::cout << scores[1] << '\n';
        return 0;
    }
    if (n == 2) {
        std::cout << scores[1] + scores[2] << '\n';
        return 0;
    }

    long long dp1 = scores[1];
    long long dp2 = dp1 + scores[2];

    long long p1 = dp2;
    long long p2 = dp1;
    long long p3 = 0;

    for (int i = 3; i <= n; ++i) {
        long long next = std::max(p2, p3 + scores[i - 1]) + scores[i];
        p3 = p2;
        p2 = p1;
        p1 = next;
    }

    std::cout << p1 << '\n';
    return 0;
}