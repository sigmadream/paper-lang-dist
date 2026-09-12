#include <iostream>
#include <vector>
using namespace std;

int n, ans = 0;
vector<bool> col(15), diag1(30), diag2(30);

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
    cin >> n;
    solve(0);
    cout << ans << endl;
    return 0;
}
