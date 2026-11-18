#include <iostream>
#include <numeric>

int main() {
    long long A, B;
    if (!(std::cin >> A >> B)) return 0;
    long long G = std::gcd(A, B);
    long long L = (A / G) * B;
    std::cout << G << '\n' << L << '\n';
    return 0;
}