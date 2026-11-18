#include <iostream>

void hanoi(int n, int start, int mid, int end) {
    if (n == 1) {
        std::cout << start << ' ' << end << '\n';
        return;
    }

    hanoi(n - 1, start, end, mid);
    std::cout << start << ' ' << end << '\n';
    hanoi(n - 1, mid, start, end);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) {
        return 0;
    }

    int count = (1 << n) - 1;
    std::cout << count << '\n';
    hanoi(n, 1, 2, 3);

    return 0;
}