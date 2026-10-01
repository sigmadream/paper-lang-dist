#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) {
        return 0;
    }

    if (n <= 0) {
        putchar('\n');
        return 0;
    }

    long long *a = (long long *)malloc((size_t)n * sizeof(long long));
    if (!a) {
        return 1;
    }

    for (int i = 0; i < n; ++i) {
        if (scanf("%lld", &a[i]) != 1) {
            break;
        }
    }

    int write_idx = 0;
    for (int read_idx = 0; read_idx < n; ++read_idx) {
        if (a[read_idx] != 0) {
            long long temp = a[write_idx];
            a[write_idx] = a[read_idx];
            a[read_idx] = temp;
            write_idx++;
        }
    }

    for (int i = 0; i < n; ++i) {
        if (i > 0) {
            putchar(' ');
        }
        printf("%lld", a[i]);
    }
    putchar('\n');

    free(a);
    return 0;
}
