#include <bits/stdc++.h>
using namespace std;

int main() {
    long long A, B;
    if (!(cin >> A >> B)) return 0;
    long long g = __gcd(A, B);
    long long l = A / g * B;
    cout << g << "\n" << l << "\n";
    return 0;
}