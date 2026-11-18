#include <iostream>
#include <string>
#include <vector>

using namespace std;

string solve(const vector<string>& grid, int r, int c, int size) {
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
    string tl = solve(grid, r, c, half);
    string tr = solve(grid, r, c + half, half);
    string bl = solve(grid, r + half, c, half);
    string br = solve(grid, r + half, c + half, half);

    return "(" + tl + tr + bl + br + ")";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    cin.ignore();  // consume newline after n

    vector<string> grid(n);
    for (int i = 0; i < n; ++i) {
        getline(cin, grid[i]);
    }

    cout << solve(grid, 0, 0, n) << '\n';
    return 0;
}