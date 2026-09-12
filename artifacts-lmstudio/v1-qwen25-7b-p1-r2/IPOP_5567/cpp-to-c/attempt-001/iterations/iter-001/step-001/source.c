#include <stdio.h>
#include <stdlib.h>

#define MAXN 501
#define MAXM 10001

int n, m;
int adj[MAXN][MAXN];
int dist[MAXN];

void bfs() {
    int q[MAXN];
    int front = 0, rear = 0;
    q[rear++] = 1;
    dist[1] = 0;

    while (front < rear) {
        int curr = q[front++];
        for (int next_node = 1; next_node <= n; next_node++) {
            if (adj[curr][next_node] && dist[next_node] == -1) {
                dist[next_node] = dist[curr] + 1;
                q[rear++] = next_node;
                if (dist[next_node] <= 2) {
                    dist[next_node] = 1;
                }
            }
        }
    }
}

int main() {
    scanf("%d %d", &n, &m);
    for (int i = 0; i < m; i++) {
        int u, v;
        scanf("%d %d", &u, &v);
        adj[u][v] = 1;
        adj[v][u] = 1;
    }

    for (int i = 1; i <= n; i++) {
        dist[i] = -1;
    }

    bfs();

    int ans = 0;
    for (int i = 1; i <= n; i++) {
        if (dist[i] <= 2) {
            ans++;
        }
    }

    printf("%d\n", ans);
    return 0;
}
