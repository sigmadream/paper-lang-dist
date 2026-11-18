#include <iostream>
#include <vector>
#include <string>

using namespace std;

bool allSame(const vector<string>& grid, int r, int c, int size, char value) {
    for (int i = r; i < r + size; ++i) {
        for (int j = c; j < c + size; ++j) {
            if (grid[i][j] != value) return false;
        }
    }
    return true;
}

string solve(const vector<string>& grid, int r, int c, int size) {
    char value = grid[r][c];

    if (allSame(grid, r, c, size, value)) {
        return string(1, value);
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
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;

    vector<string> grid(N);
    for (int i = 0; i < N; ++i) {
        cin >> grid[i];
    }

    cout << solve(grid, 0, 0, N) << '\n';

    return 0;
}