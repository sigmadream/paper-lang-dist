#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    vector<int> dist(n + 1, -1);
    queue<int> q;

    if (n >= 1) {
        dist[1] = 0;
        q.push(1);
    }

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

    int ans = 0;
    for (int i = 1; i <= n; ++i) {
        if (i != 1 && dist[i] >= 1 && dist[i] <= 2) {
            ++ans;
        }
    }

    cout << ans << '\n';
    return 0;
}