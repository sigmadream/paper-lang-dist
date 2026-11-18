#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string nStr;
    if (!(cin >> nStr)) return 0;

    int n = stoi(nStr);
    int limit = max(0, n);

    vector<long long> xs;
    xs.reserve(limit);

    long long x;
    while ((int)xs.size() < limit && (cin >> x)) {
        xs.push_back(x);
    }

    if (xs.empty()) return 0;

    long long cur = xs[0];
    long long best = xs[0];

    for (size_t i = 1; i < xs.size(); ++i) {
        cur = max(xs[i], cur + xs[i]);
        best = max(best, cur);
    }

    cout << best << '\n';
    return 0;
}