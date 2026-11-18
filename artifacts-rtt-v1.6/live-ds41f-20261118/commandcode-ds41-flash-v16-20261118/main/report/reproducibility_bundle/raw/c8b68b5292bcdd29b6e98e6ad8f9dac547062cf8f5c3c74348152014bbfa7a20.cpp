#include <iostream>

using namespace std;

long long dfs(int n, int full, int row, int cols, int diag1, int diag2) {
    if (row == n) return 1;
    long long result = 0;
    int available = full & ~(cols | diag1 | diag2);
    while (available) {
        int bit = available & -available;
        available &= available - 1;
        result += dfs(n, full, row + 1,
                      cols | bit,
                      (diag1 | bit) << 1,
                      (diag2 | bit) >> 1);
    }
    return result;
}

int main() {
    int n;
    cin >> n;
    int full = (1 << n) - 1;
    cout << dfs(n, full, 0, 0, 0, 0) << '\n';
    return 0;
}