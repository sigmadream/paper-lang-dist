#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    long long x;
    if (!(cin >> x)) {
        cout << 0 << '\n';
        return 0;
    }

    long long best = x;
    long long cur = x;

    for (int i = 1; i < n; ++i) {
        long long v;
        cin >> v;
        cur = max(v, cur + v);
        best = max(best, cur);
    }

    cout << best << '\n';
    return 0;
}