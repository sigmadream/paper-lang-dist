#include <iostream>
#include <vector>

int main() {
    long long n;
    if (!(std::cin >> n)) return 0;

    std::vector<long long> nonZeros;
    long long zeros = 0;
    for (long long i = 0; i < n; ++i) {
        long long x;
        std::cin >> x;
        if (x == 0) {
            ++zeros;
        } else {
            nonZeros.push_back(x);
        }
    }

    bool first = true;
    for (long long x : nonZeros) {
        if (!first) std::cout << ' ';
        std::cout << x;
        first = false;
    }
    for (long long i = 0; i < zeros; ++i) {
        if (!first) std::cout << ' ';
        std::cout << 0;
        first = false;
    }
    std::cout << '\n';
    return 0;
}