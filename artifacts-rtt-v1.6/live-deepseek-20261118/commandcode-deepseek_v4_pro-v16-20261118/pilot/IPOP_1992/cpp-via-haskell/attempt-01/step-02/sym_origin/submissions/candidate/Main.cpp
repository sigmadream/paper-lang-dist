#include <iostream>
#include <vector>
#include <string>

using namespace std;

string solve(const vector<string>& grid, int r, int c, int size) {
    char first = grid[r][c];
    bool allSame = true;

    for (int i = 0; i < size && allSame; ++i) {
        for (int j = 0; j < size; ++j) {
            if (grid[r + i][c + j] != first) {
                allSame = false;
                break;
            }
        }
    }

    if (allSame) {
        return string(1, first);
    }

    int half = size / 2;
    return "(" +
           solve(grid, r, c, half) +
           solve(grid, r, c + half, half) +
           solve(grid, r + half, c, half) +
           solve(grid, r + half, c + half, half) +
           ")";
}

int main() {
    int N;
    if (!(cin >> N)) {
        return 0;
    }

    vector<string> grid(N);
    for (int i = 0; i < N; ++i) {
        cin >> grid[i];
    }

    cout << solve(grid, 0, 0, N) << '\n';

    return 0;
}