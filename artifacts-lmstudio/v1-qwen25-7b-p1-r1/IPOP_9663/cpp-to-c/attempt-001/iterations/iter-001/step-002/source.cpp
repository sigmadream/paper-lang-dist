#include <iostream>
using namespace std;

int ans = 0;
int n;
int *col, *diag1, *diag2;

void solve(int r) {
    if (r == n) {
        ans++;
        return;
    }
    for (int c = 0; c < n; c++) {
        if (col[c] || diag1[r + c] || diag2[r - c + n - 1]) continue;
        col[c] = diag1[r + c] = diag2[r - c + n - 1] = 1;
        solve(r + 1);
        col[c] = diag1[r + c] = diag2[r - c + n - 1] = 0;
    }
}

int main() {
    cin >> n;
    
    col = new int[n];
    diag1 = new int[2 * n - 1];
    diag2 = new int[2 * n - 1];
    
    for (int i = 0; i < n; i++) col[i] = diag1[i] = diag2[i] = 0;
    solve(0);
    
    cout << ans << endl;
    delete[] col;
    delete[] diag1;
    delete[] diag2;
    return 0;
}
