#include <iostream>
#include <numeric>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    long long a, b;
    if (!(std::cin >> a >> b)) {
        return 0;
    }

    long long g = std::gcd(a, b);
    std::cout << g << '\n';
    std::cout << (a / g) * b << '\n';

    return 0;
}