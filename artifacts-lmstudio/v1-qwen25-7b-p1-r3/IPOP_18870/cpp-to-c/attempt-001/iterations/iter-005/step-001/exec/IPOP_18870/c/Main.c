#include <stdio.h>
#include <stdlib.h>

int compare(const void *a, const void *b) {
    return (*(int*)a - *(int*)b);
}

int main() {
    int n;
    scanf("%d", &n);
    
    int a[n];
    for (int i = 0; i < n; i++) scanf("%d", &a[i]);
    
    int sorted_a[n];
    for (int i = 0; i < n; i++) sorted_a[i] = a[i];
    qsort(sorted_a, n, sizeof(int), compare);
    
    int unique_a[n];
    int unique_count = 0;
    for (int i = 0; i < n; i++) {
        if (i == 0 || sorted_a[i] != sorted_a[i - 1]) {
            unique_a[unique_count++] = sorted_a[i];
        }
    }
    
    for (int i = 0; i < n; i++) {
        int compressed = 0;
        for (int j = 0; j < unique_count; j++) {
            if (a[i] > unique_a[j]) compressed++;
        }
        printf("%d ", compressed);
    }
    printf("\n");
    
    return 0;
}
