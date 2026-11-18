#include <bits/stdc++.h>
using namespace std;

int N;
vector<string> grid;

bool allSame(int r, int c, int size, char value) {
    for (int i = r; i < r + size; ++i) {
        for (int j = c; j < c + size; ++j) {
            if (grid[i][j] != value) return false;
        }
    }
    return true;
}

string solve(int r, int c, int size) {
    char value = grid[r][c];
    if (allSame(r, c, size, value)) {
        return string(1, value);
    }

    int half = size / 2;
    string result = "(";
    result += solve(r, c, half);
    result += solve(r, c + half, half);
    result += solve(r + half, c, half);
    result += solve(r + half, c + half, half);
    result += ")";
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> N;
    grid.resize(N);
    for (int i = 0; i < N; ++i) {
        cin >> grid[i];
    }

    cout << solve(0, 0, N) << '\n';
    return 0;
}