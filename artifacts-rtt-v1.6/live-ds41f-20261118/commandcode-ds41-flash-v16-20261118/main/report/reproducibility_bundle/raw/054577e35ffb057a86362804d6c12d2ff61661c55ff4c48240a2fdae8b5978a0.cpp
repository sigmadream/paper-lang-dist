#include <iostream>
#include <numeric>
using namespace std;

int main() {
    long long A, B;
    if (!(cin >> A >> B)) return 0;
    long long G = std::gcd(A, B);
    long long L = (A / G) * B;
    cout << G << '\n' << L << '\n';
    return 0;
}