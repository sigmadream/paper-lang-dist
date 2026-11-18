#include <cstdio>
#include <algorithm>
#include <vector>

int main() {
    int n, c;
    if (scanf("%d %d", &n, &c) != 2) return 0;

    std::vector<int> a(n);
    for (int i = 0; i < n; i++) {
        scanf("%d", &a[i]);
    }

    std::sort(a.begin(), a.end());

    int left = 1;
    int right = a[n - 1] - a[0];
    int ans = 0;

    while (left <= right) {
        int mid = left + (right - left) / 2;
        int count = 1;
        int prev = a[0];

        for (int i = 1; i < n; i++) {
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

    printf("%d\n", ans);
    return 0;
}