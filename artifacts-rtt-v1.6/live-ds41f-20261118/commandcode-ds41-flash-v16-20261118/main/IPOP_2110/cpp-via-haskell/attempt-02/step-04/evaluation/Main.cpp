#include <bits/stdc++.h>
using namespace std;

static bool canPlace(const vector<long long>& houses, int c, long long d) {
    if (houses.empty()) return false;
    int cnt = 1;
    long long prev = houses[0];
    for (size_t i = 1; i < houses.size(); ++i) {
        if (houses[i] - prev >= d) {
            ++cnt;
            prev = houses[i];
            if (cnt >= c) return true;
        }
    }
    return cnt >= c;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, c;
    if (!(cin >> n >> c)) return 0;

    vector<long long> houses(n);
    for (int i = 0; i < n; ++i) cin >> houses[i];

    sort(houses.begin(), houses.end());

    long long lo = 1;
    long long hi = houses.back() - houses.front();
    long long answer = 0;

    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        if (canPlace(houses, c, mid)) {
            answer = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }

    cout << answer << '\n';
    return 0;
}