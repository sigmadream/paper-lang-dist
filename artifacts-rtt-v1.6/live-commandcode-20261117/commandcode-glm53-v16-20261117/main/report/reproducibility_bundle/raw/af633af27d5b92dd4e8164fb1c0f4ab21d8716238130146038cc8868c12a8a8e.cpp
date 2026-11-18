#include <bits/stdc++.h>
using namespace std;

int n;
vector<string> g;
string out;

bool same(int r, int c, int s) {
    char ch = g[r][c];
    for (int i = 0; i < s; i++)
        for (int j = 0; j < s; j++)
            if (g[r+i][c+j] != ch) return false;
    return true;
}

void solve(int r, int c, int s) {
    if (same(r, c, s)) { out += g[r][c]; return; }
    int h = s / 2;
    out += '(';
    solve(r, c, h);
    solve(r, c + h, h);
    solve(r + h, c, h);
    solve(r + h, c + h, h);
    out += ')';
}

int main() {
    cin >> n;
    g.resize(n);
    for (int i = 0; i < n; i++) cin >> g[i];
    if (n > 0) {
        solve(0, 0, n);
        cout << out << "\n";
    }
    return 0;
}