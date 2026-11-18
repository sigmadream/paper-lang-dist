#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, M;
    if (!(cin >> N)) return 0;
    if (!(cin >> M)) M = 0;

    vector<vector<int>> adj(N + 1);
    for (int i = 0; i < M; ++i) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    vector<int> dist(N + 1, -1);
    queue<int> q;
    dist[1] = 0;
    q.push(1);

    int ans = 0;
    while (!q.empty()) {
        int u = q.front();
        q.pop();

        if (dist[u] >= 2) continue;

        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                if (dist[v] <= 2) ++ans;
                q.push(v);
            }
        }
    }

    cout << ans << '\n';
    return 0;
}