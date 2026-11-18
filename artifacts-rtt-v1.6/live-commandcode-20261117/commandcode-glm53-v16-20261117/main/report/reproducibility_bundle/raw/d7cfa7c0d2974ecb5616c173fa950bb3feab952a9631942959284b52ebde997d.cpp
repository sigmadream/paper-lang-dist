#include <bits/stdc++.h>
using namespace std;

int main() {
    long long n;
    if (!(cin >> n)) n = 0;
    vector<int> counts(n + 1);
    counts[0] = 0;
    for (long long i = 1; i <= n; ++i) {
        counts[i] = counts[i / 2] + (i % 2);
    }
    for (long long i = 0; i <= n; ++i) {
        if (i) cout << ' ';
        cout << counts[i];
    }
    cout << '\n';
    return 0;
}