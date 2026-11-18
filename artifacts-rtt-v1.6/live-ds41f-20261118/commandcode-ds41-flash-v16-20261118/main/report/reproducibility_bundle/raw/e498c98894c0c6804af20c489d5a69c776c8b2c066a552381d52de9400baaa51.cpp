#include <iostream>

static int gcdInt(int a, int b) {
    while (b != 0) {
        int r = a % b;
        a = b;
        b = r;
    }
    return a;
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int a, b;
    if (!(std::cin >> a)) return 0;
    if (!(std::cin >> b)) return 0;

    int g = gcdInt(a, b);
    std::cout << g << '\n';
    std::cout << static_cast<long long>(a / g) * b << '\n';

    return 0;
}