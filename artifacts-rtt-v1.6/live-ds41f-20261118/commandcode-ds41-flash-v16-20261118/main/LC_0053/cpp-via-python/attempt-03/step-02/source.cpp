#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<long long> data;
    long long x;
    while (cin >> x) data.push_back(x);
    if (data.empty()) return 0;

    int n = (int)data[0];
    vector<long long> a(data.begin() + 1, data.begin() + 1 + n);

    long long cur = a[0], best = a[0];
    for (int i = 1; i < n; ++i) {
        cur = max(a[i], cur + a[i]);
        best = max(best, cur);
    }

    cout << best << '\n';
    return 0;
}