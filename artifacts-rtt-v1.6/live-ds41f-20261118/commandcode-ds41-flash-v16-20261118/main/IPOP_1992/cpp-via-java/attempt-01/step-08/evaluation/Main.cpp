#include <iostream>
#include <vector>
#include <string>
using namespace std;

static vector<string> grid;

string solve(int r, int c, int size) {
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

    if (same) return string(1, first);

    int half = size / 2;
    string result;
    result += '(';
    result += solve(r, c, half);
    result += solve(r, c + half, half);
    result += solve(r + half, c, half);
    result += solve(r + half, c + half, half);
    result += ')';
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string line;
    if (!getline(cin, line)) return 0;

    if (!line.empty() && line.back() == '\r') line.pop_back();
    if (line.empty()) return 0;

    int n = stoi(line);
    grid.resize(n);

    for (int i = 0; i < n; ++i) {
        if (!getline(cin, grid[i])) grid[i] = "";
        if (!grid[i].empty() && grid[i].back() == '\r') grid[i].pop_back();
    }

    cout << solve(0, 0, n) << '\n';
    return 0;
}