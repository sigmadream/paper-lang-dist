#include <iostream>

int popCount(int x) {
    int count = 0;
    while (x > 0) {
        count += x % 2;
        x /= 2;
    }
    return count;
}

int main() {
    int n;
    if (!(std::cin >> n)) return 0;

    for (int i = 0; i <= n; ++i) {
        if (i > 0) std::cout << ' ';
        std::cout << popCount(i);
    }
    std::cout << '\n';

    return 0;
}