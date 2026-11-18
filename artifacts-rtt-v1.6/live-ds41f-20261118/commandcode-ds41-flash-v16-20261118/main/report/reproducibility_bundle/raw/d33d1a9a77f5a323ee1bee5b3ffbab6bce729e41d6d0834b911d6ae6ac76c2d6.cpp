#include <iostream>
#include <vector>
#include <string>

static std::vector<std::string> grid;
static std::string result;

static void solve(int r, int c, int size) {
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
        result.push_back(first);
        return;
    }

    int half = size / 2;
    result.push_back('(');
    solve(r, c, half);
    solve(r, c + half, half);
    solve(r + half, c, half);
    solve(r + half, c + half, half);
    result.push_back(')');
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

    solve(0, 0, n);
    std::cout << result << '\n';

    return 0;
}