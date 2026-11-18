#include <iostream>
#include <numeric>

int gcd(int a, int b) {
    while (b != 0) {
        int r = a % b;
        a = b;
        b = r;
    }
    return a;
}

int main() {
    int a, b;
    if (!(std::cin >> a)) return 0;
    std::cin >> b;
    int g = gcd(a, b);
    std::cout << g << '\n';
    std::cout << (a / g) * b << '\n';
    return 0;
}