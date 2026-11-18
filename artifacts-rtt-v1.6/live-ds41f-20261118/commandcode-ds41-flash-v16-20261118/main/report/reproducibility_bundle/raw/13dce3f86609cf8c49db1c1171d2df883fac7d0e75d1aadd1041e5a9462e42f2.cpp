#include <iostream>

void hanoi(int k, int start, int mid, int end) {
    if (k == 1) {
        std::cout << start << ' ' << end << '\n';
        return;
    }

    hanoi(k - 1, start, end, mid);
    std::cout << start << ' ' << end << '\n';
    hanoi(k - 1, mid, start, end);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) {
        return 0;
    }

    std::cout << ((1LL << n) - 1) << '\n';
    hanoi(n, 1, 2, 3);

    return 0;
}