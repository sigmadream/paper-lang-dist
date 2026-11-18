#include <iostream>
#include <vector>
#include <queue>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    if (!(std::cin >> n)) return 0;

    int m;
    std::cin >> m;

    std::vector<std::vector<int>> adj(n + 1);

    for (int i = 0; i < m; ++i) {
        int u, v;
        std::cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    std::vector<int> dist(n + 1, -1);
    std::queue<int> q;

    q.push(1);
    dist[1] = 0;

    int ans = 0;

    while (!q.empty()) {
        int curr = q.front();
        q.pop();

        for (int nextNode : adj[curr]) {
            if (dist[nextNode] == -1) {
                dist[nextNode] = dist[curr] + 1;
                q.push(nextNode);

                if (dist[nextNode] <= 2) {
                    ++ans;
                }
            }
        }
    }

    std::cout << ans << '\n';

    return 0;
}