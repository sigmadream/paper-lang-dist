#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    int m = 0;
    if (!(cin >> m)) m = 0;

    if (n <= 0) {
        cout << 0 << "\n";
        return 0;
    }

    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; ++i) {
        int a, b;
        if (!(cin >> a >> b)) break;
        if (a >= 1 && a <= n && b >= 1 && b <= n) {
            adj[a].push_back(b);
            adj[b].push_back(a);
        }
    }

    vector<int> dist(n + 1, -1);
    queue<int> q;
    dist[1] = 0;
    q.push(1);

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }

    int ans = 0;
    for (int i = 2; i <= n; ++i) {
        if (dist[i] == 1 || dist[i] == 2) {
            ++ans;
        }
    }

    cout << ans << "\n";
    return 0;
}