#include <iostream>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    long long x;
    std::cin >> x;

    long long cur = x;
    long long best = x;

    for (int i = 1; i < n; ++i) {
        std::cin >> x;
        cur = std::max(x, cur + x);
        best = std::max(best, cur);
    }

    std::cout << best << '\n';
    return 0;
}