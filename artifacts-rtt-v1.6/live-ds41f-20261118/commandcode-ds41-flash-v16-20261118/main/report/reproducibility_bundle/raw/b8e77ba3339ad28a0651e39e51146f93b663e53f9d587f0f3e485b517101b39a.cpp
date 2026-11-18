#include <iostream>
#include <string>
#include <vector>

static std::vector<std::string> grid;

static std::string solve(int r, int c, int size) {
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
    std::string result;
    result += '(';
    result += solve(r, c, half);
    result += solve(r, c + half, half);
    result += solve(r + half, c, half);
    result += solve(r + half, c + half, half);
    result += ')';
    return result;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string line;
    if (!std::getline(std::cin, line)) return 0;

    // trim
    while (!line.empty() && (line.back() == '\r' || line.back() == '\n' || line.back() == ' ' || line.back() == '\t')) {
        line.pop_back();
    }
    size_t start = 0;
    while (start < line.size() && (line[start] == ' ' || line[start] == '\t')) ++start;
    if (start >= line.size()) return 0;

    int n = std::stoi(line.substr(start));
    grid.assign(n, std::string());
    for (int i = 0; i < n; ++i) {
        std::getline(std::cin, grid[i]);
        while (!grid[i].empty() && (grid[i].back() == '\r' || grid[i].back() == '\n')) {
            grid[i].pop_back();
        }
    }

    std::cout << solve(0, 0, n) << '\n';
    return 0;
}