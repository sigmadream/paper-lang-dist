#include <bits/stdc++.h>
using namespace std;

int main() {
    long long n;
    if (!(cin >> n)) return 0;
    vector<int> counts(n + 1, 0);
    for (long long i = 1; i <= n; ++i)
        counts[i] = counts[i / 2] + (int)(i % 2);
    for (long long i = 0; i <= n; ++i) {
        if (i) cout << ' ';
        cout << counts[i];
    }
    cout << '\n';
    return 0;
}