#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

bool possible(const vector<int>& homes, int c, int dist) {
    int count = 1;
    int prev = homes[0];

    for (size_t i = 1; i < homes.size(); ++i) {
        if (homes[i] - prev >= dist) {
            ++count;
            prev = homes[i];
            if (count >= c) return true;
        }
    }

    return count >= c;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, c;
    cin >> n >> c;

    vector<int> homes(n);
    for (int i = 0; i < n; ++i) {
        cin >> homes[i];
    }

    sort(homes.begin(), homes.end());

    int low = 1;
    int high = homes.back() - homes.front();
    int answer = 0;

    while (low <= high) {
        int mid = low + (high - low) / 2;

        if (possible(homes, c, mid)) {
            answer = mid;
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }

    cout << answer << '\n';

    return 0;
}