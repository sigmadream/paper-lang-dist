#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>

using namespace std;

void dfs(int cur, const vector<vector<int>>& adj, vector<bool>& vis) {
    vis[cur] = true;
    cout << cur << " ";
    for (int nxt : adj[cur]) {
        if (!vis[nxt]) dfs(nxt, adj, vis);
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n, m, v;
    if (!(cin >> n >> m >> v)) return 0;
    
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    for (int i = 1; i <= n; i++) sort(adj[i].begin(), adj[i].end());
    
    vector<bool> vis(n + 1, false);
    dfs(v, adj, vis);
    cout << "\n";
    
    fill(vis.begin(), vis.end(), false);
    queue<int> q;
    q.push(v);
    vis[v] = true;
    while (!q.empty()) {
        int cur = q.front();
        q.pop();
        cout << cur << " ";
        for (int nxt : adj[cur]) {
            if (!vis[nxt]) {
                vis[nxt] = true;
                q.push(nxt);
            }
        }
    }
    cout << "\n";
    return 0;
}
