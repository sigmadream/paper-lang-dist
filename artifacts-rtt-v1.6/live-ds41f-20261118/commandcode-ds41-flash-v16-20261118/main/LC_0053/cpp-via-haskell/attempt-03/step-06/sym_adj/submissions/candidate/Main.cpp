#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    std::vector<long long> vals;
    vals.reserve(std::max(0, n));
    for (int i = 0; i < n; ++i) {
        long long x;
        if (!(std::cin >> x)) break;
        vals.push_back(x);
    }

    if (vals.empty()) {
        std::cout << 0 << '\n';
        return 0;
    }

    long long cur = vals[0];
    long long best = vals[0];
    for (size_t i = 1; i < vals.size(); ++i) {
        long long x = vals[i];
        cur = std::max(x, cur + x);
        best = std::max(best, cur);
    }

    std::cout << best << '\n';
    return 0;
}