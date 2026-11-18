#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    long long cur = a[0], best = a[0];
    for (int i = 1; i < n; i++) {
        cur = max((long long)a[i], cur + a[i]);
        best = max(best, cur);
    }
    printf("%lld\n", best);
    return 0;
}