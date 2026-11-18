#include <iostream>

int main() {
    int N = 0;
    if (!(std::cin >> N)) {
        N = 0;
    }

    std::cout << 0;
    for (int i = 1; i <= N; ++i) {
        int x = i;
        int c = 0;
        while (x > 0) {
            c += x & 1;
            x >>= 1;
        }
        std::cout << ' ' << c;
    }
    std::cout << '\n';

    return 0;
}