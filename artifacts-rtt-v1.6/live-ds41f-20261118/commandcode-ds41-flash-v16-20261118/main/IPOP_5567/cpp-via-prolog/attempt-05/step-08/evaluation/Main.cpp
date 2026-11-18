#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N;
    if (!(cin >> N)) return 0;
    int M;
    if (!(cin >> M)) return 0;

    vector<vector<int>> adj(N + 1);
    for (int i = 0; i < M; ++i) {
        int a, b;
        cin >> a >> b;
        if (a >= 1 && a <= N && b >= 1 && b <= N) {
            adj[a].push_back(b);
            adj[b].push_back(a);
        }
    }

    if (N < 1) {
        cout << 0 << '\n';
        return 0;
    }

    vector<int> dist(N + 1, -1);
    queue<int> q;
    dist[1] = 0;
    q.push(1);

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        if (dist[u] == 2) continue;

        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }

    int ans = 0;
    for (int v = 1; v <= N; ++v) {
        if (v != 1 && (dist[v] == 1 || dist[v] == 2)) {
            ++ans;
        }
    }

    cout << ans << '\n';
    return 0;
}