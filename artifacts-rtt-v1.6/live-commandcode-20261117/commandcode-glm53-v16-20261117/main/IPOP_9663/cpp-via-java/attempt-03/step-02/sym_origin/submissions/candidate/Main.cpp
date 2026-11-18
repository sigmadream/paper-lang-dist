#include <bits/stdc++.h>
using namespace std;

int n, ans = 0;
vector<char> col, diag1, diag2;

void solve(int r) {
    if (r == n) { ans++; return; }
    for (int c = 0; c < n; c++) {
        if (col[c] || diag1[r + c] || diag2[r - c + n - 1]) continue;
        col[c] = diag1[r + c] = diag2[r - c + n - 1] = 1;
        solve(r + 1);
        col[c] = diag1[r + c] = diag2[r - c + n - 1] = 0;
    }
}

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    // trim
    size_t s = line.find_first_not_of(" \t\r\n");
    if (s == string::npos) return 0;
    n = stoi(line.substr(s));
    col.assign(n, 0);
    diag1.assign(2 * n - 1, 0);
    diag2.assign(2 * n - 1, 0);
    solve(0);
    cout << ans << "\n";
    return 0;
}