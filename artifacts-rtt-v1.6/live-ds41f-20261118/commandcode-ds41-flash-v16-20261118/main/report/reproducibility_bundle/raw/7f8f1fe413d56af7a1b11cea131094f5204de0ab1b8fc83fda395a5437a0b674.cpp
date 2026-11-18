#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    long long n;
    if (!(std::cin >> n)) return 0;

    std::vector<long long> a(n);
    for (long long i = 0; i < n; ++i) {
        std::cin >> a[i];
    }

    if (n == 0) {
        std::cout << 0 << '\n';
        return 0;
    }

    long long cur = a[0];
    long long best = a[0];

    for (long long i = 1; i < n; ++i) {
        cur = std::max(a[i], cur + a[i]);
        best = std::max(best, cur);
    }

    std::cout << best << '\n';
    return 0;
}