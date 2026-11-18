#include <iostream>
using namespace std;

int n;
int fullMask;

int dfs(int row, int cols, int diag1, int diag2) {
    if (row == n) return 1;

    int available = fullMask & ~(cols | diag1 | diag2);
    int total = 0;

    while (available) {
        int bit = available & -available;
        available &= available - 1;

        total += dfs(
            row + 1,
            cols | bit,
            (diag1 | bit) << 1,
            (diag2 | bit) >> 1
        );
    }

    return total;
}

int main() {
    if (!(cin >> n)) return 0;

    fullMask = (1 << n) - 1;
    cout << dfs(0, 0, 0, 0) << '\n';

    return 0;
}