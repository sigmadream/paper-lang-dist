#include <iostream>

int countBits(int n) {
    int count = 0;
    while (n > 0) {
        count += (n & 1);
        n >>= 1;
    }
    return count;
}

int main() {
    int N;
    if (!(std::cin >> N)) {
        return 0;
    }

    std::cout << 0;
    for (int i = 1; i <= N; ++i) {
        std::cout << ' ' << countBits(i);
    }
    std::cout << '\n';

    return 0;
}