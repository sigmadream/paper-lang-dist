#include <bits/stdc++.h>
using namespace std;

static bool canPlace(const vector<int>& houses, int c, int dist) {
    int count = 1;
    int lastPos = houses[0];

    for (size_t i = 1; i < houses.size(); ++i) {
        int h = houses[i];
        if (h - lastPos >= dist) {
            if (count + 1 >= c) return true;
            ++count;
            lastPos = h;
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
    for (int i = 0; i < n; ++i) {
        cin >> houses[i];
    }

    sort(houses.begin(), houses.end());

    int lo = 1;
    int hi = houses.back() - houses.front();
    int answer = 0;

    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;

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