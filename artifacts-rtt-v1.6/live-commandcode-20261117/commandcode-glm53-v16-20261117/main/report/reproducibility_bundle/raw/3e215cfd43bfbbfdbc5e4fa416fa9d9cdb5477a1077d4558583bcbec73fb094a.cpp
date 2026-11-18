#include <bits/stdc++.h>
using namespace std;

static bool feasible(const vector<long long>& a, long long mid, long long c) {
    long long prev = a[0];
    long long cnt = 1;
    for (size_t i = 1; i < a.size(); ++i) {
        if (a[i] - prev >= mid) {
            prev = a[i];
            ++cnt;
        }
    }
    return cnt >= c;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long n, c;
    if (!(cin >> n >> c)) return 0;
    vector<long long> a(n);
    for (long long i = 0; i < n; ++i) cin >> a[i];
    sort(a.begin(), a.end());
    long long lo = 1, hi = a[n - 1] - a[0], ans = 0;
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        if (feasible(a, mid, c)) {
            ans = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    cout << ans << "\n";
    return 0;
}