#include <bits/stdc++.h>
using namespace std;

int countPlacements(long long d, const vector<long long>& homes) {
    int cnt = 1;
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

    int N, C;
    cin >> N >> C;

    vector<long long> homes(N);
    for (int i = 0; i < N; ++i) {
        cin >> homes[i];
    }

    sort(homes.begin(), homes.end());

    long long left = 1;
    long long right = homes.back() - homes.front();
    long long ans = 0;

    while (left <= right) {
        long long mid = left + (right - left) / 2;
        if (countPlacements(mid, homes) >= C) {
            ans = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    cout << ans << '\n';
    return 0;
}