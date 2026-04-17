#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int main() {
    int n, m;
    cin >> n >> m;

    vector<vector<int>> adj(n + 1, vector<int>(n + 1, 0));
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        adj[u][v] = 1;
        adj[v][u] = 1;
    }

    vector<int> dist(n + 1, -1);
    dist[1] = 0;

    queue<int> q;
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

    cout << ans << endl;
    return 0;
}
