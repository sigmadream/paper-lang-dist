#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    long long x;
    cin >> x;

    long long cur = x;
    long long best = x;

    for (int i = 1; i < n; ++i) {
        cin >> x;
        cur = max(x, cur + x);
        best = max(best, cur);
    }

    cout << best << '\n';
    return 0;
}