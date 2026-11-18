#include <bits/stdc++.h>
using namespace std;

bool canPlace(const vector<int>& houses, int c, int d) {
    if (houses.empty()) return false;
    int count = 1;
    int prev = houses[0];
    for (size_t i = 1; i < houses.size(); ++i) {
        if (houses[i] - prev >= d) {
            ++count;
            prev = houses[i];
        }
    }
    return count >= c;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, c;
    if (!(cin >> n >> c)) return 0;

    vector<int> houses(n);
    for (int i = 0; i < n; ++i) cin >> houses[i];

    sort(houses.begin(), houses.end());

    int lo = 1;
    int hi = houses.back() - houses.front();
    int ans = 0;

    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (canPlace(houses, c, mid)) {
            ans = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }

    cout << ans << '\n';
    return 0;
}