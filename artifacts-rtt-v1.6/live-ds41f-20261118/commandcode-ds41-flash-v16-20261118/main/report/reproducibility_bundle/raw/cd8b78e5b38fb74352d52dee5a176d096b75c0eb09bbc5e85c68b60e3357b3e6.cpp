#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    vector<long long> arr(n);
    for (int i = 0; i < n; ++i) cin >> arr[i];

    if (n == 0) return 0;

    long long cur = arr[0];
    long long best = arr[0];

    for (int i = 1; i < n; ++i) {
        cur = max(arr[i], cur + arr[i]);
        best = max(best, cur);
    }

    cout << best << '\n';
    return 0;
}