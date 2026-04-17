#include <iostream>
#include <vector>
#include <queue>

#define MAXN 501

int main() {
    int n, m;
    std::cin >> n >> m;

    std::vector<std::vector<int>> adj(n + 1, std::vector<int>(n + 1, 0));
    for (int i = 0; i < m; i++) {
        int u, v;
        std::cin >> u >> v;
        adj[u][v] = 1;
        adj[v][u] = 1;
    }

    std::vector<int> dist(n + 1, -1);
    dist[1] = 0;

    std::queue<int> q;
    q.push(1);

    int ans = 0;
    while (!q.empty()) {
        int curr = q.front();
        q.pop();
        for (int next_node = 1; next_node <= n; next_node++) {
            if (adj[curr][next_node] == 1 && dist[next_node] == -1) {
                dist[next_node] = dist[curr] + 1;
                q.push(next_node);
                if (dist[next_node] <= 2) {
                    ans++;
                }
            }
        }
    }

    std::cout << ans << std::endl;
    return 0;
}
