#include <iostream>
#include <string>
#include <vector>

using namespace std;

string solve(const vector<string>& grid, int r, int c, int size) {
    int half = size / 2;
    char first = grid[r][c];

    bool allSame = true;
    for (int i = r; i < r + size; ++i) {
        for (int j = c; j < c + size; ++j) {
            if (grid[i][j] != first) {
                allSame = false;
                break;
            }
        }
        if (!allSame) break;
    }

    if (allSame) {
        return string(1, first);
    }

    return "(" +
           solve(grid, r, c, half) +
           solve(grid, r, c + half, half) +
           solve(grid, r + half, c, half) +
           solve(grid, r + half, c + half, half) +
           ")";
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

    cout << solve(grid, 0, 0, n) << '\n';

    return 0;
}