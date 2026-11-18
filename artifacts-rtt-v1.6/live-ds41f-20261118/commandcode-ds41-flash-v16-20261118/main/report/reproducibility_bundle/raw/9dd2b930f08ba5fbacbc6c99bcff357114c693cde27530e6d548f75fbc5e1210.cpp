#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    if (!(cin >> n)) return 0;

    vector<long long> a;
    a.reserve((size_t)max(0LL, n));
    for (long long i = 0; i < n; ++i) {
        long long x;
        if (!(cin >> x)) break;
        a.push_back(x);
    }

    if (a.empty()) return 0;

    long long cur = a[0];
    long long best = a[0];

    for (size_t i = 1; i < a.size(); ++i) {
        cur = max(a[i], cur + a[i]);
        best = max(best, cur);
    }

    cout << best << '\n';
    return 0;
}