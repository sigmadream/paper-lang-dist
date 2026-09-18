#include <iostream>
#include <vector>

int uniquePaths(int m, int n) {
    std::vector<std::vector<int>> table(m, std::vector<int>(n, 0));
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            if (i == 0 || j == 0) {
                table[i][j] = 1;
            } else {
                table[i][j] = table[i-1][j] + table[i][j-1];
            }
        }
    }
    return table[m-1][n-1];
}

int main() {
    int m, n;
    std::cin >> m >> n;
    std::cout << uniquePaths(m, n) << std::endl;
    return 0;
}