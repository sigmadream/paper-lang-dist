#include <iostream>

void hanoi(int n, int from, int aux, int to) {
    if (n == 1) {
        std::cout << from << " " << to << '\n';
        return;
    }
    hanoi(n - 1, from, to, aux);
    std::cout << from << " " << to << '\n';
    hanoi(n - 1, aux, from, to);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    std::cin >> n;

    int moves = (1 << n) - 1;
    std::cout << moves << '\n';

    hanoi(n, 1, 2, 3);

    return 0;
}