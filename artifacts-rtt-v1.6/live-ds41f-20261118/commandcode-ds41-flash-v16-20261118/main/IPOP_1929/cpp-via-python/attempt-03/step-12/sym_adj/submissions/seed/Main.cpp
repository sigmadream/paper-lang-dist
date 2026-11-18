#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int M, N;
    if (!(std::cin >> M >> N)) return 0;

    std::vector<bool> is_prime(N + 1, true);
    if (N >= 0) is_prime[0] = false;
    if (N >= 1) is_prime[1] = false;

    for (int i = 2; i * i <= N; ++i) {
        if (is_prime[i]) {
            for (int j = i * i; j <= N; j += i) {
                is_prime[j] = false;
            }
        }
    }

    for (int x = M; x <= N; ++x) {
        if (is_prime[x]) {
            std::cout << x << '\n';
        }
    }

    return 0;
}