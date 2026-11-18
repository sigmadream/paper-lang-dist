#include <bits/stdc++.h>
using namespace std;

int n;
vector<string> grid;
string solve(int r, int c, int sz) {
    char first = grid[r][c];
    for (int i = r; i < r + sz; i++)
        for (int j = c; j < c + sz; j++)
            if (grid[i][j] != first) {
                int h = sz / 2;
                return "(" + solve(r, c, h) + solve(r, c + h, h)
                       + solve(r + h, c, h) + solve(r + h, c + h, h) + ")";
            }
    return string(1, first);
}

int main() {
    if (!(cin >> n)) return 0;
    grid.resize(n);
    for (int i = 0; i < n; i++) cin >> grid[i];
    cout << solve(0, 0, n) << "\n";
    return 0;
}