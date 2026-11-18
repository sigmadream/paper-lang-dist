#include <iostream>

static int n;
static int ans = 0;
static bool col[15];
static bool diag1[30];
static bool diag2[30];

static void solve(int r) {
    if (r == n) {
        ++ans;
        return;
    }

    for (int c = 0; c < n; ++c) {
        int d1 = r + c;
        int d2 = r - c + n - 1;

        if (col[c] || diag1[d1] || diag2[d2]) continue;

        col[c] = diag1[d1] = diag2[d2] = true;
        solve(r + 1);
        col[c] = diag1[d1] = diag2[d2] = false;
    }
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    if (!(std::cin >> n)) return 0;

    solve(0);
    std::cout << ans << '\n';

    return 0;
}