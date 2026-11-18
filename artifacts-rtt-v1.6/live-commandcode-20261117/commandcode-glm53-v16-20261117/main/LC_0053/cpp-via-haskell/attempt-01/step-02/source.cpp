#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<int> xs(n);
    for (int i = 0; i < n; ++i) cin >> xs[i];
    if (xs.empty()) return 0;
    long long cur = xs[0], best = xs[0];
    for (int i = 1; i < n; ++i) {
        cur = max((long long)xs[i], cur + xs[i]);
        best = max(best, cur);
    }
    cout << best << "\n";
    return 0;
}