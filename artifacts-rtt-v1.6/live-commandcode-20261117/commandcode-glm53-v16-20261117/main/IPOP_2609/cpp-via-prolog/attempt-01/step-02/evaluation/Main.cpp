#include <iostream>
using namespace std;

int main() {
    long long a, b;
    if (cin >> a >> b) {
        long long x = a, y = b;
        while (y != 0) {
            long long r = x % y;
            x = y;
            y = r;
        }
        cout << x << "\n" << (a / x) * b << "\n";
    }
    return 0;
}