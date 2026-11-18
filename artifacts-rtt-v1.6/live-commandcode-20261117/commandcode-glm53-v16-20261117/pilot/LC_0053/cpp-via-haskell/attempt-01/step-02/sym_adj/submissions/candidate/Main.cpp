#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> xs(n);
    for (int i = 0; i < n; ++i) cin >> xs[i];
    long long cur = xs[0], best = xs[0];
    for (int i = 1; i < n; ++i) {
        cur = max(xs[i], cur + xs[i]);
        best = max(best, cur);
    }
    cout << best << "\n";
    return 0;
}