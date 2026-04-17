#include <stdio.h>
#include <stdlib.h>

static int cmp_int(const void *a, const void *b) {
    int x = *(const int *)a;
    int y = *(const int *)b;
    if (x < y) return -1;
    if (x > y) return 1;
    return 0;
}

int main(void) {
    int n, c;
    if (scanf("%d %d", &n, &c) != 2) return 0;

    int *a = (int *)malloc((size_t)n * sizeof(int));
    if (!a) return 0;

    for (int i = 0; i < n; i++) scanf("%d", &a[i]);

    qsort(a, (size_t)n, sizeof(int), cmp_int);

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

    free(a);
    return 0;
}
