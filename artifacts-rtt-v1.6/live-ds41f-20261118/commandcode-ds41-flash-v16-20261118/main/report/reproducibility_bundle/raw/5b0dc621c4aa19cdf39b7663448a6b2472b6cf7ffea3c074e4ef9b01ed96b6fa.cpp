#include <iostream>
using namespace std;

int n;
long long ans;
bool col[15], diag1[30], diag2[30];

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

    ans = 0;
    solve(0);

    cout << ans << '\n';
    return 0;
}