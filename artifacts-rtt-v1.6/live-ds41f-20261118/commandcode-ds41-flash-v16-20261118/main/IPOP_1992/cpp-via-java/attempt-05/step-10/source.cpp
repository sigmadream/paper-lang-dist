#include <iostream>
#include <vector>
#include <string>

static int N;
static std::vector<std::string> grid;

std::string solve(int r, int c, int size) {
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

    if (same) return std::string(1, first);

    int half = size / 2;
    std::string tl = solve(r, c, half);
    std::string tr = solve(r, c + half, half);
    std::string bl = solve(r + half, c, half);
    std::string br = solve(r + half, c + half, half);

    return "(" + tl + tr + bl + br + ")";
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    if (!(std::cin >> N)) return 0;
    grid.resize(N);
    for (int i = 0; i < N; ++i) {
        std::cin >> grid[i];
    }

    std::cout << solve(0, 0, N) << '\n';
    return 0;
}