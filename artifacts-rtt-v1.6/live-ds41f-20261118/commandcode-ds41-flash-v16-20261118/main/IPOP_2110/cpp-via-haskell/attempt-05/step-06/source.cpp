#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int countPlacements(int d, const vector<int>& homes) {
    int count = 1;
    int prev = homes[0];
    for (size_t i = 1; i < homes.size(); ++i) {
        if (homes[i] - prev >= d) {
            ++count;
            prev = homes[i];
        }
    }
    return count;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, c;
    if (!(cin >> n >> c)) return 0;

    vector<int> homes(n);
    for (int i = 0; i < n; ++i) cin >> homes[i];

    sort(homes.begin(), homes.end());

    int left = 1;
    int right = homes.back() - homes.front();
    int answer = 0;

    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (countPlacements(mid, homes) >= c) {
            answer = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    cout << answer << '\n';
    return 0;
}