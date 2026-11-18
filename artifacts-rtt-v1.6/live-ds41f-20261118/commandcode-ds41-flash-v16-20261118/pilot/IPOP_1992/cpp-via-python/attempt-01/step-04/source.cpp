#include <bits/stdc++.h>
using namespace std;

string solve(int r, int c, int size, const vector<string>& grid) {
    char first = grid[r][c];
    bool same = true;

    for (int i = r; i < r + size && same; ++i) {
        for (int j = c; j < c + size; ++j) {
            if (grid[i][j] != first) {
                same = false;
                break;
            }
        }
    }

    if (same) {
        return string(1, first);
    }

    int half = size / 2;
    string tl = solve(r, c, half, grid);
    string tr = solve(r, c + half, half, grid);
    string bl = solve(r + half, c, half, grid);
    string br = solve(r + half, c + half, half, grid);

    return "(" + tl + tr + bl + br + ")";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<string> grid(n);
    for (int i = 0; i < n; ++i) {
        cin >> grid[i];
    }

    cout << solve(0, 0, n, grid) << '\n';

    return 0;
}