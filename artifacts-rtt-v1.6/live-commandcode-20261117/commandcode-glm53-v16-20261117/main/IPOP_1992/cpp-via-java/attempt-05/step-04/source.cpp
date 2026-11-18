#include <bits/stdc++.h>
using namespace std;

int n;
vector<string> grid;

string solve(int r, int c, int size) {
    char first = grid[r][c];
    bool same = true;
    for (int i = r; i < r + size && same; i++)
        for (int j = c; j < c + size; j++)
            if (grid[i][j] != first) { same = false; break; }
    if (same) return string(1, first);
    int half = size / 2;
    return "(" + solve(r, c, half) + solve(r, c + half, half)
            + solve(r + half, c, half) + solve(r + half, c + half, half) + ")";
}

int main() {
    if (!(cin >> n)) return 0;
    grid.resize(n);
    for (int i = 0; i < n; i++) {
        string line;
        while (line.empty() && getline(cin, line)) {
            // trim
            size_t a = line.find_first_not_of(" \t\r\n");
            if (a == string::npos) { line.clear(); continue; }
            size_t b = line.find_last_not_of(" \t\r\n");
            line = line.substr(a, b - a + 1);
            break;
        }
        grid[i] = line;
    }
    cout << solve(0, 0, n) << "\n";
    return 0;
}