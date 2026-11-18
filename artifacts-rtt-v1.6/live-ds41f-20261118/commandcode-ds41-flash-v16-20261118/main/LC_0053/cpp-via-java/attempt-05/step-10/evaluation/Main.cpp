#include <iostream>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    long long n;
    if (!(std::cin >> n)) return 0;
    if (n <= 0) return 0;

    long long x;
    if (!(std::cin >> x)) return 0;

    long long cur = x;
    long long best = x;

    for (long long i = 1; i < n; ++i) {
        if (!(std::cin >> x)) break;
        cur = std::max(x, cur + x);
        best = std::max(best, cur);
    }

    std::cout << best << "\n";
    return 0;
}