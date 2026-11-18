#include <iostream>

long long comb(int n, int k) {
    if (k > n - k) k = n - k;
    long long result = 1;
    for (int i = 1; i <= k; ++i) {
        result = result * (n - k + i) / i;
    }
    return result;
}

int main() {
    int M, N;
    if (std::cin >> M >> N) {
        int total = M + N - 2;
        int k = M - 1;
        std::cout << comb(total, k) << '\n';
    }
    return 0;
}