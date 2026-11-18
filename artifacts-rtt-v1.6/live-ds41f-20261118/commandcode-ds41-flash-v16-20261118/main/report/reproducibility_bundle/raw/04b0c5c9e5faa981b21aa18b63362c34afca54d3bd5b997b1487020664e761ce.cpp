#include <iostream>

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
    std::cin >> a >> b;
    int g = gcd(a, b);
    std::cout << g << '\n';
    std::cout << (a / g) * b << '\n';
    return 0;
}