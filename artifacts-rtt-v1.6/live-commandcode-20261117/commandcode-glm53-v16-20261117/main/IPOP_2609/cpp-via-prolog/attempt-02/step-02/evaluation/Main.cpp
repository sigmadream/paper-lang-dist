#include <bits/stdc++.h>
using namespace std;

int main() {
    long long A, B;
    if (cin >> A >> B) {
        long long a = A, b = B;
        while (b != 0) { long long r = a % b; a = b; b = r; }
        cout << a << "\n" << (A / a) * B << "\n";
    }
    return 0;
}