#include <bits/stdc++.h>
using namespace std;

int N;
vector<string> grid;

void solve(int r, int c, int size) {
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
        cout << first;
    } else {
        int half = size / 2;
        cout << '(';
        solve(r, c, half);
        solve(r, c + half, half);
        solve(r + half, c, half);
        solve(r + half, c + half, half);
        cout << ')';
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    if (!(cin >> N)) return 0;
    grid.resize(N);
    for (int i = 0; i < N; ++i) cin >> grid[i];
    solve(0, 0, N);
    cout << '\n';
    return 0;
}