#include <bits/stdc++.h>
using namespace std;

static long long countPlacements(long long d, const vector<long long>& homes) {
    if (homes.empty()) return 0;
    long long cnt = 1;
    long long prev = homes[0];
    for (size_t i = 1; i < homes.size(); ++i) {
        if (homes[i] - prev >= d) {
            ++cnt;
            prev = homes[i];
        }
    }
    return cnt;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    long long C;
    if (!(cin >> N >> C)) return 0;

    vector<long long> homes(N);
    for (int i = 0; i < N; ++i) cin >> homes[i];

    sort(homes.begin(), homes.end());

    long long lo = 1;
    long long hi = homes.back() - homes.front();
    long long best = 0;

    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        if (countPlacements(mid, homes) >= C) {
            best = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }

    cout << best << '\n';
    return 0;
}