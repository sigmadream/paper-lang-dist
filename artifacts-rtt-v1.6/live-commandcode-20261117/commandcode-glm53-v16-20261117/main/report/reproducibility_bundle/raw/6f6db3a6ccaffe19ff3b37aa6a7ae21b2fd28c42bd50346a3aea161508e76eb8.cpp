#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long n, c;
    if (!(cin >> n >> c)) return 0;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    sort(a.begin(), a.end());
    long long left = 1, right = a[n-1] - a[0], ans = 0;
    while (left <= right) {
        long long mid = (left + right) / 2;
        long long count = 1, prev = a[0];
        for (size_t i = 1; i < a.size(); ++i) {
            if (a[i] - prev >= mid) {
                count++;
                prev = a[i];
            }
        }
        if (count >= c) {
            ans = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    cout << ans << "\n";
    return 0;
}