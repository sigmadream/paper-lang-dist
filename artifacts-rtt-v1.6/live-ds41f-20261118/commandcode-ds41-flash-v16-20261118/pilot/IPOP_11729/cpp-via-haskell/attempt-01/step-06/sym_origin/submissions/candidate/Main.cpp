#include <iostream>

void hanoi(int n, int s, int m, int e) {
    if (n == 1) {
        std::cout << s << ' ' << e << '\n';
    } else {
        hanoi(n - 1, s, e, m);
        std::cout << s << ' ' << e << '\n';
        hanoi(n - 1, m, s, e);
    }
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    std::cin >> n;

    std::cout << ((1LL << n) - 1) << '\n';
    hanoi(n, 1, 2, 3);

    return 0;
}