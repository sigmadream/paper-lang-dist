#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m, n;
    if (!(cin >> m >> n)) return 0;

    vector<char> is_prime(n + 1, 1);
    if (n >= 0) is_prime[0] = 0;
    if (n >= 1) is_prime[1] = 0;

    for (int i = 2; 1LL * i * i <= n; ++i) {
        if (is_prime[i]) {
            for (long long j = 1LL * i * i; j <= n; j += i) {
                is_prime[(int)j] = 0;
            }
        }
    }

    string output;
    for (int x = m; x <= n; ++x) {
        if (is_prime[x]) {
            output += to_string(x);
            output += '\n';
        }
    }

    cout << output;
    return 0;
}