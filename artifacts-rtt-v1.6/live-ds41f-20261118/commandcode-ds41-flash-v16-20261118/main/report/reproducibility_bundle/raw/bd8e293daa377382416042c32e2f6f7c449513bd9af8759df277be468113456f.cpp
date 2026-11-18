#include <iostream>
using namespace std;

int N;
unsigned fullMask;

long long dfs(int row, unsigned cols, unsigned diag1, unsigned diag2) {
    if (row == N) return 1;

    unsigned available = fullMask & ~(cols | diag1 | diag2);
    long long total = 0;

    while (available) {
        unsigned bit = available & (~available + 1);
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
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if (!(cin >> N)) return 0;

    fullMask = (1u << N) - 1u;
    cout << dfs(0, 0, 0, 0) << '\n';

    return 0;
}