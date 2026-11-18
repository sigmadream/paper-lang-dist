#include <iostream>

void hanoi(int n, int from, int aux, int to) {
    if (n == 1) {
        std::cout << from << ' ' << to << '\n';
    } else {
        hanoi(n - 1, from, to, aux);
        std::cout << from << ' ' << to << '\n';
        hanoi(n - 1, aux, from, to);
    }
}

int main() {
    int N;
    std::cin >> N;
    std::cout << (1 << N) - 1 << '\n';
    hanoi(N, 1, 2, 3);
    return 0;
}