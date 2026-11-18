#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int N;
    if (!(std::cin >> N)) return 0;

    std::vector<int> values(N);
    for (int i = 0; i < N; ++i) {
        std::cin >> values[i];
    }

    long long current = values[0];
    long long best = values[0];

    for (int i = 1; i < N; ++i) {
        long long x = values[i];
        current = std::max<long long>(x, current + x);
        best = std::max(best, current);
    }

    std::cout << best << '\n';
    return 0;
}