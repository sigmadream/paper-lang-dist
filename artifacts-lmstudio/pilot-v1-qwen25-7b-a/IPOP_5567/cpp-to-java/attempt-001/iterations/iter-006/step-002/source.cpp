#include <iostream>
#include <vector>
#include <queue>
#include <cstring>

using namespace std;

int main() {
    int n, m;
    cin >> n >> m;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    int dist[n + 1];
    memset(dist, -1, sizeof(dist));
    queue<int> q;

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
                    ans++;
                }
            }
        }
    }

    cout << ans << endl;

    return 0;
}
