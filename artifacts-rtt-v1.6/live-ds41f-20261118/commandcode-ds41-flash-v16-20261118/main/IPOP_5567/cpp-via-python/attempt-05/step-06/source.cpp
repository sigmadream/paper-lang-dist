#include <iostream>
#include <vector>
#include <queue>

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::vector<int> data;
    int x;
    while (std::cin >> x) data.push_back(x);

    if (data.empty()) return 0;

    int n = data[0];
    int m = (data.size() > 1) ? data[1] : 0;

    std::vector<std::vector<int>> adj(n + 1);

    int idx = 2;
    for (int i = 0; i < m; ++i) {
        int u = data[idx];
        int v = data[idx + 1];
        idx += 2;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    std::vector<int> dist(n + 1, -1);
    dist[1] = 0;

    std::queue<int> q;
    q.push(1);

    int ans = 0;

    while (!q.empty()) {
        int curr = q.front();
        q.pop();

        for (int nxt : adj[curr]) {
            if (dist[nxt] == -1) {
                dist[nxt] = dist[curr] + 1;
                q.push(nxt);
                if (dist[nxt] <= 2) {
                    ++ans;
                }
            }
        }
    }

    std::cout << ans << '\n';
    return 0;
}