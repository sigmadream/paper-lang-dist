#include <bits/stdc++.h>
using namespace std;

int main() {
    int m, n;
    if (scanf("%d %d", &m, &n) != 2) return 0;

    vector<bool> isPrime(n + 1, true);
    if (n >= 0) isPrime[0] = false;
    if (n >= 1) isPrime[1] = false;

    for (long long i = 2; i * i <= n; i++) {
        if (isPrime[(int)i]) {
            for (long long j = i * i; j <= n; j += i) {
                isPrime[(int)j] = false;
            }
        }
    }

    string out;
    for (int i = m; i <= n; i++) {
        if (isPrime[i]) {
            out += to_string(i);
            out += '\n';
        }
    }
    fputs(out.c_str(), stdout);
    return 0;
}