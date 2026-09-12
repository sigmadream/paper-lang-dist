#include <stdio.h>

int main() {
    int n;
    long long m;
    scanf("%d %lld", &n, &m);
    
    long long a[n];
    for (int i = 0; i < n; i++) scanf("%lld", &a[i]);
    
    int ans = 0;
    long long sum = 0;
    int end = 0;
    
    for (int start = 0; start < n; start++) {
        while (sum < m && end < n) {
            sum += a[end];
            end++;
        }
        if (sum == m) ans++;
        sum -= a[start];
    }
    
    printf("%d\n", ans);
    return 0;
}
