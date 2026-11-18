#include <iostream>
#include <vector>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    long long n;
    if (!(std::cin >> n)) {
        return 0;
    }

    if (n < 0) {
        return 0;
    }

    std::vector<int> counts(static_cast<size_t>(n) + 1);
    counts[0] = 0;
    for (long long i = 1; i <= n; ++i) {
        counts[static_cast<size_t>(i)] =
            counts[static_cast<size_t>(i >> 1)] + static_cast<int>(i & 1LL);
    }

    for (long long i = 0; i <= n; ++i) {
        if (i) {
            std::cout << ' ';
        }
        std::cout << counts[static_cast<size_t>(i)];
    }
    std::cout << '\n';

    return 0;
}