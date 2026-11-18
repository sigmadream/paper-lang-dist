#include <iostream>
#include <vector>

int main() {
    long long m, n;
    if (!(std::cin >> m >> n)) return 0;

    std::vector<long long> row(n, 1);
    for (long long i = 1; i < m; ++i) {
        for (long long j = 1; j < n; ++j) {
            row[j] += row[j - 1];
        }
    }

    std::cout << row[n - 1] << '\n';
    return 0;
}