#include <stdio.h>

int main() {
    int h, w;
    if (scanf("%d %d", &h, &w) != 2) return 0;
    
    int a[w];
    for (int i = 0; i < w; i++) scanf("%d", &a[i]);
    
    int ans = 0;
    for (int i = 1; i < w - 1; i++) {
        int left_max = 0, right_max = 0;
        for (int j = 0; j <= i; j++) left_max = (left_max > a[j]) ? left_max : a[j];
        for (int j = i; j < w; j++) right_max = (right_max > a[j]) ? right_max : a[j];
        int bound = (left_max < right_max) ? left_max : right_max;
        if (bound > a[i]) ans += bound - a[i];
    }
    
    printf("%d\n", ans);
    return 0;
}
