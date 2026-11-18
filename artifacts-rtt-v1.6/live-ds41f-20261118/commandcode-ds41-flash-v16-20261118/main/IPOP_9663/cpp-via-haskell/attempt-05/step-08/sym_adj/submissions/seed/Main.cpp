#include <iostream>

int n;
int full;

int dfs(int row, int cols, int diag1, int diag2) {
    if (row == n) return 1;

    int available = full & ~(cols | diag1 | diag2);
    int result = 0;

    while (available) {
        int bit = available & -available;
        available &= available - 1;

        result += dfs(
            row + 1,
            cols | bit,
            (diag1 | bit) << 1,
            (diag2 | bit) >> 1
        );
    }

    return result;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    if (!(std::cin >> n)) return 0;

    full = (1 << n) - 1;
    std::cout << dfs(0, 0, 0, 0) << '\n';

    return 0;
}