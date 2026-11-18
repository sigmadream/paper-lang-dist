#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

bool canPlace(const vector<long long>& houses, int C, long long dist) {
    int count = 1;
    long long prev = houses[0];

    for (size_t i = 1; i < houses.size(); ++i) {
        if (houses[i] - prev >= dist) {
            ++count;
            prev = houses[i];
            if (count >= C) return true;
        }
    }

    return false;
}

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

        if (canPlace(houses, C, mid)) {
            answer = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    cout << answer << '\n';

    return 0;
}