#include <iostream>
#include <vector>

int main() {
    int N;
    if (!(std::cin >> N)) {
        return 0;
    }

    if (N >= 0) {
        std::vector<int> bits(N + 1, 0);
        for (int i = 1; i <= N; ++i) {
            bits[i] = bits[i >> 1] + (i & 1);
        }

        for (int i = 0; i <= N; ++i) {
            if (i > 0) {
                std::cout << ' ';
            }
            std::cout << bits[i];
        }
    }

    std::cout << '\n';
    return 0;
}