#include <iostream>

static int gcd(int a, int b) {
    while (b != 0) {
        int r = a % b;
        a = b;
        b = r;
    }
    return a;
}

int main() {
    int a, b;
    if (!(std::cin >> a >> b)) return 0;
    int g = gcd(a, b);
    std::cout << g << '\n';
    std::cout << (a / g) * b << '\n';
    return 0;
}