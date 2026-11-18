#include <iostream>
#include <vector>
#include <string>

using namespace std;

bool allSame(const vector<string>& grid, int r, int c, int size, char first) {
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            if (grid[r + i][c + j] != first) {
                return false;
            }
        }
    }
    return true;
}

string solve(const vector<string>& grid, int r, int c, int size) {
    char first = grid[r][c];

    if (allSame(grid, r, c, size, first)) {
        return string(1, first);
    }

    int half = size / 2;
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
    if (!(cin >> n)) return 0;

    vector<string> grid(n);
    for (int i = 0; i < n; ++i) {
        cin >> grid[i];
    }

    cout << solve(grid, 0, 0, n) << '\n';
    return 0;
}