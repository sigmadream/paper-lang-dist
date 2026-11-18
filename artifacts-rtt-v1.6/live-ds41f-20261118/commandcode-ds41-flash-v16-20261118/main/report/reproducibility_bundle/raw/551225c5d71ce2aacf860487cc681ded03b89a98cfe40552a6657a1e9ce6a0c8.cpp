#include <iostream>
#include <vector>

int n;
int ans = 0;
std::vector<bool> col, diag1, diag2;

void solve(int r) {
    if (r == n) {
        ++ans;
        return;
    }

    for (int c = 0; c < n; ++c) {
        int d1 = r + c;
        int d2 = r - c + n - 1;

        if (col[c] || diag1[d1] || diag2[d2]) continue;

        col[c] = true;
        diag1[d1] = true;
        diag2[d2] = true;

        solve(r + 1);

        col[c] = false;
        diag1[d1] = false;
        diag2[d2] = false;
    }
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    if (!(std::cin >> n)) return 0;

    col.assign(n, false);
    diag1.assign(2 * n - 1, false);
    diag2.assign(2 * n - 1, false);
    ans = 0;

    solve(0);

    std::cout << ans << '\n';
    return 0;
}