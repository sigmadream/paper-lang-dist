#include <iostream>

void hanoi(int n, int from, int via, int to) {
    if (n == 0) return;
    hanoi(n - 1, from, to, via);
    std::cout << from << ' ' << to << '\n';
    hanoi(n - 1, via, from, to);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    int moves = (1 << n) - 1;
    std::cout << moves << '\n';
    hanoi(n, 1, 2, 3);

    return 0;
}