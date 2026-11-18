#include <iostream>
#include <string>
using namespace std;

static int n;
static int ans = 0;
static int col[15];
static int diag1[29];
static int diag2[29];

static void solve(int r) {
    if (r == n) {
        ++ans;
        return;
    }
    for (int c = 0; c < n; ++c) {
        if (col[c] == 1 || diag1[r + c] == 1 || diag2[r - c + n - 1] == 1) continue;
        col[c] = 1;
        diag1[r + c] = 1;
        diag2[r - c + n - 1] = 1;

        solve(r + 1);

        col[c] = 0;
        diag1[r + c] = 0;
        diag2[r - c + n - 1] = 0;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string line;
    if (!getline(cin, line)) return 0;

    size_t first = line.find_first_not_of(" \t\r\n");
    if (first == string::npos) return 0;
    size_t last = line.find_last_not_of(" \t\r\n");
    line = line.substr(first, last - first + 1);
    if (line.empty()) return 0;

    n = stoi(line);

    solve(0);
    cout << ans << '\n';
    return 0;
}