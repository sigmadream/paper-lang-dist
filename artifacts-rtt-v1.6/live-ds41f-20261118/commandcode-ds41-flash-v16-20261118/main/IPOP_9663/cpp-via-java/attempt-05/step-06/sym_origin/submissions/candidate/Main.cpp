#include <iostream>
#include <vector>

static int n;
static int ans = 0;
static std::vector<bool> col;
static std::vector<bool> diag1;
static std::vector<bool> diag2;

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
    if (!(std::cin >> n)) return 0;
    col.assign(n, false);
    diag1.assign(2 * n, false);
    diag2.assign(2 * n, false);
    solve(0);
    std::cout << ans << '\n';
    return 0;
}