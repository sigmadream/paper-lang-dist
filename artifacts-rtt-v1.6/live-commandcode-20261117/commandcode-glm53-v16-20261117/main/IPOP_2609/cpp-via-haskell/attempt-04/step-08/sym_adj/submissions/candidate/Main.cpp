#include <iostream>
#include <numeric>

int main() {
    long long a, b;
    std::cin >> a >> b;
    long long g = std::gcd(a, b);
    std::cout << g << "\n";
    std::cout << (a / g) * b << "\n";
    return 0;
}