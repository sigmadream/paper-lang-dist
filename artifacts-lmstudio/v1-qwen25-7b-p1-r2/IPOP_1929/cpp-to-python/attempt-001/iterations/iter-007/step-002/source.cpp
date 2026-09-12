#include <iostream>
#include <vector>
#include <cmath>

void sieve_of_eratosthenes(int m, int n) {
    std::vector<bool> is_prime(n + 1, true);
    is_prime[0] = is_prime[1] = false;
    
    for (int i = 2; i <= std::sqrt(n); ++i) {
        if (is_prime[i]) {
            for (int j = i * i; j <= n; j += i) {
                is_prime[j] = false;
            }
        }
    }
    
    for (int i = m; i <= n; ++i) {
        if (is_prime[i]) {
            std::cout << i << std::endl;
        }
    }
}

int main() {
    int m, n;
    std::cin >> m >> n;
    sieve_of_eratosthenes(m, n);
    return 0;
}
