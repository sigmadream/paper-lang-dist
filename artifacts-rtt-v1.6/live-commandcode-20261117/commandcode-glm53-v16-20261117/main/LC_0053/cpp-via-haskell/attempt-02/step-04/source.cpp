#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long n;
    if (!(cin >> n)) return 0;
    if (n < 1) return 0;
    vector<long long> xs(n);
    for (long long i = 0; i < n; ++i) cin >> xs[i];
    long long best = xs[0], cur = xs[0];
    for (size_t i = 1; i < xs.size(); ++i) {
        cur = max(xs[i], cur + xs[i]);
        best = max(best, cur);
    }
    cout << best << "\n";
    return 0;
}