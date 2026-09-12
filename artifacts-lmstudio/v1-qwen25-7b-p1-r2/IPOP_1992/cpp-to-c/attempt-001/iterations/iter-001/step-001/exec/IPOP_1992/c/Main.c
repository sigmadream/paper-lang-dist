#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* solve(char** grid, int r, int c, int size) {
    char first = grid[r][c];
    int same = 1;
    for (int i = r; i < r + size; i++) {
        for (int j = c; j < c + size; j++) {
            if (grid[i][j] != first) {
                same = 0;
                break;
            }
        }
        if (!same) break;
    }
    
    if (same) return (char*)malloc(2 * sizeof(char));
    sprintf((char*)malloc(2 * sizeof(char)), "%c", first);
    
    int half = size / 2;
    char* tl = solve(grid, r, c, half);
    char* tr = solve(grid, r, c + half, half);
    char* bl = solve(grid, r + half, c, half);
    char* br = solve(grid, r + half, c + half, half);
    
    int len = 1 + strlen(tl) + strlen(tr) + strlen(bl) + strlen(br) + 1;
    char* result = (char*)malloc(len * sizeof(char));
    sprintf(result, "(%s%s%s%s)", tl, tr, bl, br);
    
    free(tl);
    free(tr);
    free(bl);
    free(br);
    
    return result;
}

int main() {
    int n;
    scanf("%d", &n);
    char** grid = (char**)malloc(n * sizeof(char*));
    for (int i = 0; i < n; i++) {
        grid[i] = (char*)malloc((n + 1) * sizeof(char));
        scanf("%s", grid[i]);
    }
    char* result = solve(grid, 0, 0, n);
    printf("%s\n", result);
    for (int i = 0; i < n; i++) free(grid[i]);
    free(grid);
    free(result);
    return 0;
}
