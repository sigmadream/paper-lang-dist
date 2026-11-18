#include <iostream>

void hanoi(int n, int from, int mid, int to) {
    if (n == 1) {
        std::cout << from << ' ' << to << '\n';
        return;
    }
    hanoi(n - 1, from, to, mid);
    std::cout << from << ' ' << to << '\n';
    hanoi(n - 1, mid, from, to);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    std::cout << ((1 << n) - 1) << '\n';
    hanoi(n, 1, 2, 3);

    return 0;
}