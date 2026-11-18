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
    if (!(cin >> a)) return 0;
    cin >> b;
    int g = gcd(a, b);
    cout << g << "\n";
    cout << (a / g) * b << "\n";
    return 0;
}