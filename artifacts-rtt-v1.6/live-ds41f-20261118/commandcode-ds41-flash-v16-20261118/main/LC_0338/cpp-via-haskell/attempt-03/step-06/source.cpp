#include <iostream>
#include <vector>
int main() {
    long long n;
    if (!(std::cin >> n)) return 0;
    std::vector<int> counts(n + 1, 0);
    for (long long i = 1; i <= n; ++i) {
        counts[i] = counts[i / 2] + (int)(i % 2);
    }
    for (long long i = 0; i <= n; ++i) {
        if (i) std::cout << ' ';
        std::cout << counts[i];
    }
    std::cout << '\n';
    return 0;
}