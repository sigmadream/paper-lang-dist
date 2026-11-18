#include <iostream>

void hanoi(int n, int start, int middle, int end) {
    if (n == 1) {
        std::cout << start << ' ' << end << '\n';
        return;
    }

    hanoi(n - 1, start, end, middle);
    std::cout << start << ' ' << end << '\n';
    hanoi(n - 1, middle, start, end);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    long long moves = (1LL << n) - 1;
    std::cout << moves << '\n';
    hanoi(n, 1, 2, 3);

    return 0;
}