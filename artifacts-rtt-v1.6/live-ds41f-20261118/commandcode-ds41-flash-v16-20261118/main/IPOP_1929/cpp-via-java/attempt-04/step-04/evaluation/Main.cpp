#include <iostream>
#include <vector>
#include <string>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int m, n;
    if (!(std::cin >> m >> n)) return 0;

    std::vector<char> isPrime(n + 1, 1);
    if (n >= 0) isPrime[0] = 0;
    if (n >= 1) isPrime[1] = 0;

    for (long long i = 2; i * i <= n; ++i) {
        if (isPrime[i]) {
            for (long long j = i * i; j <= n; j += i) {
                isPrime[j] = 0;
            }
        }
    }

    std::string output;
    for (int i = m; i <= n; ++i) {
        if (isPrime[i]) {
            output += std::to_string(i);
            output += '\n';
        }
    }

    std::cout << output;
    return 0;
}