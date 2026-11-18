#include <iostream>
#include <numeric>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int a, b;
    std::cin >> a >> b;

    int g = std::gcd(a, b);
    long long l = (long long)(a / g) * b;

    std::cout << g << '\n' << l << '\n';
    return 0;
}