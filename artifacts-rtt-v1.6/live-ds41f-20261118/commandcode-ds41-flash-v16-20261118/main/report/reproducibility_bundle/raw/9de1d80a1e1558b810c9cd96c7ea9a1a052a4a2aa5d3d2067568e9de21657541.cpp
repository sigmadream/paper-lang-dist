#include <iostream>
#include <numeric>
using namespace std;

int main() {
    long long a, b;
    if (cin >> a >> b) {
        long long g = gcd(a, b);
        cout << g << '\n';
        cout << (a / g) * b << '\n';
    }
    return 0;
}