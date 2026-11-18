#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m, n;
    if (!(cin >> m >> n)) return 0;

    vector<char> isPrime(n + 1, 0);
    for (int i = 2; i <= n; ++i) isPrime[i] = 1;

    for (long long i = 2; i * i <= n; ++i) {
        if (isPrime[i]) {
            for (long long j = i * i; j <= n; j += i) {
                isPrime[(int)j] = 0;
            }
        }
    }

    string out;
    for (int i = m; i <= n; ++i) {
        if (isPrime[i]) {
            out += to_string(i);
            out += '\n';
        }
    }
    cout << out;

    return 0;
}