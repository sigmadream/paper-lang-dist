#include <iostream>
#include <vector>

int main() {
    int m, n;
    if (!(std::cin >> m >> n)) return 0;

    std::vector<long long> row(n, 1);
    for (int i = 2; i <= m; ++i) {
        for (int j = 1; j < n; ++j) {
            row[j] += row[j - 1];
        }
    }

    std::cout << row[n - 1] << '\n';
    return 0;
}