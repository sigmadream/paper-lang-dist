#include <iostream>

int n;
int full_mask;
long long answer = 0;

void solve(int row, int cols, int diag1, int diag2) {
    if (row == n) {
        ++answer;
        return;
    }

    int available = full_mask & ~(cols | diag1 | diag2);

    while (available) {
        int bit = available & -available;
        available -= bit;
        solve(row + 1, cols | bit, (diag1 | bit) << 1, (diag2 | bit) >> 1);
    }
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    if (!(std::cin >> n)) return 0;

    full_mask = (1 << n) - 1;
    solve(0, 0, 0, 0);

    std::cout << answer << '\n';
    return 0;
}