#include <iostream>
#include <vector>
#include <string>
using namespace std;

bool sameRegion(int r, int c, int size, const vector<string>& grid, char v) {
    for (int i = r; i < r + size; ++i) {
        for (int j = c; j < c + size; ++j) {
            if (grid[i][j] != v) return false;
        }
    }
    return true;
}

string solve(int r, int c, int size, const vector<string>& grid) {
    char v = grid[r][c];
    if (sameRegion(r, c, size, grid, v)) {
        return string(1, v);
    }

    int half = size / 2;
    string result = "(";
    result += solve(r, c, half, grid);             // top-left
    result += solve(r, c + half, half, grid);      // top-right
    result += solve(r + half, c, half, grid);      // bottom-left
    result += solve(r + half, c + half, half, grid); // bottom-right
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

    cout << solve(0, 0, N, grid) << '\n';
    return 0;
}