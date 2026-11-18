#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    if (!(cin >> n)) return 0;

    vector<long long> a;
    if (n > 0) a.reserve(static_cast<size_t>(n));

    for (long long i = 0; i < n; ++i) {
        long long x;
        if (cin >> x) a.push_back(x);
        else break;
    }

    if (a.empty()) {
        cout << 0 << '\n';
        return 0;
    }

    long long cur = a[0];
    long long best = a[0];

    for (size_t i = 1; i < a.size(); ++i) {
        long long v = a[i];
        cur = max(v, cur + v);
        best = max(best, cur);
    }

    cout << best << '\n';
    return 0;
}