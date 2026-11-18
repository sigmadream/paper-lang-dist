#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    std::vector<int> nonzero;
    int zeroCount = 0;
    for (int i = 0; i < n; ++i) {
        int x;
        std::cin >> x;
        if (x != 0) nonzero.push_back(x);
        else ++zeroCount;
    }

    bool first = true;
    for (int x : nonzero) {
        if (!first) std::cout << ' ';
        std::cout << x;
        first = false;
    }
    for (int i = 0; i < zeroCount; ++i) {
        if (!first) std::cout << ' ';
        std::cout << 0;
        first = false;
    }
    std::cout << '\n';

    return 0;
}