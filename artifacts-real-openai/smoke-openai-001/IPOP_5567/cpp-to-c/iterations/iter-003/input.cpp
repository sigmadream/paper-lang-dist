#include <cstdio>
#include <cstdlib>

struct Node {
    int v;
    Node *next;
};

struct Queue {
    int *data;
    int front;
    int back;
};

int main() {
    int n, m;
    if (std::scanf("%d %d", &n, &m) != 2) return 0;

    Node **adj = (Node **)std::calloc(n + 1, sizeof(Node *));
    for (int i = 0; i < m; i++) {
        int u, v;
        std::scanf("%d %d", &u, &v);

        Node *a = (Node *)std::malloc(sizeof(Node));
        a->v = v;
        a->next = adj[u];
        adj[u] = a;

        Node *b = (Node *)std::malloc(sizeof(Node));
        b->v = u;
        b->next = adj[v];
        adj[v] = b;
    }

    int *dist = (int *)std::malloc((n + 1) * sizeof(int));
    for (int i = 0; i <= n; i++) dist[i] = -1;

    Queue q;
    q.data = (int *)std::malloc((n + 5) * sizeof(int));
    q.front = 0;
    q.back = 0;

    q.data[q.back++] = 1;
    dist[1] = 0;

    int ans = 0;

    while (q.front < q.back) {
        int curr = q.data[q.front++];

        Node *p = adj[curr];
        while (p) {
            int next_node = p->v;
            if (dist[next_node] == -1) {
                dist[next_node] = dist[curr] + 1;
                q.data[q.back++] = next_node;
                if (dist[next_node] <= 2) {
                    ans++;
                }
            }
            p = p->next;
        }
    }

    std::printf("%d\n", ans);

    for (int i = 1; i <= n; i++) {
        Node *p = adj[i];
        while (p) {
            Node *tmp = p;
            p = p->next;
            std::free(tmp);
        }
    }
    std::free(adj);
    std::free(dist);
    std::free(q.data);

    return 0;
}
