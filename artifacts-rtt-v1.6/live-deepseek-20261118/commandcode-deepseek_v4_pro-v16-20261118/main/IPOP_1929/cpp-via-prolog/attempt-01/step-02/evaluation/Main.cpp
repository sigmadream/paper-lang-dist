#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int M, N;
    if (!(std::cin >> M >> N)) {
        return 0;
    }

    if (N < 2) {
        return 0;
    }

    std::vector<bool> is_prime(N + 1, true);
    is_prime[0] = is_prime[1] = false;

    for (int p = 2; p * p <= N; ++p) {
        if (is_prime[p]) {
            for (int multiple = p * p; multiple <= N; multiple += p) {
                is_prime[multiple] = false;
            }
        }
    }

    int start = std::max(M, 2);
    for (int i = start; i <= N; ++i) {
        if (is_prime[i]) {
            std::cout << i << '\n';
        }
    }

    return 0;
}