#include <bits/stdc++.h>
using namespace std;

static long long countPlacements(long long d, const vector<long long>& xs) {
    if (xs.empty()) return 0;
    long long cnt = 1;
    long long prev = xs[0];
    for (size_t i = 1; i < xs.size(); ++i) {
        if (xs[i] - prev >= d) {
            ++cnt;
            prev = xs[i];
        }
    }
    return cnt;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n, c;
    if (!(cin >> n >> c)) return 0;
    vector<long long> homes(n);
    for (long long i = 0; i < n; ++i) cin >> homes[i];
    sort(homes.begin(), homes.end());

    long long lo = 1;
    long long hi = homes.back() - homes.front();
    long long best = 0;
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        if (countPlacements(mid, homes) >= c) {
            best = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    cout << best << "\n";
    return 0;
}