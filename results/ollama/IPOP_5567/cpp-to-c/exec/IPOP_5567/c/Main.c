#include <stdio.h>
#include <stdlib.h>

#define MAXN 501

int main() {
    int n, m;
    scanf("%d %d", &n, &m);

    int adj[MAXN][MAXN] = {0};
    for (int i = 0; i < m; i++) {
        int u, v;
        scanf("%d %d", &u, &v);
        adj[u][v] = 1;
        adj[v][u] = 1;
    }

    int dist[MAXN];
    for (int i = 0; i <= n; i++) {
        dist[i] = -1;
    }
    dist[1] = 0;

    int q[MAXN], front = 0, rear = 0;
    q[rear++] = 1;

    int ans = 0;
    while (front != rear) {
        int curr = q[front++];
        for (int next_node = 1; next_node <= n; next_node++) {
            if (adj[curr][next_node] == 1 && dist[next_node] == -1) {
                dist[next_node] = dist[curr] + 1;
                q[rear++] = next_node;
                if (dist[next_node] <= 2) {
                    ans++;
                }
            }
        }
    }

    printf("%d\n", ans);
    return 0;
}
