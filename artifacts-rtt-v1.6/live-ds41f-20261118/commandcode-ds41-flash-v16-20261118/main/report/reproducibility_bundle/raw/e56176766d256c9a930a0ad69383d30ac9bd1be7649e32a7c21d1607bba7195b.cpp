#include <iostream>
#include <vector>
#include <queue>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n, m;
    if (!(std::cin >> n >> m)) return 0;

    std::vector<std::vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int a, b;
        std::cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    std::vector<int> dist(n + 1, -1);
    std::queue<int> q;

    if (n >= 1) {
        dist[1] = 0;
        q.push(1);
    }

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }

    int answer = 0;
    for (int i = 2; i <= n; ++i) {
        if (dist[i] == 1 || dist[i] == 2) {
            ++answer;
        }
    }

    std::cout << answer << '\n';
    return 0;
}