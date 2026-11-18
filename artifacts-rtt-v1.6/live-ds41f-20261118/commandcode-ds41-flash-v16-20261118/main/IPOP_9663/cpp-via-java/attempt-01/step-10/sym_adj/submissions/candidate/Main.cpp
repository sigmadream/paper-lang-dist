#include <iostream>

using namespace std;

int n;
int ans = 0;
bool col[15];
bool diag1[29];
bool diag2[29];

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
    if (!(cin >> n)) return 0;
    for (int i = 0; i < n; ++i) col[i] = false;
    for (int i = 0; i < 2 * n - 1; ++i) {
        diag1[i] = false;
        diag2[i] = false;
    }
    solve(0);
    cout << ans << '\n';
    return 0;
}