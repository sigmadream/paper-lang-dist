#include <iostream>
#include <vector>

int main() {
    int m, n;
    std::cin >> m >> n;

    std::vector<std::vector<int>> table(m, std::vector<int>(n));

    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            if (i == 0 || j == 0) {
                table[i][j] = 1;
            } else {
                table[i][j] = table[i-1][j] + table[i][j-1];
            }
        }
    }

    std::cout << table[m-1][n-1] << std::endl;

    return 0;
}