#include <iostream>
#include <algorithm>
#include <climits>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    long long cur = 0, best = LLONG_MIN;
    for (int i = 0; i < n; ++i) {
        long long x;
        std::cin >> x;
        if (i == 0) {
            cur = x;
            best = x;
        } else {
            cur = std::max(x, cur + x);
            best = std::max(best, cur);
        }
    }
    std::cout << best << '\n';
    return 0;
}