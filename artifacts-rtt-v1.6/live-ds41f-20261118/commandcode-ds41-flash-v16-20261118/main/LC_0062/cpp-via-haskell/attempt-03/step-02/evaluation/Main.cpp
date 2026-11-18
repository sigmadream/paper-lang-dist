#include <iostream>
#include <vector>

int main() {
    int m, n;
    std::cin >> m >> n;

    std::vector<long long> row(n, 1);
    for (int i = 1; i < m; ++i) {
        for (int j = 1; j < n; ++j) {
            row[j] += row[j - 1];
        }
    }

    std::cout << row[n - 1] << '\n';
    return 0;
}