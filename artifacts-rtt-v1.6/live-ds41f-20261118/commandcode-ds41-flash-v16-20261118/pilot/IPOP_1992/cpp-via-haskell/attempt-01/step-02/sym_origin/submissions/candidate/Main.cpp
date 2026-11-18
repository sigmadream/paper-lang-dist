#include <iostream>
#include <vector>
#include <string>

std::vector<std::string> grid;

bool same(int r, int c, int size) {
    char first = grid[r][c];
    for (int i = r; i < r + size; ++i)
        for (int j = c; j < c + size; ++j)
            if (grid[i][j] != first)
                return false;
    return true;
}

std::string solve(int r, int c, int size) {
    if (same(r, c, size))
        return std::string(1, grid[r][c]);
    int half = size / 2;
    return "(" + solve(r, c, half)
               + solve(r, c + half, half)
               + solve(r + half, c, half)
               + solve(r + half, c + half, half) + ")";
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    int n;
    if (!(std::cin >> n)) return 0;
    grid.resize(n);
    for (int i = 0; i < n; ++i) std::cin >> grid[i];
    std::cout << solve(0, 0, n) << "\n";
    return 0;
}