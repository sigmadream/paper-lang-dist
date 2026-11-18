#include <bits/stdc++.h>
using namespace std;

int n;
vector<string> grid;
string out;

void solve(int r, int c, int size) {
    char first = grid[r][c];
    bool same = true;
    for (int i = r; i < r + size && same; i++)
        for (int j = c; j < c + size; j++)
            if (grid[i][j] != first) { same = false; break; }
    if (same) { out += first; return; }
    int half = size / 2;
    out += '(';
    solve(r, c, half);
    solve(r, c + half, half);
    solve(r + half, c, half);
    solve(r + half, c + half, half);
    out += ')';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;
    grid.resize(n);
    for (int i = 0; i < n; i++) cin >> grid[i];
    solve(0, 0, n);
    out += '\n';
    cout << out;
    return 0;
}