#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, C;
    if (!(cin >> N >> C)) return 0;

    vector<int> houses(N);
    for (int i = 0; i < N; ++i) cin >> houses[i];

    sort(houses.begin(), houses.end());

    auto canInstall = [&](int dist) {
        int count = 1;
        int prev = houses[0];

        for (int i = 1; i < N; ++i) {
            if (houses[i] - prev >= dist) {
                ++count;
                prev = houses[i];
                if (count >= C) return true;
            }
        }
        return count >= C;
    };

    int lo = 1;
    int hi = houses.back() - houses.front();
    int ans = 0;

    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;

        if (canInstall(mid)) {
            ans = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }

    cout << ans << '\n';
    return 0;
}