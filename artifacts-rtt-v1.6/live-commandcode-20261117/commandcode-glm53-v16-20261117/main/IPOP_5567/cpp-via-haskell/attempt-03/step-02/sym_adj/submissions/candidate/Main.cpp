#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m;
    if (!(cin >> n)) return 0;
    cin >> m;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    vector<int> dist(n + 1, -1);
    dist[1] = 0;
    queue<int> q;
    q.push(1);
    while (!q.empty()) {
        int c = q.front(); q.pop();
        for (int v : adj[c]) {
            if (dist[v] == -1) {
                dist[v] = dist[c] + 1;
                q.push(v);
            }
        }
    }
    int ans = 0;
    for (int i = 1; i <= n; ++i)
        if (dist[i] == 1 || dist[i] == 2) ++ans;
    cout << ans << "\n";
    return 0;
}