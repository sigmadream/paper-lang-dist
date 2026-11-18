#include <iostream>
#include <string>
#include <vector>

static std::vector<std::string> grid;
static int n;

std::string solve(int r, int c, int size) {
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
    size_t start = line.find_first_not_of(" \t\r\n");
    if (start == std::string::npos) return 0;
    size_t end = line.find_last_not_of(" \t\r\n");
    line = line.substr(start, end - start + 1);

    n = std::stoi(line);
    grid.assign(n, "");

    int row = 0;
    while (row < n && std::getline(std::cin, line)) {
        size_t s = line.find_first_not_of(" \t\r\n");
        if (s == std::string::npos) continue;
        size_t e = line.find_last_not_of(" \t\r\n");
        line = line.substr(s, e - s + 1);
        grid[row] = line;
        row++;
    }

    std::cout << solve(0, 0, n) << '\n';
    return 0;
}