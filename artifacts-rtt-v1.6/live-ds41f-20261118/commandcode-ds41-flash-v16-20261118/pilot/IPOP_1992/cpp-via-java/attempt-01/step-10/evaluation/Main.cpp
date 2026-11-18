#include <bits/stdc++.h>
using namespace std;

int N;
vector<string> grid;

static string trim(const string& s) {
    size_t start = s.find_first_not_of(" \t\r\n\f\v");
    if (start == string::npos) return "";
    size_t end = s.find_last_not_of(" \t\r\n\f\v");
    return s.substr(start, end - start + 1);
}

static string solve(int r, int c, int size) {
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

    line = trim(line);
    if (line.empty()) return 0;

    N = stoi(line);
    grid.assign(N, "");

    for (int i = 0; i < N; ++i) {
        string row;
        while (getline(cin, row) && row.empty()) {
        }
        if (!cin && row.empty()) return 0;

        row = trim(row);
        grid[i] = row;
    }

    cout << solve(0, 0, N) << '\n';
    return 0;
}