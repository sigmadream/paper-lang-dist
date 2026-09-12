#include <stdio.h>
#include <stdlib.h>

int main() {
    int n, k;
    if (scanf("%d %d", &n, &k) != 2) return 0;
    
    int *q = (int *)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) q[i] = i + 1;
    
    printf("<");
    int idx = 0;
    while (n > 0) {
        idx = (idx + k - 1) % n;
        printf("%d", q[idx]);
        n--;
        if (n > 0) printf(", ");
    }
    printf(">\n");
    free(q);
    return 0;
}
