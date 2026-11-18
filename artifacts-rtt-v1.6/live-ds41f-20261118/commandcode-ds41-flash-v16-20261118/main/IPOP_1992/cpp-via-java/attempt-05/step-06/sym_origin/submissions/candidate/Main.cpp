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
    string tl = solve(r, c, half);
    string tr = solve(r, c + half, half);
    string bl = solve(r + half, c, half);
    string br = solve(r + half, c + half, half);
    return "(" + tl + tr + bl + br + ")";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string line;
    if (!getline(cin, line)) return 0;
    while (!line.empty() && (line.back() == '\r' || line.back() == '\n')) line.pop_back();
    if (line.empty()) return 0;

    int n = stoi(line);
    grid.resize(n);

    for (int i = 0; i < n; ++i) {
        string s;
        getline(cin, s);
        while (!s.empty() && (s.back() == '\r' || s.back() == '\n')) s.pop_back();
        grid[i] = s;
    }

    cout << solve(0, 0, n) << "\n";
    return 0;
}