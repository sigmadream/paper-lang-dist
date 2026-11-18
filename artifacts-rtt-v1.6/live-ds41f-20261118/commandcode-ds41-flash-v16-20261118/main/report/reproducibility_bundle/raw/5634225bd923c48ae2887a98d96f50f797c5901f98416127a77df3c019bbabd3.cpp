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

    int N;
    std::cin >> N;

    long long count = (1LL << N) - 1;
    std::cout << count << '\n';

    hanoi(N, 1, 2, 3);

    return 0;
}