#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int M, N;
    if (!(std::cin >> M >> N)) return 0;

    std::vector<char> isPrime(N + 1, true);

    if (N >= 0) isPrime[0] = false;
    if (N >= 1) isPrime[1] = false;

    for (int i = 2; 1LL * i * i <= N; ++i) {
        if (isPrime[i]) {
            for (long long j = 1LL * i * i; j <= N; j += i) {
                isPrime[static_cast<int>(j)] = false;
            }
        }
    }

    int start = std::max(M, 2);
    for (int i = start; i <= N; ++i) {
        if (isPrime[i]) {
            std::cout << i << '\n';
        }
    }

    return 0;
}