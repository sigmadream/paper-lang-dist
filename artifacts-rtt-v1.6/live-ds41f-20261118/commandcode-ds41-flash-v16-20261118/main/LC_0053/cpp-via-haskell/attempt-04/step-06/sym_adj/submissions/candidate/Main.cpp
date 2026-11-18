#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string first;
    if (!(cin >> first)) return 0;

    int n = stoi(first);
    int limit = max(0, n);

    vector<long long> xs;
    xs.reserve(limit);
    for (int i = 0; i < limit; ++i) {
        long long x;
        if (!(cin >> x)) break;
        xs.push_back(x);
    }

    if (xs.empty()) return 0;

    long long cur = xs[0];
    long long best = xs[0];

    for (size_t i = 1; i < xs.size(); ++i) {
        long long x = xs[i];
        cur = max(x, cur + x);
        best = max(best, cur);
    }

    cout << best << '\n';
    return 0;
}