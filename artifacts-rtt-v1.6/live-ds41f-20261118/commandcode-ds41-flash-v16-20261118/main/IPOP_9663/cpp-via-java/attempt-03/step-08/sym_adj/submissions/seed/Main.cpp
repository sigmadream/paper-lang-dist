#include <iostream>
#include <vector>

using namespace std;

int n;
int ans;
vector<bool> col, diag1, diag2;

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
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if (!(cin >> n)) return 0;

    col.assign(n, false);
    diag1.assign(2 * n - 1, false);
    diag2.assign(2 * n - 1, false);

    ans = 0;
    solve(0);

    cout << ans << "\n";

    return 0;
}