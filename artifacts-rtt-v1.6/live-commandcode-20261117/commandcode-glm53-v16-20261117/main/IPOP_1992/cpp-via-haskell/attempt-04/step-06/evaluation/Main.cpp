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
    int dr[] = {0, 0, half, half};
    int dc[] = {0, half, 0, half};
    for (int k = 0; k < 4; ++k)
        res += solve(r + dr[k], c + dc[k], half);
    res += ")";
    return res;
}

int main() {
    cin >> n;
    grid.resize(n);
    for (int i = 0; i < n; ++i) cin >> grid[i];
    cout << solve(0, 0, n) << "\n";
    return 0;
}