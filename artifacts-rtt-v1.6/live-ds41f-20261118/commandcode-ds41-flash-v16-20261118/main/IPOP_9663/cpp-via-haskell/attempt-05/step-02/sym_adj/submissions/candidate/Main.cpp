#include <iostream>

int n;
int full;
long long countSolutions;

void dfs(int row, int cols, int diag1, int diag2) {
    if (row == n) {
        ++countSolutions;
        return;
    }

    int available = full & ~(cols | diag1 | diag2);

    while (available != 0) {
        int bit = available & -available;
        available &= available - 1;

        dfs(row + 1,
            cols | bit,
            (diag1 | bit) << 1,
            (diag2 | bit) >> 1);
    }
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::cin >> n;

    full = (1 << n) - 1;
    countSolutions = 0;

    dfs(0, 0, 0, 0);

    std::cout << countSolutions << '\n';

    return 0;
}