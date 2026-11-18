#include <iostream>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    long long first;
    if (!(std::cin >> first)) return 0;

    long long cur = first;
    long long best = first;

    for (int i = 1; i < n; ++i) {
        long long x;
        if (!(std::cin >> x)) {
            std::cout << best << '\n';
            return 0;
        }
        cur = std::max(x, cur + x);
        best = std::max(best, cur);
    }

    std::cout << best << '\n';
    return 0;
}