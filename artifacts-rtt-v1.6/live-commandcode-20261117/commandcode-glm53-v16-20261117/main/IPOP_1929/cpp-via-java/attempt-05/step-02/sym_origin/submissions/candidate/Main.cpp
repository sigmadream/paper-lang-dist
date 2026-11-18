#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m, n;
    if (!(cin >> m >> n)) return 0;

    vector<bool> isPrime(n + 1, true);
    if (n >= 0) isPrime[0] = false;
    if (n >= 1) isPrime[1] = false;

    for (int i = 2; (long long)i * i <= n; i++) {
        if (isPrime[i]) {
            for (long long j = (long long)i * i; j <= n; j += i) {
                isPrime[j] = false;
            }
        }
    }

    string out;
    for (int i = m; i <= n; i++) {
        if (isPrime[i]) { out += to_string(i); out += '\n'; }
    }
    cout << out;
    return 0;
}