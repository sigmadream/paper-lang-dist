#include <iostream>

void hanoi(int count, int start, int mid, int end) {
    if (count == 1) {
        std::cout << start << ' ' << end << '\n';
        return;
    }
    hanoi(count - 1, start, end, mid);
    std::cout << start << ' ' << end << '\n';
    hanoi(count - 1, mid, start, end);
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    int total = (1 << n) - 1;
    std::cout << total << '\n';
    hanoi(n, 1, 2, 3);

    return 0;
}