#include <iostream>
#include <vector>

int main() {
    int N;
    if (!(std::cin >> N)) return 0;

    std::vector<int> bits(N + 1, 0);
    std::cout << 0;

    for (int i = 1; i <= N; ++i) {
        bits[i] = bits[i >> 1] + (i & 1);
        std::cout << ' ' << bits[i];
    }

    std::cout << '\n';
    return 0;
}