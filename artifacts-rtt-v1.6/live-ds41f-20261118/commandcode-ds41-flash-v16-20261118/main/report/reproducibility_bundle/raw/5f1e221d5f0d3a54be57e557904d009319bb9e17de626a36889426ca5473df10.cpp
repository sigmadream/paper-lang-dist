#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;

    vector<vector<int>> adj(n + 1);

    for (int i = 0; i < m; ++i) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    vector<int> dist(n + 1, -1);
    dist[1] = 0;

    queue<int> q;
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

    cout << ans << '\n';
    return 0;
}