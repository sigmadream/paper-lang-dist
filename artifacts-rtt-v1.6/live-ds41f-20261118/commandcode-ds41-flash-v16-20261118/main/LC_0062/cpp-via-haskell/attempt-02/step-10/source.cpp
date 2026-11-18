#include <bits/stdc++.h>
using namespace std;

int main() {
    long long m, n;
    if (!(cin >> m >> n)) return 0;
    long long N = m + n - 2;
    long long K = min(m - 1, n - 1);
    long long res = 1;
    for (long long i = 1; i <= K; ++i) {
        res = res * (N - K + i) / i;
    }
    cout << res << "\n";
    return 0;
}