#include <iostream>
#include <vector>

int main() {
    int n;
    if (!(std::cin >> n)) {
        return 0;
    }

    std::vector<int> counts(n + 1, 0);
    for (int i = 1; i <= n; ++i) {
        counts[i] = counts[i >> 1] + (i & 1);
    }

    for (int i = 0; i <= n; ++i) {
        if (i > 0) {
            std::cout << ' ';
        }
        std::cout << counts[i];
    }
    std::cout << '\n';

    return 0;
}