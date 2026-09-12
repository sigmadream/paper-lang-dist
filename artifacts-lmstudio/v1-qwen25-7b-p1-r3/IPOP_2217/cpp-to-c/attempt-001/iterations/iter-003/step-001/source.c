#include <stdio.h>
#include <stdlib.h>

int compare(const void *a, const void *b) {
    return (*(int*)b - *(int*)a);
}

int main() {
    int n;
    scanf("%d", &n);

    int ropes[n];
    for (int i = 0; i < n; i++) {
        scanf("%d", &ropes[i]);
    }

    qsort(ropes, n, sizeof(int), compare);

    long long max_weight = 0;
    for (int i = 0; i < n; i++) {
        long long current_weight = (long long)ropes[i] * (i + 1);
        if (current_weight > max_weight) {
            max_weight = current_weight;
        }
    }

    printf("%lld\n", max_weight);
    return 0;
}
