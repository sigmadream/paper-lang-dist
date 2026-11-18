#include <iostream>
#include <vector>
#include <string>
using namespace std;

string solve(const vector<string>& grid, int r, int c, int size) {
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
    } else {
        int half = size / 2;
        return "(" + solve(grid, r, c, half)
                   + solve(grid, r, c + half, half)
                   + solve(grid, r + half, c, half)
                   + solve(grid, r + half, c + half, half) + ")";
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    cin.ignore();
    vector<string> grid(n);
    for (int i = 0; i < n; ++i) {
        getline(cin, grid[i]);
    }
    string result = solve(grid, 0, 0, n);
    cout << result << '\n';
    return 0;
}