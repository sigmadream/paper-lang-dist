#include <iostream>
#include <vector>
#include <string>

std::string solve(const std::vector<std::string>& grid, int r, int c, int size) {
    char first = grid[r][c];
    bool same = true;
    for (int i = r; i < r + size; ++i) {
        for (int j = c; j < c + size; ++j) {
            if (grid[i][j] != first) {
                same = false;
                break;
            }
        }
        if (!same) break;
    }
    
    if (same) return std::string(1, first);
    
    int half = size / 2;
    std::string tl = solve(grid, r, c, half);
    std::string tr = solve(grid, r, c + half, half);
    std::string bl = solve(grid, r + half, c, half);
    std::string br = solve(grid, r + half, c + half, half);
    
    return "(" + tl + tr + bl + br + ")";
}

int main() {
    int n;
    std::cin >> n;
    std::vector<std::string> grid(n);
    for (int i = 0; i < n; ++i) {
        std::cin >> grid[i];
    }
    
    std::cout << solve(grid, 0, 0, n) << std::endl;

    return 0;
}
