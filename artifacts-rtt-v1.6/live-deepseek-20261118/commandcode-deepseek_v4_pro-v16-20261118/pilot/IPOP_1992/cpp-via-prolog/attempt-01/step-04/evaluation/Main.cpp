#include <iostream>
#include <string>
#include <vector>

std::string quadtree(const std::vector<std::string>& grid, int r, int c, int size) {
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
        return std::string(1, first);
    } else {
        int half = size / 2;
        std::string tl = quadtree(grid, r, c, half);
        std::string tr = quadtree(grid, r, c + half, half);
        std::string bl = quadtree(grid, r + half, c, half);
        std::string br = quadtree(grid, r + half, c + half, half);
        return "(" + tl + tr + bl + br + ")";
    }
}

int main() {
    std::string line;
    std::getline(std::cin, line);
    if (!line.empty() && line.back() == '\r') line.pop_back();
    int N = std::stoi(line);
    std::vector<std::string> grid;
    grid.reserve(N);
    for (int i = 0; i < N; ++i) {
        std::getline(std::cin, line);
        if (!line.empty() && line.back() == '\r') line.pop_back();
        grid.push_back(line);
    }
    std::cout << quadtree(grid, 0, 0, N) << '\n';
    return 0;
}