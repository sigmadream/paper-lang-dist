#include <iostream>
#include <algorithm>

long long comb(long long n, long long k) {
    if (k < 0 || k > n) return 0;
    long long kk = std::min(k, n - k);
    long long result = 1;
    for (long long i = 1; i <= kk; ++i) {
        result = result * (n - kk + i) / i;
    }
    return result;
}

long long uniquePaths(long long m, long long n) {
    return comb(m + n - 2, std::min(m - 1, n - 1));
}

int main() {
    long long m, n;
    if (std::cin >> m >> n) {
        std::cout << uniquePaths(m, n) << '\n';
    }
    return 0;
}