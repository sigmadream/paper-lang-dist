#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, C;
    if (!(cin >> N >> C)) return 0;

    vector<long long> houses(N);
    for (int i = 0; i < N; ++i) {
        cin >> houses[i];
    }

    sort(houses.begin(), houses.end());

    auto canPlace = [&](long long dist) -> bool {
        int count = 1;
        long long last = houses[0];

        for (int i = 1; i < N; ++i) {
            if (houses[i] - last >= dist) {
                ++count;
                last = houses[i];
                if (count >= C) return true;
            }
        }

        return count >= C;
    };

    long long lo = 1;
    long long hi = houses.back() - houses.front();
    long long answer = 0;

    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;

        if (canPlace(mid)) {
            answer = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }

    cout << answer << '\n';
    return 0;
}