#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<int> vals;
    int x;
    while (cin >> x) vals.push_back(x);

    if (vals.empty()) return 0;

    int n = vals[0];

    if (n <= 0) {
        cout << 0 << '\n';
        return 0;
    }

    size_t idx = 1;
    int m = 0;
    if (idx < vals.size()) {
        m = vals[idx];
        ++idx;
    }

    int limit = max(0, m);
    vector<vector<int>> adj(n + 1);

    for (int i = 0; i < limit; ++i) {
        if (idx + 1 >= vals.size()) break;

        int a = vals[idx++];
        int b = vals[idx++];

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

        if (dist[u] >= 2) continue;

        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }

    int ans = 0;
    for (int v = 2; v <= n; ++v) {
        if (dist[v] == 1 || dist[v] == 2) {
            ++ans;
        }
    }

    cout << ans << '\n';

    return 0;
}