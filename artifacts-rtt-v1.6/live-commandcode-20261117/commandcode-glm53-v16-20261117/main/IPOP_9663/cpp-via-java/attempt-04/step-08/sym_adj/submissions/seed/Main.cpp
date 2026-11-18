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
    for (char ch : line) if (!isspace((unsigned char)ch)) trimmed += ch;
    if (trimmed.empty()) return 0;
    n = stoi(trimmed);
    col.assign(n, false);
    diag1.assign(2 * n - 1, false);
    diag2.assign(2 * n - 1, false);
    solve(0);
    cout << ans << "\n";
    return 0;
}