#include <iostream>
using namespace std;

int gcd_(int a, int b) {
    while (b != 0) {
        int t = a % b;
        a = b;
        b = t;
    }
    return a;
}

int main() {
    int a, b;
    if (cin >> a >> b) {
        int g = gcd_(a, b);
        cout << g << "\n" << (a / g) * b << "\n";
    }
    return 0;
}