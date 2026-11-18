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
    dist[1] = 0;
    q.push(1);
    int ans = 0;
    while (!q.empty()) {
        int x = q.front();
        q.pop();
        if (dist[x] >= 2) continue;
        for (int y : adj[x]) {
            if (dist[y] == -1) {
                dist[y] = dist[x] + 1;
                if (dist[y] <= 2) ++ans;
                q.push(y);
            }
        }
    }
    std::cout << ans << '\n';
    return 0;
}