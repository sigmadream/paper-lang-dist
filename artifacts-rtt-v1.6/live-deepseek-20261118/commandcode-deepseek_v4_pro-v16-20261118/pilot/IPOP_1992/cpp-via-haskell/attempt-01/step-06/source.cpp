#include <iostream>
#include <vector>
#include <string>

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

    string line;
    getline(cin, line);
    int N = stoi(line);

    vector<string> grid;
    for (int i = 0; i < N; ++i) {
        string row;
        getline(cin, row);
        grid.push_back(row);
    }

    string result = solve(grid, 0, 0, N);
    cout << result << '\n';

    return 0;
}