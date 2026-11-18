#include <iostream>
#include <vector>
#include <queue>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n = 0, m = 0;
    if (!(std::cin >> n)) return 0;
    std::cin >> m;

    if (n <= 0) {
        std::cout << 0 << '\n';
        return 0;
    }

    std::vector<std::vector<int>> adj(n + 1);

    for (int i = 0; i < m; ++i) {
        int a, b;
        std::cin >> a >> b;
        if (a >= 1 && a <= n && b >= 1 && b <= n) {
            adj[a].push_back(b);
            adj[b].push_back(a);
        }
    }

    std::vector<int> dist(n + 1, -1);
    std::queue<int> q;

    dist[1] = 0;
    q.push(1);

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        if (dist[u] >= 2) continue;

        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }

    int answer = 0;
    for (int v = 2; v <= n; ++v) {
        if (dist[v] == 1 || dist[v] == 2) {
            ++answer;
        }
    }

    std::cout << answer << '\n';
    return 0;
}