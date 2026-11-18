#include <iostream>

void hanoi(int n, int from, int mid, int to) {
    if (n == 1) {
        std::cout << from << " " << to << "\n";
    } else {
        hanoi(n - 1, from, to, mid);
        std::cout << from << " " << to << "\n";
        hanoi(n - 1, mid, from, to);
    }
}

int main() {
    int N;
    if (!(std::cin >> N)) return 0;
    if (N < 1 || N > 20) return 0;

    std::cout << (1LL << N) - 1 << "\n";
    hanoi(N, 1, 2, 3);
    return 0;
}