#include <iostream>
#include <vector>
#include <string>

static std::vector<std::string> grid;
static int n;

static std::string solve(int r, int c, int size) {
    char first = grid[r][c];
    bool same = true;

    for (int i = r; i < r + size && same; i++) {
        for (int j = c; j < c + size; j++) {
            if (grid[i][j] != first) {
                same = false;
                break;
            }
        }
    }

    if (same) return std::string(1, first);

    int half = size / 2;
    std::string sb;
    sb += '(';
    sb += solve(r, c, half);
    sb += solve(r, c + half, half);
    sb += solve(r + half, c, half);
    sb += solve(r + half, c + half, half);
    sb += ')';
    return sb;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::string line;
    if (!std::getline(std::cin, line)) return 0;

    // trim
    size_t start = line.find_first_not_of(" \t\r\n");
    size_t end = line.find_last_not_of(" \t\r\n");
    if (start == std::string::npos) return 0;
    line = line.substr(start, end - start + 1);
    if (line.empty()) return 0;

    n = std::stoi(line);
    grid.assign(n, "");

    int row = 0;
    while (row < n) {
        if (!std::getline(std::cin, line)) break;

        start = line.find_first_not_of(" \t\r\n");
        if (start == std::string::npos) continue;
        end = line.find_last_not_of(" \t\r\n");
        line = line.substr(start, end - start + 1);
        if (line.empty()) continue;

        grid[row] = line;
        row++;
    }

    std::cout << solve(0, 0, n) << '\n';
    return 0;
}