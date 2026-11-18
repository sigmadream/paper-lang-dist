#include <bits/stdc++.h>
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

static string trim(const string& s) {
    size_t begin = 0;
    size_t end = s.size();

    while (begin < end && isspace(static_cast<unsigned char>(s[begin]))) ++begin;
    while (end > begin && isspace(static_cast<unsigned char>(s[end - 1]))) --end;

    return s.substr(begin, end - begin);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string line;
    if (!getline(cin, line)) return 0;

    line = trim(line);
    if (line.empty()) return 0;

    int n = stoi(line);
    grid.assign(n, string());

    int row = 0;
    while (row < n && getline(cin, line)) {
        line = trim(line);
        if (line.empty()) continue;

        grid[row] = line;
        ++row;
    }

    cout << solve(0, 0, n) << '\n';
    return 0;
}