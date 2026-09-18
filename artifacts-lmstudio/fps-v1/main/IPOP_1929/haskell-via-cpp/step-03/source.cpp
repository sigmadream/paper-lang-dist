#include <iostream>
#include <cmath>
using namespace std;

bool isPrime(int n) {
    if (n < 2) return false;
    for (int d = 2; d <= sqrt(n); ++d) {
        if (n % d == 0) return false;
    }
    return true;
}

int main() {
    int lo, hi;
    cin >> lo >> hi;
    for (int i = lo; i <= hi; ++i) {
        if (isPrime(i)) cout << i << endl;
    }
    return 0;
}