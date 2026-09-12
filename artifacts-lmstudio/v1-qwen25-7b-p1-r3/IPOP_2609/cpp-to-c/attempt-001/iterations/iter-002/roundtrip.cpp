#include <iostream>
using namespace std;

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
    if (scanf("%d %d", &a, &b) == 2) {
        int g = gcd(a, b);
        printf("%d\n", g);
        printf("%d\n", (a / g) * b);
    }
    return 0;
}
