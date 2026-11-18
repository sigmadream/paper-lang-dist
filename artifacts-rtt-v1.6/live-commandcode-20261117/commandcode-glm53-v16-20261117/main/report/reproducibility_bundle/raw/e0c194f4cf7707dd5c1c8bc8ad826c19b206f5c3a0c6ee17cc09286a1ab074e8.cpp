#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, m;
    if (scanf("%d", &n) != 1) return 0;
    scanf("%d", &m);
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        scanf("%d %d", &u, &v);
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
        for (int next : adj[curr]) {
            if (dist[next] == -1) {
                dist[next] = dist[curr] + 1;
                q.push(next);
                if (dist[next] <= 2) ans++;
            }
        }
    }
    printf("%d\n", ans);
    return 0;
}