#include <bits/stdc++.h>
using namespace std;

int main() {
    long long m, n;
    if (!(cin >> m >> n)) return 0;
    vector<char> isPrime(n + 1, 1);
    if (n >= 0) isPrime[0] = 0;
    if (n >= 1) isPrime[1] = 0;
    for (long long i = 2; i * i <= n; ++i) {
        if (isPrime[i]) {
            for (long long j = i * i; j <= n; j += i) isPrime[j] = 0;
        }
    }
    string out;
    for (long long i = m; i <= n; ++i) {
        if (isPrime[i]) {
            out += to_string(i);
            out += '\n';
        }
    }
    if (!out.empty()) out.pop_back();
    if (!out.empty()) out += '\n';
    fputs(out.c_str(), stdout);
    return 0;
}