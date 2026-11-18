#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    long long first;
    if (!(cin >> first)) return 0;

    long long cur = first;
    long long best = first;

    for (int i = 1; i < n; ++i) {
        long long x;
        cin >> x;
        cur = max(x, cur + x);
        best = max(best, cur);
    }

    cout << best << '\n';
    return 0;
}