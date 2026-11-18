#include <bits/stdc++.h>
using namespace std;

int n;
vector<string> g;

string solve(int r, int c, int size) {
    char first = g[r][c];
    bool same = true;
    for (int i = r; i < r + size && same; ++i)
        for (int j = c; j < c + size; ++j)
            if (g[i][j] != first) { same = false; break; }
    if (same) return string(1, first);
    int h = size / 2;
    return "(" + solve(r, c, h) + solve(r, c + h, h)
             + solve(r + h, c, h) + solve(r + h, c + h, h) + ")";
}

int main() {
    cin >> n;
    g.resize(n);
    for (int i = 0; i < n; ++i) cin >> g[i];
    cout << solve(0, 0, n) << "\n";
    return 0;
}