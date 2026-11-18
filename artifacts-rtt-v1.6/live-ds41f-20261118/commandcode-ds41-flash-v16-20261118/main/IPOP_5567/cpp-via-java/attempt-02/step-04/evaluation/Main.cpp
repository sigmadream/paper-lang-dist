#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;

    int m;
    if (!(cin >> m)) return 0;

    vector<vector<int>> adj(n + 1);

    for (int i = 0; i < m; ++i) {
        int u, v;
        if (!(cin >> u >> v)) break;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    vector<int> dist(n + 1, -1);
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
                    ++ans;
                }
            }
        }
    }

    cout << ans << '\n';
    return 0;
}