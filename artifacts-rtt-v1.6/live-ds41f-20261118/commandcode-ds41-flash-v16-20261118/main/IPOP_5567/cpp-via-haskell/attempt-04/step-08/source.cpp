#include <iostream>
#include <vector>
#include <queue>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n, m;
    if (!(std::cin >> n)) return 0;
    std::cin >> m;

    std::vector<std::vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int a, b;
        std::cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    std::vector<int> dist(n + 1, -1);
    std::queue<int> q;
    dist[1] = 0;
    q.push(1);

    while (!q.empty()) {
        int v = q.front();
        q.pop();

        if (dist[v] == 2) continue;

        for (int nxt : adj[v]) {
            if (dist[nxt] == -1) {
                dist[nxt] = dist[v] + 1;
                q.push(nxt);
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