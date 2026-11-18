#include <iostream>
#include <vector>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    long long nInput;
    if (!(std::cin >> nInput)) {
        return 0;
    }

    int n = static_cast<int>(nInput);
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