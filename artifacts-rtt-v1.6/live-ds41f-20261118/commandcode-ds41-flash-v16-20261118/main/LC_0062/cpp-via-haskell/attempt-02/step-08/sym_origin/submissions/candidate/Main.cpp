#include <iostream>
#include <algorithm>

long long choose(long long n, long long k) {
    if (k < 0 || k > n) return 0;
    long long kk = std::min(k, n - k);
    long long res = 1;
    for (long long i = 1; i <= kk; ++i) {
        res = res * (n - kk + i) / i;
    }
    return res;
}

int main() {
    long long m, n;
    if (std::cin >> m >> n) {
        std::cout << choose(m + n - 2, std::min(m - 1, n - 1)) << '\n';
    }
    return 0;
}