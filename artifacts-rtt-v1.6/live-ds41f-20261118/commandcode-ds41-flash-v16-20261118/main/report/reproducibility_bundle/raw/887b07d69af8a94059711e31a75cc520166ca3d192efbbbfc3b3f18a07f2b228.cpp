#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) {
        return 0;
    }

    std::vector<long long> xs;
    xs.reserve(n > 0 ? n : 0);

    for (int i = 0; i < n; ++i) {
        long long x;
        if (!(std::cin >> x)) {
            break;
        }
        xs.push_back(x);
    }

    if (n <= 0 || xs.empty()) {
        return 0;
    }

    long long cur = xs[0];
    long long best = xs[0];

    for (std::size_t i = 1; i < xs.size(); ++i) {
        cur = std::max(xs[i], cur + xs[i]);
        best = std::max(best, cur);
    }

    std::cout << best << '\n';
    return 0;
}