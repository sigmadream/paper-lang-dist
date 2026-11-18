#include <iostream>
#include <vector>
#include <string>

using namespace std;

static vector<string> grid;

string solve(int r, int c, int size) {
    char first = grid[r][c];
    bool same = true;
    for (int i = r; i < r + size && same; i++) {
        for (int j = c; j < c + size; j++) {
            if (grid[i][j] != first) {
                same = false;
                break;
            }
        }
    }

    if (same) return string(1, first);

    int half = size / 2;
    string tl = solve(r, c, half);
    string tr = solve(r, c + half, half);
    string bl = solve(r + half, c, half);
    string br = solve(r + half, c + half, half);

    return "(" + tl + tr + bl + br + ")";
}

int main() {
    string line;
    if (!getline(cin, line)) return 0;
    if (line.empty()) return 0;
    int n = stoi(line);

    grid.resize(n);
    for (int i = 0; i < n; i++) {
        getline(cin, grid[i]);
        while (!grid[i].empty() && (grid[i].back() == '\r' || grid[i].back() == '\n')) {
            grid[i].pop_back();
        }
    }

    cout << solve(0, 0, n) << "\n";
    return 0;
}