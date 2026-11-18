#include <iostream>
#include <vector>
#include <string>

std::vector<std::string> grid;

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
    if (same) {
        return std::string(1, first);
    }
    int half = size / 2;
    std::string result = "(";
    result += solve(r, c, half);
    result += solve(r, c + half, half);
    result += solve(r + half, c, half);
    result += solve(r + half, c + half, half);
    result += ")";
    return result;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    grid.resize(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> grid[i];
    }

    std::cout << solve(0, 0, n) << "\n";
    return 0;
}