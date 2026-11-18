#include <iostream>
#include <vector>
#include <string>
using namespace std;

int N;
vector<string> grid;

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

    if (!(cin >> N)) return 0;

    grid.resize(N);
    for (int i = 0; i < N; ++i) {
        cin >> grid[i];
    }

    cout << solve(0, 0, N) << '\n';
    return 0;
}