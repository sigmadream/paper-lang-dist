#include <iostream>
#include <string>
using namespace std;

long long gcd_(long long a, long long b) {
    while (b != 0) {
        long long t = a % b;
        a = b;
        b = t;
    }
    return a;
}

int main() {
    long long a, b;
    if (cin >> a >> b) {
        long long g = gcd_(a, b);
        cout << g << "\n" << (a / g) * b << "\n";
    }
    return 0;
}