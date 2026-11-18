#include <bits/stdc++.h>
using namespace std;

int main() {
    long long n;
    if (!(cin >> n)) return 0;
    vector<long long> xs;
    long long x;
    while ((long long)xs.size() < n && (cin >> x)) xs.push_back(x);
    if (n < 1 || xs.empty()) return 0;
    long long best = xs[0], cur = xs[0];
    for (size_t i = 1; i < xs.size(); ++i) {
        cur = max(xs[i], cur + xs[i]);
        best = max(best, cur);
    }
    cout << best << "\n";
    return 0;
}