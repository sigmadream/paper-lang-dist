#include <bits/stdc++.h>
using namespace std;

static int n;
static long long ans;
static bool col[15];
static bool diag1[30];
static bool diag2[30];

static void solve(int r) {
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
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    if (!getline(cin, s)) return 0;

    size_t first = s.find_first_not_of(" \t\r\n");
    if (first == string::npos) return 0;
    size_t last = s.find_last_not_of(" \t\r\n");
    n = stoi(s.substr(first, last - first + 1));

    ans = 0;
    solve(0);

    cout << ans << '\n';
    return 0;
}