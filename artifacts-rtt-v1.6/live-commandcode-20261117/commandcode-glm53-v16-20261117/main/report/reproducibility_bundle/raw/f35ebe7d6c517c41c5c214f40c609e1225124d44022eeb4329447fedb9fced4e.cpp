#include <bits/stdc++.h>
using namespace std;

int main() {
    long long n, c;
    if (scanf("%lld %lld", &n, &c) != 2) return 0;
    vector<long long> s(n);
    for (long long i = 0; i < n; i++) scanf("%lld", &s[i]);
    sort(s.begin(), s.end());
    long long lo = 1, hi = s.back() - s.front(), ans = 0;
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        long long k = 1;
        long long p = s[0];
        for (size_t j = 1; j < s.size(); j++) {
            if (s[j] - p >= mid) { k++; p = s[j]; }
        }
        if (k >= c) { ans = mid; lo = mid + 1; }
        else hi = mid - 1;
    }
    printf("%lld\n", ans);
    return 0;
}