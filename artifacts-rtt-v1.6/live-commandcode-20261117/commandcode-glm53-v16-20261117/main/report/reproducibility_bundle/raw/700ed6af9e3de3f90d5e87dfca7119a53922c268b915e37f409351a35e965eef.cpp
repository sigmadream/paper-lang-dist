#include <bits/stdc++.h>
using namespace std;

int N; long long C;
vector<long long> s;

long long countGE(long long mid) {
    if (s.empty()) return 0;
    long long prev = s[0], k = 1;
    for (size_t i = 1; i < s.size(); i++) {
        if (s[i] - prev >= mid) { prev = s[i]; k++; }
    }
    return k;
}

long long search_(long long lo, long long hi, long long acc) {
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        if (countGE(mid) >= C) { acc = mid; lo = mid + 1; }
        else hi = mid - 1;
    }
    return acc;
}

int main() {
    long long n, c;
    if (scanf("%lld %lld", &n, &c) != 2) return 0;
    vector<long long> a(n);
    for (long long i = 0; i < n; i++) scanf("%lld", &a[i]);
    sort(a.begin(), a.end());
    s = a;
    N = (int)n; C = c;
    long long lo = 1, hi = s.back() - s.front();
    printf("%lld\n", search_(lo, hi, 0));
    return 0;
}