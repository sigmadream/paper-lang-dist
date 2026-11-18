#include <iostream>

using namespace std;

int n;
unsigned int fullMask;
long long answer = 0;

void solve(int row, unsigned int cols, unsigned int diag1, unsigned int diag2) {
    if (row == n) {
        ++answer;
        return;
    }

    unsigned int available = fullMask & ~(cols | diag1 | diag2);

    while (available) {
        unsigned int bit = available & (~available + 1);
        available -= bit;

        solve(
            row + 1,
            cols | bit,
            (diag1 | bit) << 1,
            (diag2 | bit) >> 1
        );
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if (!(cin >> n)) {
        return 0;
    }

    fullMask = (1u << n) - 1;
    solve(0, 0, 0, 0);

    cout << answer << '\n';
    return 0;
}