#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    if (!(cin >> n)) return 0;

    vector<long long> vals;
    vals.reserve((size_t)max(0LL, n));

    for (long long i = 0; i < n; ++i) {
        long long x;
        if (!(cin >> x)) break;
        vals.push_back(x);
    }

    if (vals.empty()) {
        cout << 0 << '\n';
        return 0;
    }

    long long cur = vals[0];
    long long best = vals[0];

    for (size_t i = 1; i < vals.size(); ++i) {
        cur = max(vals[i], cur + vals[i]);
        best = max(best, cur);
    }

    cout << best << '\n';
    return 0;
}