#include <stdio.h>
#include <stdlib.h>

int ans = 0;
int n;
int *col, *diag1, *diag2;

void solve(int r) {
    if (r == n) {
        ans++;
        return;
    }
    for (int c = 0; c < n; c++) {
        if (col[c] || diag1[r + c] || diag2[r - c + n - 1]) continue;
        col[c] = diag1[r + c] = diag2[r - c + n - 1] = 1;
        solve(r + 1);
        col[c] = diag1[r + c] = diag2[r - c + n - 1] = 0;
    }
}

int main() {
    scanf("%d", &n);
    
    col = (int *)malloc(n * sizeof(int));
    diag1 = (int *)malloc((2 * n - 1) * sizeof(int));
    diag2 = (int *)malloc((2 * n - 1) * sizeof(int));
    
    for (int i = 0; i < n; i++) col[i] = diag1[i] = diag2[i] = 0;
    solve(0);
    
    printf("%d\n", ans);
    free(col);
    free(diag1);
    free(diag2);
    return 0;
}
