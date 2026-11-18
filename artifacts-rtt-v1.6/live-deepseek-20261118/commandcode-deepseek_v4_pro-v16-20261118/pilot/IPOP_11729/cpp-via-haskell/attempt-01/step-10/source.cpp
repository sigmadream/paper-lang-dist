#include <iostream>

void hanoi(int n, int from, int aux, int to) {
    if (n == 0) return;
    hanoi(n - 1, from, to, aux);
    std::cout << from << ' ' << to << '\n';
    hanoi(n - 1, aux, from, to);
}

int main() {
    int n;
    if (!(std::cin >> n)) return 0;

    long long total = (1LL << n) - 1;
    std::cout << total << '\n';

    hanoi(n, 1, 2, 3);
    return 0;
}