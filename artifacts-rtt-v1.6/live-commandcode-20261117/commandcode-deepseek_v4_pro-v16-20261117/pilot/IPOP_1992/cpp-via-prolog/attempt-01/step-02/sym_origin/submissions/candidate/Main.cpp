#include <iostream>
#include <vector>
#include <string>

using namespace std;

static string compress(const vector<string>& grid, int r, int c, int size) {
    char first = grid[r][c];
    bool uniform = true;
    for (int i = r; i < r + size && uniform; ++i) {
        for (int j = c; j < c + size; ++j) {
            if (grid[i][j] != first) {
                uniform = false;
                break;
            }
        }
    }

    if (uniform) {
        return string(1, first);
    }

    int half = size / 2;
    string tl = compress(grid, r, c, half);
    string tr = compress(grid, r, c + half, half);
    string bl = compress(grid, r + half, c, half);
    string br = compress(grid, r + half, c + half, half);

    return "(" + tl + tr + bl + br + ")";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    cin >> N;

    vector<string> grid(N);
    for (int i = 0; i < N; ++i) {
        cin >> grid[i];
    }

    cout << compress(grid, 0, 0, N) << '\n';

    return 0;
}