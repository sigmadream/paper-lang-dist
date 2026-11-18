#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int N;
    if (!(std::cin >> N)) return 0;

    std::vector<int> counts(N + 1, 0);
    for (int i = 1; i <= N; ++i) {
        counts[i] = counts[i >> 1] + (i & 1);
    }

    for (int i = 0; i <= N; ++i) {
        if (i > 0) std::cout << ' ';
        std::cout << counts[i];
    }
    std::cout << '\n';

    return 0;
}