#include <bits/stdc++.h>
using namespace std;

int n;
vector<string> grid;
string res;

void solve(int r, int c, int size) {
    char first = grid[r][c];
    bool same = true;
    for (int i = r; i < r + size && same; i++)
        for (int j = c; j < c + size; j++)
            if (grid[i][j] != first) { same = false; break; }
    if (same) { res += first; return; }
    int half = size / 2;
    res += '(';
    solve(r, c, half);
    solve(r, c + half, half);
    solve(r + half, c, half);
    solve(r + half, c + half, half);
    res += ')';
}

int main() {
    cin >> n;
    grid.resize(n);
    for (int i = 0; i < n; i++) cin >> grid[i];
    solve(0, 0, n);
    cout << res << "\n";
    return 0;
}