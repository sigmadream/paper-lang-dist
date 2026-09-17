#include <iostream>
#include <vector>

using namespace std;

int ans = 0;
int n;
vector<bool> col, diag1, diag2;

void solve(int r) {
    if (r == n) {
        ans++;
        return;
    }
    for (int c = 0; c < n; c++) {
        if (col[c] || diag1[r + c] || diag2[r - c + n - 1]) continue;
        col[c] = diag1[r + c] = diag2[r - c + n - 1] = true;
        solve(r + 1);
        col[c] = diag1[r + c] = diag2[r - c + n - 1] = false;
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    if (!(cin >> n)) return 0;
    
    col.assign(n, false);
    diag1.assign(2 * n - 1, false);
    diag2.assign(2 * n - 1, false);
    solve(0);
    
    cout << ans << "\n";
    return 0;
}
