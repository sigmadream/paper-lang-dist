#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    long long n;
    if (!(std::cin >> n)) {
        return 0;
    }

    if (n <= 0) {
        return 0;
    }

    std::vector<long long> xs;
    xs.reserve(static_cast<size_t>(n));

    for (long long i = 0; i < n; ++i) {
        long long x;
        if (!(std::cin >> x)) {
            break;
        }
        xs.push_back(x);
    }

    if (xs.empty()) {
        return 0;
    }

    long long cur = xs[0];
    long long best = xs[0];

    for (size_t i = 1; i < xs.size(); ++i) {
        cur = std::max(xs[i], cur + xs[i]);
        best = std::max(best, cur);
    }

    std::cout << best << '\n';
    return 0;
}