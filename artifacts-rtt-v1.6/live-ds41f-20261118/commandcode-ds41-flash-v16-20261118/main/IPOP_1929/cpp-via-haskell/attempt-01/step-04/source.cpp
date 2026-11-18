#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int m, n;
    if (!(std::cin >> m >> n)) {
        return 0;
    }

    std::vector<char> isPrime(n + 1, true);
    if (n >= 0) isPrime[0] = false;
    if (n >= 1) isPrime[1] = false;

    for (int i = 2; 1LL * i * i <= n; ++i) {
        if (isPrime[i]) {
            for (long long j = 1LL * i * i; j <= n; j += i) {
                isPrime[j] = false;
            }
        }
    }

    for (int i = m; i <= n; ++i) {
        if (isPrime[i]) {
            std::cout << i << '\n';
        }
    }

    return 0;
}