#include <iostream>

static int n;
static int ans = 0;
static int col[15];
static int diag1[29];
static int diag2[29];

static void solve(int r) {
    if (r == n) {
        ++ans;
        return;
    }

    for (int c = 0; c < n; ++c) {
        if (col[c] == 1 || diag1[r + c] == 1 || diag2[r - c + n - 1] == 1) {
            continue;
        }

        col[c] = 1;
        diag1[r + c] = 1;
        diag2[r - c + n - 1] = 1;

        solve(r + 1);

        col[c] = 0;
        diag1[r + c] = 0;
        diag2[r - c + n - 1] = 0;
    }
}

int main() {
    if (!(std::cin >> n)) {
        return 0;
    }

    solve(0);
    std::cout << ans << '\n';

    return 0;
}