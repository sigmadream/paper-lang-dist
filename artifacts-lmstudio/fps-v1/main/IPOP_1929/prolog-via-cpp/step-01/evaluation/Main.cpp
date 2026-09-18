#include <iostream>
#include <vector>
#include <cmath>

bool prime(int n) {
    if (n < 2) return false;
    for (int d = 2; d <= std::sqrt(n); ++d) {
        if (n % d == 0) return false;
    }
    return true;
}

int main() {
    int L, H;
    std::cin >> L >> H;
    for (int N = L; N <= H; ++N) {
        if (prime(N)) {
            std::cout << N << '\n';
        }
    }
    return 0;
}