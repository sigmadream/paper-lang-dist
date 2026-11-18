#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

bool canPlace(const vector<long long>& coords, long long dist, int c) {
    int count = 1;
    long long prev = coords[0];
    for (size_t i = 1; i < coords.size(); ++i) {
        if (coords[i] - prev >= dist) {
            count++;
            prev = coords[i];
            if (count >= c) return true;
        }
    }
    return count >= c;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n, c;
    cin >> n >> c;
    vector<long long> coords(n);
    for (int i = 0; i < n; ++i) {
        cin >> coords[i];
    }
    sort(coords.begin(), coords.end());
    
    long long left = 1;
    long long right = coords[n-1] - coords[0];
    long long ans = 0;
    
    while (left <= right) {
        long long mid = left + (right - left) / 2;
        if (canPlace(coords, mid, c)) {
            ans = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    
    cout << ans << '\n';
    return 0;
}