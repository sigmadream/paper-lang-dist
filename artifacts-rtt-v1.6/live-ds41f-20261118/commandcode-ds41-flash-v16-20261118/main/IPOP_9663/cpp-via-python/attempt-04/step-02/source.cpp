#include <iostream>

using namespace std;

int n;
int fullMask;
long long answer = 0;

void solve(int row, int cols, int diag1, int diag2) {
    if (row == n) {
        ++answer;
        return;
    }

    int available = fullMask & ~(cols | diag1 | diag2);

    while (available) {
        int bit = available & -available;
        available -= bit;
        solve(row + 1, cols | bit, (diag1 | bit) << 1, (diag2 | bit) >> 1);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if (!(cin >> n)) {
        return 0;
    }

    fullMask = (1 << n) - 1;
    solve(0, 0, 0, 0);

    cout << answer << '\n';
    return 0;
}