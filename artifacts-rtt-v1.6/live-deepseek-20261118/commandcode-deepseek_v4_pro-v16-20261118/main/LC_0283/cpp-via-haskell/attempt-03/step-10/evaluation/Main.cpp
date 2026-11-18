#include <iostream>
#include <vector>
#include <cstdint>

int main() {
    int n;
    if (!(std::cin >> n)) return 0;

    std::vector<int32_t> nonZeros;
    nonZeros.reserve(n);
    int zeroCount = 0;

    for (int i = 0; i < n; ++i) {
        int32_t x;
        if (!(std::cin >> x)) return 0;
        if (x != 0) {
            nonZeros.push_back(x);
        } else {
            ++zeroCount;
        }
    }

    bool first = true;
    for (int32_t x : nonZeros) {
        if (!first) std::cout << ' ';
        first = false;
        std::cout << x;
    }
    for (int i = 0; i < zeroCount; ++i) {
        if (!first) std::cout << ' ';
        first = false;
        std::cout << 0;
    }
    std::cout << '\n';

    return 0;
}