#include <iostream>
using namespace std;

int main() {
    long long a, b;
    if (!(cin >> a >> b)) return 0;
    long long x = a, y = b;
    while (y != 0) {
        long long r = x % y;
        x = y;
        y = r;
    }
    long long g = x;
    cout << g << "\n" << (a / g) * b << "\n";
    return 0;
}