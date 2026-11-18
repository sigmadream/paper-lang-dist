#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m, n;
    cin >> m >> n;

    vector<char> isPrime(n + 1, true);
    if (n >= 0) isPrime[0] = false;
    if (n >= 1) isPrime[1] = false;

    for (long long i = 2; i * i <= n; ++i) {
        if (isPrime[(int)i]) {
            for (long long j = i * i; j <= n; j += i) {
                isPrime[(int)j] = false;
            }
        }
    }

    for (int i = m; i <= n; ++i) {
        if (isPrime[i]) {
            cout << i << '\n';
        }
    }

    return 0;
}