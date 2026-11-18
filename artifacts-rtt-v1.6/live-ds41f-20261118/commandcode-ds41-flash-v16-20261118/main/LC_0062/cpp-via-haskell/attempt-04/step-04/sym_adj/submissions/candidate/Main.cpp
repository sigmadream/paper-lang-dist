#include <iostream>
#include <algorithm>

long long comb(long long n, long long k) {
    if (k < 0 || k > n) return 0;
    k = std::min(k, n - k);
    long long res = 1;
    for (long long i = 1; i <= k; ++i) {
        res = res * (n - k + i) / i;
    }
    return res;
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