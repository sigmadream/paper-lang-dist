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
    int n;
    if (!(std::cin >> n)) return 0;
    if (n < 1 || n > 20) return 0;

    unsigned long long count = (1ULL << n) - 1;
    std::cout << count << '\n';
    hanoi(n, 1, 2, 3);
    return 0;
}