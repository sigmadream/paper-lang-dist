#include <iostream>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) {
        return 0;
    }
    if (n == 0) {
        return 0;
    }

    int x;
    std::cin >> x;
    int cur = x;
    int best = x;

    for (int i = 1; i < n; ++i) {
        std::cin >> x;
        cur = std::max(x, cur + x);
        best = std::max(best, cur);
    }

    std::cout << best << '\n';
    return 0;
}