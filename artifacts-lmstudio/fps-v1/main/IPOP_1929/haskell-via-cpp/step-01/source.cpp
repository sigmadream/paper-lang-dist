#include <iostream>
#include <vector>
using namespace std;

bool is_prime(int n) {
    if (n < 2) return false;
    for (int d = 2; d * d <= n; ++d) {
        if (n % d == 0) return false;
    }
    return true;
}

int main() {
    int lo, hi;
    cin >> lo >> hi;
    for (int i = lo; i <= hi; ++i) {
        if (is_prime(i)) {
            cout << i << endl;
        }
    }
    return 0;
}