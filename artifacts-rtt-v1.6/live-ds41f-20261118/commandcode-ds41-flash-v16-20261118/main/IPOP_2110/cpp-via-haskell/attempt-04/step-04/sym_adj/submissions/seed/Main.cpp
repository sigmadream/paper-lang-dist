#include <bits/stdc++.h>
using namespace std;

bool canPlace(const vector<long long>& arr, int c, long long d) {
    if (arr.empty()) return false;
    int count = 1;
    long long prev = arr[0];
    for (size_t i = 1; i < arr.size(); ++i) {
        if (arr[i] - prev >= d) {
            ++count;
            prev = arr[i];
        }
    }
    return count >= c;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, c;
    if (!(cin >> n >> c)) return 0;

    vector<long long> arr(n);
    for (int i = 0; i < n; ++i) cin >> arr[i];

    sort(arr.begin(), arr.end());

    long long lo = 1;
    long long hi = arr.back() - arr.front();
    long long ans = 0;

    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        if (canPlace(arr, c, mid)) {
            ans = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }

    cout << ans << '\n';
    return 0;
}