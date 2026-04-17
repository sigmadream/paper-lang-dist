#include <stdio.h>
#include <stdlib.h>

int cmp_desc(const void *a, const void *b) {
    int x = *(const int *)a;
    int y = *(const int *)b;
    return y - x;
}

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    int *ropes = (int *)malloc(sizeof(int) * n);
    if (!ropes) return 0;

    for (int i = 0; i < n; i++) {
        scanf("%d", &ropes[i]);
    }

    qsort(ropes, n, sizeof(int), cmp_desc);

    long long max_weight = 0;
    for (int i = 0; i < n; i++) {
        long long current_weight = 1LL * ropes[i] * (i + 1);
        if (current_weight > max_weight) {
            max_weight = current_weight;
        }
    }

    printf("%lld\n", max_weight);

    free(ropes);
    return 0;
}
