#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long m, n;
    if (!(cin >> m >> n)) return 0;

    vector<char> isComposite(n + 1, 0);
    if (n >= 0) isComposite[0] = 1;
    if (n >= 1) isComposite[1] = 1;

    for (long long i = 2; i * i <= n; i++) {
        if (!isComposite[i]) {
            for (long long j = i * i; j <= n; j += i) {
                isComposite[j] = 1;
            }
        }
    }

    string out;
    for (long long i = m; i <= n; i++) {
        if (!isComposite[i]) {
            out += to_string(i);
            out += '\n';
        }
    }
    cout << out;
    return 0;
}