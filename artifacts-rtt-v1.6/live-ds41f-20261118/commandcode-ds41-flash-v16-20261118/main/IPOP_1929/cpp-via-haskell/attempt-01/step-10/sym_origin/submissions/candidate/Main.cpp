#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int m, n;
    if (!(std::cin >> m >> n)) return 0;

    std::vector<bool> isPrime(n + 1, true);
    if (n >= 0) isPrime[0] = false;
    if (n >= 1) isPrime[1] = false;

    for (int i = 2; static_cast<long long>(i) * i <= n; ++i) {
        if (isPrime[i]) {
            for (long long j = static_cast<long long>(i) * i; j <= n; j += i) {
                isPrime[static_cast<int>(j)] = false;
            }
        }
    }

    int start = std::max(2, m);
    for (int i = start; i <= n; ++i) {
        if (isPrime[i]) {
            std::cout << i << '\n';
        }
    }

    return 0;
}