#include <bits/stdc++.h>
using namespace std;

int main() {
    long long m, n;
    if (!(cin >> m >> n)) return 0;
    vector<char> sieve(n + 1, 1);
    if (n >= 0) sieve[0] = 0;
    if (n >= 1) sieve[1] = 0;
    for (long long i = 2; i * i <= n; ++i) {
        if (sieve[i]) {
                for (long long j = i * i; j <= n; j += i) sieve[j] = 0;
        }
    }
    string out;
    for (long long i = m; i <= n; ++i) {
        if (sieve[i]) {
            out += to_string(i);
            out += '\n';
        }
    }
    if (!out.empty()) out.pop_back();
    cout << out << "\n";
    return 0;
}