#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    std::vector<long long> xs(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> xs[i];
    }

    if (n == 0) {
        std::cout << 0 << '\n';
        return 0;
    }

    long long best = xs[0];
    long long cur = xs[0];

    for (int i = 1; i < n; ++i) {
        cur = std::max(xs[i], cur + xs[i]);
        best = std::max(best, cur);
    }

    std::cout << best << '\n';
    return 0;
}