#include <iostream>

using namespace std;

long long comb(int n, int k) {
    if (k < 0 || k > n) return 0;
    int kk = min(k, n - k);
    long long acc = 1;
    for (int i = 1; i <= kk; ++i) {
        acc = acc * (n - kk + i) / i;
    }
    return acc;
}

long long uniquePaths(long long m, long long n) {
    return comb((int)(m + n - 2), (int)min(m - 1, n - 1));
}

int main() {
    long long m, n;
    if (cin >> m >> n) {
        cout << uniquePaths(m, n) << endl;
    }
    return 0;
}