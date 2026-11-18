#include <iostream>
#include <string>
#include <cstdlib>
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
        int d1 = r + c;
        int d2 = r - c + n - 1;
        if (col[c] || diag1[d1] || diag2[d2]) continue;
        col[c] = diag1[d1] = diag2[d2] = true;
        solve(r + 1);
        col[c] = diag1[d1] = diag2[d2] = false;
    }
}

int main() {
    string line;
    if (!getline(cin, line)) return 0;

    size_t start = line.find_first_not_of(" \t\r\n");
    if (start == string::npos) return 0;
    size_t end = line.find_last_not_of(" \t\r\n");
    line = line.substr(start, end - start + 1);

    n = stoi(line);

    col.assign(n, false);
    diag1.assign(2 * n - 1, false);
    diag2.assign(2 * n - 1, false);

    solve(0);

    cout << ans << '\n';
    return 0;
}