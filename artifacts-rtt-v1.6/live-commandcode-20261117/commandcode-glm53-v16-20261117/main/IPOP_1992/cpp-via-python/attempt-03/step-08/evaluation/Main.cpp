#include <bits/stdc++.h>
using namespace std;

int n;
vector<string> grid;
string res;

void solve(int r, int c, int size) {
    char first = grid[r][c];
    for (int i = r; i < r + size; i++) {
        for (int j = c; j < c + size; j++) {
            if (grid[i][j] != first) {
                int half = size / 2;
                res += '(';
                solve(r, c, half);
                solve(r, c + half, half);
                solve(r + half, c, half);
                solve(r + half, c + half, half);
                res += ')';
                return;
            }
        }
    }
    res += first;
}

int main() {
    if (!(cin >> n)) return 0;
    grid.resize(n);
    for (int i = 0; i < n; i++) cin >> grid[i];
    solve(0, 0, n);
    cout << res << "\n";
    return 0;
}