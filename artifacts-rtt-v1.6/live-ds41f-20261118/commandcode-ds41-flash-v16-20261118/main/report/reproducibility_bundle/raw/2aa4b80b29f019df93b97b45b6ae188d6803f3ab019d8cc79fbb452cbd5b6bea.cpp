#include <iostream>
#include <algorithm>

int main() {
    long long m, n;
    if (!(std::cin >> m >> n)) {
        return 0;
    }

    long long total = m + n - 2;
    long long k = std::min(m - 1, n - 1);

    long long result = 1;
    for (long long i = 1; i <= k; ++i) {
        result = result * (total - k + i) / i;
    }

    std::cout << result << '\n';
    return 0;
}