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

    std::vector<long long> vals;
    vals.reserve(static_cast<size_t>(n > 0 ? n : 0));
    long long x;
    while (static_cast<long long>(vals.size()) < n && (std::cin >> x)) {
        vals.push_back(x);
    }

    if (n == 0 || vals.empty()) {
        std::cout << 0 << '\n';
        return 0;
    }

    long long cur = vals[0];
    long long best = vals[0];
    for (size_t i = 1; i < vals.size(); ++i) {
        cur = std::max(vals[i], cur + vals[i]);
        best = std::max(best, cur);
    }

    std::cout << best << '\n';
    return 0;
}