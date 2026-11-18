#include <iostream>
#include <vector>
#include <cmath>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int m, n;
    if (!(std::cin >> m >> n)) return 0;

    std::vector<char> isPrime(n + 1, 1);
    if (n >= 0) isPrime[0] = 0;
    if (n >= 1) isPrime[1] = 0;

    for (int i = 2; i * i <= n; ++i) {
        if (isPrime[i]) {
            for (int j = i * i; j <= n; j += i) {
                isPrime[j] = 0;
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