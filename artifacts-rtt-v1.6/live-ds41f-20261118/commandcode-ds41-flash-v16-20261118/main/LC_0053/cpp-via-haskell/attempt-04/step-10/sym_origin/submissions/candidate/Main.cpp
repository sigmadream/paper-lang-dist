#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::vector<long long> tokens;
    long long x;
    while (std::cin >> x) {
        tokens.push_back(x);
    }

    if (tokens.empty()) {
        return 0;
    }

    long long n = tokens[0];
    if (n <= 0) {
        return 0;
    }

    long long available = static_cast<long long>(tokens.size()) - 1;
    long long m = std::min(n, available);

    if (m <= 0) {
        return 0;
    }

    long long first = tokens[1];
    long long cur = first;
    long long best = first;

    for (long long i = 1; i < m; ++i) {
        long long y = tokens[1 + i];
        cur = std::max(y, cur + y);
        best = std::max(best, cur);
    }

    std::cout << best << '\n';
    return 0;
}