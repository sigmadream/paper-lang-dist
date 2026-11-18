#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, C;
    cin >> N >> C;

    vector<long long> houses(N);
    for (int i = 0; i < N; ++i) {
        cin >> houses[i];
    }

    sort(houses.begin(), houses.end());

    long long left = 1;
    long long right = houses.back() - houses.front();
    long long answer = 0;

    while (left <= right) {
        long long mid = left + (right - left) / 2;

        int installed = 1;
        long long previous = houses[0];

        for (int i = 1; i < N; ++i) {
            if (houses[i] - previous >= mid) {
                ++installed;
                previous = houses[i];
            }
        }

        if (installed >= C) {
            answer = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    cout << answer << '\n';

    return 0;
}