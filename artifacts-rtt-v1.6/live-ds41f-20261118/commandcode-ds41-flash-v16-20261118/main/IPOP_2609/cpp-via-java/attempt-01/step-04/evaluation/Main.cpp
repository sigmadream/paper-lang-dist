#include <iostream>
using namespace std;

static int gcd(int a, int b) {
    while (b != 0) {
        int r = a % b;
        a = b;
        b = r;
    }
    return a;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int a, b;
    if (!(cin >> a)) return 0;
    if (!(cin >> b)) return 0;

    int g = gcd(a, b);
    cout << g << '\n';
    cout << (long long)(a / g) * b << '\n';

    return 0;
}