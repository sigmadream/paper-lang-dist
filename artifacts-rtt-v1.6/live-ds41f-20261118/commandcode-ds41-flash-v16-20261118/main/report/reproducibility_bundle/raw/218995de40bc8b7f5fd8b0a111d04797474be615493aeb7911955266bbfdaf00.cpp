#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) {
        return 0;
    }

    std::vector<int> a(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> a[i];
    }

    if (n == 0) {
        return 0;
    }

    int cur = a[0];
    int best = a[0];

    for (int i = 1; i < n; ++i) {
        cur = std::max(a[i], cur + a[i]);
        best = std::max(best, cur);
    }

    std::cout << best << '\n';
    return 0;
}