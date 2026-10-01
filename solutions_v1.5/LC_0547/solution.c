#include <stdio.h>
#include <stdbool.h>

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) {
        return 0;
    }

    int g[205][205];
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (scanf("%d", &g[i][j]) != 1) {
                g[i][j] = 0;
            }
        }
    }

    bool seen[205] = {false};
    int stack_nodes[205];
    int components = 0;

    for (int i = 0; i < n; ++i) {
        if (!seen[i]) {
            components++;
            int top = 0;
            stack_nodes[top++] = i;
            seen[i] = true;
            while (top > 0) {
                int u = stack_nodes[--top];
                for (int v = 0; v < n; ++v) {
                    if (g[u][v] && !seen[v]) {
                        seen[v] = true;
                        stack_nodes[top++] = v;
                    }
                }
            }
        }
    }

    printf("%d\n", components);
    return 0;
}
