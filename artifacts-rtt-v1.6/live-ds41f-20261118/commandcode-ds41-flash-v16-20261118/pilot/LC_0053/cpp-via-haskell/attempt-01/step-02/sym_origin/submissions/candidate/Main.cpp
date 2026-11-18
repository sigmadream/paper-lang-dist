#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;
    if (n <= 0) return 0;

    std::vector<long long> values(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> values[i];
    }

    long long current = values[0];
    long long best = values[0];
    for (int i = 1; i < n; ++i) {
        current = std::max(values[i], current + values[i]);
        best = std::max(best, current);
    }

    std::cout << best << '\n';
    return 0;
}