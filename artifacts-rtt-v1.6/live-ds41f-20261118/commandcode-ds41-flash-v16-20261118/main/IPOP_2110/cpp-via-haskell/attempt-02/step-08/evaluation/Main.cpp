#include <bits/stdc++.h>
using namespace std;

int countHouses(const vector<int>& houses, int d, int c) {
    if (houses.empty()) return 0;
    int cnt = 1;
    int prev = houses[0];
    for (size_t i = 1; i < houses.size(); i++) {
        if (cnt >= c) return cnt;
        if (houses[i] - prev >= d) { prev = houses[i]; cnt++; }
    }
    return cnt;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, c;
    if (!(cin >> n >> c)) return 0;
    vector<int> houses(n);
    for (int i = 0; i < n; i++) cin >> houses[i];
    sort(houses.begin(), houses.end());
    int lo = 1, hi = houses[n-1] - houses[0], ans = 0;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (countHouses(houses, mid, c) >= c) { ans = mid; lo = mid + 1; }
        else hi = mid - 1;
    }
    cout << ans << "\n";
    return 0;
}