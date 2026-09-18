#include <iostream>
using namespace std;

int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int a, b;
    cin >> a >> b;

    int g = gcd(a, b);
    cout << g << '\n';
    cout << (a / g) * b << '\n';

    return 0;
}