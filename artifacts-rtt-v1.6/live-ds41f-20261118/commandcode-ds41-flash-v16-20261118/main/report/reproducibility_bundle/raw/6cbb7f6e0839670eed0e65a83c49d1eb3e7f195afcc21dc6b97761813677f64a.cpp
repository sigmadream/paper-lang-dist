#include <iostream>

static int count_bits(int n) {
    int c = 0;
    while (n > 0) {
        c += (n & 1);
        n >>= 1;
    }
    return c;
}

int main() {
    int N;
    if (!(std::cin >> N)) {
        return 0;
    }

    std::cout << 0;
    for (int i = 1; i <= N; ++i) {
        std::cout << ' ' << count_bits(i);
    }
    std::cout << '\n';

    return 0;
}