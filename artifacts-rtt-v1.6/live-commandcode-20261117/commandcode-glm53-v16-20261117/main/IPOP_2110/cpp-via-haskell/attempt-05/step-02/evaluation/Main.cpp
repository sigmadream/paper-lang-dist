#include <bits/stdc++.h>
using namespace std;

int n;
long long c;
vector<long long> a;

long long countGE(long long mid) {
    long long cnt = 1;
    long long prev = a[0];
    for (int i = 1; i < n; i++) {
        if (a[i] - prev >= mid) {
            cnt++;
            prev = a[i];
        }
    }
    return cnt;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    long long nn, cc;
    cin >> nn >> cc;
    n = (int)nn; c = cc;
    a.resize(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    sort(a.begin(), a.end());
    long long l = 1, r = a[n-1] - a[0], ans = 0;
    while (l <= r) {
        long long mid = l + (r - l) / 2;
        if (countGE(mid) >= c) {
            ans = mid;
            l = mid + 1;
        } else {
            r = mid - 1;
        }
    }
    cout << ans << "\n";
    return 0;
}