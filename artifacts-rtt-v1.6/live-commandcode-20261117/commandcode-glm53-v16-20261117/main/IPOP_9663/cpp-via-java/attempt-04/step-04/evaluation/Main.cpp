#include <bits/stdc++.h>
using namespace std;

int n;
long long ans = 0;
vector<bool> col, diag1, diag2;

void solve(int r) {
    if (r == n) { ans++; return; }
    for (int c = 0; c < n; c++) {
        if (col[c] || diag1[r + c] || diag2[r - c + n - 1]) continue;
        col[c] = diag1[r + c] = diag2[r - c + n - 1] = true;
        solve(r + 1);
        col[c] = diag1[r + c] = diag2[r - c + n - 1] = false;
    }
}

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    string trimmed;
    size_t s = line.find_first_not_of(" \t\r\n");
    if (s == string::npos) return 0;
    size_t e = line.find_last_not_of(" \t\r\n");
    trimmed = line.substr(s, e - s + 1);
    n = stoi(trimmed);
    col.assign(n, false);
    diag1.assign(2 * n - 1, false);
    diag2.assign(2 * n - 1, false);
    solve(0);
    cout << ans << "\n";
    return 0;
}