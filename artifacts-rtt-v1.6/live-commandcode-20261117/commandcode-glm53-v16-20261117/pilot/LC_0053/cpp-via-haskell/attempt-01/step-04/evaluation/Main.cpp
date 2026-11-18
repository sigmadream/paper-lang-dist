#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<long long> xs(n);
    for (int i = 0; i < n; i++) cin >> xs[i];
    long long best = xs[0], cur = xs[0];
    for (int i = 1; i < n; i++) {
        cur = max(xs[i], cur + xs[i]);
        best = max(best, cur);
    }
    cout << best << "\n";
    return 0;
}