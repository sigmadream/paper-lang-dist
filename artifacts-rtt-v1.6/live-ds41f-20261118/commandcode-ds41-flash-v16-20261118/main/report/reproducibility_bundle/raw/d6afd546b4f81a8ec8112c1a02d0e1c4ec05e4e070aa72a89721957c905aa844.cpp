#include <iostream>
#include <numeric>

static int gcd_int(int a, int b) {
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
    if (!(std::cin >> b)) return 0;

    int g = gcd_int(a, b);
    std::cout << g << '\n';
    std::cout << (long long)(a / g) * b << '\n';
    return 0;
}