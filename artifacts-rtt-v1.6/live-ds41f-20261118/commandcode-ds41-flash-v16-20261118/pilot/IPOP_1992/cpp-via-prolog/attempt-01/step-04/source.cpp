#include <iostream>
#include <vector>
#include <string>
using namespace std;

bool allSame(const vector<string>& grid, int r, int c, int size, char v) {
    for (int i = r; i < r + size; ++i) {
        for (int j = c; j < c + size; ++j) {
            if (grid[i][j] != v) return false;
        }
    }
    return true;
}

string solve(const vector<string>& grid, int r, int c, int size) {
    char v = grid[r][c];
    if (allSame(grid, r, c, size, v)) {
        return string(1, v);
    }

    int half = size / 2;
    string result = "(";
    result += solve(grid, r, c, half);
    result += solve(grid, r, c + half, half);
    result += solve(grid, r + half, c, half);
    result += solve(grid, r + half, c + half, half);
    result += ")";
    return result;
}

int main() {
    int n;
    cin >> n;

    vector<string> grid(n);
    for (int i = 0; i < n; ++i) {
        cin >> grid[i];
    }

    cout << solve(grid, 0, 0, n) << '\n';
    return 0;
}