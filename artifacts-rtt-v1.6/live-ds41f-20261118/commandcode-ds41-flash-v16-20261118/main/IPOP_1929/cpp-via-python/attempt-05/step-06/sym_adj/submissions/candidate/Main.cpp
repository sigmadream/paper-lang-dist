#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int m, n;
    if (!(std::cin >> m >> n)) return 0;

    std::vector<char> is_prime(n + 1, 1);
    if (n >= 0) is_prime[0] = 0;
    if (n >= 1) is_prime[1] = 0;

    for (int i = 2; 1LL * i * i <= n; ++i) {
        if (is_prime[i]) {
            for (long long j = 1LL * i * i; j <= n; j += i) {
                is_prime[j] = 0;
            }
        }
    }

    for (int x = m; x <= n; ++x) {
        if (is_prime[x]) {
            std::cout << x << '\n';
        }
    }

    return 0;
}