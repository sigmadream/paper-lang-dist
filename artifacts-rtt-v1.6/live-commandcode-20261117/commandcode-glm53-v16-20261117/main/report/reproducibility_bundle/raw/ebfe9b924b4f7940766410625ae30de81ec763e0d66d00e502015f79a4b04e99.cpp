#include <bits/stdc++.h>
using namespace std;

int n;
vector<string> grid;

string solve(int r, int c, int size) {
    char first = grid[r][c];
    bool same = true;
    for (int i = r; i < r + size && same; ++i)
        for (int j = c; j < c + size; ++j)
            if (grid[i][j] != first) { same = false; break; }
    if (same) return string(1, first);
    int half = size / 2;
    string res = "(";
    int dr[] = {0, 0, 1, 1}, dc[] = {0, 1, 0, 1};
    for (int q = 0; q < 4; ++q)
        res += solve(r + dr[q] * half, c + dc[q] * half, half);
    return res + ")";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;
    grid.resize(n);
    for (int i = 0; i < n; ++i) cin >> grid[i];
    cout << solve(0, 0, n) << "\n";
    return 0;
}