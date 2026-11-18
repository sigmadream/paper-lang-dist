#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long m, n;
    if (!(cin >> m >> n)) return 0;

    vector<char> is_prime(n + 1, 1);
    if (n >= 0) is_prime[0] = 0;
    if (n >= 1) is_prime[1] = 0;

    for (long long i = 2; i * i <= n; ++i) {
        if (is_prime[i]) {
            for (long long j = i * i; j <= n; j += i) {
                is_prime[j] = 0;
            }
        }
    }

    string out;
    for (long long x = m; x <= n; ++x) {
        if (is_prime[x]) {
            out += to_string(x);
            out += '\n';
        }
    }

    cout << out;
    return 0;
}