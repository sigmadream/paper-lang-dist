#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long n, c;
    if (!(cin >> n >> c)) return 0;
    vector<long long> s(n);
    for (auto &x : s) cin >> x;
    sort(s.begin(), s.end());
    long long lo = 1, hi = s.back() - s.front(), acc = 0;
    auto countGE = [&](long long mid) {
        long long k = 1;
        long long prev = s[0];
        for (size_t i = 1; i < s.size(); ++i) {
            if (s[i] - prev >= mid) { ++k; prev = s[i]; }
        }
        return k;
    };
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        if (countGE(mid) >= c) { acc = mid; lo = mid + 1; }
        else hi = mid - 1;
    }
    cout << acc << "\n";
    return 0;
}