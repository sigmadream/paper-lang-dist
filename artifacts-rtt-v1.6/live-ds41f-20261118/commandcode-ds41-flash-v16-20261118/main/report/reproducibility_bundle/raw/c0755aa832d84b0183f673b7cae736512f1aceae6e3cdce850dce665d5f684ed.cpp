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

    long long lo = 1;
    long long hi = houses.back() - houses.front();
    long long answer = 0;

    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;

        int count = 1;
        long long prev = houses[0];

        for (int i = 1; i < N; ++i) {
            if (houses[i] - prev >= mid) {
                ++count;
                prev = houses[i];
                if (count >= C) break;
            }
        }

        if (count >= C) {
            answer = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }

    cout << answer << '\n';
    return 0;
}