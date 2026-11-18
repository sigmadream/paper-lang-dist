#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m, n;
    cin >> m >> n;

    vector<bool> isPrime(n + 1, true);
    isPrime[0] = false;
    if (n >= 1) isPrime[1] = false;

    for (int i = 2; 1LL * i * i <= n; ++i) {
        if (isPrime[i]) {
            for (long long j = 1LL * i * i; j <= n; j += i) {
                isPrime[j] = false;
            }
        }
    }

    string output;
    for (int i = m; i <= n; ++i) {
        if (isPrime[i]) {
            output += to_string(i);
            output += '\n';
        }
    }

    cout << output;
    return 0;
}